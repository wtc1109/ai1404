import time
import wtclib
import datetime
import os, sys

print time.time(), time.clock()

while True:
    (cur, conn) = wtclib.get_a_sql_cur("../conf/conf.conf","algbackup")
    if None != cur:
        cur.close()
        conn.close()
        break
    else:
        print ("can not connect to backup db and sleep 20")
        time.sleep(20)
while True:
    (log_cur, _log_conn) = wtclib.get_a_sql_cur("../conf/conf.conf","alglog")
    if None != cur:

        break
    else:
        print ("can not connect to log db and sleep 20")
        time.sleep(20)

while True:
    (cur, conn) = wtclib.get_a_sql_cur("../conf/conf.conf")
    if None != cur:
        break
    else:
        print ("can not connect to db and sleep 20")
        time.sleep(20)

#cur.execute("select * from reoutfiltertable where cameraID='1712436093'")
#reout = cur.fetchone()

try:
    cur.execute("create table if not exists ScreenConnectTable("
                "ScreenSn char(16)not null primary key,"
                "ScreenName char(16),"
                "returnval char(64),"
                "display1 char(160),"
                "display2 char(160),"
                "display3 char(160),"
                "display4 char(160),"
                "display5 char(160),"
                "display6 char(160),"
                "display7 char(160),"
                "display8 char(160),"
                "display9 char(160),"
                "display10 char(160),"
                "display11 char(160),"
                "display12 char(160),"
                "display13 char(160),"
                "display14 char(160),"
                "display15 char(160),"
                "display16 char(160),"
                "display17 char(160),"
                "display18 char(160),"
                "display19 char(160),"
                "display20 char(160),"
                "display21 char(160),"
                "display22 char(160),"
                "display23 char(160),"
                "display24 char(160)"
                ")engine=memory")
    dsc = cur.execute("desc ScreenConnectTable")
    table1 = cur.fetchall()
    if 'char(160)' != table1[3][1]:
        cur.execute("drop table ScreenConnectTable")
        cur.execute("create table ScreenConnectTable("
                    "ScreenSn char(16)not null primary key,"
                    "ScreenName char(16),"
                    "returnval char(64),"
                    "display1 char(160),"
                    "display2 char(160),"
                    "display3 char(160),"
                    "display4 char(160),"
                    "display5 char(160),"
                    "display6 char(160),"
                    "display7 char(160),"
                    "display8 char(160),"
                    "display9 char(160),"
                    "display10 char(160),"
                    "display11 char(160),"
                    "display12 char(160),"
                    "display13 char(160),"
                    "display14 char(160),"
                    "display15 char(160),"
                    "display16 char(160),"
                    "display17 char(160),"
                    "display18 char(160),"
                    "display19 char(160),"
                    "display20 char(160),"
                    "display21 char(160),"
                    "display22 char(160),"
                    "display23 char(160),"
                    "display24 char(160)"
                    ")engine=memory")
except Exception, e:
    print str(e)
    pass


try:
    cur.execute("create table if not exists ScreenSpecialConfigTable("
                "ScreenSn char(16),"
                "opt char(4),"# allow '>', '<', '=', '<>', 'BT'
                "val1 int,"
                "val2 int default 0,"
                "displayInfo char(160),"
                "primary key(ScreenSn, opt, val1, val2))")
    dsc = cur.execute("desc ScreenSpecialConfigTable")
    table1 = cur.fetchall()
    if 'char(160)' != table1[4][1]:
        cur.execute("drop table ScreenSpecialConfigTable")
        cur.execute("create table if not exists ScreenSpecialConfigTable("
                    "ScreenSn char(16),"
                    "opt char(4),"  # allow '>', '<', '=', '<>', 'BT'
                    "val1 int,"
                    "val2 int default 0,"
                    "displayInfo char(160),"
                    "primary key(ScreenSn, opt, val1, val2))")
except Exception, e:
    print str(e)
    pass



try:

    cur.execute("create table if not exists ScreenConfigTable("
                "ScreenSn char(16)not null primary key,"
                "CtrlMode int,"
                "Weight int, "
                "height int,"
                "AllRegion int default 0,"
                "Region1 int, "
                "Region2 int,"
                "Region3 int,"
                "Region4 int,"
                "Region5 int,"
                "Region6 int,"
                "Region7 int,"
                "Region8 int,"
                "Region9 int, "
                "Region10 int,"
                "Region11 int,"
                "Region12 int,"
                "Region13 int,"
                "Region14 int,"
                "Region15 int,"
                "Region16 int,"
                "Region17 int, "
                "Region18 int,"
                "Region19 int,"
                "Region20 int,"
                "Region21 int,"
                "Region22 int,"
                "Region23 int,"
                "Region24 int,"
                "RegionNum_len int default 0,"
                "specialFlag int default 0"
                ")engine=memory")
    dsc = cur.execute("desc ScreenConfigTable")
    if 31 != dsc:
        cur.execute("drop table ScreenConfigTable")
        cur.execute("create table if not exists ScreenConfigTable("
                    "ScreenSn char(16)not null primary key,"
                    "CtrlMode int,"
                    "Weight int, "
                    "height int,"
                    "AllRegion int default 0,"
                    "Region1 int, "
                    "Region2 int,"
                    "Region3 int,"
                    "Region4 int,"
                    "Region5 int,"
                    "Region6 int,"
                    "Region7 int,"
                    "Region8 int,"
                    "Region9 int, "
                    "Region10 int,"
                    "Region11 int,"
                    "Region12 int,"
                    "Region13 int,"
                    "Region14 int,"
                    "Region15 int,"
                    "Region16 int,"
                    "Region17 int, "
                    "Region18 int,"
                    "Region19 int,"
                    "Region20 int,"
                    "Region21 int,"
                    "Region22 int,"
                    "Region23 int,"
                    "Region24 int,"
                    "RegionNum_len int default 0,"
                    "specialFlag int default 0"
                    ")engine=memory")
except Exception, e:
    print str(e)
    pass

try:

    cur.execute("create table if not exists ScreenRegionConfigTable("
                "RegionSn int not null primary key,"
                "TopLeftX int,"
                "TopLeftY int, "
                "BottomRightX int,"
                "BottomRightY int,"
                "Action int,"
                "Font int, "
                "Color int,"
                "Display char(160)"
                ")engine=memory")
    dsc = cur.execute("desc ScreenRegionConfigTable")
    table1 = cur.fetchall()
    if 'char(160)' != table1[8][1]:
        cur.execute("drop table ScreenRegionConfigTable")
    cur.execute("create table if not exists ScreenRegionConfigTable("
                "RegionSn int not null primary key,"
                "TopLeftX int,"
                "TopLeftY int, "
                "BottomRightX int,"
                "BottomRightY int,"
                "Action int,"
                "Font int, "
                "Color int,"
                "Display char(160)"
                ")engine=memory")
except Exception, e:
    print str(e)
    pass

try:
    cur.execute("create table if not exists Space2LedTable("
                "id char(32)primary key,"
                "Spaceid char(32), "
                "RegionSn int)engine=memory")
    dsc = cur.execute("desc Space2LedTable")
    if 3 != dsc:
        cur.execute("drop table Space2LedTable")
        cur.execute("create table if not exists Space2LedTable("
                    "id char(32)primary key,"
                    "Spaceid char(32), "
                    "RegionSn int)engine=memory")
except Exception, e:
    print str(e)
    pass

try:
    cur.execute("create table if not exists AiSoftwareVersion("
                "SoftwareName char(32) primary key,"
                "version char(32),"
                "warning char(64)"
                ")")
    dsc = cur.execute("desc AiSoftwareVersion")
    if 3 != dsc:
        cur.execute("drop table AiSoftwareVersion")
        cur.execute("create table if not exists AiSoftwareVersion("
                    "SoftwareName char(32) primary key,"
                    "version char(32),"
                    "warning char(64)"
                    ")")

    _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
    if "createdb" in _dic1:
        _version = _dic1["createdb"]
    else:
        stat = os.stat(__file__)
        _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
    cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('createDB','%s')"
                "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
except Exception, e:
    print str(e)
    pass


