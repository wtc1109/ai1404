import wtclib
import time, random

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
    mylogger = wtclib.create_logging("../log/vm_rf.log")
    cur = get_a_sql_cur_forever(mylogger)
    _timesec = time.time()
    _cameras = {}
    _bays = {}
    for i in range(1,1000):
        _offset = random.randint(10,20)
        _cameras.update({'%d'%(1809435000+i):_timesec+_offset})
        for j in range(1,4):
            _bays.update({'%d%d' % (1809435000 + i, j): 0})
    while True:
        try:
            _timesec = time.time()
            for i in range(1, 1000):
                if _cameras['%d'%(1809435000+i)] < _timesec:
                    _offset = random.randint(100, 200)
                    _cameras.update({'%d' % (1809435000 + i): _timesec + _offset})
                    _sql_str = "update onlinehvpdstatustablemem set LatestConnect=now() where cameraID='%d'"%(1809435000 + i)
                    cur.execute(_sql_str)
            for i in range(13):
                _offset = random.randint(1, 999)
                _bay = random.randint(1,3)
                if 0 == _bays['%d%d' % (1809435000 + _offset, _bay)]:
                    _sql_str = "update spacestatustable set CarportStatus=1,parkin_time=now(),parkin_timet=%d" \
                               " where Spaceid='%d%d'"%(_timesec,1809435000 + _offset,_bay)
                    _bays['%d%d' % (1809435000 + _offset, _bay)] = 1
                else:
                    _sql_str = "update spacestatustable set CarportStatus=0,parkout_time=now(),parkout_timet=%d" \
                               " where Spaceid='%d%d'" % (_timesec,1809435000 + _offset, _bay)
                    _bays['%d%d' % (1809435000 + _offset, _bay)] = 0
                cur.execute(_sql_str)
            time.sleep(1)
        except Exception,e:
            print e