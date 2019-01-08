import time
import wtclib
import datetime
import os, sys,thread,json,shutil
import psutil

def python_cmd(cmd):
    str1 = "@%d"%(os.getpid())
    print cmd + str1
    os.system(cmd)
    #os.system("pause")
    time.sleep(0.5)


def continue_video_process(_cur, _table):
    global mylogger, _CurServerID
    snfile = "/tmp/rtsp2mp4/%s%d.%d"%(_table[0], _table[1],(_table[14]-1)&3)
    localtime1 = time.localtime()
    _video_name = "%02d%02d%02d"%(localtime1.tm_hour,localtime1.tm_min,localtime1.tm_sec)
    _timeSec = int(time.time())
    try:
        fp = open(snfile,'w')
        ms_dic = {"end":2,"fileC":_video_name}
        fp.write(json.dumps(ms_dic))
        fp.close()
    except Exception,e:
        mylogger.error(str(e))

    _day_str = "%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
    _to_file = "../../video/" + _day_str

    _to_file += "/%s%d" % (_table[0], _table[1])
    if not os.path.exists(_to_file):
        try:
            os.mkdir(_to_file)
        except Exception, e:
            mylogger.error(e)


    try:
        _sql = "select video_pid,video_p_state from video_rtsp2mp4_table where cameraID='%s' and cmosID=%d"%(_table[0], _table[1])
        cur.execute(_sql)
        (_rtsp_pid, _rtsp_state,) = cur.fetchone()
        if _rtsp_pid < 0 or _rtsp_state < 50:
            return
        _sql = "select exp,gain from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d"%(_table[0], _table[1])
        _exp = 31372
        _gain = 16
        if 0 != cur.execute(_sql):
            (_exp,_gain,) = cur.fetchone()


        _to_file += "/%s_%d_%d" % (_video_name,_exp,_gain)
        mylogger.info("continue, %s%d_%s.mp4" % (_table[0], _table[1], _video_name))

        _sql = "insert into video_files_table(cameraID,cmosID,src_name, to_name,waiting_Timet,ServerID)values" \
               "('%s',%d,'%s%d_%s.mp4','%s',0,'%s')" % (_table[0], _table[1],_table[0], _table[1], _video_name, _to_file,_CurServerID)
        _cur.execute(_sql)#waiting for move



        _sql = "update video_rtsp2mp4_table set startTimet=%d,movedetectTimet=%d, waiting_filename='%s', waiting_Timet=%d," \
               "CurFileName='%s' where cameraID='%s' and cmosID=%d" % (
            _timeSec,_timeSec, _table[7], _timeSec, _video_name, _table[0], _table[1])
        _cur.execute(_sql)

    except Exception, e:
        mylogger.error(str(e))
        mylogger.error(_sql)


def close_video_process(_cur,_table):
    global mylogger
    snfile = "/tmp/rtsp2mp4/%s%d.%d" % (_table[0], _table[1],(_table[14]-1)&3)
    #localtime1 = time.localtime()
    #_video_name = "%02d%02d%02d" % (localtime1.tm_hour, localtime1.tm_min, localtime1.tm_sec)
    _timeSec = int(time.time())
    try:
        fp = open(snfile, 'w')
        ms_dic = {"end": 1}
        fp.write(json.dumps(ms_dic))
        fp.close()
    except Exception, e:
        mylogger.error(str(e))
    mylogger.info("close %s%d_%s.mp4"%(_table[0],_table[1],_table[7]))
    try:
        _cur.execute("update video_rtsp2mp4_table set startTimet=0, ServerID=NULL, movedetectTimet=0,waiting_filename='%s',"
                     " waiting_Timet=%d,video_pid=0,video_p_state=0 where cameraID='%s' and cmosID=%d"%(_table[7],_timeSec,_table[0],_table[1]))
    except Exception, e:
        mylogger.error(str(e))
    return

