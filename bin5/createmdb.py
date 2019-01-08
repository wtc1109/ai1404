import time
import wtclib
import datetime
import os, sys



while True:
    (cur, conn) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd2db2_backup")
    if None != cur:
        cur.close()
        conn.close()
        break
    else:
        print ("can not connect to db and sleep 20")
        time.sleep(20)

while True:
    (cur, conn) = wtclib.get_a_sql_cur("../conf/conf.conf","alglog")
    if None != cur:
        break
    else:
        print ("can not connect to db and sleep 20")
        time.sleep(20)
try:
    localtime1 = time.localtime()
    _alg_log = "ailog%d%02d%02d"%(localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
    cur.execute("create table if not exists %s("
                "aijpgname varchar(128) primary key,"
                "JpgLatestUpdate DATETIME,"
                "cameraID varchar(24), "
                "cmosID tinyint default 0,"
                "CarCount tinyint default 0, "
                "parking1State tinyint default 0, "
                "parking2State tinyint default 0, "
                "parking3State tinyint default 0, "
                "parking4State tinyint default 0, "
                "parking5State tinyint default 0, "
                "parking6State tinyint default 0, "
                "parking1IsCrossLine tinyint default 0, "
                "parking2IsCrossLine tinyint default 0, "
                "parking3IsCrossLine tinyint default 0,"

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
                "parkingLine1Confidence smallint default 0, "
                "parkingLine2Confidence smallint default 0, "
                "parkingLine3Confidence smallint default 0, "

                "Car1posLTx smallint default 0, "
                "Car1posLTy smallint default 0, "
                "Car1posRBx smallint default 0, "
                "Car1posRBy smallint default 0, "
                "Car2posLTx smallint default 0, "
                "Car2posLTy smallint default 0, "
                "Car2posRBx smallint default 0, "
                "Car2posRBy smallint default 0, "
                "Car3posLTx smallint default 0, "
                "Car3posLTy smallint default 0, "
                "Car3posRBx smallint default 0, "
                "Car3posRBy smallint default 0, "
                "Car4posLTx smallint default 0, "
                "Car4posLTy smallint default 0, "
                "Car4posRBx smallint default 0, "
                "Car4posRBy smallint default 0, "
                "Car5posLTx smallint default 0, "
                "Car5posLTy smallint default 0, "
                "Car5posRBx smallint default 0, "
                "Car5posRBy smallint default 0, "
                "Car6posLTx smallint default 0, "
                "Car6posLTy smallint default 0, "
                "Car6posRBx smallint default 0, "
                "Car6posRBy smallint default 0, "

                "plate1posLTx smallint default 0, "
                "plate1posLTy smallint default 0, "
                "plate1posRBx smallint default 0, "
                "plate1posRBy smallint default 0, "
                "plate2posLTx smallint default 0, "
                "plate2posLTy smallint default 0, "
                "plate2posRBx smallint default 0, "
                "plate2posRBy smallint default 0, "
                "plate3posLTx smallint default 0, "
                "plate3posLTy smallint default 0, "
                "plate3posRBx smallint default 0, "
                "plate3posRBy smallint default 0, "
                "plate4posLTx smallint default 0, "
                "plate4posLTy smallint default 0, "
                "plate4posRBx smallint default 0, "
                "plate4posRBy smallint default 0, "
                "plate5posLTx smallint default 0, "
                "plate5posLTy smallint default 0, "
                "plate5posRBx smallint default 0, "
                "plate5posRBy smallint default 0, "
                "plate6posLTx smallint default 0, "
                "plate6posLTy smallint default 0, "
                "plate6posRBx smallint default 0, "
                "plate6posRBy smallint default 0, "
                "platePos1Confidence smallint default 0, "
                "platePos2Confidence smallint default 0, "
                "platePos3Confidence smallint default 0, "
                "platePos4Confidence smallint default 0, "
                "platePos5Confidence smallint default 0, "
                "platePos6Confidence smallint default 0, "

                "reyuv1name varchar(128),"
                "plate1Number varchar(32),"
                "plate1confidence smallint default 0,"
                "plate1brightness smallint default 0,"
                "plate1stable smallint default 0,"
                "stableplate1number varchar(32),"
                "plate1updateTimet DATETIME, "
                "reyuv2name varchar(128),"
                "plate2Number varchar(32),"
                "plate2confidence smallint default 0,"
                "plate2brightness smallint default 0,"
                "plate2stable smallint default 0,"
                "stableplate2number varchar(32),"
                "plate2updateTimet DATETIME, "
                "reyuv3name varchar(128),"
                "plate3Number varchar(32),"
                "plate3confidence smallint default 0,"
                "plate3brightness smallint default 0,"
                "plate3stable smallint default 0,"
                "stableplate3number varchar(32),"
                "plate3updateTimet DATETIME, "
                "reyuv4name varchar(128),"
                "plate4Number varchar(32),"
                "plate4confidence smallint default 0,"
                "plate4brightness smallint default 0,"
                "plate4stable smallint default 0,"
                "stableplate4number varchar(32),"
                "plate4updateTimet DATETIME, "
                "reyuv5name varchar(128),"
                "plate5Number varchar(32),"
                "plate5confidence smallint default 0,"
                "plate5brightness smallint default 0,"
                "plate5stable smallint default 0,"
                "stableplate5number varchar(32),"
                "plate5updateTimet DATETIME, "
                "reyuv6name varchar(128),"
                "plate6Number varchar(32),"
                "plate6confidence smallint default 0,"
                "plate6brightness smallint default 0,"
                "plate6stable smallint default 0,"
                "stableplate6number varchar(32),"
                "plate6updateTimet DATETIME, "
                "LampStatus varchar(32)"
                ")engine=MyISAM" % (_alg_log))
    dsc = cur.execute("desc %s"%_alg_log)
    table1 = cur.fetchall()
    #if 'parking1IsCrossLine' != table1[8][0]:
        #cur.execute("drop table %s"%_alg_log)
    conn.close()
except Exception, e:
    print

while True:
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
    if None != cur:
        break
    else:
        print ("can not connect to db and sleep 20")
        time.sleep(20)



print time.time(), time.clock()

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
                "CtrlMode int default 0,"
                "Weight int default 0, "
                "height int default 0,"
                "AllRegion int default 0,"
                "Region1 int default 0, "
                "Region2 int default 0,"
                "Region3 int default 0,"
                "Region4 int default 0,"
                "Region5 int default 0,"
                "Region6 int default 0,"
                "Region7 int default 0,"
                "Region8 int default 0,"
                "Region9 int default 0, "
                "Region10 int default 0,"
                "Region11 int default 0,"
                "Region12 int default 0,"
                "Region13 int default 0,"
                "Region14 int default 0,"
                "Region15 int default 0,"
                "Region16 int default 0,"
                "Region17 int default 0, "
                "Region18 int default 0,"
                "Region19 int default 0,"
                "Region20 int default 0,"
                "Region21 int default 0,"
                "Region22 int default 0,"
                "Region23 int default 0,"
                "Region24 int default 0,"
                "RegionNum_len int default 0,"
                "specialFlag int default 0"
                ")engine=memory")
    dsc = cur.execute("desc ScreenConfigTable")
    if 31 != dsc:
        cur.execute("drop table ScreenConfigTable")
        cur.execute("create table if not exists ScreenConfigTable("
                    "ScreenSn char(16)not null primary key,"
                    "CtrlMode int,"
                    "Weight int default 0, "
                    "height int default 0,"
                    "AllRegion int default 0,"
                    "Region1 int default 0, "
                    "Region2 int default 0,"
                    "Region3 int default 0,"
                    "Region4 int default 0,"
                    "Region5 int default 0,"
                    "Region6 int default 0,"
                    "Region7 int default 0,"
                    "Region8 int default 0,"
                    "Region9 int default 0, "
                    "Region10 int default 0,"
                    "Region11 int default 0,"
                    "Region12 int default 0,"
                    "Region13 int default 0,"
                    "Region14 int default 0,"
                    "Region15 int default 0,"
                    "Region16 int default 0,"
                    "Region17 int default 0, "
                    "Region18 int default 0,"
                    "Region19 int default 0,"
                    "Region20 int default 0,"
                    "Region21 int default 0,"
                    "Region22 int default 0,"
                    "Region23 int default 0,"
                    "Region24 int default 0,"
                    "RegionNum_len int default 0,"
                    "specialFlag int default 0"
                    ")engine=memory")
