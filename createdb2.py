import time
from bin import wtclib
import time

from bin import wtclib

print time.time(), time.clock()

while True:
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
    if None != cur:
        break
    else:
        print ("can not connect to db and sleep 20")
        time.sleep(20)

try:
    cur.execute("create table if not exists ScreenConnectTable("
                "ScreenSn char(16)not null primary key,"
                "ScreenName char(16))engine=memory")
except Exception, e:
    print str(e)
    pass

try:
    cur.execute("create table if not exists ScreenConfigTable("
                "ScreenSn char(16)not null primary key,"
                "CtrlMode int,"
                "Weight int, "
                "height int,"
                "AllRegion int,"
                "Region1 int, "
                "Region2 int,"
                "Region3 int,"
                "Region4 int,"
                "Region5 int,"
                "Region6 int,"
                "Region7 int,"
                "Region8 int"
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
                "Display char(32)"
                ")engine=memory")
except Exception, e:
    print str(e)
    pass

try:
    cur.execute("create table if not exists Space2LedTable("
                "id int not null auto_increment primary key,"
                "Spaceid char(32), "
                "RegionSn int)engine=memory")
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
except Exception, e:
    print "create table HvpdUpgradeTable", e
    pass
try:
    cur.execute("insert into HvpdUpgradeTable(cameraID, cmosID, filename, ReNewFlag)values('123456789', 1, "
                "'multi_ucmq.pyc.tar.gz', 0)")
    cur.execute("insert into HvpdUpgradeTable(cameraID, cmosID, filename, ReNewFlag)values('123456780', 1, "
                "'multi_ucmq.pyc.tar.gz', 0)")
    cur.execute("insert into HvpdUpgradeTable(cameraID, cmosID, filename, ReNewFlag)values('123456781', 1, "
                "'multi_ucmq.pyc.tar.gz', 0)")
except:
    pass
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
                "CMOS tinyint, "
                "bluetooth char(20), "
                "LatestConnect datetime, "
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except Exception, e:
    print "create table OnlineHvpdStatusTableMem", e
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
    cur.execute("create table if not exists HvpdHardwareStatusTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "uart_V char(32),"
                "camera_V char(32),"
                "udp_V char(32), "
                "arm_V char(32), "

                "renew_time DATETIME,"
                "primary key(cameraID, cmosID)"
                ")")
except Exception, e:
    print "create table HvpdHardwareStatusTable", e
    pass