def move_video_files(_cur):
    global mylogger, ServerIP, _CurServerID, Keep_moving_video, log_cur
    _timeSec = int(time.time())
    try:
        #_src_file = "%s%d_%s.mp4" % (_table[0], _table[1], _table[8])
        localtime1 = time.localtime()
        _day_str = "%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
        _sql = "select * from video_files_table where waiting_Timet<%d and waiting_Timet!=0 and ServerID=%s"\
               %(_timeSec-25,_CurServerID)
        _a1 = _cur.execute(_sql)
        if 0 != _a1:
            _files = _cur.fetchall()
            for _file in _files:
                if None == _file[7]:
                    continue
                _video_type_int = int(_file[7])

                if 0 != Keep_moving_video or (
                            3 != _video_type_int and 33 != _video_type_int and 333 != _video_type_int):
                    if _file[8] < 50:
                        try:
                            _cur.execute("delete from video_files_table where id=%d" % _file[0])
                            os.remove(_file[3])
                        except Exception,e:
                            mylogger.warning("file %s is end with %d"%(_file[3],_file[8]))
                            mylogger.error(str(e))
                        continue
                    _ret = -1
                    _retry = _file[6] + 1
                    if os.path.exists(_file[3]):
                        try:
                            #os.rename(_file[3], _file[4])
                            if None == _file[7]:
                                _to_file = _file[4]+'_xxx.mp4'
                            else:
                                _to_file = _file[4]+'_%s.mp4'%_file[7]
                            shutil.move(_file[3], _to_file)
                            _ret = 0
                        except Exception,e:
                            mylogger.error(str(e)+' : '+_file[3] + " retry %d"%_retry)

                    if 0 == _ret or _retry > 3:
                        _cur.execute("delete from video_files_table where id=%d"%_file[0])
                        if 0 == _ret:
                            _db_filename = _to_file.lstrip("../").lstrip("../")
                            _sql = "insert into video_log_%s(cameraID,cmosID,get_time,filename,video_type,serverIP)" \
                                   "values('%s',%d,now(),'%s','%s','%s')" \
                                   % (_day_str, _file[1], _file[2], _db_filename, _file[7],ServerIP)
                            try:
                                log_cur.execute(_sql)  # logs, get_time is the same as filename
                            except Exception, e:
                                mylogger.error("log_cur:"+str(e))
                                if 'MySQL server has gone away' in str(e):
                                    log_cur = get_a_sql_cur_forever('alglog')  # logs, get_time is the same as filename
                        if _retry > 3:
                            mylogger.warning("move %s > 3 times"%_file[3])
                    else:
                        _cur.execute("update video_files_table set waiting_Timet=%d, retry_flag=%d where id=%d" \
                                     % (_timeSec, _retry, _file[0]))
                else:
                    try:
                        _cur.execute("delete from video_files_table where id=%d" % _file[0])
                        os.remove(_file[3])
                        mylogger.info(_file[3]+" is moving,remove file")
                    except Exception, e:
                        mylogger.warning("file %s is end with %d" % (_file[3], _file[8]))
                        mylogger.error(str(e))
                    continue
    except Exception,e:
        mylogger.error(str(e))
    return


"""
video type:
1:in
2:out
3:moving
4:out a car,and in
"""
def video_files_log(_cur,_table):
    global mylogger

    try:
        _sql = "select bays from aisettingtable_camera_mem where cameraID='%s' and cmosID=%d"% (_table[0], _table[1])
        _cur.execute(_sql)
        (_bays,) = _cur.fetchone()
        if None == _bays:
            _video_type = '666'
            _bays = 0
        else:
            _sql = "select bay,State from aiouttable_bay where cameraID='%s' and cmosID=%d and bay<=%d ORDER BY bay" % (_table[0], _table[1],_bays)
            _cur.execute(_sql)
            _aiStates = _cur.fetchall()
            if None == _aiStates:
                _video_type = '555'
            else:
                _video_type = ""
                for i in range(_bays):
                    if _table[6][i] == '4':
                        _video_type += '4'
                    elif _table[6][i] == '1' and 0 == _aiStates[i][1]:#out
                        _video_type += '2'
                    elif _table[6][i] == '0' and 1 == _aiStates[i][1]:#in
                        _video_type += '1'
                    elif _table[6][i] == '0' and 0 == _aiStates[i][1]:
                        _video_type += '3'
                    elif _table[6][i] == '1' and 1 == _aiStates[i][1]:
                        _video_type += '3'
                    else:
                        _video_type += '3'  #moving

        _sql = "update video_files_table set video_type='%s',waiting_Timet=%d where src_name='%s%d_%s.mp4'"\
               %(_video_type, int(time.time()), _table[0], _table[1],_table[8])
        _cur.execute(_sql)
        _cur.execute("update video_rtsp2mp4_table set waiting_Timet=0 where cameraID='%s' and cmosID=%d" % (
            _table[0], _table[1]))
    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(_sql)
        mylogger.error("start_aiout=%s,len=%d" % (_table[6], _bays))
    return


