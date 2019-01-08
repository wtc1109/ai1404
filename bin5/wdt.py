import os
import signal
import time
import sqlite3
import psutil

import wtclib

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur

if __name__ == '__main__':
    mylog = wtclib.create_logging("../log/wdt.log")
    mylog.info("start running")
    #print os.getcwd()
    #for proc in psutil.process_iter():
    #    print proc.name()
    """
    while True:
        (sqlite3_cur, err) = wtclib.get_sqlite_cur("/tmp/softdog.db")
        if None != sqlite3_cur:
            break
        else:
            mylog.info("can not connect to db and sleep 20")
            time.sleep(20)
    """
    cur = get_a_sql_cur_forever(mylog)
    """before running, remove very old program"""
    ServerID = wtclib.get_serverID()
    try:
        a1 = cur.execute("select * from WatchdogTable where ServerID='%s'"%ServerID)
        if 0 != a1:
            try:
                pids = cur.fetchall()
            except Exception, e:
                mylog.error(str(e))
                os._exit()

            try:
                pids1 = psutil.pids()
                for pid1 in pids:           #remove the program which is not running
                    if not pid1[0] in pids1:
                        cur.execute("delete from WatchdogTable where pid=%d and ServerID='%s'" % (pid1[0],ServerID))

            except Exception, e:
                mylog.error(str(e))
                os._exit()

    except Exception, e:
        mylog.error(str(e))
        os._exit()

    while True:
        try:
            a1 = cur.execute("select * from WatchdogTable where ServerID='%s'"%ServerID)
            if 0 == a1:
                time.sleep(20)
                mylog.debug("alive @ " + time.asctime())
                continue
        except Exception, e:
            mylog.error(str(e))
            if 1 != cur.connection.open:
                mylog.error("cur.connection.open = %d" % (cur.connection.open))
                cur = get_a_sql_cur_forever(mylog)
        try:
            pids = cur.fetchall()
        except Exception, e:
            mylog.error(str(e))
            os._exit()
        _timeSec = int(time.time())
        try:
            pids1 = psutil.pids()
            for pid1 in pids:
                """
                if not pid1[0] in pids1 and 1 != pid1[7]:
                    _sql = "delete from WatchdogTable where pid=%d" % pid1[0]
                    cur.execute(_sql)
                    continue
                    """
                if 0 == pid1[7]:#normal
                    if _timeSec > pid1[2] + pid1[3]: #time to delay after kill
                        try:
                            #p = psutil.Process(pid1[0])

                            if 0 == pid1[4]:#rerun
                                try:
                                    os.kill(pid1[0], signal.SIGKILL)
                                except Exception,e:
                                    mylog.warning("kill %d=%s"%(pid1[0],str(e)))
                                mylog.info("kill %d=%s"%(pid1[0], pid1[1]))
                                cur.execute("update WatchdogTable set killTimet=%d, wdtStep=1 where pid=%d and ServerID='%s'"%(_timeSec, pid1[0],ServerID))

                            elif 1 == pid1[4]:
                                os.system("reboot")

                        except Exception, e:
                            mylog.warning(str(e))
                            cur.execute("delete from WatchdogTable where pid=%d and ServerID='%s'" % (pid1[0],ServerID))
                elif 1 == pid1[7]:#after kill
                    if _timeSec > pid1[5] + pid1[6]:
                        if 0 == pid1[4]:#rerun
                            try:
                                _spl = pid1[1].split(' ')
                                if '&' == _spl[-1]:
                                    os.system(pid1[1])
                                    mylog.warning("rerun %s"%(pid1[1]))
                                cur.execute("delete from WatchdogTable where pid=%d and ServerID='%s'"%(pid1[0],ServerID))
                            except Exception, e:
                                mylog.warning(str(e))
                                cur.execute("delete from WatchdogTable where pid=%d and ServerID='%s'" % (pid1[0],ServerID))

        except Exception, e:
            mylog.error(str(e))
            os._exit()
        mylog.debug("alive @ "+time.asctime())
        time.sleep(5)