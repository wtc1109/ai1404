import random
import json
import os
import sys
import time,datetime
import socket
import pika
import string
import wtclib

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur


def wdi(cur):
    global mylogger,ServerID
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(),ServerID))
    except Exception, e:
        mylogger.error(str(e))
        #Sqlite_cur, sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")

def msg_consumer(channel, method, header, body):
        global cur, mylogger, Lamp_interval, Lamp_max
        channel.basic_ack(delivery_tag=method.delivery_tag)
        _timesecFloat = time.time()
        _timeSec = int(_timesecFloat)
        #test = cur.execute("select * from ScreenConfigTable")
        wdi(cur)
        mylogger.info("msg recv:"+body)
        try:
            _dic_info = json.loads(body)
        except:
            mylogger.warning(body)
            mylogger.warning("len = "+len(body))
            return

        if "quit" in _dic_info:
            mylogger.warning("quit")
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()

        if not "sn" in _dic_info:
            mylogger.info("no sn section "+body)
            return

        if not "CMOS" in _dic_info:
            mylogger.error("no CMOS section")
            return
        elif not type(_dic_info["CMOS"])==int:
            mylogger.error("type('CMOS')=%s, %s"%(str(type(_dic_info["CMOS"])), str(_dic_info["CMOS"])))
            return

        _cmos = _dic_info["CMOS"]

        try:
            _sql_str = "select * from AiOutTable where cameraID='%s' and cmosID=%d" % (_dic_info["sn"], _cmos)
            a1 = cur.execute(_sql_str)
            if 0 == a1:
                mylogger.warning('0=' + _sql_str)
                return
            _ai_out = cur.fetchone()
        except Exception, e:
            mylogger.error(_sql_str+str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylogger)
            return


        _hvpd = _dic_info["sn"]
        _sql_str = "select * from hvpd2LampSettingTableMem where cameraID='%s' and cmosID=%d"%(_ai_out[0], _ai_out[1])
        try:
            a1 = cur.execute(_sql_str)
            if 0 == a1:
                mylogger.warning('0=' + _sql_str)
                return
            _effect = cur.fetchone()
        except Exception, e:
            mylogger.error(_sql_str+str(e))
            return

        try:
            if None == _effect[3]:
                mylogger.warning("hvpd2LampSettingTableMem Effect1EquipID is none")
                return
            for i in range(3,6):
                if 0 == _effect[i] or None == _effect[i]:
                    mylogger.debug("0 == _effect[%d]"%i)
                    continue

                try:
                    _sql_str = "select * from LampSettingTableMem where equipmentID='%s'" % _effect[i]
                    a1 = cur.execute(_sql_str)
                    if 0 == a1:
                        mylogger.info('0=' + _sql_str)
                        continue
                    _equipment = cur.fetchone()
                except Exception, e:
                    mylogger.error(_sql_str+str(e))
                    continue

                try:
                    _sql_str = "select * from Equipment2cameraIdMem where equipmentID='%s'" % _effect[i]
                    a1 = cur.execute(_sql_str)
                    if 0 == a1:
                        mylogger.info('0=' + _sql_str)
                        continue
                    _equipment2cameras = cur.fetchone()
                    if None == _equipment2cameras[4] and None == _equipment2cameras[2]:
                        mylogger.error("equip%s camera1 and camera2 is all Null" % _equipment2cameras[0])
                        continue
                except Exception, e:
                    mylogger.error(_sql_str+str(e))
                    continue


                _camera2Info = None
                if None != _equipment2cameras[4]:
                    try:
                        _sql_str = "select * from OnlineHvpdStatusTableMem where cameraID='%s' and " \
                                   "cmosID=%d"%(_equipment2cameras[4],_equipment2cameras[5])
                        a2 = cur.execute(_sql_str)
                        if 0 != a2:
                            _camera2Info = cur.fetchone()
                            if None == _camera2Info[4]:
                                _camera2Info = None
                    except Exception, e:
                        mylogger.warning(_sql_str)
                        mylogger.warning(str(e))
                        continue

                _camera1Info = None
                if None != _equipment2cameras[2]:
                    try:
                        _sql_str = "select * from OnlineHvpdStatusTableMem where cameraID='%s' and " \
                                   "cmosID=%d"%(_equipment2cameras[2],_equipment2cameras[3])
                        a2 = cur.execute(_sql_str)
                        if 0 != a2:
                            _camera1Info = cur.fetchone()
                            if None == _camera1Info[4]:
                                _camera1Info = None
                    except Exception, e:
                        mylogger.warning(_sql_str + str(e))
                        continue

                if None == _camera2Info and None == _camera1Info:
                    mylogger.warning("camera1 and camera2 online info all None")
                    continue

                _dict_msg = None
                if 55 == _equipment[10]:
                    _sql_str = "select * from LampUserCtlTable where equipmentID='%s'"%_equipment[i]
                    try:
                        a1 = cur.execute(_sql_str)
                        if 0 == a1:
                            mylogger.error('0=' + _sql_str)
                            continue
                    except Exception, e:
                        mylogger.error(_sql_str + str(e))
                        continue

                    _sql_str = "select userCtrl1Sn from LampUserCtlTable where equipmentID='%s'"%_equipment[i]
                    try:
                        a1 = cur.execute(_sql_str)
                        if 0 == a1:
                            mylogger.error('0=' + _sql_str)
                            continue
                    except Exception, e:
                        mylogger.error(_sql_str + str(e))
                        continue

                    try:
                        (_dict_msg,) = cur.fetchmany(1)[0]
                        if _dict_msg == _equipment2cameras[6] and _timeSec - _equipment2cameras[7] < Lamp_interval:
                            continue
                    except Exception, e:
                        mylogger.debug(_sql_str + str(e))

                else:

                    if _equipment[3] > 6 or _equipment[3] < 1:
                        mylogger.error("Equip %d space All=%d"%(_equipment[0],_equipment[3]))
                        continue
                    _space_str = ''
                    for j in range(_equipment[3]):
                        _sql_str = "select CarportStatus from SpaceStatusTable where Spaceid='%s'"%_equipment[4+j]
                        try:
                            a1 = cur.execute(_sql_str)
                            if 0 == a1:
                                mylogger.error('0=' + _sql_str)
                                break
                        except Exception, e:
                            mylogger.error(_sql_str + str(e))
                            break

                        try:
                            (_space_for,) = cur.fetchmany(1)[0]
                            if 0 == _space_for:
                                _space_str +='o'
                            else:
                                _space_str += 'x'
                        except Exception, e:
                            mylogger.error(_sql_str + str(e))
                            continue
                    mylogger.info("bays=%s"%_space_str)
                    try:
                        _sql_str = "select output from %s where Flag_used='%s'"%(_equipment[2], _space_str)
                        try:
                            a1 = cur.execute(_sql_str)
                        except Exception, e:
                            mylogger.warning(_sql_str)
                            _sql_str = "select output from defaultXspace where Flag_used='%s'"%(_space_str)
                            try:
                                a1 = cur.execute(_sql_str)
                            except Exception, e:
                                mylogger.error(str(e))
                                return
                        if 0 != a1:
                            try:
                                (_dict_msg,) = cur.fetchmany(1)[0]
                                mylogger.debug("Lamp:"+_dict_msg+"&"+_sql_str+" @%d"%_timeSec)

                                rgb1 = _dict_msg.split(',')
                                rgb2 = {}
                                for rg in rgb1:
                                    rg2 = rg.split(':')
                                    rgb2.update({rg2[0]: rg2[1]})
                                if 'R' in rgb2 and 'G' in rgb2 and 'B' in rgb2:
                                    _r = string.atoi(rgb2['R'])
                                    _g = string.atoi(rgb2['G'])
                                    _b = string.atoi(rgb2['B'])
                                    _sum = _r+_g +_b
                                    if _sum > Lamp_max:
                                        _dev = float(Lamp_max)/_sum
                                        _r = _r*_dev
                                        _g = _g * _dev
                                        _b = _b * _dev
                                        _dict_msg = 'R:%d,G:%d,B:%d'%(_r, _g,_b)
                                if _dict_msg == _equipment2cameras[6] and _timeSec > _equipment2cameras[7] and \
                                                        _timeSec - _equipment2cameras[7] < Lamp_interval:
                                    mylogger.info("%s lamp is %s in %d and now %d" % (
                                        _equipment2cameras[0],_dict_msg, _equipment2cameras[7], _timeSec))
                                    continue
                            except Exception, e:
                                mylogger.error(str(e))
                                return
                        else:
                            mylogger.info("0==cur.execute "+_sql_str)
                    except Exception, e:
                        mylogger.warning(_sql_str + " get " + str(e))
                if None == _dict_msg:
                    mylogger.error("%s lamp is None"%_effect[i])
                    continue

                mylogger.info('lamp should be %s, and now is %s'%(_dict_msg, _equipment2cameras[6]))
                try:
                    if _dict_msg != _equipment2cameras[6]:
                        if None != _camera1Info:
                            cur.execute("INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)"
                                        "VALUES('%s','%s','%s','%s',6)"
                                        "ON DUPLICATE KEY UPDATE LampStatus='%s', ip='%s',equipmentID='%s', priority_new=6"
                                        ""%(_camera1Info[0], _dict_msg, _camera1Info[4], _equipment2cameras[0],
                                            _dict_msg, _camera1Info[4], _equipment2cameras[0]))
                            mylogger.info("renew to %s"%_camera1Info[0])
                        if None != _camera2Info:
                            cur.execute(
                                "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)"
                                "VALUES('%s','%s','%s','%s',6)ON DUPLICATE KEY UPDATE "
                                "LampStatus='%s', ip='%s',equipmentID='%s',priority_new=6"
                                ""%(_camera2Info[0], _dict_msg, _camera2Info[4], _equipment2cameras[0],
                                    _dict_msg, _camera2Info[4], _equipment2cameras[0]))
                            mylogger.info("renew to %s"%_camera2Info[0])
                    else:
                        if None != _camera1Info:
                            cur.execute("INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)"
                                        "VALUES('%s','%s','%s','%s',3)ON DUPLICATE KEY UPDATE "
                                        "LampStatus='%s', ip='%s', equipmentID='%s',priority_new=3"
                                        ""%(_camera1Info[0], _dict_msg, _camera1Info[4], _equipment2cameras[0],
                                            _dict_msg, _camera1Info[4], _equipment2cameras[0]))
                            mylogger.info("update to %s" % _camera1Info[0])
                        if None != _camera2Info:
                            cur.execute(
                                "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)"
                                "VALUES('%s','%s','%s','%s',3)ON DUPLICATE KEY UPDATE "
                                "LampStatus='%s', ip='%s', equipmentID='%s',priority_new=3"
                                ""%(_camera2Info[0], _dict_msg, _camera2Info[4], _equipment2cameras[0],
                                    _dict_msg, _camera2Info[4], _equipment2cameras[0]))
                            mylogger.info("update to %s" % _camera2Info[0])
                except Exception,e:
                    mylogger.error(str(e))

        except Exception, e:
            mylogger.debug("try "+str(e))
            pass
        mylogger.debug("used time in %f second"%(time.time()-_timesecFloat))
        return




