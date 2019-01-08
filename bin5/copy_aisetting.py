import wtclib,time

if __name__ == '__main__':
    while True:
        cur1,err = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != cur1:
            break
        time.sleep(1)
    while True:
        cur2,err = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != cur2:
            break
        time.sleep(1)
    cur2.execute("select * from aisettingtable_camera")
    _cameras = cur2.fetchall()
    for _camera in _cameras:
        for i in range(_camera[2]):
            _sql_str = "insert into aisettingtable_bay(cameraID,bay,ctrlEquipment,set_time)values('%s',%d,'%s',now())"\
                       %(_camera[0], i+1, _camera[0])
            cur2.execute(_sql_str)
    cur1.execute("select * from aisettingtable")
    _settings = cur1.fetchall()
    for _set in _settings:
        slot_region = [_set[i] for i in range(7, 31)]
        _sql_str = "insert into aisettingtable_camera(cameraID,bays,InstallType,SlotBitmap,user_manual_parking_line," \
                   "manual_parking_line1LTx,manual_parking_line1LTy,manual_parking_line1RTx,manual_parking_line1RTy," \
                   "manual_parking_line1LBx,manual_parking_line1LBy,manual_parking_line1RBx,manual_parking_line1RBy," \
                   "manual_parking_line2LTx,manual_parking_line2LTy,manual_parking_line2RTx,manual_parking_line2RTy," \
                   "manual_parking_line2LBx,manual_parking_line2LBy,manual_parking_line2RBx,manual_parking_line2RBy," \
                   "manual_parking_line3LTx,manual_parking_line3LTy,manual_parking_line3RTx,manual_parking_line3RTy," \
                   "manual_parking_line3LBx,manual_parking_line3LBy,manual_parking_line3RBx,manual_parking_line3RBy,set_time)values(" \
                   "'%s',%d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d,NOW())"\
                   %(_set[0],_set[3],_set[4],_set[5],_set[6],
                     _set[7],_set[8],_set[9],_set[10],_set[11],_set[12],_set[13],_set[14],
                     _set[15], _set[16], _set[17], _set[18], _set[19], _set[20], _set[21], _set[22],
                     _set[23], _set[24], _set[25], _set[26], _set[27], _set[28], _set[29], _set[30],)
        cur2.execute(_sql_str)