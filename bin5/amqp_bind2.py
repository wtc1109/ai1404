
import MySQLdb
import pika
import time,datetime
import json
import psutil
import urllib2
import os, sys
import Queue
import wtclib
import shutil
import sysv_ipc
import struct,binascii
import threading,thread
import glob

#import Tyf

from PIL import Image as ImagePIL

NEW_daybook_create = 1
RE_settings = {}
AI_out2s = {}
title_queue = Queue.Queue(maxsize=5)
result_queue = Queue.Queue(maxsize=5)
yuvjpg_queue = Queue.Queue(maxsize=5)


class sync_data_from_HDD(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/re_shell/sync.log')
        threading.Thread.__init__(self)
    def run(self):

        self.__logger.info("sync start")

        sync_cur = get_a_sql_cur_forever(self.__logger)
        try:
            _sql_str = "select max(set_time) from resettingtable"
            sync_cur.execute(_sql_str)
            _datetime, = sync_cur.fetchone()
            if None == _datetime:
                _datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _sql_str = "TRUNCATE TABLE resettingtablemem"
            sync_cur.execute(_sql_str)
            _sql_str = "insert into resettingtablemem select * from resettingtable"
            sync_cur.execute(_sql_str)
            _sql_str = "SELECT * FROM resettingtable"
            if 0 != sync_cur.execute(_sql_str):
                _settings = sync_cur.fetchall()
                for _setting in _settings:
                    RE_settings.update({_setting[0]: [info for info in _setting]})
        except Exception,e:
            self.__logger.error(str(e))
            self.__logger.error(_sql_str)
            if 'MySQL server has gone away' in str(e):
                sync_cur = get_a_sql_cur_forever(self.__logger)

        while True:
            try:
                _sql_str = "select * from resettingtable where set_time >'%s'"%_datetime
                if 0 != sync_cur.execute(_sql_str):
                    _new_settings = sync_cur.fetchall()
                    for _new_set in _new_settings:
                        _sql_str = "replace into resettingtablemem select * from resettingtable where " \
                                   "cameraID='%s' and cmosID=%d"%(_new_set[0],_new_set[1])
                        sync_cur.execute(_sql_str)
                        RE_settings.update({_new_set[0]: [info for info in _new_set]})
                else:
                    self.__logger.debug("None resetting need update")
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    sync_cur = get_a_sql_cur_forever(self.__logger)

            time.sleep(5)
                #finally:


class get_ai_out2_info(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/re_shell/ai_out2.log')
        threading.Thread.__init__(self)

    def run(self):

        self.__logger.info("aiout2 start")

        aiout2_cur = get_a_sql_cur_forever(self.__logger)
        try:
            _sql_str = "select max(LatestUpdate) from aiouttable_bay2"
            aiout2_cur.execute(_sql_str)
            _datetime, = aiout2_cur.fetchone()
            if None == _datetime:
                _datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__logger.info("latest time is %s"%_datetime)

            _sql_str = "SELECT * FROM aiouttable_bay2"
            _a1 = aiout2_cur.execute(_sql_str)
            if 0 != _a1:
                self.__logger.info("get %d aiouttable_bay2" % _a1)
                _settings = aiout2_cur.fetchall()
                for _setting in _settings:
                    _sql_str = "SELECT bays FROM aiouttable_camera2 where cameraID='%s'"%_setting[0]
                    aiout2_cur.execute(_sql_str)
                    _bays, = aiout2_cur.fetchone()
                    if None == _bays:
                        continue
                    for i in range(_bays):
                        _bay_id = "%s0%d"%(_setting[0], _setting[2])
                        AI_out2s.update({_bay_id: [[info for info in _setting],_bays]})

            ServerID = wtclib.get_serverID()
            _sql_str = "insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, " \
                       "'python %s &', 360, %d,'%s')" % (os.getpid(), __file__, time.time(), ServerID)
        except Exception, e:
            self.__logger.error(str(e))
            self.__logger.error(_sql_str)
            if 'MySQL server has gone away' in str(e):
                aiout2_cur = get_a_sql_cur_forever(self.__logger)
        wdi_time30sec = int(time.time()) / 32
        while True:
            try:

                _sql_str = "select * from aiouttable_bay2 where LatestUpdate >'%s'" % _datetime
                if 0 != aiout2_cur.execute(_sql_str):
                    _new_settings = aiout2_cur.fetchall()
                    _sql_str = "select max(LatestUpdate) from aiouttable_bay2"
                    aiout2_cur.execute(_sql_str)
                    _datetime, = aiout2_cur.fetchone()

                    for _new_set in _new_settings:
                        _sql_str = "SELECT bays FROM aiouttable_camera2 where cameraID='%s'"%_new_set[0]
                        aiout2_cur.execute(_sql_str)
                        _bays, = aiout2_cur.fetchone()
                        if None == _bays:
                            continue
                        for i in range(_bays):
                            _bay_id = "%s0%d" % (_new_set[0], _new_set[2])
                            AI_out2s.update({_bay_id: [[info for info in _new_set],_bays]})

                else:
                    self.__logger.debug("None aiout2 need update")
                _aiout2_time_Sec = int(time.time())
                _new_32sec = _aiout2_time_Sec / 32
                if wdi_time30sec != _new_32sec:
                    wdi_time30sec = _new_32sec
                    _sql_str = "update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" \
                               % (_aiout2_time_Sec, os.getpid(), ServerID)
                    aiout2_cur.execute(_sql_str)
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    aiout2_cur = get_a_sql_cur_forever(self.__logger)
            time.sleep(5)
            # finally:

class backup_yuv_jpg_files(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/re_shell/backup.log')
        threading.Thread.__init__(self)
    def run(self):
        self.__logger.info("backup yuv jpg start")
        #title_cur = get_a_sql_cur_forever(self.__logger)


        while True:
            msg = yuvjpg_queue.get(block=True)
            _dic_info = json.loads(msg)
            del msg
            self.__logger.info("receive yuv from %s %s"%(_dic_info["cam_id"], str(_dic_info["pic_full_name"])))
            try:
                localtime1 = time.localtime()

                _day_str = "../../re/jpg/%d%02d%02d/" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)

                if not os.path.isdir(_day_str):
                    os.mkdir(_day_str)
                _day_str += _dic_info["cam_id"]
                if not os.path.isdir(_day_str):
                    os.mkdir(_day_str)
                _re_yuv_path = "../../re/yuv/%d%02d%02d/%s" % (localtime1.tm_year, localtime1.tm_mon,
                                                               localtime1.tm_mday,_dic_info["cam_id"])

                _path, _file = os.path.split(str(_dic_info["pic_full_name"]))
                _filen, _ext = os.path.splitext(_file)
                _height = _dic_info["RBy"] - _dic_info["LTy"] + 1
                _width = _dic_info["RBx"] - _dic_info["LTx"] + 1
                _filename = "%d_%s_%dx%d"%(_dic_info["plateGet"], _filen, _width, _height)
                _jpg_tmp_name = os.path.join("/tmp/", _filename + '.jpg')

                yuv2jpg(os.path.join(_re_yuv_path, _filename+'.yuv'), _jpg_tmp_name, _width, _height)
                shutil.move(_jpg_tmp_name, os.path.join(_day_str, _filename + '.jpg'))
                #del _height,_width,_yuv_filename1,_new_yuv_name,_day_str,_dic_info,localtime1
            except Exception, e:
                #self.__logger.error(_sql_str)
                self.__logger.error(str(e))





class insert_reout_title(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/re_shell/title.log')
        threading.Thread.__init__(self)
    def run(self):
        self.__logger.info("title start")
        title_cur = get_a_sql_cur_forever(self.__logger)


        title_update_dict = {}

        while True:
            msg = title_queue.get(block=True)
            _dic_info = json.loads(msg)
            self.__logger.info("receive tile " + _dic_info["cam_id"])
            try:
                _title_time_Sec = int(time.time())
                if _dic_info["cam_id"] in title_update_dict:
                    if _title_time_Sec - title_update_dict[_dic_info["cam_id"]] < 10:
                        self.__logger.debug("not need title update with %s"%_dic_info["cam_id"])
                        continue
                    title_update_dict[_dic_info["cam_id"]] = _title_time_Sec
                else:
                    title_update_dict.update({_dic_info["cam_id"]:_title_time_Sec})

                _sql_str = "insert into reouttable_bay(cameraID,bay)values('%s',%d)ON DUPLICATE KEY UPDATE PlateupdateTimet=0;" \
                           % (_dic_info["cam_id"], _dic_info["plateGet"])
                title_cur.execute(_sql_str)
                _sql_str = "insert into reoutfiltertable(cameraID,bay)values('%s',%d)ON DUPLICATE KEY UPDATE PlateupdateTimet=0;" \
                           % (_dic_info["cam_id"], _dic_info["plateGet"])
                title_cur.execute(_sql_str)

                _sql_str = "select * from refiltertable where cameraID='%s' and bay=%d"% (_dic_info["cam_id"], _dic_info["plateGet"])
                if 0 == title_cur.execute(_sql_str ):
                    _sql_str = "insert into refiltertable(cameraID,bay)values('%s',%d)" % (_dic_info["cam_id"], _dic_info["plateGet"])
                    title_cur.execute(_sql_str)
                """
                _sql_str = "insert into resettingtable(cameraID,cmosID,set_time)values('%s',0,now())" \
                           "ON DUPLICATE KEY UPDATE ReNewFlag=0;" % (_dic_info["cam_id"])
                title_cur.execute(_sql_str)
                """
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):

                    title_cur = get_a_sql_cur_forever(self.__logger)

            #time.sleep(5)
                #finally:


def write_jpg_file_exif_comment(infile, _comment, outfile, logfile):
    try:
        fd = open(infile)
        fdp = fd.read()
        fd.close()
        #msg1 = "hello xxsfsdf"

        msg = struct.pack(">BBH%ds" % len(_comment), 255, 254, len(_comment) + 2, _comment)
        #print binascii.hexlify(msg)
        fd2 = open("/tmp/125.jpg", "wr")
        fd2.write(fdp[:2])
        fd2.write(msg)
        fd2.write(fdp[2:])
        fd2.close()
        shutil.copy("/tmp/125.jpg", outfile)
    except Exception,e:
        logfile.error(str(e))


class insert_reout_result(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/re_shell/result.log')
        threading.Thread.__init__(self)
    def run(self):
        global msg_props, REOUT_CH, Backup_re_jpg

        self.__logger.info("result start")
        conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "db")
        if "ai_daybook_en" in conf_dict:
            AI_daybook_en = int(conf_dict["ai_daybook_en"])
        else:
            AI_daybook_en = 0
        del conf_dict
        if 0 != AI_daybook_en:
            log_cur = get_a_sql_cur_forever(self.__logger, 'alglog')
        result_cur = get_a_sql_cur_forever(self.__logger)



        while True:
            msg = result_queue.get(block=True)

            try:
                _timeSec = int(time.time())
                try:
                    _O_cam_id, _O_cmos_id, _O_which_slot, _O_pic_full_name = struct.unpack("32s2b128s",msg[:162])
                    _cam_id = str(_O_cam_id.rstrip('\0'))
                    del _O_cam_id, _O_cmos_id
                    has_result, plate, plate_type, aveBrightnessCarplate, confidence = struct.unpack("b24s8s2B",msg[162:197])
                    """
                    has_result1, plate1, plate_type1, aveBrightnessCarplate1, confidence1 = struct.unpack("b24s8s2B",
                                                                                                     msg1[0][197:232])
                    has_result2, plate2, plate_type2, aveBrightnessCarplate2, confidence2 = struct.unpack("b24s8s2B",
                                                                                                     msg1[0][232:267])
                    """
                    _O_plate_stable, _O_staisitc_plate = struct.unpack("i24s", msg[268:296])

                    _O_use_by_statistic_plate = struct.unpack("24s24s24s24s24s24s24s24s", msg[296:488])
                    _O_ai_filename, = struct.unpack("128s", msg[488:616])
                    _ai_filename = str(_O_ai_filename.rstrip('\0'))
                    _plate = str(plate.rstrip('\0'))
                    _plate_type = str(plate_type.rstrip('\0'))
                    #_plate_type = "blue"
                    print "pic full name " + _O_pic_full_name
                    _pic_name_after = str(_O_pic_full_name).rstrip('\0')
                    _staisitc_plate = str(_O_staisitc_plate).rstrip('\0')
                    del plate, plate_type, _O_pic_full_name, _O_ai_filename
                    del msg,_O_staisitc_plate
                    #_O_which_slot += 1
                    self.__logger.info(
                        "get %s bay%d VLPR out staisitc:%s, %s" % (_cam_id, _O_which_slot, _staisitc_plate, _plate))
                    body = json.dumps({"cam_id":_cam_id,"CMOS":0})
                except Exception, e:
                    self.__logger.error(str(e))
                    continue

                localtime1 = time.localtime()
                if 0 != AI_daybook_en:
                    mylogger.debug("AI daybook")

                    ailog_table = "ailog%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)

                    try:

                        _sql_str = "UPDATE %s SET reyuv%dname='%s',plate%dNumber='%s',plate%dconfidence=%d," \
                                   "plate%dbrightness=%d,plate%dstable=%d,stableplate%dnumber='%s'," \
                                   "plate%dupdateTimet=now() WHERE aijpgname='%s'" \
                                   % (ailog_table, _O_which_slot, _pic_name_after,
                                      _O_which_slot, _plate, _O_which_slot,
                                      confidence, _O_which_slot, aveBrightnessCarplate, _O_which_slot,
                                      _O_plate_stable,
                                      _O_which_slot, _staisitc_plate, _O_which_slot,
                                      _ai_filename)
                        log_cur.execute(_sql_str)
                        self.__logger.debug(_sql_str)
                    except Exception, e:
                        self.__logger.error(str(e))
                        self.__logger.error(_sql_str)
                        if 'MySQL server has gone away' in str(e):
                            log_cur = get_a_sql_cur_forever(self.__logger, 'alglog')
                        continue
                _after_filename1 = _pic_name_after.split('.')[0]
                _after_filename = _after_filename1.split('/')[-1]
                _day_file = "%d%02d%02d/%s0/%s.jpg"%(localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday,_cam_id,_after_filename)
                _path_file = os.path.join('../../re/save_orig_jpg',_day_file)

                if False == has_result:  # not result
                    self.__logger.debug("no result")
                    try:
                        _sql_str = "update reouttable_bay set PlateupdateTimet=%d,PlateNumber=null,Platetype=null," \
                                   "set_time=now() where cameraID='%s' and bay=%d" % (_timeSec,_cam_id,_O_which_slot)
                        result_cur.execute(_sql_str)


                        _comment = "sn:%s; plate:noplr"%_cam_id
                    except Exception, e:
                        self.__logger.error(_sql_str)
                        self.__logger.error(str(e))
                        if 'MySQL server has gone away' in str(e):
                            result_cur = get_a_sql_cur_forever(self.__logger)
                        continue
                else:
                    self.__logger.debug("has result")

                    try:
                        _sql_str = "update reouttable_bay set PlateupdateTimet=%d,PlateNumber='%s'," \
                                   "Platetype='%s',set_time=now() where cameraID='%s' and bay=%d" \
                                   % (_timeSec, _plate,_plate_type, _cam_id, _O_which_slot)
                        result_cur.execute(_sql_str)

                        _comment = "sn:%s; plate:%s, type:%s, bright:%d, confidence:%d, stableplate=%s"\
                                   %(_cam_id,_plate,_plate_type,aveBrightnessCarplate,confidence,_staisitc_plate)

                        result_cur.execute(_sql_str)
                    except Exception, e:
                        self.__logger.error(_sql_str)
                        self.__logger.error(str(e))
                        if 'MySQL server has gone away' in str(e):
                            result_cur = get_a_sql_cur_forever(self.__logger)
                        continue

                try:
                    _sql_str = "update refiltertable set "
                    for i in range(1, 9):
                        _sql_str += "PlateNumber%d='%s'," % (i, str(_O_use_by_statistic_plate[i - 1].rstrip('\0')))

                    _sql_str += "cmosID=0 where cameraID='%s' and bay=%d" % (_cam_id,  _O_which_slot)

                    result_cur.execute(_sql_str)
                    if "1801430011" == _cam_id:
                        self.__logger.warning(_sql_str)

                    if '' == _staisitc_plate:
                        _sql_str = "UPDATE reoutfiltertable SET PlateupdateTimet=%d,PlateDatetime=now()," \
                                   "PlateNumber=null,Platetype=null WHERE cameraID='%s' and bay=%d" \
                                   % (_timeSec, _cam_id, _O_which_slot)
                    else:
                        _sql_str = "UPDATE reoutfiltertable SET PlateupdateTimet=%d,PlateDatetime=now()," \
                                   "PlateNumber='%s',Platetype='%s' WHERE cameraID='%s'and bay=%d" \
                                   % (_timeSec, _staisitc_plate, _plate_type, _cam_id, _O_which_slot)
                    result_cur.execute(_sql_str)
                    if "1801430011" == _cam_id:
                        self.__logger.warning(_sql_str)
                        self.__logger.warning("_staisitc_plate=%s" % _staisitc_plate)


                    _sql_str = "select ip from onlinehvpdstatustablemem where cameraID='%s'"%_cam_id

                    _ip = ''
                    if 0 != result_cur.execute(_sql_str):
                        _ip, = result_cur.fetchone()
                        _comment += "; ip:%s"%_ip

                    #_sql_str = "insert into jpgexif(file,comment)values('%s','%s')"% (_path_file, _comment)
                    #result_cur.execute(_sql_str)
                    write_jpg_file_exif_comment(_path_file, _comment, _path_file, self.__logger)
                    if _staisitc_plate != _plate and '' != _staisitc_plate and '1' == Backup_re_jpg:
                        try:
                            self.__logger.info("un %s file while staisitc is %s,and plate is %s"%(_path_file, _staisitc_plate,_plate))
                            _day_path = '../../re/un_jpg/%d%02d%02d/' % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
                            if not os.path.isdir(_day_path):
                                os.mkdir(_day_path)
                            _camera_path = _day_path+"%s0"%_cam_id
                            if not os.path.isdir(_camera_path):
                                os.mkdir(_camera_path)
                            _path_file2 = os.path.join('../../re/un_jpg', _day_file)
                            shutil.copy(_path_file, _path_file2)

                            _day_file_yuv = "%d%02d%02d/%s0/%s.yuv" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday, _cam_id, _after_filename)
                            _path_file_yuv = os.path.join('../../re/save_orig_yuv', _day_file_yuv)
                            _path_file_yuv2 = os.path.join('../../re/un_yuv', _day_file_yuv)
                            _day_path = '../../re/un_yuv/%d%02d%02d/'% (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
                            if not os.path.isdir(_day_path):
                                os.mkdir(_day_path)
                            _camera_path = _day_path+"%s0"%_cam_id
                            if not os.path.isdir(_camera_path):
                                os.mkdir(_camera_path)
                            shutil.copy(_path_file_yuv, _path_file_yuv2)
                        except Exception,e:
                            self.__logger.error(str(e))
                            self.__logger.error(_day_path)


                    _path = "../../ai/save_img/%d%02d%02d/%02d/%s0/" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday,
                                                                        4 * (localtime1.tm_hour / 4), _cam_id)
                    (_file, _ext) = os.path.splitext(_ai_filename)
                    _filename = "%s*.jpg" % _file
                    _find_file = glob.glob(_path + _filename)
                    if 0 == len(_find_file) or len(_find_file) > 1:
                        continue

                    _comment = "sn:%s; ip: %s; "%(_cam_id,_ip)
                    for i in range(3):
                        _sql_str = "select * from reoutfiltertable where cameraID='%s' and bay=%d" % (_cam_id,i+1)
                        if 0 == result_cur.execute(_sql_str):
                            continue
                        _reoutfilter = result_cur.fetchone()
                        if None == _reoutfilter or None == _reoutfilter[5]:
                            continue
                        _comment += "plate%d:%s,plate%dtype:%s "%(i+1,_reoutfilter[5],i+1,_reoutfilter[6])


                    #_sql_str = "insert into jpgexif(file,comment)values('%s','%s')" % (_find_file[0], _comment)
                    #result_cur.execute(_sql_str)
                    write_jpg_file_exif_comment(_find_file[0], _comment, _find_file[0], self.__logger)
                except Exception, e:
                    self.__logger.error(str(e))
                    self.__logger.error(_sql_str)
                    if 'MySQL server has gone away' in str(e):
                        result_cur = get_a_sql_cur_forever(self.__logger)
                    continue


            except Exception,e:
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    result_cur = get_a_sql_cur_forever(self.__logger)
                continue
            try:
                self.__logger.debug("rabbitmq publish:VLPR " + body)
                REOUT_CH.basic_publish(body=body, exchange="ReOut.tr", properties=msg_props,
                                       routing_key="plate queue")
            except Exception,e:
                self.__logger.error(str(e))
                self.__logger.error("REOUT_CH.basic_publish false")
                REOUT_CH = get_plateOUT_rabbitmq_channel()





def get_a_sql_cur_forever(mylog, db_name=None):
    while True:
        if None == db_name:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        else:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf", dbn=db_name)
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur



def yuv444_torgb888(width, height, yuv):
    rgb_bytes = bytearray(width*height*3)

    red_index = 0
    green_index = 1
    blue_index = 2
    y_index = 0
    for row in range(height):
        u_index = width*height+(row)*(width)
        v_index = width*height*2+(row)*(width)
        for column in range(width):
            Y = ord(yuv[y_index])
            U = ord(yuv[u_index])
            V = ord(yuv[v_index])
            C = (Y-16)*298
            D = U-128
            E = V-128
            R = (C + 409*E + 128)//256
            G = (C - 100*D -208*E + 128)//256
            B = (C + 516*D + 128) // 256
            R = 255 if(R>255) else (0 if(R < 0) else R)
            G = 255 if(G > 255) else (0 if(G < 0) else G)
            B = 255 if(B > 255) else (0 if(B < 0) else B)
            rgb_bytes[red_index] = R
            rgb_bytes[green_index] = G
            rgb_bytes[blue_index] = B
            u_index += 1
            v_index += 1
            y_index += 1
            red_index += 3
            green_index += 3
            blue_index += 3
    return rgb_bytes


def yuv2jpg(fi, fo, w, h):
    f = open(fi, "rb")
    yuv = f.read()
    f.close()

    rgb_bytes = yuv444_torgb888(w, h, yuv)
    img1 = ImagePIL.frombytes("RGB", (w, h), bytes(rgb_bytes))
    img1.save(fo, "JPEG", quality=99)

MSG_send_error_cnt = 0

def clear_reset_vlpr():
    global msgsnd_ipc, mylogger, MSG_send_error_cnt
    os.system("killall ai_vlpr")
    mylogger.error("killall ai_vlpr")
    cnt = 0
    while True:
        try:
            msgsnd_ipc.receive(block=False,type=0)
            cnt += 1
        except Exception,e:
            mylogger.error(str(e))
            mylogger.error("recv %d msg"%cnt)
            break
    time.sleep(0.5)
    cmd1 = "./ai_vlpr &"
    thread.start_new_thread(python_cmd, (cmd1,))
    MSG_send_error_cnt = 0
    mylogger.error("restart vlpr")
    time.sleep(5)
    os.system("rabbitmqctl purge_queue plate.in")


def msg_consumer(channel, method, header, body):
    global mylogger,  msg_props, interval_sec,REOUT_CH,msgsnd_ipc, msgrcv_ipc,AI_daybook_en,NEW_daybook_create,MSG_send_error_cnt, Backup_re_jpg
    mylogger.info("receive mq")
    channel.basic_ack(delivery_tag=method.delivery_tag)
    #
    #wdi()

    mylogger.debug("msg recv" + body)
    try:
        _dic_info = json.loads(body)
    except Exception, e:
        mylogger.warning(str(e))
        mylogger.warning("len=%d"%len(body))
        mylogger.warning("msg="+body)
        return
    if "quit" in _dic_info:
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()
        mylogger.debug("quit")
        #mylogger.debug(body)
    if not "cam_id" in _dic_info:
        mylogger.debug("not cam_id in _dic_info")
        mylogger.debug("rabbitmq publish:REout " + body)
        try:
            REOUT_CH.basic_publish(body=body, exchange="ReOut.tr", properties=msg_props,
                                   routing_key="plate queue")
        except Exception,e:
            mylogger.error(str(e))
            mylogger.error(REOUT_CH)
            REOUT_CH = get_plateOUT_rabbitmq_channel()
        return
    _timeSec = int(time.time())
    if not "time_now" in _dic_info:
        mylogger.warning("no time_now:%s"%body)
    else:
        if _timeSec - _dic_info["time_now"] > 25:
            mylogger.info("%s timeout,where now is %d, msg time is %d"%(_dic_info["cam_id"],_timeSec,_dic_info["time_now"]))
            _timeout_dic = {"msg": "mq time=%d, now is %d, %d seconds late" % (
            _dic_info["time_now"], _timeSec, _timeSec - _dic_info["time_now"])}
            _timeout_str = json.dumps(_timeout_dic)
            mylogger.debug("rabbitmq publish:REout " + _timeout_str)
            try:
                REOUT_CH.basic_publish(body=_timeout_str, exchange="ReOut.tr", properties=msg_props,
                                       routing_key="plate queue")
            except Exception, e:
                mylogger.error(str(e))
                mylogger.error(REOUT_CH)
                REOUT_CH = get_plateOUT_rabbitmq_channel()
            return


    if not "CMOS" in _dic_info:
        mylogger.debug("not CMOS in _dic_info")
        return
    if not type(_dic_info["CMOS"])==int:
        mylogger.debug("not type CMOS is int")
        return

    _width = 2304
    _height = 1296
    if "Owidth" in _dic_info:
        _width = _dic_info["Owidth"]
    if "Oheight" in _dic_info:
        _height = _dic_info["Oheight"]

    try:
        title_queue.put(body)
        _pic_file = str(_dic_info["pic_full_name"])
        if not os.path.isfile(_pic_file):
            mylogger.warning("%s is not a file"%_pic_file)
            return
        if '1' == Backup_re_jpg:
            yuvjpg_queue.put(body)

        try:
            _cam_id = str(_dic_info["cam_id"])
            if _cam_id in RE_settings:
                _re_setting = RE_settings[_cam_id]
            else:
                _re_setting = [0]*10
                _re_setting[3] = 2.5
            _bayID = "%s0%d"%(_cam_id,_dic_info["plateGet"])
            _ai_out2 = AI_out2s[_bayID][0]
            _bays1 = AI_out2s[_bayID][1]
        except Exception,e:
            mylogger.error(str(e))
            return
        try:
            mylogger.info("start pack %s %s"%(_cam_id,_pic_file))
            msg0 = struct.pack('32s2b128s2H2b', _cam_id,_dic_info["CMOS"],_dic_info["plateGet"],_pic_file,
                               _dic_info["RBx"]-_dic_info["LTx"]+1,_dic_info["RBy"]-_dic_info["LTy"]+1,0,0)
            #print binascii.hexlify(msg0)
            #level_line1 = [_re_setting[i]*_width/100 for i in range(5, 13)]  # ; // 12
            level_line1 = [0]*12
            #level_line1[4] = _ai_out2[25]*_width/8192
            #level_line1[5] = _ai_out2[26] * _width / 8192


            undis_param_t1 = struct.pack('4B8i', int(_re_setting[3]*10),_bays1,_re_setting[2],_re_setting[4], *[level_line1[i] for i in range(8)])

            level_line2 = [0]*4
            undis_param_t2 = struct.pack('4i', *[level_line2[i] for i in range(4)])

            vertical_line = [0]*4
            undis_param_t3 = struct.pack('4i', *[vertical_line[i] for i in range(4)])
            #print binascii.hexlify(undis_param_t3)
            undis_param_t = undis_param_t1 + undis_param_t2 + undis_param_t3
            del level_line1,level_line2, vertical_line, undis_param_t1, undis_param_t2, undis_param_t3
            #mylogger.info("level_line1")
            car_coord = [0]*12
            car_coord[0] = _ai_out2[14]*_width/8192
            car_coord[1] = _ai_out2[15] * _height / 8192
            car_coord[2] = _ai_out2[16] * _width / 8192
            car_coord[3] = _ai_out2[17] * _height / 8192
            plate_location = [0]*12
            _x = _ai_out2[18] * _width / 8192
            if _x >= _dic_info["LTx"]:
                plate_location[0] = _x
            else:
                plate_location[0] = 0
            _y = _ai_out2[19] * _height / 8192
            if _y >= _dic_info["LTy"]:
                plate_location[1] = _y
            else:
                plate_location[1] = 0
            _x = _ai_out2[20] * _width / 8192
            if _x <= _dic_info["RBx"]:
                plate_location[2] = _x
            else:
                plate_location[2] = _dic_info["RBx"]
            _y = _ai_out2[21] * _height / 8192
            if _y <= _dic_info["RBy"]:
                plate_location[3] = _y
            else:
                plate_location[3] = _dic_info["RBy"]

            _x = _ai_out2[22] * _width / 8192
            if _x >= _dic_info["LTx"]:
                plate_location[4] = _x
            else:
                plate_location[4] = 0
            _y = _ai_out2[23] * _height / 8192
            if _y >= _dic_info["LTy"]:
                plate_location[5] = _y
            else:
                plate_location[5] = 0
            _x = _ai_out2[24] * _width / 8192
            if _x <= _dic_info["RBx"]:
                plate_location[6] = _x
            else:
                plate_location[6] = _dic_info["RBx"]
            _y = _ai_out2[25] * _height / 8192
            if _y <= _dic_info["RBy"]:
                plate_location[7] = _y
            else:
                plate_location[7] = _dic_info["RBy"]

            plate1pos_confidence = _ai_out2[26]
            plate2pos_confidence = _ai_out2[27]
            msg2 = struct.pack('12i', *[car_coord[i] for i in range(12)])
            msg3 = struct.pack('12i', *[plate_location[i] for i in range(12)])
            msg4 = struct.pack('2b4i128s', plate1pos_confidence,plate2pos_confidence,_dic_info["LTx"],_dic_info["LTy"],
                               _dic_info["RBx"],_dic_info["RBy"], str(_dic_info["AIfile"]))
            msg = msg0 + undis_param_t + msg2 + msg3 + msg4
            mylogger.info("end pack")
            #q2 = sysv_ipc.MessageQueue(16842753, flags=sysv_ipc.IPC_CREAT)
            try:
                msgsnd_ipc.send(msg, block=False,type=0xa014)
            except Exception, e:
                mylogger.error(str(e))
                MSG_send_error_cnt += 1
                if MSG_send_error_cnt > 30:
                    clear_reset_vlpr()
                return
            #q3 = sysv_ipc.MessageQueue(50397185, flags=sysv_ipc.IPC_CREAT)
            del msg0,msg,msg2,msg3,msg4, undis_param_t,car_coord,plate_location,plate1pos_confidence,plate2pos_confidence
        except Exception,e:
            mylogger.error(str(e))
            mylogger.error(body)
        _sleepCnt = 100
        mylogger.info("start recv")
        while _sleepCnt > 0:
            time.sleep(0.05)
            try:
                msg1 = msgrcv_ipc.receive(block=False, type=0)
                break
            except Exception,e:
                #mylogger.debug(str(e))
                pass
            _sleepCnt -= 1

        mylogger.info("recv end")


        if _sleepCnt > 0 :
            if msg1[1] == 0xa015:
                result_queue.put(msg1[0])
            else:
                mylogger.warning("msg receive type=%x"%msg1[1])

        else:
            mylogger.warning("VLPR ipc recv None in 5 seconds %d"%MSG_send_error_cnt)
            body = json.dumps({"remsg":"receive timeout"})
            MSG_send_error_cnt += 1
            if MSG_send_error_cnt > 30:
                clear_reset_vlpr()
            mylogger.debug("rabbitmq publish:VLPR " + body)
            REOUT_CH.basic_publish(body=body, exchange="ReOut.tr", properties=msg_props,
                               routing_key="plate queue")

    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(body)
        pass
    mylogger.info("end process")
    return


def get_plateOUT_rabbitmq_channel():
    global mylogger
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "reoutmq_server_addr" in conf_dict:
        _mq_host = conf_dict["reoutmq_server_addr"]
    else:
        _mq_host = "localhost"
    if "reoutmq_server_port" in conf_dict:
        _mq_port = int(conf_dict["reoutmq_server_port"])
    else:
        _mq_port = 5672
    if "reoutmq_user_name" in conf_dict:
        _mq_user_name = conf_dict["reoutmq_user_name"]
    else:
        _mq_user_name = "cpf"
    if "reoutmq_passwd" in conf_dict:
        _mq_passwd = conf_dict["reoutmq_passwd"]
    else:
        _mq_passwd = "cpf"
    if "aioutmq_vhost" in conf_dict:
        _mq_vhost = conf_dict["reoutmq_vhost"]
    else:
        _mq_vhost = "OutTrig"


    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="ReOut.tr", exchange_type="fanout",
                             passive=False, durable=False, auto_delete=False)
    return channel