def get_rabbitmq_channel():
    global mylogger
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "aioutmq_server_addr" in conf_dict:
        _mq_host = conf_dict["aioutmq_server_addr"]
    else:
        _mq_host = wtclib.get_ip_addr1("eth0")
    if "aioutmq_server_port" in conf_dict:
        _mq_port = int(conf_dict["aioutmq_server_port"])
    else:
        _mq_port = 5672
    if "aioutmq_exchange" in conf_dict:
        _mq_exchange = conf_dict["aioutmq_exchange"]
    else:
        _mq_exchange = "AiOut.tr"
    if "aioutmq_user_name" in conf_dict:
        _mq_user_name = conf_dict["aioutmq_user_name"]
    else:
        _mq_user_name = "user1"
    if "aioutmq_passwd" in conf_dict:
        _mq_passwd = conf_dict["aioutmq_passwd"]
    else:
        _mq_passwd = "9876543"
    if "aioutmq_vhost" in conf_dict:
        _mq_vhost = conf_dict["aioutmq_vhost"]
    else:
        _mq_vhost = "OutTrig"

    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials)
            conn_broker = pika.BlockingConnection(conn_params)

            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)
    while True:
        try:
            channel = conn_broker.channel()
            # channel.exchange_declare(exchange="AiOut",exchange_type="fanout", passive=False, durable=False, auto_delete=True)
            channel.queue_declare(queue="hvpd_lamp")
            channel.queue_bind(queue="hvpd_lamp", exchange="AiOut.filter")
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)
    return channel

if __name__ == '__main__':
    #global mylogger
    #socket.setdefaulttimeout(10)
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/airet/ai2lamp.log")
    mylogger.info("start running")
    cur = get_a_sql_cur_forever(mylogger)
    #Sqlite_cur, sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 135, %d,'%s')" % (os.getpid(), __file__, time.time(), ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "ai2lamp" in _dic1:
            _version = _dic1["ai2lamp"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai2Lamp','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
        os._exit()
    socket.setdefaulttimeout(2)

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "aiplace")
    if "lamp_interval" in conf_dict:
        Lamp_interval = int(conf_dict["lamp_interval"])
        if Lamp_interval < 2 or Lamp_interval > 20:
            Lamp_interval = 4
    else:
        Lamp_interval = 4

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "users")
    if "lamp_max" in conf_dict:
        Lamp_max = int(conf_dict["lamp_max"])
        if Lamp_max < 2 or Lamp_max > 299:
            Lamp_max = 19
    else:
        Lamp_max = 19
    channel = get_rabbitmq_channel()

    while True:


        mylogger.info("waiting mq")
        channel.basic_consume(msg_consumer, queue="hvpd_lamp", consumer_tag="hvpd_lamp")
        try:
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))
            channel = get_rabbitmq_channel()