def start_video_record(_cur, _table):
    global mylogger,_CurServerID

    try:
        _sql = "select * from video_user_set where cameraID='%s'" % _table[0]
        if 0 != _cur.execute(_sql):
            _video_user_set = _cur.fetchone()
            if 0 == _video_user_set[4]:
                return
        if 0 != _table[9]:
            video_files_log(_cur, _table)
        localtime1 = time.localtime()
        try:
            os.remove("/tmp/rtsp2mp4/%s%d_O"%(_table[0],_table[1]))
        except Exception,e:
            mylogger.info(str(e) + " /tmp/rtsp2mp4/%s%d_O"%(_table[0],_table[1]))
        _sql = "select ip from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d"%(_table[0],_table[1])
        _cur.execute(_sql)
        _ips = _cur.fetchone()
        if None == _ips:
            mylogger.warning("No ip = "+_sql)
            return
        else:
            _ip = _ips[0]



        _video_name = "%02d%02d%02d" % (localtime1.tm_hour, localtime1.tm_min, localtime1.tm_sec)
        cmd1 = "./rtsp_client -4 -F %s%d -P 1 -D 20 -e %d -N %s rtsp://%s/h.264" % (_table[0],_table[1],_table[14],_video_name,_ip)

        """./openRTSP -4 -K -F 18054300420 -P 1 -D 5 -e 1 -N 204446 rtsp://192.168.101.125/h.264
        -K for keep-alive default 60sec; 
        -D 20 for stream gap,if the net is broken,after 20sec,the process is end,
        -e cmd file extension, when start a new process for video stream,and the older is not closed,same cmd file will error.
        -P from 5 to 1, faster to close the older video process,when the older is closing and the new one is opening"""

        mylogger.info(cmd1)
        thread.start_new_thread(python_cmd, (cmd1,))
        _timeSec = int(time.time())

        _cur.execute("update video_rtsp2mp4_table set startTimet=%d,ServerID='%s',CurFileName='%s',"
                     "waiting_filename=NULL,waiting_Timet=0,video_pid=0,video_p_state=0,file_ext=%d"
                     " where cameraID='%s' and cmosID=%d"
                     ""%(_timeSec,_CurServerID,_video_name,(_table[14]+1)&3,_table[0],_table[1]))


        _day_str = "%d%02d%02d"% (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
        _to_file = "../../video/"+_day_str

        _to_file += "/%s%d" % (_table[0], _table[1])
        if not os.path.exists(_to_file):
            try:
                os.mkdir(_to_file)
            except Exception, e:
                mylogger.error(e)

        _sql = "select exp,gain from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d" % (_table[0], _table[1])
        _exp = 66666
        _gain = 16
        if 0 != cur.execute(_sql):
            (_exp,_gain,) = cur.fetchone()


        _to_file += "/%s_%d_%d" % (_video_name,_exp,_gain)
        try:


            _sql = "insert into video_files_table(cameraID,cmosID,src_name, to_name,waiting_Timet,ServerID)" \
                   "values('%s',%s,'%s%d_%s.mp4','%s',0,'%s')" \
                   % (_table[0], _table[1], _table[0], _table[1],_video_name,_to_file,_CurServerID)
            _cur.execute(_sql)
        except Exception, e:
            mylogger.error(str(e))
            mylogger.error(_sql)
    except Exception,e:
        mylogger.error(str(e))
    return

def check_max_rtsp_client_ch(_cur):
    _a1 = _cur.execute("select * from video_user_set where video_timet!=0 and video_en=1")
    _max_rtsp = 128
    if 0 != _a1:
        _cur.execute("select max(video_def) from video_user_set where video_timet!=0 and video_en=1")
        _max_def = _cur.fetchone()[0]
        if 0 != _max_def and _max_def > 576:
            video_def_dictH = ((1920, 25), (1600, 40), (1280, 50), (1056, 64), (864, 96), (640, 128), (576, 200))
            video_def_dictL = ((1920, 8), (1600, 16), (1280, 32), (1056, 48), (864, 64), (640, 96), (576, 128))
            pc_mem = psutil.virtual_memory()
            if pc_mem.total > 8 * 1024 * 1024 * 1024:
                video_def_ptr = video_def_dictH
            else:
                video_def_ptr = video_def_dictL
            for vdef in video_def_ptr:
                if _max_def > vdef[0]:
                    _max_rtsp = vdef[1]
                    break
    return _max_rtsp


def get_serverID():
    _dict = wtclib.get_user_config_ret_dict("../conf/id.conf", "system")
    if not "serverid" in _dict:
        _dict.update({"serverid":"1710890123"})
        wtclib.set_user_config_from_dict("../conf/id.conf", "system", _dict)

    return _dict["serverid"]


def get_a_sql_cur_forever(db_name=None):
    global mylogger
    while True:
        if None == db_name:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        else:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf", dbn=db_name)
        if None != _cur:
            break
        else:
            mylogger.info(err)
            time.sleep(20)
    return _cur


def rtsp_client_process_wdt(cmd):
    global wdtlogger,_CurServerID
    wdtlogger.info("start running")
    _cur = get_a_sql_cur_forever()

    while True:
        _timeSec = int(time.time())
        try:
            if 0 != _cur.execute("select cameraID,cmosID,video_p_state,CurFileName from video_rtsp2mp4_table where ServerID='%s' and video_pid != -1"%_CurServerID):
                _cameraIDs = _cur.fetchall()
                for _cameraID in _cameraIDs:
                    try:
                        fp = open("/tmp/rtsp2mp4/%s%d_O"%(_cameraID[0],_cameraID[1]))
                        fpd = fp.read()
                        fp.close()
                    except Exception,e:
                        mylogger.warning(str(e)+" @ "+_cameraID[0])
                        continue
                    try:
                        if None == fpd or 0 == len(fpd):
                            continue
                        _dict_pid = json.loads(fpd)
                        _sql = "update video_rtsp2mp4_table set video_pid=%d,video_p_state=%d,video_p_name='%s'," \
                               "video_p_timet=%d where cameraID='%s' and cmosID=%d"\
                               %(_dict_pid["pid"],_dict_pid["state"],_dict_pid["name"],_dict_pid["timet"],
                                 _cameraID[0],_cameraID[1])
                        _cur.execute(_sql)
                        if _cameraID[2] != _dict_pid["state"]:
                            mylogger.info("pid=%d, old_state=%d, new=%d where cameraid=%s and filename=%s"
                                          %(_dict_pid["pid"],_cameraID[2],_dict_pid["state"],_cameraID[0],_cameraID[3]))
                    except Exception,e:
                        wdtlogger.warning("not json %s"%fpd)
                    #if isinstance(fpd,(str,unicode)):


            if 0 !=  _cur.execute("select * from video_rtsp2mp4_table where video_pid > 0 and video_p_timet<%d"%(_timeSec-30)):
                _rtsp_clients = _cur.fetchall()
                pids1 = psutil.pids()
                for _rtsp_client in _rtsp_clients:
                    if not _rtsp_client[10] in pids1:
                        _sql = "update video_rtsp2mp4_table set video_pid=-1 where cameraID='%s' and cmosID=%d"%(_rtsp_client[0],_rtsp_client[1])
                        _cur.execute(_sql)
                    if _rtsp_client[11] < 50:
                        wdtlogger.warning("%s %d file=%s pid=%d end with state=%d,%s"\
                                          %(_rtsp_client[0],_rtsp_client[1],_rtsp_client[7],_rtsp_client[10],
                                            _rtsp_client[11],_rtsp_client[12]))
                    _sql = "update video_files_table set video_end =%d where src_name='%s%d_%s.mp4'"\
                           %(_rtsp_client[11], _rtsp_client[0],_rtsp_client[1],_rtsp_client[7])
                    _cur.execute(_sql)

        except Exception,e:
            wdtlogger.error(str(e))
            _cur = get_a_sql_cur_forever()
        time.sleep(2)





if __name__ == '__main__':
    #shutil.move("17124360930_161626.mp4", "../123.mp4")
    if not os.path.isdir("../log/rtsp2mp4m"):
        try:
            os.mkdir("../log/rtsp2mp4m")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()

    mylogger = wtclib.create_logging("../log/rtsp2mp4m/m.log")
    wdtlogger = wtclib.create_logging("../log/rtsp2mp4m/wdt.log")

    mylogger.info("start running")
    if not os.path.isdir("/tmp/rtsp2mp4"):
        try:
            os.mkdir("/tmp/rtsp2mp4")
        except Exception, e:
            mylogger.error(str(e))
            os._exit(1)
    _Max_video_sec = 900
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "file_save")
    if "video_length_sec" in conf_dict:
        _Max_video_sec = int(conf_dict["video_length_sec"])
    if _Max_video_sec > 1800 or _Max_video_sec < 30:
        _Max_video_sec = 900

    _end_moving_sec = 45
    if "end_moving_sec" in conf_dict:
        _end_moving_sec = int(conf_dict["end_moving_sec"])
    if _end_moving_sec > 900 or _end_moving_sec < 20:
        _end_moving_sec = 45
    Keep_moving_video = 0
    if "keep_moving_video" in conf_dict:
        Keep_moving_video = int(conf_dict["keep_moving_video"])

    try:
        _video_path = ''
        _link_to = ''
        if "video_path" in conf_dict:
            _video_path = conf_dict["video_path"]
            if os.path.isdir(_video_path):
                if not os.path.exists("../../video"):
                    os.symlink(_video_path, "../../video")
                elif os.path.islink("../../video"):
                    _link_to = os.readlink("../../video")
                    if 0 != cmp(_link_to, _video_path):
                        os.unlink("../../video")
                        os.symlink(_video_path, "../../video")
                elif os.path.isdir("../../video"):
                    if os.path.isdir("../../video2"):
                        shutil.rmtree("../../video2")
                    os.rename("../../video", "../../video2")
                    os.symlink(_video_path, "../../video")


        if not os.path.exists("../../video"):
            os.mkdir("../../video")

    except Exception,e:
        mylogger.error(str(e))
        mylogger.error("new=%s,old=%s"%(_video_path,_link_to))
    if "smart_video" in conf_dict and 0 == conf_dict["smart_video"]:
        mylogger.info("smart video disable, end")
        os._exit(0)
    del conf_dict,_video_path,_link_to

    _CurServerID = get_serverID()
    ServerIP = wtclib.get_ip_addr1("eth0")
    cur = get_a_sql_cur_forever()

    _timeSecf = time.time()
    _timeSec = int(_timeSecf)
    try:
        cur.execute("delete from video_rtsp2mp4_table where length(ServerID)=0")
        cur.execute("update video_files_table set waiting_Timet=%d where ServerID='%s'"%(_timeSec,_CurServerID))
    except Exception,e:
        mylogger.error(str(e))



    _max_rtsp_client = check_max_rtsp_client_ch(cur)
    _day_dir_flag = 0
    localtime1 = time.localtime()
    _day_str = "%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
    _to_file = "../../video/%s" % (_day_str)
    if not os.path.exists(_to_file):
        try:
            os.mkdir(_to_file)
        except Exception, e:
            mylogger.error(e)
    log_cur = get_a_sql_cur_forever('alglog')
    log_cur.execute("create table if not exists video_log_%s("
                "id int not null auto_increment primary key,"
                "cameraID char(24) , "
                "cmosID tinyint default 0,"
                "get_time DATETIME, "
                "video_type char(32),"
                "used_flag char(8),"
                "filename char(64),"
                "serverIP char(24)"
                ")" % _day_str)
    del _to_file, localtime1

    _cmd1 = "asd"

    thread.start_new_thread(rtsp_client_process_wdt, (_cmd1,))
    while True:
        _timeSecf = time.time()
        _timeSec = int(_timeSecf)

        try:
            if 0 == _timeSec%16:
                _max_rtsp_client = check_max_rtsp_client_ch(cur)
                localtime1 = time.localtime(_timeSec+3500)
                if 0 == localtime1.tm_hour:
                    if 0 == _day_dir_flag:
                        _day_dir_flag = 1
                        _day_str = "%d%02d%02d"% (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
                        _to_file = "../../video/"+_day_str
                        if not os.path.exists(_to_file):
                            try:
                                os.mkdir(_to_file)
                            except Exception, e:
                                mylogger.error(e)
                        try:
                            log_cur.execute("create table if not exists video_log_%s("
                                        "id int not null auto_increment primary key,"
                                        "cameraID char(24) , "
                                        "cmosID tinyint default 0,"
                                        "get_time DATETIME, "
                                        "video_type char(32),"
                                        "used_flag char(8),"
                                        "filename char(64),"
                                        "serverIP char(24)"
                                        ")" % _day_str)
                        except Exception,e:
                            mylogger.error('log_cur: ' + str(e))
                            if 'MySQL server has gone away' in str(e):
                                log_cur = get_a_sql_cur_forever('alglog')
                        del _day_str, _to_file
                else:
                    _day_dir_flag = 0
                del localtime1

            try:
                _a1 = cur.execute("select * from video_rtsp2mp4_table where ServerID is not NULL and ((movedetectTimet<%d and movedetectTimet!=0) or video_pid<0)"%(_timeSec-_end_moving_sec))
                if(0 != _a1):
                    _OnRecords_Ending = cur.fetchall()
                    if None != _OnRecords_Ending:
                        for _rec in _OnRecords_Ending:
                            close_video_process(cur, _rec)
                        del _OnRecords_Ending
            except Exception,e:
                mylogger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    cur = get_a_sql_cur_forever()

            _a1 = cur.execute("select * from video_rtsp2mp4_table where ServerID is not NULL and startTimet<%d and startTimet!=0" % (_timeSec - _Max_video_sec))
            if (0 != _a1):
                _OnRecords_continue = cur.fetchall()
                if None != _OnRecords_continue:
                    for _rec in _OnRecords_continue:
                        if 0 == _rec[5]:
                            close_video_process(cur, _rec)
                        else:
                            continue_video_process(cur,_rec)
                    del _OnRecords_continue

            cur.execute("select count(*) from video_rtsp2mp4_table where ServerID is not NULL")
            _recordingCnt = cur.fetchone()[0]

            _a1 = cur.execute("select * from video_rtsp2mp4_table where waiting_Timet != 0")
            if (0 != _a1):
                _waitings = cur.fetchall()
                if None != _waitings:
                    for _wait1 in _waitings:
                        video_files_log(cur, _wait1)
                    del _waitings

            _a1 = cur.execute("select * from video_rtsp2mp4_table where ServerID is NULL and movedetectTimet!=0")
            if (0 != _a1):
                _BeginRecords = cur.fetchall()
                if None != _BeginRecords:
                    for _begin in _BeginRecords:
                        if _begin[5] < _timeSec-300:
                            cur.execute("update video_rtsp2mp4_table set movedetectTimet=0 where cameraID='%s' and "
                                        "cmosID=%d"%(_begin[0],_begin[1]))
                            continue
                        if _recordingCnt > _max_rtsp_client:
                            mylogger.warning("> %d Channels RTSP video"%_max_rtsp_client)
                            break
                        _recordingCnt += 1
                        start_video_record(cur, _begin)
                    del _BeginRecords

            move_video_files(cur)
        except Exception,e:
            mylogger.error(str(e))

        _cur_timet = time.time()
        print "use %f sec, and %d Recorders @ %f" % (_cur_timet - _timeSecf, _recordingCnt, _cur_timet)
        time.sleep(0.5)