try:
    cur.execute("create table if not exists defaultXspace("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except Exception, e:
    print e
    pass
try:
    cur.execute("create table if not exists GreenDarkLamp("
                "Flag_used char(8) primary key, "
                "output char(24))engine=memory")
except Exception, e:
    print e
    pass
try:
    cur.execute("create table if not exists defaultForGirls("
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
led_pink = 'R:80,G:40,B:40'
led_dark = 'R:0,G:0,B:0'

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
if 0 == cur.execute("select * from defaultXspace"):
    for cnt in range(6):
        for i in range(len(dicX[cnt])-1):
            sql_str = "insert into defaultXspace(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_green)
            cur.execute(sql_str)
            sql_str = "insert into defaultForGirls(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_pink)
            cur.execute(sql_str)
            cur.execute("insert into GreenDarkLamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_green))
            cur.execute("insert into default6Lamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], lampX[cnt][i]))
        i = len(dicX[cnt])-1
        cur.execute("insert into default6Lamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], lampX[cnt][i]))
        sql_str = "insert into defaultXspace(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red)
        cur.execute(sql_str)
        sql_str = "insert into defaultForGirls(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_red)
        cur.execute(sql_str)
        cur.execute("insert into GreenDarkLamp(Flag_used, output) values('%s', '%s')" % (dicX[cnt][i], led_dark))

else:
    print "no need to insert into defaultXspace"

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
                "ManualCtrFlag tinyint default 0)")
except:
    pass
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
                "ManualCtrFlag tinyint)engine=memory")
except:
    pass
try:
    cur.execute("insert into LampSettingTable(equipmentID, CtrlTableName, SpaceAll, Space1ID, Space2ID, Space3ID)"
                "values('123456789', 'defaultXspace', 3,'1234567891','1234567892','1234567893')")
    cur.execute("insert into LampSettingTable(equipmentID, CtrlTableName, SpaceAll, Space1ID, Space2ID, Space3ID, Space4ID, Space5ID, Space6ID)"
                "values('123456787', 'defaultXspace', 6,'1234567891','1234567892','1234567893', '1234567871', '1234567872', '1234567873')")
except:
    pass
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
try:
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123456, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123450, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123451, 0, 1)")
    cur.execute("insert into hvpdIpAddrSettingTable(cameraID, cmosID, ReNewFlag)values(123452, 0, 1)")
except:
    pass

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
                "cmosID2 tinyint)")
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
    cur.execute("create table if not exists hvpd2LampSettingTable("
                "cameraID char(24),"
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Effect1EquipID char(24), "
                "Effect2EquipID char(24), "
                "Effect3EquipID char(24),"
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
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table hvpd2LampSettingTableMem fail"
    pass
try:
    cur.execute("insert into hvpd2LampSettingTable(cameraID,cmosID, Effect1EquipID)values('123456787', 0, '123456787')")
    cur.execute("insert into hvpd2LampSettingTable(cameraID,cmosID, Effect1EquipID)values('123456789', 1, '123456789')")
except:
    pass

try:
    cur.execute("create table if not exists AiSettingTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "Slot_count tinyint, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint, "
                "manual_parking_line1LTx smallint,"
                "manual_parking_line1LTy smallint,"
                "manual_parking_line1RTx smallint,"
                "manual_parking_line1RTy smallint,"
                "manual_parking_line1LBx smallint,"
                "manual_parking_line1LBy smallint,"
                "manual_parking_line1RBx smallint,"
                "manual_parking_line1RBy smallint,"
                "manual_parking_line2LTx smallint,"
                "manual_parking_line2LTy smallint,"
                "manual_parking_line2RTx smallint,"
                "manual_parking_line2RTy smallint,"
                "manual_parking_line2LBx smallint,"
                "manual_parking_line2LBy smallint,"
                "manual_parking_line2RBx smallint,"
                "manual_parking_line2RBy smallint,"
                "manual_parking_line3LTx smallint,"
                "manual_parking_line3LTy smallint,"
                "manual_parking_line3RTx smallint,"
                "manual_parking_line3RTy smallint,"
                "manual_parking_line3LBx smallint,"
                "manual_parking_line3LBy smallint,"
                "manual_parking_line3RBx smallint,"
                "manual_parking_line3RBy smallint,"
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
                "Slot_count tinyint, "
                "InstallType tinyint, "
                "SlotBitmap tinyint, "
                "user_manual_parking_line tinyint, "
                "manual_parking_line1LTx smallint,"
                "manual_parking_line1LTy smallint,"
                "manual_parking_line1RTx smallint,"
                "manual_parking_line1RTy smallint,"
                "manual_parking_line1LBx smallint,"
                "manual_parking_line1LBy smallint,"
                "manual_parking_line1RBx smallint,"
                "manual_parking_line1RBy smallint,"
                "manual_parking_line2LTx smallint,"
                "manual_parking_line2LTy smallint,"
                "manual_parking_line2RTx smallint,"
                "manual_parking_line2RTy smallint,"
                "manual_parking_line2LBx smallint,"
                "manual_parking_line2LBy smallint,"
                "manual_parking_line2RBx smallint,"
                "manual_parking_line2RBy smallint,"
                "manual_parking_line3LTx smallint,"
                "manual_parking_line3LTy smallint,"
                "manual_parking_line3RTx smallint,"
                "manual_parking_line3RTy smallint,"
                "manual_parking_line3LBx smallint,"
                "manual_parking_line3LBy smallint,"
                "manual_parking_line3RBx smallint,"
                "manual_parking_line3RBy smallint,"
                "primary key(cameraID, cmosID)"
                ")engine=memory")
except:
    print "create table AiSettingTableMem fail"
    pass

try:
    cur.execute("create table if not exists ReSettingTable("
                "cameraID char(24), "
                "cmosID tinyint,"
                "ReNewFlag tinyint default 0,"
                "focalLength float,"
                "useMenualUndisPos int,"
                "LevelLineB1x int,"
                "LevelLineB1y int,"
                "LevelLineB2x int,"
                "LevelLineB2y int,"
                "LevelLineB3x int,"
                "LevelLineB3y int,"
                "LevelLineB4x int,"
                "LevelLineB4y int,"
                "LevelLineT1x int,"
                "LevelLineT1y int,"
                "LevelLineT2x int,"
                "LevelLineT2y int,"
                "VertiacalLine1x int,"
                "VertiacalLine1y int,"
                "VertiacalLine2x int,"
                "VertiacalLine2y int,"
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
                "focalLength float,"
                "useMenualUndisPos int,"
                "LevelLineB1x int,"
                "LevelLineB1y int,"
                "LevelLineB2x int,"
                "LevelLineB2y int,"
                "LevelLineB3x int,"
                "LevelLineB3y int,"
                "LevelLineB4x int,"
                "LevelLineB4y int,"
                "LevelLineT1x int,"
                "LevelLineT1y int,"
                "LevelLineT2x int,"
                "LevelLineT2y int,"
                "VertiacalLine1x int,"
                "VertiacalLine1y int,"
                "VertiacalLine2x int,"
                "VertiacalLine2y int,"
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
                "RenewTime int default 0)engine=memory")
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
    cur.execute("create table if not exists SpaceFilterBuffTable("
                "id int not null auto_increment primary key,"
                "Spaceid char(24),"
                "cameraID char(24), "
                "cmosID tinyint,"
                "CarPos tinyint,"
                "RenewTime int default 0)engine=memory")
except Exception, e:
    print  "create table SpaceFilterBuffTable fail " + str(e)
    pass


try:
    cur.execute("create table if not exists WatchdogTable("
                "pid int primary key,"
                "runCMD char(128),"     #with full path,such as"/home/bluecard/hvpd/prog/bin/123.sh"
                "watchSeconds int default 0, "     #interval seconds
                "renewTimet int default 0,"       #wdi timet, the program refresh
                "strategy int default 0,"   #0:rerun, 1:reboot
                "killDelaySeconds int default 10,"     #kill the program and delay seconds for rerun
                "killTimet int default 0,"            #kill timet
                "wdtStep int default 0"     #0:waiting for wdi,1:waiting fro rerun, after rerun the msg will be delete,a new pid will comming
                ")engine=memory")
except Exception, e:
    print  "create table WatchdogTable fail " + str(e)
    pass

try:
    cur.execute("create table if not exists YUVFilterBuffTable("
                "id int not null auto_increment primary key,"
                "Spaceid char(24),"
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





try:
    cur.execute("create table if not exists AiOutTable("
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
    print "create table AiOutTable "+str(e)
    pass
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
                ")values('1711430006',0, 1,0, 1, "
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
    pass

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
print time.time(), time.clock()