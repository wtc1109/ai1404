import os
import signal
import time
#import sqlite3
import psutil

import wtclib

if __name__ == '__main__':
    mylog = wtclib.create_logging("../log/wdt2.log")
    #print os.getcwd()
    #for proc in psutil.process_iter():
    #    print proc.name()
    while True:
        (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != cur:
            break
        else:
            mylog.info("can not connect to db and sleep 20")
            time.sleep(20)

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

            cur.execute("select * from WatchdogTable")
            _watchdogs = cur.fetchall()
            for proc in _watchdogs:
                if "AI" in proc[1]:
                    _AI_in += 1
                if "amqp_consumer" in proc[1]:
                    _consumer_in += 1
                if "ai_vlpr" in proc[1]:
                    _vlpr_in += 1
                if "amqp_bind" in proc[1]:
                    _bind_in += 1
            if _AI_in > 1:
                try:
                    cur.execute("delete from WatchdogTable where pid=40015")
                except Exception,e:
                    mylog.info(str(e))
            elif 1 == _AI_in:
                _AI_delay = 300
                mylog.info("update AI")
            elif 0 == _AI_in:
                cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40015, "
                            "'./AI &', 180, %d)" % (_timeSec))



                if 0 == _consumer_in and "amqp_consumer" in proc.name() :

                    cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40016, "
                                "'./amqp_consumer &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (
                                _timeSec, _timeSec))
                    _consumer_delay = 300
                    mylog.info("update consumer")

                if 0 == _vlpr_in and "ai_vlpr" in proc.name():
                    cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40017, "
                                "'./ai_vlpr &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (_timeSec, _timeSec))
                    _vlpr_delay = 300
                    mylog.info("update vlpr")

                if 0 == _bind_in and "amqp_bind" in proc.name():
                    cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40018, "
                                "'./amqp_bind &', 180, %d)ON DUPLICATE KEY UPDATE renewTimet=%d" % (_timeSec, _timeSec))
                    _bind_delay = 300
                    mylog.info("update bind")

        except Exception, e:
            mylog.error(str(e))
            os._exit()
        mylog.debug("alive @ "+time.asctime())
        time.sleep(30)
        _AI_delay -= 30
        _consumer_delay -= 30
        _vlpr_delay -= 30
        _bind_delay -= 30
        _timeSec = int(time.time())
        try:
            if 0 == _AI_in and _AI_delay < 0:
                cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40015, "
                            "'./AI &', 180, %d)" % _timeSec)
                #os.system("./AI &")
                mylog.warning("rerun AI")
                _AI_delay = 300

            if 0 == _consumer_in and _consumer_delay < 0:
                cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40016, "
                            "'./amqp_consumer &', 180, %d)" % _timeSec)
                #os.system("./amqp_consumer &")
                mylog.warning("rerun amqp_consumer")
                _consumer_delay = 300

            if 0 == _vlpr_in and _vlpr_delay < 0:
                cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40017, "
                            "'./ai_vlpr &', 180, %d)" % _timeSec)
                #os.system("./ai_vlpr &")
                mylog.warning("rerun ai_vlpr")
                _vlpr_delay = 300

            if 0 == _bind_in and _bind_delay < 0:
                cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(40018, "
                            "'./amqp_bind &', 180, %d)" % _timeSec)
                #os.system("./amqp_bind &")
                mylog.warning("rerun amqp_bind")
                _bind_delay = 300

        except Exception,e:
            mylog.error(str(e))
            mylog.error("ai=%d,consumer=%d,vlpr=%d,bind=%d"%(_AI_delay,_consumer_delay,_vlpr_delay,_bind_delay))