except Exception, e:
    print str(e)
    pass

try:

    cur.execute("create table if not exists ScreenRegionConfigTable("
                "RegionSn int not null primary key,"
                "TopLeftX int default 0,"
                "TopLeftY int default 0, "
                "BottomRightX int default 0,"
                "BottomRightY int default 0,"
                "Action int default 0,"
                "Font int default 0, "
                "Color int default 0,"
                "Display char(160)"
                ")engine=memory")

except Exception, e:
    print str(e)
    pass



try:
    cur.execute("create table if not exists Space2LedTable("
                "id int not null auto_increment primary key,"
                "cameraID char(32), "
                "cmosID tinyint default 0,"
                "bay tinyint default 0,"
                "RegionSn int)engine=memory")
    dsc = cur.execute("desc Space2LedTable")

except Exception, e:
    print str(e)
    pass

try:
    cur.execute("drop table leddisplayerudpinfo")
    cur.execute("drop table leddisplayerudperrorinfo")
except Exception, e:
    print str(e)
    pass




try:
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
    cur.execute("create table if not exists camera_UpgradeTable("
                "cameraID char(24) primary key, "       
                "filename char(128),"
                "user char(32),"
                "ReNewFlag tinyint default 0,"
                "set_time DATETIME, "
                "end_time DATETIME" 
                ")")