def get_plate_rabbitmq_channel():
    global mylogger
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "platemq_server_addr" in conf_dict:
        _mq_host = conf_dict["platemq_server_addr"]
    else:
        _mq_host = "localhost"
    if "platemq_server_port" in conf_dict:
        _mq_port = int(conf_dict["platemq_server_port"])
    else:
        _mq_port = 5672

    if "platemq_user_name" in conf_dict:
        _mq_user_name = conf_dict["platemq_user_name"]
    else:
        _mq_user_name = "guest"
    if "platemq_passwd" in conf_dict:
        _mq_passwd = conf_dict["platemq_passwd"]
    else:
        _mq_passwd = "guest"

    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host='/', credentials=credentials)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    try:
        channel = conn_broker.channel()
        channel.exchange_declare(exchange="plate", exchange_type="direct",
                                 passive=False, durable=False, auto_delete=False)
        #channel.exchange_declare(exchange="place",exchange_type="direct", passive=False, durable=False, auto_delete=True)
        channel.queue_declare(queue="plate.in")
        channel.queue_bind(queue="plate.in", exchange='plate',routing_key="plate queue")
    except Exception, e:
        mylogger.info(str(e))

    channel.basic_consume(msg_consumer, queue="plate.in", consumer_tag="plate queue1")
    return channel


