import os
import signal
import time
#import sqlite3
import psutil

import wtclib

if __name__ == '__main__':
    if not os.path.isdir("../log/wdt2"):
        try:
            os.mkdir("../log/wdt2")
        except Exception, e:
            print str(e)
            os._exit()
    mylog = wtclib.create_logging("../log/wdt2/wdt2.log")

    Sqlite_cur, sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylog, "/tmp/softdog.db")
    _AI_delay = 300
    _consumer_delay = 300
    _vlpr_delay = 300
    _bind_delay = 300
    while True:
        _timeSec = int(time.time())
        _AI_in_proc = 0
        _consumer_in_proc = 0
        _vlpr_in_proc = 0
        _bind_in_proc = 0
        _AI_in = 0
        _consumer_in = 0
        _vlpr_in = 0
        _bind_in = 0
        try:
            for proc in psutil.process_iter():
                if "AI" in proc.name():
                    _AI_in_proc = 1
                if "amqp_consumer" in proc.name() :
                    _consumer_in_proc = 1
                if "ai_vlpr" in proc.name():
                    _vlpr_in_proc = 1
                if "amqp_bind" in proc.name():
                    _bind_in_proc = 1

            _AI_in = Sqlite_cur.execute("select * from WatchdogTable where runCMD like './AI &'")

            if _AI_in > 1:
                try:
                    mylog.info("delete AI")
                    Sqlite_cur.execute("delete from WatchdogTable where pid=40015")
                except Exception,e:
                    mylog.info(str(e))
            elif 1 == _AI_in:
                if 0 != _AI_in_proc:
                    _AI_delay = 300
                    mylog.info("update AI")
                    Sqlite_cur.execute("update WatchdogTable set renewTimet=%d where pid=40015"%_timeSec)
                else:
                    mylog.info("No process AI")
            elif 0 == _AI_in:
                Sqlite_cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40015, "
                            "'./AI &', 180, %d)" % (_timeSec))
                mylog.info("insert AI")

            _consumer_in = Sqlite_cur.execute("select * from WatchdogTable where runCMD like './amqp_consumer%'")
            if _consumer_in > 1:
                try:
                    mylog.info("delete consumer")
                    Sqlite_cur.execute("delete from WatchdogTable where pid=40016")
                except Exception,e:
                    mylog.info(str(e))
            elif 1 == _consumer_in:
                if 0 != _consumer_in_proc:
                    _consumer_delay = 300
                    mylog.info("update consumer")
                    Sqlite_cur.execute("update WatchdogTable set renewTimet=%d where pid=40016" % _timeSec)
                else:
                    mylog.info("No process consumer")
            else:
                Sqlite_cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40016, "
                            "'./amqp_consumer &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (
                                _timeSec, _timeSec))
                mylog.info("insert consumer")

            _vlpr_in = Sqlite_cur.execute("select * from WatchdogTable where runCMD like './ai_vlpr%'")
            if _vlpr_in > 1:
                try:
                    mylog.info("delete vlpr")
                    Sqlite_cur.execute("delete from WatchdogTable where pid=40017")
                except Exception,e:
                    mylog.info(str(e))
            elif 1 == _vlpr_in:
                if 0 != _vlpr_in_proc:
                    _vlpr_delay = 300
                    mylog.info("update vlpr")
                    Sqlite_cur.execute("update WatchdogTable set renewTimet=%d where pid=40017" % _timeSec)
                else:
                    mylog.info("No process vlpr")
            else:
                Sqlite_cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40017, "
                            "'./ai_vlpr &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (_timeSec, _timeSec))
                mylog.info("insert vlpr")

            _bind_in = Sqlite_cur.execute("select * from WatchdogTable where runCMD like './amqp_bind%'")
            if _bind_in > 1:
                try:
                    mylog.info("delete bind")
                    Sqlite_cur.execute("delete from WatchdogTable where pid=40018")

                except Exception,e:
                    mylog.info(str(e))
            elif 1 == _bind_in:
                if 0 != _bind_in_proc:
                    _bind_delay = 300
                    mylog.info("update bind")
                    Sqlite_cur.execute("update WatchdogTable set renewTimet=%d where pid=40018" % _timeSec)
                else:
                    mylog.info("No process bind")
            else:
                Sqlite_cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40018, "
                            "'./amqp_bind &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (_timeSec, _timeSec))
                mylog.warning("insert bind")

        except Exception, e:
            mylog.error(str(e))
            os._exit()
        mylog.debug("alive @ "+time.asctime())
        time.sleep(30)
        _AI_delay -= 30
        _consumer_delay -= 30
        _vlpr_delay -= 30
        _bind_delay -= 30