except Exception, e:
    print "create table HvpdUpgradeTable", e
    pass

try:
    cur.execute("create table if not exists alarm_table("
                "id int not null auto_increment primary key, "       
                "sql_str varchar(512),"
                "true_lamp varchar(64) default 'R1:0,G1:80,B1:80,D1:500;R2:80,G2:80,B2:0,D2:500;' " 
                ")")

except Exception, e:
    print "create table HvpdUpgradeTable", e
    pass

try:
    cur.execute("create table if not exists video_user_set("
                "cameraID char(24) , "
                "cmosID tinyint default 0,"
                "cur_resolution int,"
                "cur_bitrate_Kbps int,"
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
    _tableName = "video_log_%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
    cur.execute("create table if not exists %s("
                "id int not null auto_increment primary key,"
                "cameraID char(24) , "
                "cmosID tinyint default 0,"
                "get_time DATETIME, "
                "video_type char(32),"
                "used_flag int default 0,"
                "filename char(64),"
                "serverIP char(24)"
                ")" % _tableName)
    dsc = cur.execute("desc %s" % _tableName)

    if 8 != dsc:
        cur.execute("drop table %s" % _tableName)
        cur.execute("create table if not exists %s("
                    "id int not null auto_increment primary key,"
                    "cameraID char(24) , "
                    "cmosID tinyint default 0,"
                    "get_time DATETIME, "
                    "video_type char(32),"
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
                "startAIout char(32), "
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
                    "startAIout char(32), "
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
                "video_type char(32),"
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
                    "video_type char(32),"
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
except Exception, e:
    print e
    print "video_log"

try:
    cur.execute("create table if not exists OnlineHvpdStatusTableMem("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "neighbor_camera char(24), "
                "slave tinyint, "
                "ip char(20), "
                "exp int default 0, "
                "gain smallint default 0, "
                "uptime int default 0,"
                "bluetooth char(20), "
                "LatestConnect datetime, "
                "connectTimet int default 0,"
                "last_pic_timet int default 0,"
                "waiting_ex tinyint default 0, "
                "yuv_exp int default 0,"
    
                "alarm char(32),"
                "other char(20),"
                "primary key(cameraID, cmosID)"
                ")engine=memory")

except Exception, e:
    print "create table OnlineHvpdStatusTableMem", e
    pass

try:
    cur.execute("create table if not exists monostablepic("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
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
                    "cmosID tinyint default 0,"
                    "LatestConnect datetime, "
                    "connectTimet int default 0,"
                    "json_str text,"
             
                    "primary key(cameraID, cmosID)"
                    ")")
except Exception, e:
    print "create table monostablepic"+str(e)+" in line: " + str(sys._getframe().f_lineno)
    pass



try:
    cur.execute("create table if not exists camera_VersionTableMem("
                "cameraID char(24)primary key, "
                "uart_version char(32),"
                "camera_version char(32),"
                "udp_version char(32),"
                "video_rtsp_version char(32),"
                "video_onvif_version char(32),"
                "hard_ver char(32),"
                "renewtime datetime,"
                "renewtimet int default 0"
                ")engine=memory")

except Exception, e:
    print "create table camera_VersionTableMem", e
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
print time.time(), time.clock()

try:
    cur.execute("create table if not exists 2color_lamp("
                "color_name char(32) primary key, "
                "unused_bigger_color char(24),"
                "else_color char(24)"
                ")engine=memory")
    cur.execute("create table if not exists 2color_lamp_user("
                "color_name char(32) primary key, "
                "unused_bigger_color char(24),"
                "else_color char(24)"
                ")")
    cur.execute("TRUNCATE TABLE 2color_lamp")
    cur.execute("insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('green2red','%s','%s')"%(led_green,led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('fuchsia2red','%s','%s')" % (
        led_fuchsia, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('yellow2red','%s','%s')" % (led_yellow, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('orange2red','%s','%s')" % (led_orange, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('aqua2red','%s','%s')" % (led_aqua, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('white2red','%s','%s')" % (led_white, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('blue2red','%s','%s')" % (led_blue, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('pink2red','%s','%s')" % (led_pink, led_red))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('green2dark','%s','%s')" % (led_green, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('fuchsia2dark','%s','%s')" % (
        led_fuchsia, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('yellow2dark','%s','%s')" % (led_yellow, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('orange2dark','%s','%s')" % (led_orange, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('aqua2dark','%s','%s')" % (led_aqua, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('white2dark','%s','%s')" % (led_white, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('blue2dark','%s','%s')" % (led_blue, led_dark))
    cur.execute(
        "insert into 2color_lamp(color_name,unused_bigger_color,else_color)values('pink2dark','%s','%s')" % (led_pink, led_dark))
except Exception,e:
    print e
    pass

del lamp1,lamp2,lamp3,lamp4,lamp5,lamp6,lampX
del dic1,dic2,dic3,dic4,dic5,dic6,dicX
del led_fuchsia,led_yellow,led_orange,led_aqua,led_white,led_blue,led_green,led_dark,led_pink,led_red



try:
    cur.execute("create table if not exists LampSettingTable("
                "equipmentID char(24) primary key, "
                "CtrlTableName char(32) default '2color_lamp' , "
                "lamp_colcor tinyint default 2,"  
                "colcor_name char(32) default 'green2red', "
                "colcor_bigger_than tinyint default 0,"
                "ManualCtrLampFlag tinyint default 0,"               
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0"
                ")")
except:
    pass


try:
    cur.execute("create table if not exists LampSettingTableMem("
                "equipmentID char(24) primary key, "
                "CtrlTableName char(32) default '2color_lamp', "   
                "lamp_colcor tinyint default 2,"  
                "colcor_name char(32) default 'green2red', "
                "colcor_bigger_than tinyint default 0,"
                "ManualCtrLampFlag tinyint default 0,"
                "ManualCtrSpaceFlag tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "LampStatus char(32),"
                "LampRenewTimet int default 0"
                ")engine=memory")
except:
    pass

try:
    cur.execute("create table if not exists LampUserCtlTable("
                "equipmentID char(24) primary key, "
                "userCtrl1Sn char(24))")
except:
    print "create table LampUserCtlTable fail"
    pass


try:
    cur.execute("create table if not exists camera_IpAddrSettingTable("
                "cameraID char(24) primary key,"
                "ReNewFlag tinyint default 0,"
                "CurIP char(24),"
                "CurMask char(24),"
                "CurGateway char(24),"
                "NewIP char(24), "
                "NewMask char(24), "
                "NewGateway char(24)"
                ")")
except:
    print "create table hvpdIpAddrSettingTable fail"
    pass


try:
    cur.execute("create table if not exists Equipment2cameraId("
                "equipmentID char(24) primary key, "
                "set_timet int default 0,"
                "cameraID1 char(24), "
                "cmosID1 tinyint default 0,"
                "cameraID2 char(24) default 0,"
                "cmosID2 tinyint default 0)")
    cur.execute("create table if not exists Equipment2cameraIdMem("
                "equipmentID char(24) primary key, "
                "set_timet int default 0,"
                "cameraID1 char(24), "
                "cmosID1 tinyint default 0,"
                "cameraID2 char(24) default 0,"
                "cmosID2 tinyint default 0"
                ")engine=memory")

except:
    print "create table Equipment2cameraId fail"
    pass


try:
    cur.execute("create table if not exists camera2equipTable("
                "cameraID char(24),"
                "cmosID tinyint default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")")
    cur.execute("create table if not exists camera2equipTablemem("
                "cameraID char(24),"
                "cmosID tinyint default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
                "set_time DATETIME,"
                "set_timet int default 0,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table camera2equipTable fail"
    pass

"""
try:
    cur.execute("create table if not exists phaseCheckSettingTableMem_bay("
                "cameraID char(24),"
                "cmosID tinyint default 0,"
                "bay  tinyint,"
                "phasepos char(20), "
                "RenewTimet int default 0,"
                "RenewDate datetime,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")

except:
    print "create table phaseCheckSettingTableMem_bay fail"
    pass
"""

try:
    cur.execute("create table if not exists AiSettingTable_camera("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bays tinyint default 3, "
                "InstallType tinyint default 0, "
                "SlotBitmap tinyint default 0, "
                "user_manual_parking_line tinyint default 1, " 
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
                "set_timet int default 0,"   
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"              
                "primary key(cameraID, cmosID)"
                ")")
    cur.execute("create table if not exists AiSettingTable_bay("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "ctrlEquipment char(24),"
                "parking_line1LTx smallint default 0,"
                "parking_line1LTy smallint default 0,"
                "parking_line1RTx smallint default 0,"
                "parking_line1RTy smallint default 0,"
                "parking_line1LBx smallint default 0,"
                "parking_line1LBy smallint default 0,"
                "parking_line1RBx smallint default 0,"
                "parking_line1RBy smallint default 0,"
                "set_time DATETIME,"   
                "set_timet int," 
                "need_plate int default 1,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "ctrlEquipment2 char(24),"
                "ctrlEquipment3 char(24),"
                "ctrlEquipment4 char(24),"
                "ctrlEquipment5 char(24),"
                "ctrlEquipment6 char(24),"
                "alarm_table_id1 int default 0,"
                "alarm_table_id2 int default 0,"
                "alarm_table_id3 int default 0,"
                "alarm_table_id4 int default 0,"
                "alarm_table_id5 int default 0,"
                "alarm_table_id6 int default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")")


except:
    print "create table AiSettingTable_camera fail"
    pass
try:
    cur.execute("create table if not exists AiSettingTable_camera_mem("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bays tinyint default 3, "
                "InstallType tinyint default 0, "
                "SlotBitmap tinyint default 0, "
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
                "set_timet int default 0,"  
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"              
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    cur.execute("create table if not exists AiSettingTable_bay_mem("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "ctrlEquipment char(24),"
                "parking_line1LTx smallint default 0,"
                "parking_line1LTy smallint default 0,"
                "parking_line1RTx smallint default 0,"
                "parking_line1RTy smallint default 0,"
                "parking_line1LBx smallint default 0,"
                "parking_line1LBy smallint default 0,"
                "parking_line1RBx smallint default 0,"
                "parking_line1RBy smallint default 0,"
                "set_time DATETIME,"   
                "set_timet int default 0," 
                "need_plate int default 1,"
                "Event1Flag int default 0,"
                "Event2Flag int default 0,"
                "ctrlEquipment2 char(24),"
                "ctrlEquipment3 char(24),"
                "ctrlEquipment4 char(24),"
                "ctrlEquipment5 char(24),"
                "ctrlEquipment6 char(24),"
                "alarm_table_id1 int default 0,"
                "alarm_table_id2 int default 0,"
                "alarm_table_id3 int default 0,"
                "alarm_table_id4 int default 0,"
                "alarm_table_id5 int default 0,"
                "alarm_table_id6 int default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")


except:
    print "create table AiSettingTableMem fail"
    pass




try:
    cur.execute("create table if not exists ReSettingTable("
                "cameraID char(24), "
                "cmosID tinyint default 0,"   
                "set_time DATETIME,"
                "set_timet int default 0,"
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
                "primary key(cameraID, cmosID)"
                ")")

except:
    print "create table ReSettingTable fail"
    pass

try:
    cur.execute("create table if not exists ReSettingTableMem("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "set_time DATETIME,"
                "set_timet int default 0,"
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
                "primary key(cameraID, cmosID)"
                ")engine=memory")

except:
    print "create table ReSettingTableMem fail"
    pass


try:
    cur.execute("create table if not exists ReOutTable_bay("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "PlateupdateTimet int default 0,"
                "PlateNumber char(16),"
                "Platetype char(8),"
                "SlotNumber char(12),"
                "set_time DATETIME,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")

except:
    print "create table ReOutTable fail"
    pass


try:
    cur.execute("create table if not exists ReOutFilterTable("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "PlateupdateTimet int default 0,"
                "PlateDatetime datetime,"
                "PlateNumber char(16),"
                "Platetype char(8),"
                "SlotNumber char(12),"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")

except:
    print "create table ReOutFilterTable fail"
    pass

try:
    cur.execute("create table if not exists ReFilterTable("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
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
                "matchTimet8 int default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")
except Exception, e:
    print  "create table ReFilterTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists Lamp_for_user("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "ctrlEquipment char(24),"
              
                "set_Timet int default 0,"
                "set_Date datetime,"
                "primary key(cameraID, cmosID,bay)"
                ")")
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
except Exception, e:
    print  "create table Lamp_for_user fail " + str(e)
    pass

try:
    cur.execute("create table if not exists SpaceStatusTable("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "ctrlEquipment char(24),"
                "CarportStatus int default 0,"
                "RegionSn int default 0,"
                "StatusChange0Time int default 0,"
                "YUVRenewTime  int default 0,"
                "YUVGetfilesTime  int default 0,"
                "Status_changeTime int default 0,"
                "Lamp_changeTime int default 0,"
                "plateLTx int default 0,"
                "plateLTy int default 0,"
                "plateRBx int default 0,"
                "plateRBy int default 0,"
                "plate_RenewTime int default 0,"
                "phase_pos char(20), "
                "phase_Timet int default 0,"
                "phase_Date datetime,"
                "video_aiout_old tinyint default 0,"
                "parkin_timet int default 0,"
                "parkout_timet int default 0,"
                "parkin_time datetime,"
                "parkout_time datetime,"
                "reserved tinyint default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")
except Exception, e:
    print  "create table SpaceStatusTable fail " + str(e)
    pass


"""
try:
    cur.execute("create table if not exists SpaceForReInfoTable("
                "cameraID char(24),"
                "cmosID tinyint default 0,"
                "bay tinyint,"
                "plateLTx int default 0,"
                "plateLTy int default 0,"
                "plateRBx int default 0,"
                "plateRBy int default 0,"
                "RenewTime int default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")
except Exception, e:
    print  "create table SpaceForReInfoTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists SpaceYUVFilterBuffTable("
                "cameraID char(24), "
                "cmosID tinyint default 0,"
                "bay tinyint default 0,"
                "SpaceRenewTime int default 0,"
                "YUVRenewTime  int default 0,"
                "YUVGetfilesTime  int default 0,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")
except Exception, e:
    print  "create table SpaceYUVFilterBuffTable fail " + str(e)
    pass
"""

try:

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
    dsc = cur.execute("desc WatchdogTable")
    # table1 = cur.fetchall()
    # if 'PRI' != table1[8][3]:
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


try:
    cur.execute("create table if not exists AiOutTable_camera("
                "cameraID char(24), "
                "cmosID int default 0,"
                "pic_full_name char(255), "
                "LatestUpdate datetime, "
                "bays tinyint default 3, "
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    cur.execute("create table if not exists AiOutTable_bay("
                "cameraID char(24), "
                "cmosID int default 0,"
                "bay int,"
                "State tinyint default 0, "
                "IsCrossLine tinyint default 0, "
                "parkingLineLTx smallint default 0, "
                "parkingLineLTy smallint default 0, "
                "parkingLineRTx smallint default 0, "
                "parkingLineRTy smallint default 0, "
                "parkingLineLBx smallint default 0, "
                "parkingLineLBy smallint default 0, "
                "parkingLineRBx smallint default 0, "
                "parkingLineRBy smallint default 0, "
                "parkingLineConfidence smallint default 0, "
                "CarposLTx smallint default 0, "
                "CarposLTy smallint default 0, "
                "CarposRBx smallint default 0, "
                "CarposRBy smallint default 0, "
                "plate1posLTx smallint default 0, "
                "plate1posLTy smallint default 0, "
                "plate1posRBx smallint default 0, "
                "plate1posRBy smallint default 0, "
                "plate2posLTx smallint default 0, "
                "plate2posLTy smallint default 0, "
                "plate2posRBx smallint default 0, "
                "plate2posRBy smallint default 0, "
                "platePos1Confidence smallint default 0, "
                "platePos2Confidence smallint default 0,"
                "LatestUpdate  datetime,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")
except Exception, e:
    print "create table AiOutTable "+str(e)
    pass

try:
    cur.execute("create table if not exists AiOutTable_camera2("
                "cameraID char(24), "
                "cmosID int default 0,"
                "pic_full_name char(255), "
                "LatestUpdate datetime, "
                "bays tinyint default 3, "
                "primary key(cameraID, cmosID)"
                ")engine=memory")
    cur.execute("create table if not exists AiOutTable_bay2("
                "cameraID char(24), "
                "cmosID int default 0,"
                "bay int,"
                "State tinyint default 0, "
                "IsCrossLine tinyint default 0, "
                "parkingLineLTx smallint default 0, "
                "parkingLineLTy smallint default 0, "
                "parkingLineRTx smallint default 0, "
                "parkingLineRTy smallint default 0, "
                "parkingLineLBx smallint default 0, "
                "parkingLineLBy smallint default 0, "
                "parkingLineRBx smallint default 0, "
                "parkingLineRBy smallint default 0, "
                "parkingLineConfidence smallint default 0, "
                "CarposLTx smallint default 0, "
                "CarposLTy smallint default 0, "
                "CarposRBx smallint default 0, "
                "CarposRBy smallint default 0, "
                "plate1posLTx smallint default 0, "
                "plate1posLTy smallint default 0, "
                "plate1posRBx smallint default 0, "
                "plate1posRBy smallint default 0, "
                "plate2posLTx smallint default 0, "
                "plate2posLTy smallint default 0, "
                "plate2posRBx smallint default 0, "
                "plate2posRBy smallint default 0, "
                "platePos1Confidence smallint default 0, "
                "platePos2Confidence smallint default 0, "
                "LatestUpdate  datetime,"
                "primary key(cameraID, cmosID,bay)"
                ")engine=memory")


except Exception, e:
    print "create table AiOutTable2 " + str(e)
    pass





print time.time(), time.clock()