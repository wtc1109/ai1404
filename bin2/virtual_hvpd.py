import wtclib
import time

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur

if __name__ == '__main__':
    mylogger = wtclib.create_logging("../log/vm.log")
    cur = get_a_sql_cur_forever(mylogger)
    try:

        _sql_str = "select * from aisettingtable where cameraID='1804430019' "
        cur.execute(_sql_str)
        _src = cur.fetchone()

        for i in range(1,1000):
            _sql_str = "insert into aisettingtable(cameraID,cmosID,InstallType,SlotBitmap,user_manual_parking_line," \
                       "manual_parking_line1LTx,manual_parking_line1LTy,manual_parking_line1RTx,manual_parking_line1RTy," \
                       "manual_parking_line1LBx,manual_parking_line1LBy,manual_parking_line1RBx,manual_parking_line1RBy," \
                       "manual_parking_line2LTx,manual_parking_line2LTy,manual_parking_line2RTx,manual_parking_line2RTy," \
                       "manual_parking_line2LBx,manual_parking_line2LBy,manual_parking_line2RBx,manual_parking_line2RBy," \
                       "manual_parking_line3LTx,manual_parking_line3LTy,manual_parking_line3RTx,manual_parking_line3RTy," \
                       "manual_parking_line3LBx,manual_parking_line3LBy,manual_parking_line3RBx,manual_parking_line3RBy" \
                       ")values('%d',0,0,0,1,%d,%d,%d,%d,%d,%d,%d,%d,  %d,%d,%d,%d,%d,%d,%d,%d,  %d,%d,%d,%d,%d,%d,%d,%d)" \
                       "ON DUPLICATE KEY UPDATE ReNewFlag=0"\
                       %(1809435000+i,_src[7],_src[8],_src[9],_src[10],_src[11],_src[12],_src[13],_src[14]
                         , _src[15], _src[16], _src[17], _src[18],_src[19],_src[20],_src[21],_src[22]
                         , _src[23], _src[24], _src[25], _src[26],_src[27],_src[28],_src[29],_src[30])
            cur.execute(_sql_str)
            _sql_str = "insert into onlinehvpdstatustablemem(cameraID,cmosID,ip)values('%d',0,'192.168.101.203')" \
                       "ON DUPLICATE KEY UPDATE ip='192.168.101.203'"%(1809435000+i)
            cur.execute(_sql_str)
            _sql_str = "insert into aiouttable(cameraID,cmosID,CarCount,parking1State,parking2State,parking3State," \
                       "parking1IsCrossLine,parking2IsCrossLine,parking3IsCrossLine)values('%d',0,3,0,0,0, 0,0,0)" \
                       "ON DUPLICATE KEY UPDATE LatestUpdate=now()"%(1809435000+i)
            cur.execute(_sql_str)
            _sql_str = "insert into reoutfiltertable(cameraID,cmosID,Plate1Number,Plate2Number,Plate3Number)values" \
                       "('%d',0,'ef1233','ab98766','pptt9995')" \
                       "ON DUPLICATE KEY UPDATE cmosID=0" % (1809435000 + i)
            cur.execute(_sql_str)
            for j in range(1,4):
                _sql_str = "insert into spacestatustable(Spaceid,cameraID,cmosID,CarportStatus)values('%d%d','%d',0,0)" \
                           "ON DUPLICATE KEY UPDATE cmosID=0"%(1809435000+i,j, 1809435000+i)
                cur.execute(_sql_str)

    except Exception,e:
        print e