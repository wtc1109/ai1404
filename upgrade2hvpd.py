import os
import sys
import time

from bin import wtclib


def check_and_upgrad_hvpd(cur):
    try:
        (a1,) = cur.fetchmany(cur.execute("select count(*) from HvpdUpgradeTable where ReNewFlag=1"))[0]
        if 0 == a1:
            return
        _hvpds = cur.fetchmany(cur.execute("select * from HvpdUpgradeTable where ReNewFlag=1"))
        for _hvpd in _hvpds:
            if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'and cmosID=%d"%(_hvpd[0], _hvpd[1])):
                continue
            _camera = cur.fetchmany(1)[0]
            ret = wtclib.http_post_file2device("/home/bluecard/hvpd/firmwares/" + _hvpd[2], _camera[4], "upgrade.cgi")
            if None == ret:
                continue
            cur.execute("update HvpdUpgradeTable set ReNewFlag=0, end_time=now()")
            time.sleep(0.5)
    except:
        pass

if __name__ == '__main__':
    if not os.path.isdir("../log/upgradelog"):
        try:
            os.mkdir("../log/upgradelog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/upgradelog/upgrade.log")
    mylogger.info("start running")
    while True:
        (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None == cur:
            time.sleep(20)
        else:
            break

    _pid = os.getpid()
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 130, %d)" % (_pid, __file__, int(time.time())))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())

    _pid = os.getpid()
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 30, %d)" % (_pid, __file__, int(time.time())))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())

    while True:
        _timeSec = int(time.time())
        try:
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
        except Exception, e:
            mylogger.error(str(e))
            continue

        try:
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
        except Exception, e:
            mylogger.error(str(e))
            continue
        check_and_upgrad_hvpd(cur)
        time.sleep(30)
        mylogger.debug("running @ "+ time.asctime())