try:
    cur.execute("create table if not exists HvpdUpgradeTable("
                "cameraID char(24) , "
                "cmosID tinyint,"
                "filename char(128),"
                "user char(32),"
                "ReNewFlag tinyint default 0,"
                "set_time DATETIME, "
                "end_time DATETIME,"
               
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc HvpdUpgradeTable")
    if 7 != dsc:
        cur.execute("drop table HvpdUpgradeTable")
        cur.execute("create table if not exists HvpdUpgradeTable("
                    "cameraID char(24) , "
                    "cmosID tinyint,"
                    "filename char(128),"
                    "user char(32),"
                    "ReNewFlag tinyint default 0,"
                    "set_time DATETIME, "
                    "end_time DATETIME,"
                    
                    "primary key(cameraID, cmosID)"
                    ")")
except Exception, e:
    print "create table HvpdUpgradeTable", e
    pass


try:
    cur.execute("create table if not exists video_user_set("
                "cameraID char(24) , "
                "cmosID tinyint,"
                "cur_resolution int,"
                "cur_bitrate_kbps int,"
                "video_en int default 1,"
                "video_def int default 0,"
                "video_bitrate_Kbps int default 0,"
                "video_timet int default 0,"
                "get_time DATETIME, "
                "set_time DATETIME,"
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc video_user_set")
    if 10 != dsc:
        cur.execute("drop table video_user_set")
        cur.execute("create table if not exists video_user_set("
                    "cameraID char(24) , "
                    "cmosID tinyint,"
                    "cur_resolution int,"
                    "cur_bitrate_kbps int,"
                    "video_en int default 1,"
                    "video_def int default 0,"
                    "video_bitrate_Kbps int default 0,"
                    "video_timet int default 0,"
                    "get_time DATETIME, "
                    "set_time DATETIME,"
                    "primary key(cameraID, cmosID)"
                    ")")
except Exception, e:
    print "create table video_user_set", e
    pass

try:
    localtime1 = time.localtime()
    _tableName = "video_log_%d%02d%02d"%(localtime1.tm_year,localtime1.tm_mon,localtime1.tm_mday)
    log_cur.execute("create table if not exists %s("
                "id int not null auto_increment primary key," 
                "cameraID char(24) , "
                "cmosID tinyint default 0,"
                "get_time DATETIME, "
                "video_type char(8),"
                "used_flag int default 0,"
                "filename char(64),"
                "serverIP char(24)"
                ")"%_tableName)
    dsc = log_cur.execute("desc %s"%_tableName)

    if 8 != dsc:
        log_cur.execute("drop table %s"%_tableName)
        log_cur.execute("create table if not exists %s("
                    "id int not null auto_increment primary key,"
                    "cameraID char(24) , "
                    "cmosID tinyint default 0,"
                    "get_time DATETIME, "
                    "video_type char(8),"
                    "used_flag int default 0,"
                    "filename char(64),"
                    "serverIP char(24)"
                    ")" % _tableName)
    """
    cur.execute("insert into %s(cameraID,get_time,video_type,filename)values('17124301245',"
                "now(),'110','video/20180524/17124360020/111603.mp4')"%_tableName)
    cur.execute("insert into %s(cameraID,get_time,video_type,filename)values('17124301245',"
                "now(),'201','video/20180524/17124360020/111603.mp4')"%_tableName)
    """
    cur.execute("create table if not exists video_rtsp2mp4_table("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "startTimet int default 0,"
                "ServerID char(20) default NULL, "
                "movedetect char(8),"
                "movedetectTimet int default 0,"
                "startAIout char(8), "
                "CurFileName char(20), "
                "waiting_filename char(20) default NULL,"
                "waiting_Timet int default 0,"
                "video_pid int default 0,"
                "video_p_state int default 0,"
                "video_p_name char(32),"
                "video_p_timet int default 0,"
                "file_ext int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc video_rtsp2mp4_table")
    if 15 != dsc:
        cur.execute("drop table video_rtsp2mp4_table")
        cur.execute("create table if not exists video_rtsp2mp4_table("
                    "cameraID char(24), "
                    "cmosID tinyint default 0,"
                    "startTimet int default 0,"
                    "ServerID char(20) default NULL, "
                    "movedetect char(8),"
                    "movedetectTimet int default 0,"
                    "startAIout char(8), "
                    "CurFileName char(20), "
                    "waiting_filename char(20) default NULL,"
                    "waiting_Timet int default 0,"
                    "video_pid int default 0,"
                    "video_p_state int default 0,"
                    "video_p_name char(32),"
                    "video_p_timet int default 0,"
                    "file_ext int default 0,"
                    "primary key(cameraID, cmosID)"
                    ")engine=memory")

    cur.execute("create table if not exists video_files_table("
                "id int not null auto_increment primary key," 
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "src_name char(64),"
                "to_name char(240),"
                "waiting_Timet int default 0,"
                "retry_flag int default 0,"
                "video_type char(8),"
                "video_end int default 50,"
                "ServerID char(20) default NULL "
                ")engine=memory")
    dsc = cur.execute("desc video_files_table")
    if 10 != dsc:
        cur.execute("drop table video_files_table")
        cur.execute("create table if not exists video_files_table("
                    "id int not null auto_increment primary key,"
                    "cameraID char(24), "
                    "cmosID tinyint default 0,"
                    "src_name char(64),"
                    "to_name char(240),"
                    "waiting_Timet int default 0,"
                    "retry_flag int default 0,"
                    "video_type char(8),"
                    "video_end int default 50,"
                    "ServerID char(20) default NULL "
                    ")engine=memory")

    """
    cur.execute("insert into video_rtsp2mp4_table(cameraID,movedetectTimet,startAIout,CurFileName)"
                "values('1712436001',%d,'100','104201')"%(time.time()))
    cur.execute("insert into video_rtsp2mp4_table(cameraID,waiting_filename,waiting_Timet)"
                "values('1804430021','104201',%d)" % (time.time()))
    cur.execute("insert into video_rtsp2mp4_table(cameraID,movedetectTimet)values('1712436093',%d)"%(time.time()))
"""
except Exception,e:
    print e
    print "video_log"


try:
    cur.execute("create table if not exists LampDelayQueueTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "AiOutTime int, "
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table LampDelayQueueTableMem", e
    pass

try:
    cur.execute("create table if not exists OnlineHvpdStatusTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "neighbor_camera char(24), "
                "slave tinyint, "
                "ip char(20), "
                "exp int, "
                "gain smallint, "
                "CMOS tinyint default 0, "
                "bluetooth char(20), "
                "LatestConnect datetime, "
                "connectTimet int default 0,"
                "last_pic_timet int default 0,"
                "waiting_ex tinyint default 0, "
                "yuv_exp int, "
                "alarm char(32),"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc OnlineHvpdStatusTableMem")
    if 15 != dsc:
        cur.execute("drop table OnlineHvpdStatusTableMem")
    cur.execute("create table if not exists OnlineHvpdStatusTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "neighbor_camera char(24), "
                "slave tinyint, "
                "ip char(20), "
                "exp int, "
                "gain smallint, "
                "CMOS tinyint default 0, "
                "bluetooth char(20), "
                "LatestConnect datetime, "
                "connectTimet int,"
                "last_pic_timet int default 0,"
                "waiting_ex tinyint default 0, "
                "yuv_exp int, "
                "alarm char(32),"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table OnlineHvpdStatusTableMem", e
    pass

try:
    cur.execute("create table if not exists monostablepic("
                "cameraID char(24), "
                "cmosID tinyint,"
                "LatestConnect datetime, "
                "connectTimet int default 0,"
                "json_str text,"
      
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc monostablepic")
    if 5 != dsc:
        cur.execute("drop table monostablepic")
        cur.execute("create table if not exists monostablepic("
                    "cameraID char(24), "
                    "cmosID tinyint,"
                    "LatestConnect datetime, "
                    "connectTimet int default 0,"
                    "json_str text,"
                    
                    "primary key(cameraID, cmosID)"
                    ")")
except Exception, e:
    print "create table monostablepic"+str(e)+" in line: " + str(sys._getframe().f_lineno)
    pass


try:
    cur.execute("create table if not exists hvpdEquipmentsTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "Mac char(20), "
                "newCameraFlag tinyint default 0,"
                "primary key(cameraID, cmosID)"
                ")")
except Exception, e:
    print "create table hvpdEquipmentsTable", e
    pass
try:
    cur.execute("create table if not exists HvpdVersionTableMem("
                "cameraID char(24)primary key, "
                "uart_version char(32),"
                "camera_version char(32),"
                "udp_version char(32),"
                "hard_ver char(32),"
                "renewtime datetime,"
                "renewtimet int default 0"
                ")engine=memory")
    dsc = cur.execute("desc HvpdVersionTableMem")
    if 7 != dsc:
        cur.execute("drop table HvpdVersionTableMem")
    cur.execute("create table if not exists HvpdVersionTableMem("
                "cameraID char(24)primary key, "
                "uart_version char(32),"
                "camera_version char(32),"
                "udp_version char(32),"
                "hard_ver char(32),"
                "renewtime datetime,"
                "renewtimet int default 0"
                ")engine=memory")
except Exception, e:
    print "create table HvpdVersionTableMem", e
    pass




try:
    cur.execute("create table if not exists defaultXspace("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except Exception, e:
    print e
    pass
try:
    cur.execute("create table if not exists 1Green2DarkLamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except Exception, e:
    print e
    pass
try:
    cur.execute("create table if not exists 1pink2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1blue2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1white2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1aqua2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1fuchsia2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1orange2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists 1yellow2redlamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except:
    pass
try:
    cur.execute("create table if not exists default6Lamp("
                "Flag_used char(8) primary key, "
                "output char(32))engine=memory")
except:
    pass
led_green = 'R:0,G:80,B:0'
led_red = 'R:80,G:0,B:0'
led_blue = 'R:0,G:0,B:80'
led_pink = 'R:80,G:60,B:64'
led_dark = 'R:0,G:0,B:0'
led_white = 'R:80,G:80,B:80'
led_aqua = 'R:0,G:80,B:80'
led_fuchsia = 'R:80,G:0,B:80'
led_orange = 'R:80,G:51,B:80'
led_yellow = 'R:80,G:80,B:0'


dic1 = {0:'o', 1:'x'}
dic2 = {0:'oo', 1:'ox', 2:'xo', 3:'xx'}
dic3 = {0:'ooo',1:'oox', 2:'oxo', 3:'oxx',4:'xoo', 5:'xox', 6:'xxo', 7:'xxx'}
dic4 = {0:'oooo',1:'ooox', 2:'ooxo', 3:'ooxx',4:'oxoo', 5:'oxox', 6:'oxxo', 7:'oxxx',
        8: 'xooo', 9: 'xoox',10 : 'xoxo', 11: 'xoxx', 12: 'xxoo', 13: 'xxox', 14: 'xxxo', 15: 'xxxx'}
dic5 = {0: 'ooooo', 1: 'oooox', 2: 'oooxo', 3: 'oooxx', 4: 'ooxoo', 5: 'ooxox', 6: 'ooxxo', 7: 'ooxxx',
        8: 'oxooo', 9: 'oxoox', 10: 'oxoxo', 11: 'oxoxx', 12: 'oxxoo', 13: 'oxxox', 14: 'oxxxo', 15: 'oxxxx',
        16: 'xoooo', 17: 'xooox', 18: 'xooxo', 19: 'xooxx', 20: 'xoxoo', 21: 'xoxox', 22: 'xoxxo', 23: 'xoxxx',
        24: 'xxooo', 25: 'xxoox', 26: 'xxoxo', 27: 'xxoxx', 28: 'xxxoo', 29: 'xxxox', 30: 'xxxxo', 31: 'xxxxx'
        }
dic6 = {0: 'oooooo', 1: 'ooooox', 2: 'ooooxo', 3: 'ooooxx', 4: 'oooxoo', 5: 'oooxox', 6: 'oooxxo', 7: 'oooxxx',
        8: 'ooxooo', 9: 'ooxoox', 10: 'ooxoxo', 11: 'ooxoxx', 12: 'ooxxoo', 13: 'ooxxox', 14: 'ooxxxo', 15: 'ooxxxx',
        16: 'oxoooo', 17: 'oxooox', 18: 'oxooxo', 19: 'oxooxx', 20: 'oxoxoo', 21: 'oxoxox', 22: 'oxoxxo', 23: 'oxoxxx',
        24: 'oxxooo', 25: 'oxxoox', 26: 'oxxoxo', 27: 'oxxoxx', 28: 'oxxxoo', 29: 'oxxxox', 30: 'oxxxxo', 31: 'oxxxxx',
        32: 'xooooo', 33: 'xoooox', 34: 'xoooxo', 35: 'xoooxx', 36: 'xooxoo', 37: 'xooxox', 38: 'xooxxo', 39: 'xooxxx',
        40: 'xoxooo', 41: 'xoxoox', 42: 'xoxoxo', 43: 'xoxoxx', 44: 'xoxxoo', 45: 'xoxxox', 46: 'xoxxxo', 47: 'xoxxxx',
        48: 'xxoooo', 49: 'xxooox', 50: 'xxooxo', 51: 'xxooxx', 52: 'xxoxoo', 53: 'xxoxox', 54: 'xxoxxo', 55: 'xxoxxx',
        56: 'xxxooo', 57: 'xxxoox', 58: 'xxxoxo', 59: 'xxxoxx', 60: 'xxxxoo', 61: 'xxxxox', 62: 'xxxxxo', 63: 'xxxxxx'
        }

lamp1 = {0:'A:1,B:1,C:1,D:1:E:1,F:0', 1:'A:1,B:1,C:1,D:1:E:1,F:1'}
lamp2 = {0:'A:1,B:1,C:1,D:1:E:0,F:0', 1:'A:1,B:1,C:1,D:1:E:0,F:1',
         2: 'A:1,B:1,C:1,D:1:E:1,F:0', 3: 'A:1,B:1,C:1,D:1:E:1,F:1'}
lamp3 = {0:'A:1,B:1,C:1,D:0:E:0,F:0', 1:'A:1,B:1,C:1,D:0:E:0,F:1',
         2: 'A:1,B:1,C:1,D:0:E:1,F:0', 3: 'A:1,B:1,C:1,D:0:E:1,F:1',
        4:'A:1,B:1,C:1,D:1:E:0,F:0', 5:'A:1,B:1,C:1,D:1:E:0,F:1',
         6: 'A:1,B:1,C:1,D:1:E:1,F:0', 7: 'A:1,B:1,C:1,D:1:E:1,F:1'
         }
lamp4 = {0:'A:1,B:1,C:0,D:0:E:0,F:0', 1:'A:1,B:1,C:0,D:0:E:0,F:1',
         2: 'A:1,B:1,C:0,D:0:E:1,F:0', 3: 'A:1,B:1,C:0,D:0:E:1,F:1',
        4:'A:1,B:1,C:0,D:1:E:0,F:0', 5:'A:1,B:1,C:0,D:1:E:0,F:1',
         6: 'A:1,B:1,C:0,D:1:E:1,F:0', 7: 'A:1,B:1,C:0,D:1:E:1,F:1',
        8:'A:1,B:1,C:1,D:0:E:0,F:0', 9:'A:1,B:1,C:1,D:0:E:0,F:1',
         10: 'A:1,B:1,C:1,D:0:E:1,F:0', 11: 'A:1,B:1,C:1,D:0:E:1,F:1',
        12:'A:1,B:1,C:1,D:1:E:0,F:0', 13:'A:1,B:1,C:1,D:1:E:0,F:1',
         14: 'A:1,B:1,C:1,D:1:E:1,F:0', 15: 'A:1,B:1,C:1,D:1:E:1,F:1'
         }
lamp5 = {0:'A:1,B:0,C:0,D:0:E:0,F:0', 1:'A:1,B:0,C:0,D:0:E:0,F:1',
         2: 'A:1,B:0,C:0,D:0:E:1,F:0', 3: 'A:1,B:0,C:0,D:0:E:1,F:1',
        4:'A:1,B:0,C:0,D:1:E:0,F:0', 5:'A:1,B:0,C:0,D:1:E:0,F:1',
         6: 'A:1,B:0,C:0,D:1:E:1,F:0', 7: 'A:1,B:0,C:0,D:1:E:1,F:1',
        8:'A:1,B:0,C:1,D:0:E:0,F:0', 9:'A:1,B:0,C:1,D:0:E:0,F:1',
         10: 'A:1,B:0,C:1,D:0:E:1,F:0', 11: 'A:1,B:0,C:1,D:0:E:1,F:1',
        12:'A:1,B:0,C:1,D:1:E:0,F:0', 13:'A:1,B:0,C:1,D:1:E:0,F:1',
         14: 'A:1,B:0,C:1,D:1:E:1,F:0', 15: 'A:1,B:0,C:1,D:1:E:1,F:1',
        16:'A:1,B:1,C:0,D:0:E:0,F:0', 17:'A:1,B:1,C:0,D:0:E:0,F:1',
         18: 'A:1,B:1,C:0,D:0:E:1,F:0', 19: 'A:1,B:1,C:0,D:0:E:1,F:1',
        20:'A:1,B:1,C:0,D:1:E:0,F:0', 21:'A:1,B:1,C:0,D:1:E:0,F:1',
         22: 'A:1,B:1,C:0,D:1:E:1,F:0', 23: 'A:1,B:1,C:0,D:1:E:1,F:1',
        24:'A:1,B:1,C:1,D:0:E:0,F:0', 25:'A:1,B:1,C:1,D:0:E:0,F:1',
         26: 'A:1,B:1,C:1,D:0:E:1,F:0', 27: 'A:1,B:1,C:1,D:0:E:1,F:1',
        28:'A:1,B:1,C:1,D:1:E:0,F:0', 29:'A:1,B:1,C:1,D:1:E:0,F:1',
         30: 'A:1,B:1,C:1,D:1:E:1,F:0', 31: 'A:1,B:1,C:1,D:1:E:1,F:1'
         }
lamp6 = {0:'A:0,B:0,C:0,D:0:E:0,F:0', 1:'A:0,B:0,C:0,D:0:E:0,F:1',
         2: 'A:0,B:0,C:0,D:0:E:1,F:0', 3: 'A:0,B:0,C:0,D:0:E:1,F:1',
        4:'A:0,B:0,C:0,D:1:E:0,F:0', 5:'A:0,B:0,C:0,D:1:E:0,F:1',
         6: 'A:0,B:0,C:0,D:1:E:1,F:0', 7: 'A:0,B:0,C:0,D:1:E:1,F:1',
        8:'A:0,B:0,C:1,D:0:E:0,F:0', 9:'A:0,B:0,C:1,D:0:E:0,F:1',
         10: 'A:0,B:0,C:1,D:0:E:1,F:0', 11: 'A:0,B:0,C:1,D:0:E:1,F:1',
        12:'A:0,B:0,C:1,D:1:E:0,F:0', 13:'A:0,B:0,C:1,D:1:E:0,F:1',
         14: 'A:0,B:0,C:1,D:1:E:1,F:0', 15: 'A:0,B:0,C:1,D:1:E:1,F:1',
        16:'A:0,B:1,C:0,D:0:E:0,F:0', 17:'A:0,B:1,C:0,D:0:E:0,F:1',
         18: 'A:0,B:1,C:0,D:0:E:1,F:0', 19: 'A:0,B:1,C:0,D:0:E:1,F:1',
        20:'A:0,B:1,C:0,D:1:E:0,F:0', 21:'A:0,B:1,C:0,D:1:E:0,F:1',
         22: 'A:0,B:1,C:0,D:1:E:1,F:0', 23: 'A:0,B:1,C:0,D:1:E:1,F:1',
        24:'A:0,B:1,C:1,D:0:E:0,F:0', 25:'A:0,B:1,C:1,D:0:E:0,F:1',
         26: 'A:0,B:1,C:1,D:0:E:1,F:0', 27: 'A:0,B:1,C:1,D:0:E:1,F:1',
        28:'A:0,B:1,C:1,D:1:E:0,F:0', 29:'A:0,B:1,C:1,D:1:E:0,F:1',
         30: 'A:0,B:1,C:1,D:1:E:1,F:0', 31: 'A:0,B:1,C:1,D:1:E:1,F:1',
        32:'A:1,B:0,C:0,D:0:E:0,F:0', 33:'A:1,B:0,C:0,D:0:E:0,F:1',
         34: 'A:1,B:0,C:0,D:0:E:1,F:0', 35: 'A:1,B:0,C:0,D:0:E:1,F:1',
        36:'A:1,B:0,C:0,D:1:E:0,F:0', 37:'A:1,B:0,C:0,D:1:E:0,F:1',
         38: 'A:1,B:0,C:0,D:1:E:1,F:0', 39: 'A:1,B:0,C:0,D:1:E:1,F:1',
        40:'A:1,B:0,C:1,D:0:E:0,F:0', 41:'A:1,B:0,C:1,D:0:E:0,F:1',
         42: 'A:1,B:0,C:1,D:0:E:1,F:0', 43: 'A:1,B:0,C:1,D:0:E:1,F:1',
        44:'A:1,B:0,C:1,D:1:E:0,F:0', 45:'A:1,B:0,C:1,D:1:E:0,F:1',
         46: 'A:1,B:0,C:1,D:1:E:1,F:0', 47: 'A:1,B:0,C:1,D:1:E:1,F:1',
        48:'A:1,B:1,C:0,D:0:E:0,F:0', 49:'A:1,B:1,C:0,D:0:E:0,F:1',
         50: 'A:1,B:1,C:0,D:0:E:1,F:0', 51: 'A:1,B:1,C:0,D:0:E:1,F:1',
        52:'A:1,B:1,C:0,D:1:E:0,F:0', 53:'A:1,B:1,C:0,D:1:E:0,F:1',
         54: 'A:1,B:1,C:0,D:1:E:1,F:0', 55: 'A:1,B:1,C:0,D:1:E:1,F:1',
        56:'A:1,B:1,C:1,D:0:E:0,F:0', 57:'A:1,B:1,C:1,D:0:E:0,F:1',
         58: 'A:1,B:1,C:1,D:0:E:1,F:0', 59: 'A:1,B:1,C:1,D:0:E:1,F:1',
        60:'A:1,B:1,C:1,D:1:E:0,F:0', 61:'A:1,B:1,C:1,D:1:E:0,F:1',
         62: 'A:1,B:1,C:1,D:1:E:1,F:0', 63: 'A:1,B:1,C:1,D:1:E:1,F:1'

         }
dicX = []
dicX.append(dic1)
dicX.append(dic2)
dicX.append(dic3)
dicX.append(dic4)
dicX.append(dic5)
dicX.append(dic6)
lampX = []
lampX.append(lamp1)
lampX.append(lamp2)
lampX.append(lamp3)
lampX.append(lamp4)
lampX.append(lamp5)
lampX.append(lamp6)
print time.time(), time.clock()
a1=cur.execute("select * from defaultXspace")
a2= cur.execute("select * from 1yellow2redlamp")
if 0 == a1 or 0 == a2:
    try:
        cur.execute("TRUNCATE TABLE defaultXspace")
        cur.execute("TRUNCATE TABLE 1pink2redlamp")
        cur.execute("TRUNCATE TABLE 1Green2DarkLamp")
        cur.execute("TRUNCATE TABLE 1blue2redlamp")
        cur.execute("TRUNCATE TABLE 1white2redlamp")
        cur.execute("TRUNCATE TABLE 1aqua2redlamp")
        cur.execute("TRUNCATE TABLE 1fuchsia2redlamp")
        cur.execute("TRUNCATE TABLE default6Lamp")
        cur.execute("TRUNCATE TABLE 1orange2redlamp")
        cur.execute("TRUNCATE TABLE 1yellow2redlamp")
    except Exception, e:
        print str(e)

    for cnt in range(6):
        for i in range(len(dicX[cnt])-1):
            sql_str = "insert into defaultXspace(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_green)
            cur.execute(sql_str)
            sql_str = "insert into 1pink2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_pink)
            cur.execute(sql_str)
            cur.execute("insert into 1Green2DarkLamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_green))
            cur.execute("insert into 1blue2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_blue))
            cur.execute("insert into 1white2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_white))
            cur.execute("insert into 1aqua2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_aqua))
            cur.execute("insert into 1fuchsia2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_fuchsia))
            cur.execute(
                "insert into 1orange2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_orange))
            cur.execute(
                "insert into 1yellow2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_yellow))

            cur.execute("insert into default6Lamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], lampX[cnt][i]))
        i = len(dicX[cnt])-1

        cur.execute("insert into default6Lamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], lampX[cnt][i]))
        sql_str = "insert into defaultXspace(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red)
        cur.execute(sql_str)
        sql_str = "insert into 1pink2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red)
        cur.execute(sql_str)
        cur.execute("insert into 1Green2DarkLamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_dark))
        cur.execute("insert into 1blue2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))
        cur.execute("insert into 1white2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))
        cur.execute("insert into 1aqua2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))
        cur.execute("insert into 1fuchsia2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))
        cur.execute("insert into 1orange2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))
        cur.execute("insert into 1yellow2redlamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red))

else:
    print "no need to insert into defaultXspace"

del dic1, dic2, dic3, dic4, dic5, dic6, dicX, lamp1, lamp2, lamp3, lamp4, lamp5, lamp6, lampX

try:
    cur.execute("create table if not exists LampSettingTable("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "SpaceAll tinyint, "
                "Space1ID char(24), "
                "Space2ID char(24), "
                "Space3ID char(24), "
                "Space4ID char(24), "
                "Space5ID char(24), "
                "Space6ID char(24), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")")
    dsc = cur.execute("desc LampSettingTable")
    if 14 != dsc:
        cur.execute("drop table LampSettingTable")
    cur.execute("create table if not exists LampSettingTable("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "SpaceAll tinyint, "
                "Space1ID char(24), "
                "Space2ID char(24), "
                "Space3ID char(24), "
                "Space4ID char(24), "
                "Space5ID char(24), "
                "Space6ID char(24), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")")
except:
    pass


"""
try:
    cur.execute("create table if not exists LampCtrl1("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")")
    cur.execute("create table if not exists LampCtrl1Mem("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")engine=memory")
    cur.execute("create table if not exists LampListPort1("
                "id int AUTO_INCREMENT primary key, "
                "ReNewFlag tinyint default 0,"
                "equipmentID char(24)"
                "cameraID char(24),"
                "cmosID tinyint,"
                "portID tinyint,"
                ")")
    cur.execute("create table if not exists LampListPort1Mem("
                "id int AUTO_INCREMENT primary key, "
                "ReNewFlag tinyint default 0,"
                "equipmentID char(24)"
                "cameraID char(24),"
                "cmosID tinyint,"
                "portID tinyint,"
                ")engine=memory")
    dsc = cur.execute("desc LampCtrl1")
    if 7 != dsc:
        cur.execute("drop table LampCtrl1")
    cur.execute("create table if not exists LampCtrl1("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")engine=memory")

except:
    pass
"""


try:
    cur.execute("create table if not exists LampSettingTableMem("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "CtrlTableName char(32), "
                "SpaceAll tinyint, "
                "Space1ID char(24), "
                "Space2ID char(24), "
                "Space3ID char(24), "
                "Space4ID char(24), "
                "Space5ID char(24), "
                "Space6ID char(24), "
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")engine=memory")
    dsc = cur.execute("desc LampSettingTableMem")
    if 14 != dsc:
        cur.execute("drop table LampSettingTableMem")
        cur.execute("create table LampSettingTableMem("
                    "equipmentID char(24) primary key, "
                    "ReNewFlag tinyint default 0,"
                    "CtrlTableName char(32), "
                    "SpaceAll tinyint, "
                    "Space1ID char(24), "
                    "Space2ID char(24), "
                    "Space3ID char(24), "
                    "Space4ID char(24), "
                    "Space5ID char(24), "
                    "Space6ID char(24), "
                    "ManualCtrLampFlag tinyint default 0,"
                    "ManualCtrSpaceFlag tinyint default 0,"
                    "set_time DATETIME,"
                    "set_timet int default 0"
                    ")engine=memory")
except:
    pass
"""
try:
    cur.execute("insert into LampSettingTable(equipmentID, CtrlTableName, SpaceAll, Space1ID, Space2ID, Space3ID)"
                "values('123456789', 'defaultXspace', 3,'1234567891','1234567892','1234567893')")
    cur.execute("insert into LampSettingTable(equipmentID, CtrlTableName, SpaceAll, Space1ID, Space2ID, Space3ID, Space4ID, Space5ID, Space6ID)"
                "values('123456787', 'defaultXspace', 6,'1234567891','1234567892','1234567893', '1234567871', '1234567872', '1234567873')")
except:
    pass
"""
try:
    cur.execute("create table if not exists LampUserCtlTable("
                "equipmentID char(24) primary key, "
                "userCtrl1Sn char(24), "
                "userCtrl2Sn char(24),"
                "userCtrl3Sn char(24),"
                "userCtrl4Sn char(24))")
except:
    print "create table LampUserCtlTable fail"
    pass

try:
    cur.execute("create table if not exists hvpdIpAddrSettingTable("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "CurIP char(24),"
                "CurMask char(24),"
                "CurGateway char(24),"
                "NewIP char(24), "
                "NewMask char(24), "
                "NewGateway char(24),"         
                "primary key(cameraID, cmosID)"
                ")")

except:
    print "create table hvpdIpAddrSettingTable fail"
    pass
"""
try:
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123456, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123450, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123451, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123452, 0, 1)")
except:
    pass"""

try:
    cur.execute("create table if not exists Equipment2cameraId("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "cameraID1 char(24), "
                "cmosID1 tinyint,"
                "cameraID2 char(24) default 0,"
                "cmosID2 tinyint)")
    cur.execute("create table if not exists Equipment2cameraIdMem("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "cameraID1 char(24), "
                "cmosID1 tinyint,"
                "cameraID2 char(24),"
                "cmosID2 tinyint,"
                "LampStatus char(32),"
                "LampRenewTimet int default 0,"
                "phaseVarRenewTimet int default 0"
                ")engine=memory")
    cur.execute("create table if not exists lamp_change("
                "LampRenewTimet int default 0,"
                "working tinyint default 0,"
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                
                "LampStatus char(32),"
                "ip char(20), "
                "equipmentID char(24),"
                "priority_new tinyint default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc lamp_change")
    if 8 != dsc:
        cur.execute("drop table lamp_change")
        cur.execute("create table if not exists lamp_change("
                    "LampRenewTimet int default 0,"
                    "working tinyint default 0,"
                    "cameraID char(24), "
                    "cmosID tinyint default 0,"

                    "LampStatus char(32),"
                    "ip char(20), "
                    "equipmentID char(24),"
                    "priority_new tinyint default 0,"
                    "primary key(cameraID, cmosID)"
                    ")engine=memory")

    dsc = cur.execute("desc Equipment2cameraIdMem")
    if 9 != dsc:
        cur.execute("drop table Equipment2cameraIdMem")
    cur.execute("create table if not exists Equipment2cameraIdMem("
                "equipmentID char(24) primary key, "
                "ReNewFlag tinyint default 0,"
                "cameraID1 char(24), "
                "cmosID1 tinyint,"
                "cameraID2 char(24),"
                "cmosID2 tinyint,"
                "LampStatus char(32),"
                "LampRenewTimet int default 0,"
                "phaseVarRenewTimet int default 0"
                ")engine=memory")
except:
    print "create table Equipment2cameraId fail"
    pass
"""
try:
    cur.execute("insert into Equipment2cameraId(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2)"
                "values('123456787', '123456787', 0, '123456788', 0)")
    cur.execute("insert into Equipment2cameraId(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2)"
                "values('123456789', '123456790',0, '123456789',1)")
    cur.execute("insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2)"
                "values('123456787', '123456787',0, '123456788',0)")
    cur.execute("insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2)"
                "values('123456789', '123456790',0, '123456789',1)")
except:
    pass
"""

try:
    cur.execute("drop table leddisplayerudpinfo")
    cur.execute("drop table leddisplayerudperrorinfo")
except Exception, e:
    print str(e)
    pass

try:
    cur.execute("create table if not exists hvpd2LampSettingTable("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc hvpd2LampSettingTable")
    if 8 != dsc:
        cur.execute("drop table hvpd2LampSettingTable")
    cur.execute("create table if not exists hvpd2LampSettingTable("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")")
except:
    print "create table hvpd2LampSettingTable fail"
    pass

try:

    cur.execute("create table if not exists hvpd2LampSettingTableMem("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint  default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc hvpd2LampSettingTableMem")
    if 8 != dsc:
        cur.execute("drop table hvpd2LampSettingTableMem")
    cur.execute("create table if not exists hvpd2LampSettingTableMem("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint  default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table hvpd2LampSettingTableMem fail"
    pass
"""
try:
    cur.execute("insert into hvpd2LampSettingTable(cameraID,cmosID, Effect1EquipID)values('123456787', 0, '123456787')")
    cur.execute("insert into hvpd2LampSettingTable(cameraID,cmosID, Effect1EquipID)values('123456789', 1, '123456789')")
except:
    pass"""


try:
    cur.execute("create table if not exists CameraPhaseCheckSettingTableMem("
                "cameraID char(24),"
                "cmosID tinyint,"
                "phase1pos char(20)default 0, "
                "phase2pos char(20), "
                "phase3pos char(20),"
                "RenewTimet int default 0,"
                "RenewDate datetime,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc CameraPhaseCheckSettingTableMem")
    if 7 != dsc:
        cur.execute("drop table CameraPhaseCheckSettingTableMem")
    cur.execute("create table if not exists CameraPhaseCheckSettingTableMem("
                "cameraID char(24),"
                "cmosID tinyint,"
                "phase1pos char(20)default 0, "
                "phase2pos char(20), "
                "phase3pos char(20),"
                "RenewTimet int default 0,"
                "RenewDate datetime,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table CameraPhaseCheckSettingTableMem fail"
    pass

try:
    cur.execute("create table if not exists AiSettingTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Slot_count tinyint default 3, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_line1LTx smallint default 0,"
                "manual_parking_line1LTy smallint default 0,"
                "manual_parking_line1RTx smallint default 0,"
                "manual_parking_line1RTy smallint default 0,"
                "manual_parking_line1LBx smallint default 0,"
                "manual_parking_line1LBy smallint default 0,"
                "manual_parking_line1RBx smallint default 0,"
                "manual_parking_line1RBy smallint default 0,"
                "manual_parking_line2LTx smallint default 0,"
                "manual_parking_line2LTy smallint default 0,"
                "manual_parking_line2RTx smallint default 0,"
                "manual_parking_line2RTy smallint default 0,"
                "manual_parking_line2LBx smallint default 0,"
                "manual_parking_line2LBy smallint default 0,"
                "manual_parking_line2RBx smallint default 0,"
                "manual_parking_line2RBy smallint default 0,"
                "manual_parking_line3LTx smallint default 0,"
                "manual_parking_line3LTy smallint default 0,"
                "manual_parking_line3RTx smallint default 0,"
                "manual_parking_line3RTy smallint default 0,"
                "manual_parking_line3LBx smallint default 0,"
                "manual_parking_line3LBy smallint default 0,"
                "manual_parking_line3RBx smallint default 0,"
                "manual_parking_line3RBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc AiSettingTable")
    if 36 != dsc:
        cur.execute("drop table AiSettingTable")
    cur.execute("create table if not exists AiSettingTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Slot_count tinyint default 3, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_line1LTx smallint default 0,"
                "manual_parking_line1LTy smallint default 0,"
                "manual_parking_line1RTx smallint default 0,"
                "manual_parking_line1RTy smallint default 0,"
                "manual_parking_line1LBx smallint default 0,"
                "manual_parking_line1LBy smallint default 0,"
                "manual_parking_line1RBx smallint default 0,"
                "manual_parking_line1RBy smallint default 0,"
                "manual_parking_line2LTx smallint default 0,"
                "manual_parking_line2LTy smallint default 0,"
                "manual_parking_line2RTx smallint default 0,"
                "manual_parking_line2RTy smallint default 0,"
                "manual_parking_line2LBx smallint default 0,"
                "manual_parking_line2LBy smallint default 0,"
                "manual_parking_line2RBx smallint default 0,"
                "manual_parking_line2RBy smallint default 0,"
                "manual_parking_line3LTx smallint default 0,"
                "manual_parking_line3LTy smallint default 0,"
                "manual_parking_line3RTx smallint default 0,"
                "manual_parking_line3RTy smallint default 0,"
                "manual_parking_line3LBx smallint default 0,"
                "manual_parking_line3LBy smallint default 0,"
                "manual_parking_line3RBx smallint default 0,"
                "manual_parking_line3RBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID)"
                ")")
except:
    print "create table AiSettingTable fail"
    pass
try:
    cur.execute("create table if not exists AiSettingTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Slot_count tinyint default 3, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint, "
                "manual_parking_line1LTx smallint default 0,"
                "manual_parking_line1LTy smallint default 0,"
                "manual_parking_line1RTx smallint default 0,"
                "manual_parking_line1RTy smallint default 0,"
                "manual_parking_line1LBx smallint default 0,"
                "manual_parking_line1LBy smallint default 0,"
                "manual_parking_line1RBx smallint default 0,"
                "manual_parking_line1RBy smallint default 0,"
                "manual_parking_line2LTx smallint default 0,"
                "manual_parking_line2LTy smallint default 0,"
                "manual_parking_line2RTx smallint default 0,"
                "manual_parking_line2RTy smallint default 0,"
                "manual_parking_line2LBx smallint default 0,"
                "manual_parking_line2LBy smallint default 0,"
                "manual_parking_line2RBx smallint default 0,"
                "manual_parking_line2RBy smallint default 0,"
                "manual_parking_line3LTx smallint default 0,"
                "manual_parking_line3LTy smallint default 0,"
                "manual_parking_line3RTx smallint default 0,"
                "manual_parking_line3RTy smallint default 0,"
                "manual_parking_line3LBx smallint default 0,"
                "manual_parking_line3LBy smallint default 0,"
                "manual_parking_line3RBx smallint default 0,"
                "manual_parking_line3RBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc AiSettingTableMem")
    if 36 != dsc:
        cur.execute("drop table AiSettingTableMem")
    cur.execute("create table if not exists AiSettingTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Slot_count tinyint default 3, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint, "
                "manual_parking_line1LTx smallint default 0,"
                "manual_parking_line1LTy smallint default 0,"
                "manual_parking_line1RTx smallint default 0,"
                "manual_parking_line1RTy smallint default 0,"
                "manual_parking_line1LBx smallint default 0,"
                "manual_parking_line1LBy smallint default 0,"
                "manual_parking_line1RBx smallint default 0,"
                "manual_parking_line1RBy smallint default 0,"
                "manual_parking_line2LTx smallint default 0,"
                "manual_parking_line2LTy smallint default 0,"
                "manual_parking_line2RTx smallint default 0,"
                "manual_parking_line2RTy smallint default 0,"
                "manual_parking_line2LBx smallint default 0,"
                "manual_parking_line2LBy smallint default 0,"
                "manual_parking_line2RBx smallint default 0,"
                "manual_parking_line2RBy smallint default 0,"
                "manual_parking_line3LTx smallint default 0,"
                "manual_parking_line3LTy smallint default 0,"
                "manual_parking_line3RTx smallint default 0,"
                "manual_parking_line3RTy smallint default 0,"
                "manual_parking_line3LBx smallint default 0,"
                "manual_parking_line3LBy smallint default 0,"
                "manual_parking_line3RBx smallint default 0,"
                "manual_parking_line3RBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table AiSettingTableMem fail"
    pass

"""
try:
    cur.execute("create table if not exists AiSettingPortTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "port tinyint ,"
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_lineLTx smallint default 0,"
                "manual_parking_lineLTy smallint default 0,"
                "manual_parking_lineRTx smallint default 0,"
                "manual_parking_lineRTy smallint default 0,"
                "manual_parking_lineLBx smallint default 0,"
                "manual_parking_lineLBy smallint default 0,"
                "manual_parking_lineRBx smallint default 0,"
                "manual_parking_lineRBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID, port)"
                ")")
    dsc = cur.execute("desc AiSettingPortTable")
    if 36 != dsc:
        cur.execute("drop table AiSettingPortTable")
    cur.execute("create table if not exists AiSettingPortTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "port tinyint ,"
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_lineLTx smallint default 0,"
                "manual_parking_lineLTy smallint default 0,"
                "manual_parking_lineRTx smallint default 0,"
                "manual_parking_lineRTy smallint default 0,"
                "manual_parking_lineLBx smallint default 0,"
                "manual_parking_lineLBy smallint default 0,"
                "manual_parking_lineRBx smallint default 0,"
                "manual_parking_lineRBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID, port)"
                ")")
except:
    print "create table AiSettingPortTable fail"
    pass
try:
    cur.execute("create table if not exists AiSettingPortTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "port tinyint ,"
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_lineLTx smallint default 0,"
                "manual_parking_lineLTy smallint default 0,"
                "manual_parking_lineRTx smallint default 0,"
                "manual_parking_lineRTy smallint default 0,"
                "manual_parking_lineLBx smallint default 0,"
                "manual_parking_lineLBy smallint default 0,"
                "manual_parking_lineRBx smallint default 0,"
                "manual_parking_lineRBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID, port)"
                ")engine=memory")
    dsc = cur.execute("desc AiSettingPortTableMem")
    if 36 != dsc:
        cur.execute("drop table AiSettingPortTableMem")
    cur.execute("create table if not exists AiSettingPortTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "port tinyint ,"
                "user_manual_parking_line tinyint default 0, "
                "manual_parking_lineLTx smallint default 0,"
                "manual_parking_lineLTy smallint default 0,"
                "manual_parking_lineRTx smallint default 0,"
                "manual_parking_lineRTy smallint default 0,"
                "manual_parking_lineLBx smallint default 0,"
                "manual_parking_lineLBy smallint default 0,"
                "manual_parking_lineRBx smallint default 0,"
                "manual_parking_lineRBy smallint default 0,"
                "set_time DATETIME,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "Event3Flag int default 0,"
                "Event4Flag int default 0,"
                "primary key(cameraID, cmosID, port)"
                ")engine=memory")
except:
    print "create table AiSettingPortTableMem fail"
    pass
"""

"""
try:
    cur.execute("insert into AiSettingTableMem(cameraID, cmosID, Slot_count, user_manual_parking_line, "
                "manual_parking_line1LTx,manual_parking_line1LTy, manual_parking_line1RTx,manual_parking_line1RTy,"
                "manual_parking_line1LBx,manual_parking_line1LBy, manual_parking_line1RBx,manual_parking_line1RBy,"
                "manual_parking_line2LTx,manual_parking_line2LTy, manual_parking_line2RTx,manual_parking_line2RTy,"
                "manual_parking_line2LBx,manual_parking_line2LBy, manual_parking_line2RBx,manual_parking_line2RBy,"
                "manual_parking_line3LTx,manual_parking_line3LTy, manual_parking_line3RTx,manual_parking_line3RTy,"
                "manual_parking_line3LBx,manual_parking_line3LBy, manual_parking_line3RBx,manual_parking_line3RBy"
                ")values('1712430001',0,3,1,"
                "0,0,20,0,0,80,20,80,"
                "25,5,45,6,22,75,55,88,"
                "65,20,89,10,75,75,95,95)")
    cur.execute("insert into AiSettingTableMem(cameraID, cmosID, Slot_count, user_manual_parking_line, "
                "manual_parking_line1LTx,manual_parking_line1LTy, manual_parking_line1RTx,manual_parking_line1RTy,"
                "manual_parking_line1LBx,manual_parking_line1LBy, manual_parking_line1RBx,manual_parking_line1RBy,"
                "manual_parking_line2LTx,manual_parking_line2LTy, manual_parking_line2RTx,manual_parking_line2RTy,"
                "manual_parking_line2LBx,manual_parking_line2LBy, manual_parking_line2RBx,manual_parking_line2RBy,"
                "manual_parking_line3LTx,manual_parking_line3LTy, manual_parking_line3RTx,manual_parking_line3RTy,"
                "manual_parking_line3LBx,manual_parking_line3LBy, manual_parking_line3RBx,manual_parking_line3RBy"
                ")values('123456789',0,2,1,"
                "0,0,20,0,0,80,20,80,"
                "25,5,45,6,22,75,55,88,"
                "65,20,89,10,75,75,95,95)")
    cur.execute("insert into AiSettingTableMem(cameraID, cmosID, Slot_count, user_manual_parking_line, "
                "manual_parking_line1LTx,manual_parking_line1LTy, manual_parking_line1RTx,manual_parking_line1RTy,"
                "manual_parking_line1LBx,manual_parking_line1LBy, manual_parking_line1RBx,manual_parking_line1RBy,"
                "manual_parking_line2LTx,manual_parking_line2LTy, manual_parking_line2RTx,manual_parking_line2RTy,"
                "manual_parking_line2LBx,manual_parking_line2LBy, manual_parking_line2RBx,manual_parking_line2RBy,"
                "manual_parking_line3LTx,manual_parking_line3LTy, manual_parking_line3RTx,manual_parking_line3RTy,"
                "manual_parking_line3LBx,manual_parking_line3LBy, manual_parking_line3RBx,manual_parking_line3RBy"
                ")values('123456789',1,2,0,"
                "0,0,20,0,0,80,20,80,"
                "25,5,45,6,22,75,55,88,"
                "65,20,89,10,75,75,95,95)")
except:
    pass"""


try:
    cur.execute("create table if not exists ReSettingTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "focalLength float default 2.5,"
                "useMenualUndisPos int default 0,"
                "LevelLineB1x int default 0,"
                "LevelLineB1y int default 0,"
                "LevelLineB2x int default 0,"
                "LevelLineB2y int default 0,"
                "LevelLineB3x int default 0,"
                "LevelLineB3y int default 0,"
                "LevelLineB4x int default 0,"
                "LevelLineB4y int default 0,"
                "LevelLineT1x int default 0,"
                "LevelLineT1y int default 0,"
                "LevelLineT2x int default 0,"
                "LevelLineT2y int default 0,"
                "VertiacalLine1x int default 0,"
                "VertiacalLine1y int default 0,"
                "VertiacalLine2x int default 0,"
                "VertiacalLine2y int default 0,"
                "set_time DATETIME,"
                "primary key(cameraID, cmosID)"
                ")")
    dsc = cur.execute("desc ReSettingTable")
    table1 = cur.fetchall()
    if '0' != table1[5][4]:
        cur.execute("drop table ReSettingTable")
        cur.execute("create table if not exists ReSettingTable("
                    "cameraID char(24), "
                    "cmosID tinyint,"
                    "ReNewFlag tinyint default 0,"
                    "focalLength float default 2.5,"
                    "useMenualUndisPos int default 0,"
                    "LevelLineB1x int default 0,"
                    "LevelLineB1y int default 0,"
                    "LevelLineB2x int default 0,"
                    "LevelLineB2y int default 0,"
                    "LevelLineB3x int default 0,"
                    "LevelLineB3y int default 0,"
                    "LevelLineB4x int default 0,"
                    "LevelLineB4y int default 0,"
                    "LevelLineT1x int default 0,"
                    "LevelLineT1y int default 0,"
                    "LevelLineT2x int default 0,"
                    "LevelLineT2y int default 0,"
                    "VertiacalLine1x int default 0,"
                    "VertiacalLine1y int default 0,"
                    "VertiacalLine2x int default 0,"
                    "VertiacalLine2y int default 0,"
                    "set_time DATETIME,"
                    "primary key(cameraID, cmosID)"
                    ")")
except:
    print "create table ReSettingTable fail"
    pass

try:
    cur.execute("create table if not exists ReSettingTableMem("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "focalLength float default 2.5,"
                "useMenualUndisPos int default 0,"
                "LevelLineB1x int default 0,"
                "LevelLineB1y int default 0,"
                "LevelLineB2x int default 0,"
                "LevelLineB2y int default 0,"
                "LevelLineB3x int default 0,"
                "LevelLineB3y int default 0,"
                "LevelLineB4x int default 0,"
                "LevelLineB4y int default 0,"
                "LevelLineT1x int default 0,"
                "LevelLineT1y int default 0,"
                "LevelLineT2x int default 0,"
                "LevelLineT2y int default 0,"
                "VertiacalLine1x int default 0,"
                "VertiacalLine1y int default 0,"
                "VertiacalLine2x int default 0,"
                "VertiacalLine2y int default 0,"
                "set_time DATETIME,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    dsc = cur.execute("desc ReSettingTableMem")
    table1 = cur.fetchall()
    if '0' != table1[5][4]:
        cur.execute("drop table ReSettingTableMem")
        cur.execute("create table if not exists ReSettingTableMem("
                    "cameraID char(24), "
                    "cmosID tinyint,"
                    "ReNewFlag tinyint default 0,"
                    "focalLength float default 2.5,"
                    "useMenualUndisPos int default 0,"
                    "LevelLineB1x int default 0,"
                    "LevelLineB1y int default 0,"
                    "LevelLineB2x int default 0,"
                    "LevelLineB2y int default 0,"
                    "LevelLineB3x int default 0,"
                    "LevelLineB3y int default 0,"
                    "LevelLineB4x int default 0,"
                    "LevelLineB4y int default 0,"
                    "LevelLineT1x int default 0,"
                    "LevelLineT1y int default 0,"
                    "LevelLineT2x int default 0,"
                    "LevelLineT2y int default 0,"
                    "VertiacalLine1x int default 0,"
                    "VertiacalLine1y int default 0,"
                    "VertiacalLine2x int default 0,"
                    "VertiacalLine2y int default 0,"
                    "set_time DATETIME,"
                    "primary key(cameraID, cmosID)"
                    ")engine=memory")


except:
    print "create table ReSettingTableMem fail"
    pass


try:
    cur.execute("create table if not exists ReOutTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "Plate1updateTimet int default 0,"
                "Plate1Number char(16),"
                "Plate1type char(8),"
                "Slot1Number char(12),"
                "Plate2updateTimet int default 0,"
                "Plate2Number char(16),"
                "Plate2type char(8),"
                "Slot2Number char(12),"
                "Plate3updateTimet int default 0,"
                "Plate3Number char(16),"
                "Plate3type char(8),"
                "Slot3Number char(12),"
                "primary key(cameraID, cmosID)"
                ")engine=memory")

except:
    print "create table ReOutTable fail"
    pass


try:
    cur.execute("create table if not exists ReOutFilterTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "Plate1updateTimet int default 0,"
                "Plate1Datetime datetime,"
                "Plate1Number char(16),"
                "Plate1type char(8),"
                "Slot1Number char(12),"
                "Plate2updateTimet int default 0,"
                "Plate2Datetime datetime,"
                "Plate2Number char(16),"
                "Plate2type char(8),"
                "Slot2Number char(12),"
                "Plate3updateTimet int default 0,"
                "Plate3Datetime datetime,"
                "Plate3Number char(16),"
                "Plate3type char(8),"
                "Slot3Number char(12),"
                "primary key(cameraID, cmosID)"
                ")engine=memory")

except:
    print "create table ReOutFilterTable fail"
    pass

try:
    cur.execute("create table if not exists ReFilterTable("
                "Spaceid char(24) not null primary key,"
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "inuse1 int default 0,"
                "PlateNumber1 char(16),"
                "sameCnt1 int default 0,"
                "matchCnt1 int default 0,"
                "sameTimet1 int default 0,"            
                "matchTimet1 int default 0,"
                "inuse2 int default 0,"
                "PlateNumber2 char(16),"
                "sameCnt2 int default 0,"
                "matchCnt2 int default 0,"
                "sameTimet2 int default 0,"            
                "matchTimet2 int default 0,"
                "inuse3 int default 0,"
                "PlateNumber3 char(16),"
                "sameCnt3 int default 0,"
                "matchCnt3 int default 0,"
                "sameTimet3 int default 0,"            
                "matchTimet3 int default 0,"
                "inuse4 int default 0,"
                "PlateNumber4 char(16),"
                "sameCnt4 int default 0,"
                "matchCnt4 int default 0,"
                "sameTimet4 int default 0,"            
                "matchTimet4 int default 0,"
                "inuse5 int default 0,"
                "PlateNumber5 char(16),"
                "sameCnt5 int default 0,"
                "matchCnt5 int default 0,"
                "sameTimet5 int default 0,"            
                "matchTimet5 int default 0,"
                "inuse6 int default 0,"
                "PlateNumber6 char(16),"
                "sameCnt6 int default 0,"
                "matchCnt6 int default 0,"
                "sameTimet6 int default 0,"            
                "matchTimet6 int default 0,"
                "inuse7 int default 0,"
                "PlateNumber7 char(16),"
                "sameCnt7 int default 0,"
                "matchCnt7 int default 0,"
                "sameTimet7 int default 0,"            
                "matchTimet7 int default 0,"
                "inuse8 int default 0,"
                "PlateNumber8 char(16),"
                "sameCnt8 int default 0,"
                "matchCnt8 int default 0,"
                "sameTimet8 int default 0,"            
                "matchTimet8 int default 0"
                ")engine=memory")
except Exception, e:
    print  "create table ReFilterTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists SpaceStatusTable("
                "Spaceid char(24) not null primary key,"
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "CarportStatus int,"
                "RenewTime int default 0,"
                "parkin_timet int default 0,"
                "parkout_timet int default 0,"
                "parkin_time datetime,"
                "parkout_time datetime,"
                "reserved tinyint default 0"
                ")engine=memory")
    dsc = cur.execute("desc SpaceStatusTable")

    if 10 != dsc:
        cur.execute("drop table SpaceStatusTable")
        cur.execute("create table if not exists SpaceStatusTable("
                    "Spaceid char(24) not null primary key,"
                    "cameraID char(24), "
                    "cmosID tinyint default 0,"
                    "CarportStatus int,"
                    "RenewTime int default 0,"
                    "parkin_timet int default 0,"
                    "parkout_timet int default 0,"
                    "parkin_time datetime,"
                    "parkout_time datetime,"
                    "reserved tinyint default 0"
                    ")engine=memory")

except Exception, e:
    print  "create table SpaceStatusTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists SpaceForReInfoTable("
                "Spaceid char(24) not null primary key,"
                "plateLTx int default 0,"
                "plateLTy int default 0,"
                "plateRBx int default 0,"
                "plateRBy int default 0,"
                "RenewTime int default 0)engine=memory")
except Exception, e:
    print  "create table SpaceForReInfoTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists SpaceYUVFilterBuffTable("
                "Spaceid char(24) primary key,"
                "cameraID char(24), "
                "cmosID tinyint,"
                "CarPos tinyint default 0,"
                "SpaceRenewTime int default 0,"
                "YUVRenewTime  int default 0,"
                "YUVGetfilesTime  int default 0"
                ")engine=memory")
except Exception, e:
    print  "create table SpaceYUVFilterBuffTable fail " + str(e)
    pass


try:

    cur.execute("create table if not exists WatchdogTable("
                "pid int ,"
                "runCMD char(128),"     #with full path,such as"/home/bluecard/hvpd/prog/bin/123.sh"
                "watchSeconds int default 0, "     #interval seconds
                "renewTimet int default 0,"       #wdi timet, the program refresh
                "strategy int default 0,"   #0:rerun, 1:reboot
                "killDelaySeconds int default 10,"     #kill the program and delay seconds for rerun
                "killTimet int default 0,"            #kill timet
                "wdtStep int default 0,"     #0:waiting for wdi,1:waiting fro rerun, after rerun the msg will be delete,a new pid will comming
                "ServerID char(20), "
                "primary key(pid, ServerID)"
                ")engine=memory")
    dsc = cur.execute("desc WatchdogTable")
    #table1 = cur.fetchall()
    #if 'PRI' != table1[8][3]:
    if 9 != dsc:
        cur.execute("drop table WatchdogTable")
        cur.execute("create table if not exists WatchdogTable("
                    "pid int ,"
                    "runCMD char(128),"  # with full path,such as"/home/bluecard/hvpd/prog/bin/123.sh"
                    "watchSeconds int default 0, "  # interval seconds
                    "renewTimet int default 0,"  # wdi timet, the program refresh
                    "strategy int default 0,"  # 0:rerun, 1:reboot
                    "killDelaySeconds int default 10,"  # kill the program and delay seconds for rerun
                    "killTimet int default 0,"  # kill timet
                    "wdtStep int default 0,"  # 0:waiting for wdi,1:waiting fro rerun, after rerun the msg will be delete,a new pid will comming
                    "ServerID char(20), "
                    "primary key(pid, ServerID)"
                    ")engine=memory")
    """
    while True:
        (sqlite3_cur, conn3) = wtclib.get_sqlite_cur("/tmp/softdog.db")
        if None != sqlite3_cur:
            break
        else:
            print  "can not connect to sqlite db and sleep 20"
            time.sleep(20)
    sqlite3_cur.execute("create table if not exists WatchdogTable("
                "pid int primary key,"
                "runCMD char(128),"  # with full path,such as"/home/bluecard/hvpd/prog/bin/123.sh"
                "watchSeconds int default 0, "  # interval seconds
                "renewTimet int default 0,"  # wdi timet, the program refresh
                "strategy int default 0,"  # 0:rerun, 1:reboot
                "killDelaySeconds int default 10,"  # kill the program and delay seconds for rerun
                "killTimet int default 0,"  # kill timet
                "wdtStep int default 0"  # 0:waiting for wdi,1:waiting fro rerun, after rerun the msg will be delete,a new pid will comming
              
                ")")
    conn3.close()
    """
except Exception, e:
    print  "create table WatchdogTable fail " + str(e)
    pass

"""
try:
    cur.execute("create table if not exists YUVFilterBuffTable("
                "Spaceid char(24) primary key,"
                "cameraID char(24), "
                "cmosID tinyint,"
                "CarPos tinyint,"
                "RenewTime int default 0)engine=memory")
except Exception, e:
    print  "create table YUVFilterBuffTable fail " + str(e)
    pass


try:
    cur.execute("create table if not exists YUVRenewTimeTable("
                "Spaceid char(24) primary key,"         
                "RenewTime int default 0"
                ")engine=memory")
except Exception, e:
    print  "create table YUVRenewTimeTable fail " + str(e)
    pass
"""

try:
    localtime1 = time.localtime()
    _alg_log = "ailog%d%02d%02d"%(localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
    log_cur.execute("create table if not exists %s("
                "aijpgname varchar(128) primary key,"
                "JpgLatestUpdate DATETIME,"
                "cameraID varchar(24), "
                "cmosID tinyint,"
                "CarCount tinyint, "
                "parking1State tinyint, "
                "parking2State tinyint, "
                "parking3State tinyint, "
                "parking1IsCrossLine tinyint, "
                "parking2IsCrossLine tinyint, "
                "parking3IsCrossLine tinyint,"
                "parkingLine1LTx smallint default 0, "
                "parkingLine1LTy smallint default 0, "
                "parkingLine1RTx smallint default 0, "
                "parkingLine1RTy smallint default 0, "
                "parkingLine1LBx smallint default 0, "
                "parkingLine1LBy smallint default 0, "
                "parkingLine1RBx smallint default 0, "
                "parkingLine1RBy smallint default 0, "
                "parkingLine2LTx smallint default 0, "
                "parkingLine2LTy smallint default 0, "
                "parkingLine2RTx smallint default 0, "
                "parkingLine2RTy smallint default 0, "
                "parkingLine2LBx smallint default 0, "
                "parkingLine2LBy smallint default 0, "
                "parkingLine2RBx smallint default 0, "
                "parkingLine2RBy smallint default 0, "
                "parkingLine3LTx smallint default 0, "
                "parkingLine3LTy smallint default 0, "
                "parkingLine3RTx smallint default 0, "
                "parkingLine3RTy smallint default 0, "
                "parkingLine3LBx smallint default 0, "
                "parkingLine3LBy smallint default 0, "
                "parkingLine3RBx smallint default 0, "
                "parkingLine3RBy smallint default 0, "
                "parkingLine1Confidence smallint, "
                "parkingLine2Confidence smallint, "
                "parkingLine3Confidence smallint, "
                "Car1posLTx smallint, "
                "Car1posLTy smallint, "
                "Car1posRBx smallint, "
                "Car1posRBy smallint, "
                "Car2posLTx smallint, "
                "Car2posLTy smallint, "
                "Car2posRBx smallint, "
                "Car2posRBy smallint, "
                "Car3posLTx smallint, "
                "Car3posLTy smallint, "
                "Car3posRBx smallint, "
                "Car3posRBy smallint, "

                "plate1posLTx smallint, "
                "plate1posLTy smallint, "
                "plate1posRBx smallint, "
                "plate1posRBy smallint, "
                "plate2posLTx smallint, "
                "plate2posLTy smallint, "
                "plate2posRBx smallint, "
                "plate2posRBy smallint, "
                "plate3posLTx smallint, "
                "plate3posLTy smallint, "
                "plate3posRBx smallint, "
                "plate3posRBy smallint, "
                "plate4posLTx smallint, "
                "plate4posLTy smallint, "
                "plate4posRBx smallint, "
                "plate4posRBy smallint, "
                "plate5posLTx smallint, "
                "plate5posLTy smallint, "
                "plate5posRBx smallint, "
                "plate5posRBy smallint, "
                "plate6posLTx smallint, "
                "plate6posLTy smallint, "
                "plate6posRBx smallint, "
                "plate6posRBy smallint, "
                "platePos1Confidence smallint, "
                "platePos2Confidence smallint, "
                "platePos3Confidence smallint, "
                "platePos4Confidence smallint, "
                "platePos5Confidence smallint, "
                "platePos6Confidence smallint, "

                "reyuv1name varchar(128),"
                "plate1Number varchar(32),"
                "plate1confidence smallint,"
                "plate1brightness smallint,"
                "plate1stable smallint,"
                "stableplate1number varchar(32),"
                "plate1updateTimet DATETIME, "
                "reyuv2name varchar(128),"
                "plate2Number varchar(32),"
                "plate2confidence smallint,"
                "plate2brightness smallint,"
                "plate2stable smallint,"
                "stableplate2number varchar(32),"
                "plate2updateTimet DATETIME, "
                "reyuv3name varchar(128),"
                "plate3Number varchar(32),"
                "plate3confidence smallint,"
                "plate3brightness smallint,"
                "plate3stable smallint,"
                "stableplate3number varchar(32),"
                "plate3updateTimet DATETIME, "
                "LampStatus varchar(32)"
                ")engine=MyISAM" % (_alg_log))
    dsc = log_cur.execute("desc %s"%_alg_log)
    table1 = log_cur.fetchall()
    if 'parking1IsCrossLine' != table1[8][0]:
        cur.execute("drop table %s"%_alg_log)
        cur.execute("create table if not exists %s("
                    "aijpgname varchar(128) primary key,"
                    "JpgLatestUpdate DATETIME,"
                    "cameraID varchar(24), "
                    "cmosID tinyint,"
                    "CarCount tinyint, "
                    "parking1State tinyint, "
                    "parking2State tinyint, "
                    "parking3State tinyint, "
                    "parking1IsCrossLine tinyint, "
                    "parking2IsCrossLine tinyint, "
                    "parking3IsCrossLine tinyint,"
                    "parkingLine1LTx smallint default 0, "
                    "parkingLine1LTy smallint default 0, "
                    "parkingLine1RTx smallint default 0, "
                    "parkingLine1RTy smallint default 0, "
                    "parkingLine1LBx smallint default 0, "
                    "parkingLine1LBy smallint default 0, "
                    "parkingLine1RBx smallint default 0, "
                    "parkingLine1RBy smallint default 0, "
                    "parkingLine2LTx smallint default 0, "
                    "parkingLine2LTy smallint default 0, "
                    "parkingLine2RTx smallint default 0, "
                    "parkingLine2RTy smallint default 0, "
                    "parkingLine2LBx smallint default 0, "
                    "parkingLine2LBy smallint default 0, "
                    "parkingLine2RBx smallint default 0, "
                    "parkingLine2RBy smallint default 0, "
                    "parkingLine3LTx smallint default 0, "
                    "parkingLine3LTy smallint default 0, "
                    "parkingLine3RTx smallint default 0, "
                    "parkingLine3RTy smallint default 0, "
                    "parkingLine3LBx smallint default 0, "
                    "parkingLine3LBy smallint default 0, "
                    "parkingLine3RBx smallint default 0, "
                    "parkingLine3RBy smallint default 0, "
                    "parkingLine1Confidence smallint, "
                    "parkingLine2Confidence smallint, "
                    "parkingLine3Confidence smallint, "
                    "Car1posLTx smallint, "
                    "Car1posLTy smallint, "
                    "Car1posRBx smallint, "
                    "Car1posRBy smallint, "
                    "Car2posLTx smallint, "
                    "Car2posLTy smallint, "
                    "Car2posRBx smallint, "
                    "Car2posRBy smallint, "
                    "Car3posLTx smallint, "
                    "Car3posLTy smallint, "
                    "Car3posRBx smallint, "
                    "Car3posRBy smallint, "

                    "plate1posLTx smallint, "
                    "plate1posLTy smallint, "
                    "plate1posRBx smallint, "
                    "plate1posRBy smallint, "
                    "plate2posLTx smallint, "
                    "plate2posLTy smallint, "
                    "plate2posRBx smallint, "
                    "plate2posRBy smallint, "
                    "plate3posLTx smallint, "
                    "plate3posLTy smallint, "
                    "plate3posRBx smallint, "
                    "plate3posRBy smallint, "
                    "plate4posLTx smallint, "
                    "plate4posLTy smallint, "
                    "plate4posRBx smallint, "
                    "plate4posRBy smallint, "
                    "plate5posLTx smallint, "
                    "plate5posLTy smallint, "
                    "plate5posRBx smallint, "
                    "plate5posRBy smallint, "
                    "plate6posLTx smallint, "
                    "plate6posLTy smallint, "
                    "plate6posRBx smallint, "
                    "plate6posRBy smallint, "
                    "platePos1Confidence smallint, "
                    "platePos2Confidence smallint, "
                    "platePos3Confidence smallint, "
                    "platePos4Confidence smallint, "
                    "platePos5Confidence smallint, "
                    "platePos6Confidence smallint, "

                    "reyuv1name varchar(128),"
                    "plate1Number varchar(32),"
                    "plate1confidence smallint,"
                    "plate1brightness smallint,"
                    "plate1stable smallint,"
                    "stableplate1number varchar(32),"
                    "plate1updateTimet DATETIME, "
                    "reyuv2name varchar(128),"
                    "plate2Number varchar(32),"
                    "plate2confidence smallint,"
                    "plate2brightness smallint,"
                    "plate2stable smallint,"
                    "stableplate2number varchar(32),"
                    "plate2updateTimet DATETIME, "
                    "reyuv3name varchar(128),"
                    "plate3Number varchar(32),"
                    "plate3confidence smallint,"
                    "plate3brightness smallint,"
                    "plate3stable smallint,"
                    "stableplate3number varchar(32),"
                    "plate3updateTimet DATETIME, "
                    "LampStatus varchar(32)"
                    ")" % (_alg_log))
except Exception, e:
    print

try:
    cur.execute("create table if not exists AiOutTable("
                "cameraID char(24), "
                "cmosID int,"
                "pic_full_name char(255), "
                "LatestUpdate datetime, "
                "CarCount tinyint default 0, "
                "parking1State tinyint default 0, "
                "parking2State tinyint default 0, "
                "parking3State tinyint default 0, "
                "parking1IsCrossLine tinyint, "
                "parking2IsCrossLine tinyint, "
                "parking3IsCrossLine tinyint,"
                "parkingLine1LTx smallint default 0, "
                "parkingLine1LTy smallint default 0, "
                "parkingLine1RTx smallint default 0, "
                "parkingLine1RTy smallint default 0, "
                "parkingLine1LBx smallint default 0, "
                "parkingLine1LBy smallint default 0, "
                "parkingLine1RBx smallint default 0, "
                "parkingLine1RBy smallint default 0, "
                "parkingLine2LTx smallint default 0, "
                "parkingLine2LTy smallint default 0, "
                "parkingLine2RTx smallint default 0, "
                "parkingLine2RTy smallint default 0, "
                "parkingLine2LBx smallint default 0, "
                "parkingLine2LBy smallint default 0, "
                "parkingLine2RBx smallint default 0, "
                "parkingLine2RBy smallint default 0, "
                "parkingLine3LTx smallint default 0, "
                "parkingLine3LTy smallint default 0, "
                "parkingLine3RTx smallint default 0, "
                "parkingLine3RTy smallint default 0, "
                "parkingLine3LBx smallint default 0, "
                "parkingLine3LBy smallint default 0, "
                "parkingLine3RBx smallint default 0, "
                "parkingLine3RBy smallint default 0, "
                "parkingLine1Confidence smallint, "
                "parkingLine2Confidence smallint, "
                "parkingLine3Confidence smallint, "
                "Car1posLTx smallint, "
                "Car1posLTy smallint, "
                "Car1posRBx smallint, "
                "Car1posRBy smallint, "
                "Car2posLTx smallint, "
                "Car2posLTy smallint, "
                "Car2posRBx smallint, "
                "Car2posRBy smallint, "
                "Car3posLTx smallint, "
                "Car3posLTy smallint, "
                "Car3posRBx smallint, "
                "Car3posRBy smallint, "
    
                "plate1posLTx smallint, "
                "plate1posLTy smallint, "
                "plate1posRBx smallint, "
                "plate1posRBy smallint, "
                "plate2posLTx smallint, "
                "plate2posLTy smallint, "
                "plate2posRBx smallint, "
                "plate2posRBy smallint, "
                "plate3posLTx smallint, "
                "plate3posLTy smallint, "
                "plate3posRBx smallint, "
                "plate3posRBy smallint, "
                "plate4posLTx smallint, "
                "plate4posLTy smallint, "
                "plate4posRBx smallint, "
                "plate4posRBy smallint, "
                "plate5posLTx smallint, "
                "plate5posLTy smallint, "
                "plate5posRBx smallint, "
                "plate5posRBy smallint, "
                "plate6posLTx smallint, "
                "plate6posLTy smallint, "
                "plate6posRBx smallint, "
                "plate6posRBy smallint, "
                "platePos1Confidence smallint, "
                "platePos2Confidence smallint, "
                "platePos3Confidence smallint, "
                "platePos4Confidence smallint, "
                "platePos5Confidence smallint, "
                "platePos6Confidence smallint, "
   
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table AiOutTable "+str(e)
    pass

try:
    cur.execute("create table if not exists AiOutTable2("
                "cameraID char(24), "
                "cmosID int,"
                "pic_full_name char(255), "
                "LatestUpdate datetime, "
                "CarCount tinyint default 0, "
                "parking1State tinyint default 0, "
                "parking2State tinyint default 0, "
                "parking3State tinyint default 0, "
                "parking1IsCrossLine tinyint, "
                "parking2IsCrossLine tinyint, "
                "parking3IsCrossLine tinyint,"
                "parkingLine1LTx smallint default 0, "
                "parkingLine1LTy smallint default 0, "
                "parkingLine1RTx smallint default 0, "
                "parkingLine1RTy smallint default 0, "
                "parkingLine1LBx smallint default 0, "
                "parkingLine1LBy smallint default 0, "
                "parkingLine1RBx smallint default 0, "
                "parkingLine1RBy smallint default 0, "
                "parkingLine2LTx smallint default 0, "
                "parkingLine2LTy smallint default 0, "
                "parkingLine2RTx smallint default 0, "
                "parkingLine2RTy smallint default 0, "
                "parkingLine2LBx smallint default 0, "
                "parkingLine2LBy smallint default 0, "
                "parkingLine2RBx smallint default 0, "
                "parkingLine2RBy smallint default 0, "
                "parkingLine3LTx smallint default 0, "
                "parkingLine3LTy smallint default 0, "
                "parkingLine3RTx smallint default 0, "
                "parkingLine3RTy smallint default 0, "
                "parkingLine3LBx smallint default 0, "
                "parkingLine3LBy smallint default 0, "
                "parkingLine3RBx smallint default 0, "
                "parkingLine3RBy smallint default 0, "
                "parkingLine1Confidence smallint, "
                "parkingLine2Confidence smallint, "
                "parkingLine3Confidence smallint, "
                "Car1posLTx smallint, "
                "Car1posLTy smallint, "
                "Car1posRBx smallint, "
                "Car1posRBy smallint, "
                "Car2posLTx smallint, "
                "Car2posLTy smallint, "
                "Car2posRBx smallint, "
                "Car2posRBy smallint, "
                "Car3posLTx smallint, "
                "Car3posLTy smallint, "
                "Car3posRBx smallint, "
                "Car3posRBy smallint, "

                "plate1posLTx smallint, "
                "plate1posLTy smallint, "
                "plate1posRBx smallint, "
                "plate1posRBy smallint, "
                "plate2posLTx smallint, "
                "plate2posLTy smallint, "
                "plate2posRBx smallint, "
                "plate2posRBy smallint, "
                "plate3posLTx smallint, "
                "plate3posLTy smallint, "
                "plate3posRBx smallint, "
                "plate3posRBy smallint, "
                "plate4posLTx smallint, "
                "plate4posLTy smallint, "
                "plate4posRBx smallint, "
                "plate4posRBy smallint, "
                "plate5posLTx smallint, "
                "plate5posLTy smallint, "
                "plate5posRBx smallint, "
                "plate5posRBy smallint, "
                "plate6posLTx smallint, "
                "plate6posLTy smallint, "
                "plate6posRBx smallint, "
                "plate6posRBy smallint, "
                "platePos1Confidence smallint, "
                "platePos2Confidence smallint, "
                "platePos3Confidence smallint, "
                "platePos4Confidence smallint, "
                "platePos5Confidence smallint, "
                "platePos6Confidence smallint, "

                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table AiOutTable2 " + str(e)
    pass

try:
    cur.execute("create table if not exists bay_using_log("
                "day int, "
                "hour int,"
                "used_bays int, "
                "primary key(day, hour)"
                ")")
except Exception, e:
    print "create table bay_using_log " + str(e)
    pass

try:
    cur.execute("create table if not exists videoAiOutTable("
                "cameraID char(24), "
                "cmosID int,"
                "parking1State tinyint, "
                "parking2State tinyint, "
                "parking3State tinyint, "
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table videoAiOutTable " + str(e)
    pass

"""
try:
    cur.execute("insert into AiOutTable(cameraID, cmosID, parking1State, parking2State, parking3State, "
                "Car1posLTx, Car1posLTy, Car1posRBx, Car1posRBy,"
                "Car2posLTx, Car2posLTy, Car2posRBx, Car2posRBy,"
                "Car3posLTx, Car3posLTy, Car3posRBx, Car3posRBy,"
                "plate1posLTx, plate1posLTy, plate1posRBx, plate1posRBy,"
                "plate2posLTx, plate2posLTy, plate2posRBx, plate2posRBy,"
                "plate3posLTx, plate3posLTy, plate3posRBx, plate3posRBy,"
                "plate4posLTx, plate4posLTy, plate4posRBx, plate4posRBy,"
                "plate5posLTx, plate5posLTy, plate5posRBx, plate5posRBy,"
                "plate6posLTx, plate6posLTy, plate6posRBx, plate6posRBy"
                ")values('1712430003',0, 1,0, 1, "
                "10, 11, 12, 13,"
                "20, 11, 12, 13,"
                "30, 11, 12, 13,"
                "10, 21, 22, 23,"
                "20, 21, 22, 23,"
                "30, 21, 22, 23,"
                "40, 21, 22, 23,"
                "50, 21, 22, 23,"
                "60, 21, 22, 23"
                ")")
    cur.execute("insert into AiOutTable(cameraID, cmosID, parking1State, parking2State, parking3State, "
                "parkingLine1LTx,parkingLine1LTy, parkingLine1RTx, parkingLine1RTy,"
                "parkingLine1LBx,parkingLine1LBy, parkingLine1RBx, parkingLine1RBy,"
                "parkingLine2LTx,parkingLine2LTy, parkingLine2RTx, parkingLine2RTy,"
                "parkingLine2LBx,parkingLine2LBy, parkingLine2RBx, parkingLine2RBy,"
                "parkingLine3LTx,parkingLine3LTy, parkingLine3RTx, parkingLine3RTy,"
                "parkingLine3LBx,parkingLine3LBy, parkingLine3RBx, parkingLine3RBy,"
                "Car1posLTx, Car1posLTy, Car1posRBx, Car1posRBy,"
                "Car2posLTx, Car2posLTy, Car2posRBx, Car2posRBy,"
                "Car3posLTx, Car3posLTy, Car3posRBx, Car3posRBy,"
                "plate1posLTx, plate1posLTy, plate1posRBx, plate1posRBy,"
                "plate2posLTx, plate2posLTy, plate2posRBx, plate2posRBy,"
                "plate3posLTx, plate3posLTy, plate3posRBx, plate3posRBy,"
                "plate4posLTx, plate4posLTy, plate4posRBx, plate4posRBy,"
                "plate5posLTx, plate5posLTy, plate5posRBx, plate5posRBy,"
                "plate6posLTx, plate6posLTy, plate6posRBx, plate6posRBy"
                ")values('123456789',1, 0,0, 0, "
                "0,0,20,0,0,80,20,80,"
                "25,5,45,6,22,75,55,88,"
                "65,20,89,10,75,75,95,95,"
                "10, 11, 12, 13,"
                "20, 11, 12, 13,"
                "30, 11, 12, 13,"
                "0, 0, 0, 0,"
                "0, 0, 0, 0,"
                "30, 21, 22, 23,"
                "0, 0, 0, 0,"
                "50, 21, 72, 78,"
                "60, 21, 73, 79"
                ")")
except Exception, e:
    print "insert into AiOutTable fail "+str(e)
    pass"""

"""
try:
    cur.execute("create table if not exists AiOutTableOlder("
                "cameraID char(24), "
                "cmosID tinyint,"
                "pic_full_name char(255), "
                "LatestUpdate datetime, "
                "CarCount tinyint, "
                "parking1State tinyint, "
                "parking2State tinyint, "
                "parking3State tinyint, "
                "parking1IsCrossLine tinyint, "
                "parking2IsCrossLine tinyint, "
                "parking3IsCrossLine tinyint,"
                "parkingLine1LTx smallint, "
                "parkingLine1LTy smallint, "
                "parkingLine1RTx smallint, "
                "parkingLine1RTy smallint, "
                "parkingLine1LBx smallint, "
                "parkingLine1LBy smallint, "
                "parkingLine1RBx smallint, "
                "parkingLine1RBy smallint, "
                "parkingLine2LTx smallint, "
                "parkingLine2LTy smallint, "
                "parkingLine2RTx smallint, "
                "parkingLine2RTy smallint, "
                "parkingLine2LBx smallint, "
                "parkingLine2LBy smallint, "
                "parkingLine2RBx smallint, "
                "parkingLine2RBy smallint, "
                "parkingLine3LTx smallint, "
                "parkingLine3LTy smallint, "
                "parkingLine3RTx smallint, "
                "parkingLine3RTy smallint, "
                "parkingLine3LBx smallint, "
                "parkingLine3LBy smallint, "
                "parkingLine3RBx smallint, "
                "parkingLine3RBy smallint, "
                "parkingLine1Confidence smallint, "
                "parkingLine2Confidence smallint, "
                "parkingLine3Confidence smallint, "
                "Car1posLTx smallint, "
                "Car1posLTy smallint, "
                "Car1posRBx smallint, "
                "Car1posRBy smallint, "
                "Car2posLTx smallint, "
                "Car2posLTy smallint, "
                "Car2posRBx smallint, "
                "Car2posRBy smallint, "
                "Car3posLTx smallint, "
                "Car3posLTy smallint, "
                "Car3posRBx smallint, "
                "Car3posRBy smallint, "

                "plate1posLTx smallint, "
                "plate1posLTy smallint, "
                "plate1posRBx smallint, "
                "plate1posRBy smallint, "
                "plate2posLTx smallint, "
                "plate2posLTy smallint, "
                "plate2posRBx smallint, "
                "plate2posRBy smallint, "
                "plate3posLTx smallint, "
                "plate3posLTy smallint, "
                "plate3posRBx smallint, "
                "plate3posRBy smallint, "
                "plate4posLTx smallint, "
                "plate4posLTy smallint, "
                "plate4posRBx smallint, "
                "plate4posRBy smallint, "
                "plate5posLTx smallint, "
                "plate5posLTy smallint, "
                "plate5posRBx smallint, "
                "plate5posRBy smallint, "
                "plate6posLTx smallint, "
                "plate6posLTy smallint, "
                "plate6posRBx smallint, "
                "plate6posRBy smallint, "
                "platePos1Confidence smallint, "
                "platePos2Confidence smallint, "
                "platePos3Confidence smallint, "
                "platePos4Confidence smallint, "
                "platePos5Confidence smallint, "
                "platePos6Confidence smallint, "

                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table AiOutTable " + str(e)
    pass
"""

try:
    _sql_str = """
DROP PROCEDURE IF EXISTS `selectSpaceAll`;

CREATE PROCEDURE `selectSpaceAll`(IN `ParamPicName` varchar(30), IN `Error_Time` int)
BEGIN
	select MySpace.cameraID,MySpace.NodeID,MySpace.PointID,MySpace.state, MySpace.pic, MySpace.ip, 
	MyPlate.PlateID,MyPlate.TypeID,ifnull(MySpace.editflag, NOW()) as I_O_datetime FROM 
	(select o.cameraID,o.cmosID as NodeID, 
	CASE o.cmosID WHEN 0 THEN SUBSTRING(st.Spaceid,-1) ELSE SUBSTRING(st.Spaceid,-1)-3 END as PointID, 
	o.ip,o.LatestConnect as editflag,st.CarportStatus as state,IFNULL(ast.Slot_count, 3) as spaceCount, 
	CONCAT('http://',o.ip,'/images/',`ParamPicName`,o.cmosID ,'.jpg') as pic 
	from OnlineHvpdStatusTableMem as o 
	LEFT JOIN SpaceStatusTable as st on st.cameraID = o.cameraID and st.cmosID = o.cmosID 
	LEFT JOIN AiSettingTable as ast on o.cameraID = ast.cameraID and o.cmosID = ast.cmosID) as MySpace 
	LEFT JOIN 
	(SELECT rft1.cameraID, rft1.cmosID, ifnull(rft1.Plate1Number,'') as PlateID, ifnull(rft1.Plate1type, 0) as TypeID, 
	ifnull(rft1.Plate1Datetime, NOW()) as I_O_datetime,ifnull(rft1.Slot1Number,1) as rPointID 
	FROM reoutfiltertable as rft1 
	LEFT JOIN onlinehvpdstatustablemem as ost1 on ost1.cameraID = rft1.cameraID and ost1.cmosID = rft1.cmosID 
	UNION 
	SELECT rft2.cameraID, rft2.cmosID, ifnull(rft2.Plate2Number,'') as PlateID, ifnull(rft2.Plate2type, 0) as TypeID,
	ifnull(rft2.Plate2Datetime, NOW()) as I_O_datetime,ifnull(rft2.Slot2Number,2) as rPointID 
	FROM reoutfiltertable as rft2 
	LEFT JOIN onlinehvpdstatustablemem as ost2 on ost2.cameraID = rft2.cameraID and ost2.cmosID = rft2.cmosID 
	UNION  
	SELECT rft3.cameraID, rft3.cmosID, ifnull(rft3.Plate3Number,'') as PlateID, ifnull(rft3.Plate3type, 0) as TypeID,
	ifnull(rft3.Plate3Datetime, NOW()) as I_O_datetime,ifnull(rft3.Slot3Number,3) as rPointID 
	FROM reoutfiltertable as rft3 
	LEFT JOIN onlinehvpdstatustablemem as ost3 on ost3.cameraID = rft3.cameraID and ost3.cmosID = rft3.cmosID) as MyPlate 
	on MyPlate.cameraID = MySpace.cameraID and MyPlate.cmosID = MySpace.NodeID and MyPlate.rPointID = MySpace.PointID 
	where (ip <> '' or ip is not null) and MySpace.editflag >= DATE_ADD(now(),INTERVAL `Error_Time` minute);
END;
"""
    cur.execute(_sql_str)
except Exception, e:
    print str(e)
conn.close()
print time.time(), time.clock()