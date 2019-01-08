import MySQLdb

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="AlgReturndb2")
    conn.autocommit(1)
    cur = conn.cursor()
except:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456")
    conn.autocommit(1)
    cur = conn.cursor()
    cur.execute("create database AlgReturndb2")
cur.execute("use AlgReturndb2")
try:
    cur.execute("create table AiSettingTable("
                "sn char(32) primary key, "             #0  A
                "ip char(32),"                          #1B
                "slave_flag int,"                       #2C
                "neighbor_sn char(32),"                 #3D
                "bluetooth_id char(16),"                #4E
                "user_set_space int, "                  #5F
                "installation_space int, "              #6G
                "valid_space_bitmap int, "              #7H
                "focal_length float,"                   #8I
                "LedCtrl_bitmap_sn char(64), "          #9J
                "LedCtrl_change_sn char(64), "          #10K
                "LedCtrl_Output_table char(64), "       #11L
                "LedCtrl_TwinkleQueue char(128), "      #12M
                "LedCtrl_Selected_auto_menu int, "                #13 N 0:AUTO, 1:menual
                "LedCtrl_Menual_Val_set char(32), "         #14 O
                "ParkingLine_auto_manual_flag int,"     #15 P
                "ParkingLine1_manual_setup char(64),"        #16 Q
                "ParkingLine2_manual_setup char(64),"        #17 R
                "ParkingLine3_manual_setup char(64),"        #18S
                "Menual_Set_ParkingLine_3confidence_coe char(8)"   #19 T
                ")")
except Exception, e:
    print "create table AiSettingTable",e
    pass
try:
    cur.execute("create table AiStatusTable("
                "sn char(32) primary key, "             #0
                "AutoLedStatus char(16),"                          #1
                "CurLedStatus char(16)"                       #2
       
   
                ")engine=memory")  #17
except Exception, e:
    print "create table AiStatusTable",e
    pass
try:
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag) values('123456788', 0, 3, 3, 7, 0, 0)")
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag) values('123456789', 0, 3, 3, 7, 0, 0)")
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag) values('123456790', 0, 3, 3, 7, 0, 0)")
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag, ParkingLine1_manual_setup, ParkingLine2_manual_setup,"
                "ParkingLine3_manual_setup"
                ") values('123456791', 0, 3, 3, 7, 0, 1, '10:10,30:10,10:80,30:80', '35:10,35:80,55:10,55:80',"
                "'60:10,60:80,80:10,80:80')")
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag, ParkingLine1_manual_setup, ParkingLine2_manual_setup,"
                "ParkingLine3_manual_setup"
                ") values('123456792', 0, 3, 3, 7, 0, 1,'10:10,30:10,10:80,30:80', '35:10,35:80,55:10,55:80',"
                "'60:10,60:80,80:10,80:80')")
    cur.execute("insert into AiSettingTable (sn, slave_flag, user_set_space, installation_space, valid_space_bitmap,"
                "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag, ParkingLine1_manual_setup, ParkingLine2_manual_setup,"
                "ParkingLine3_manual_setup"
                ") values('123456793', 0, 3, 3, 7, 0, 1,'10:10,30:10,10:80,30:80', '35:10,35:80,55:10,55:80',"
                "'60:10,60:80,80:10,80:80')")
except Exception, e:
    print("insert AiSettingTable error ",e)
    pass
aa = cur.execute("select * from AiSettingTable")
if 0 != aa:
    allinfo = cur.fetchmany(aa)
    for a1 in allinfo:

        sn = a1[0]
        update_info = "update AiSettingTable set LedCtrl_bitmap_sn = " + sn + " where sn = " + sn
        cur.execute(update_info)

try:
    cur.execute("create table AIret_vals("
                "sn char(32) primary key, "             #0A
                "latest_ctrl DATETIME,"                 #1B
                "ai_out_space int,"                     #2C
                "ai_out_space_bitmap char(8),"          #3D
                "ai_out_parkingline1_pos char(32),"     #4E
                "ai_out_parkingline2_pos char(32),"     #5F
                "ai_out_parkingline3_pos char(32),"     #6G
                "ai_out_Car1_pos char(32),"             #7H
                "ai_out_Car2_pos char(32),"             #8I
                "ai_out_Car3_pos char(32),"             #9J
                "ai_out_every_car_pos1 char(32),"         #10K
                "ai_out_every_car_pos2 char(32),"        #11L
                "ai_out_every_car_pos3 char(32),"        #12M
                "ai_out_3confidence_coe char(8),"       #13N
                "Pic_type_for char(16),"                #14 O
                "Pic_sn char(16),"                      #15     P
                "Pic_definition char(16),"              #16     Q
                "resent_Pic_path_name char(64),"             #17 R 
                "Cross_parking_alarm char(16),"         #18 S
                "Other_alarm char(16)"                 #19 T
                ")engine=memory")
except Exception, e:
    print "create table AIret_vals",e
    pass
for a1 in allinfo:
    sn = a1[0]
    update_info = "insert into AIret_vals (sn, ai_out_space_bitmap) values(" + sn + ", 'xox')"
    try:
        cur.execute(update_info)
    except Exception, e:
        print "insert into AIret_vals",e
        pass

try:
    cur.execute("create table AIChangeMQ("
                "id int not null auto_increment primary key,"
                "sn char(32),"
                "info char(32),"
                "user char(32),"
                "addition1 char(64),"
                "addition2 char(64),"
                "addition3 char(64),"
                "addition4 char(64),"
                "msg_time DATETIME" 
            
                ")engine=memory")
except Exception, e:
    print "create table AIChangeMQ", e
    pass
for a1 in allinfo:
    sn = a1[0]
    update_info = "insert into AIChangeMQ(sn, info, user, msg_time) values ('" + sn + "', 'LAMP', 'ai', now())"
    update_info2 = "insert into AIChangeMQ(sn, info, user, msg_time) values ('" + sn + "', 'REPHOTO', 'ai', now())"
    update_info3 = "insert into AIChangeMQ(sn, info, user, addition1, addition2, addition3,msg_time) " \
                   "values ('" + sn + "', 'PARKINGLINE', 'ai', '10:10,30:10,10:85,30:85', '35:10,35:80,55:10,55:85'," \
                                      "'60:10,60:85,85:10,85:85', now())"
    update_info4 = "insert into AIChangeMQ(sn, info, user, addition1, addition2, msg_time) values ('" + sn + \
                   "', 'PLACE', 'ai', '2', 'xox', now())"
    update_info5 = "insert into AIChangeMQ(sn, info, user, addition1, msg_time) values ('" + sn + \
                   "', 'UPGRADE', '/tmp/123.zip', 'xox', now())"
    try:
        cur.execute(update_info)
        cur.execute(update_info2)
        cur.execute(update_info3)
        cur.execute(update_info4)
        cur.execute(update_info5)
    except Exception, e:
        print "insert into AIChangeMQ", e
        pass