def python_cmd(cmd):
    str1 = "@%d"%(os.getpid())
    print cmd + str1
    os.system(cmd)
    #os.system("pause")
    time.sleep(0.5)

if __name__ == '__main__':
    if not os.path.isdir("../log/re_shell"):
        try:
            os.mkdir("../log/re_shell")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/re_shell/re_shell.log")
    mylogger.info("start running")
    _dic1 = wtclib.get_user_config_ret_dict("../conf/conf.conf", "file_save")
    if "backup_ai_jpg" in _dic1:
        Backup_ai_jpg = _dic1["backup_ai_jpg"]
    else:
        Backup_ai_jpg = '0'
    if "backup_re_jpg" in _dic1:
        Backup_re_jpg = _dic1["backup_re_jpg"]
    else:
        Backup_re_jpg = '0'
    del _dic1
    if '1' == Backup_re_jpg:
        if not os.path.isdir("../../re/yuv"):
            try:
                os.mkdir("../../re/yuv")
            except Exception, e:
                print str(e) + " in line: " + str(sys._getframe().f_lineno)
                os._exit()
        if not os.path.isdir("../../re/jpg"):
            try:
                os.mkdir("../../re/jpg")
            except Exception, e:
                print str(e) + " in line: " + str(sys._getframe().f_lineno)
                os._exit()

    if not os.path.isdir("../../re/un_yuv"):
        try:
            os.mkdir("../../re/un_yuv")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    if not os.path.isdir("../../re/un_jpg"):
        try:
            os.mkdir("../../re/un_jpg")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()



    cur = get_a_sql_cur_forever(mylogger)
    try:
        _pipe = os.popen("ps aux|grep ai_vlpr")
        _pipe_data = _pipe.read()
        _pipe.close()
        print _pipe_data
        _retV = _pipe_data.strip("\n").split('\n')
        print _retV[0]
        if len(_retV) > 2:
            os.system("killall ai_vlpr")
            print "kill ai_vlpr"
        cmd1 = "./ftok &"
        thread.start_new_thread(python_cmd, (cmd1,))
        cmd1 = "./ai_vlpr &"
        thread.start_new_thread(python_cmd, (cmd1,))
        print "start ai_vlpr"
        thread1 = sync_data_from_HDD(1)
        thread1.start()
        get_ai_out2_info(2).start()
        insert_reout_title(3).start()
        insert_reout_result(4).start()
        if '1' == Backup_re_jpg:
            backup_yuv_jpg_files(5).start()
        time.sleep(5)
        os.system("rabbitmqctl purge_queue plate.in")
        del _pipe, _pipe_data,_retV,cmd1
    except Exception,e:
        mylogger.error(str(e))


    #Sqlite_cur,sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylogger,"/tmp/softdog.db")
    try:

        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "re_shell" in _dic1:
            _version = _dic1["re_shell"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
            del stat
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('re_shell','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai_vlpr','1.01')"
                    "ON DUPLICATE KEY UPDATE version='1.01'" )
        cur.execute("TRUNCATE TABLE refiltertable")
        cur.execute("TRUNCATE TABLE reoutfiltertable")
        del _version, _dic1
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
        os._exit()

    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    fp = open('key.txt')
    fpd = fp.read()
    fp.close()
    _dic1 = json.loads(fpd)

    msgsnd_ipc = sysv_ipc.MessageQueue(int(_dic1["resend"]), flags=sysv_ipc.IPC_CREAT)
    msgrcv_ipc = sysv_ipc.MessageQueue(int(_dic1["rerecv"]), flags=sysv_ipc.IPC_CREAT)
    while True:#clear ipc msg
        try:
            msgrcv_ipc.receive(block=False,type=0)
        except:
            break
    del fp,fpd,_dic1

    while True:
        channel = get_plate_rabbitmq_channel()
        REOUT_CH = get_plateOUT_rabbitmq_channel()
        try:
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))

