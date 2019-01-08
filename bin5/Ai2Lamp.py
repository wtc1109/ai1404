import ConfigParser
import json
import os
import sys
import time,datetime,threading
import socket
import pika
import string
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


def wdi(cur):
    global mylogger,ServerID
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(),ServerID))
    except Exception, e:
        mylogger.error(str(e))



def update_lamp(equipment, bays_status):
    global mylogger, Lamp_max
    try:
        _sql = "select * from lampsettingtablemem where equipmentID='%s'"%equipment
        if 0 == cur.execute(_sql):
            mylogger.warning('0='+_sql)
            return 0
        _lamp_setting = cur.fetchone()
        if 2 == _lamp_setting[2]:
            _sql = "select unused_bigger_color,else_color from %s where color_name='%s'"%(_lamp_setting[1],_lamp_setting[3])
            if 0 == cur.execute(_sql):
                mylogger.warning('0=' + _sql)
                return 0
            _colors = cur.fetchone()
            if bays_status.count(0) > _lamp_setting[4]:
                _lamp_colcor = _colors[0]
            else:
                _lamp_colcor = _colors[1]
        elif 1 == _lamp_setting[2]:
            if len(bays_status) > 7:
                mylogger.warning('bays_status=%s, len>7'%bays_status)
                return 0
            _space_str = ''
            for _space_for in bays_status:
                if 0 == _space_for:
                    _space_str += 'o'
                else:
                    _space_str += 'x'
            _sql = "select output from %s where Flag_used='%s'"%(_lamp_setting[1],_space_str)
            (_lamp_colcor,) = cur.fetchone()
        else:
            mylogger.warning("lamp_colcor not 1 and 2")
            return 0


        try:
            rgb1 = _lamp_colcor.split(',')
            rgb2 = {}
            for rg in rgb1:
                rg2 = rg.split(':')
                rgb2.update({rg2[0]: rg2[1]})
            if 'R' in rgb2 and 'G' in rgb2 and 'B' in rgb2:
                _r = string.atoi(rgb2['R'])
                _g = string.atoi(rgb2['G'])
                _b = string.atoi(rgb2['B'])
                _sum = _r + _g + _b
                if _sum > Lamp_max:
                    _dev = float(Lamp_max) / _sum
                    _r = _r * _dev
                    _g = _g * _dev
                    _b = _b * _dev
                    _dict_msg = 'R:%d,G:%d,B:%d' % (_r, _g, _b)
        except Exception, e:
            mylogger.error(str(e))
            return 0

        _timeSec = int(time.time())
        _sql = "select LampStatus,LampRenewTimet from lampsettingtablemem where equipmentID='%s'"%equipment
        cur.execute(_sql)
        (_lamp, _lamp_timet,) = cur.fetchone()
        if _lamp == _dict_msg and _timeSec - _lamp_timet < 20:
            return 1

        _sql = "select * from onlinehvpdstatustablemem where cameraID='%s'"%equipment
        if 0 == cur.execute(_sql):
            mylogger.warning('0=' + _sql)
            return 0
        _camera1Info = cur.fetchone()
        _camera2Info = None
        if len(_camera1Info[2]) > 9:
            _sql = "select * from onlinehvpdstatustablemem where cameraID='%s'" % _camera1Info[2]
            if 0 != cur.execute(_sql):
                _camera2Info = cur.fetchone()
        try:
            if None != _camera1Info:
                if _lamp != _dict_msg:
                    _sql = "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)" \
                           "VALUES('%s','%s','%s','%s',6)ON DUPLICATE KEY UPDATE LampStatus='%s', ip='%s'," \
                           "equipmentID='%s', priority_new=6"%(_camera1Info[0], _dict_msg, _camera1Info[4], equipment,
                                                               _dict_msg, _camera1Info[4], equipment)
                else:
                    _sql = "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)VALUES" \
                           "('%s','%s','%s','%s',3)ON DUPLICATE KEY UPDATE LampStatus='%s', ip='%s', equipmentID='%s'," \
                           "priority_new=3"%(_camera1Info[0],_dict_msg, _camera1Info[4], equipment, _dict_msg, _camera1Info[4],equipment)
                cur.execute(_sql)
            if None != _camera2Info:
                if _lamp != _dict_msg:
                    _sql = "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)" \
                           "VALUES('%s','%s','%s','%s',6)ON DUPLICATE KEY UPDATE LampStatus='%s', ip='%s'," \
                           "equipmentID='%s', priority_new=6" % (_camera2Info[0], _dict_msg, _camera2Info[4], equipment,
                                                                 _dict_msg, _camera2Info[4], equipment)
                else:
                    _sql = "INSERT INTO lamp_change(cameraID,LampStatus,ip,equipmentID,priority_new)VALUES" \
                           "('%s','%s','%s','%s',3)ON DUPLICATE KEY UPDATE LampStatus='%s', ip='%s', equipmentID='%s'," \
                           "priority_new=3" \
                           % (_camera2Info[0], _dict_msg, _camera2Info[4], equipment, _dict_msg, _camera2Info[4], equipment)
                cur.execute(_sql)

            return 1
        except Exception, e:
            mylogger.error(str(e))
            mylogger.error(_sql)
            return 0



    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(_sql)
    return  0


def msg_consumer(channel, method, header, body):
        global cur, mylogger, Lamp_interval, Lamp_max
        channel.basic_ack(delivery_tag=method.delivery_tag)
        _timesecFloat = time.time()
        _timeSec = int(_timesecFloat)
        #test = cur.execute("select * from ScreenConfigTable")
        wdi(cur)
        mylogger.debug("msg recv"+body)
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
            _sql_str = "select ctrlEquipment,ctrlEquipment2,ctrlEquipment3,ctrlEquipment4,ctrlEquipment5,ctrlEquipment6" \
                       " from aisettingtable_bay_mem where cameraID='%s' and cmosID=%d" % (_dic_info["sn"], _cmos)
            a1 = cur.execute(_sql_str)
            if 0 == a1:
                mylogger.warning('0=' + _sql_str)
                return
            _equipments_all1 = cur.fetchall()

            _equipments_all = []
            for _equip in _equipments_all1:
                for i in range(6):
                    if None == _equip[i]:
                        continue
                    _equipments_all.append(_equip[i])
            del _equipments_all1


            if 0 == len(_equipments_all):
                _sql_str = "select neighbor_camera from onlinehvpdstatustablemem where cameraID='%s'"%_dic_info["sn"]
                cur.execute(_sql_str)
                _neighbor, = cur.fetchone()
                if len(_neighbor) < 10:
                    _equipments_all.append(_dic_info["sn"])
                    mylogger.debug("append sn=%s"%_dic_info["sn"])
                    _sql_str = "update aisettingtable_bay_mem set ctrlEquipment='%s' where cameraID='%s'"%(_dic_info["sn"],_dic_info["sn"])
                else:
                    _equip = min(_dic_info["sn"], _neighbor)
                    _equipments_all.append(_equip)
                    _sql_str = "update aisettingtable_bay_mem set ctrlEquipment='%s'" % _equip
                    mylogger.debug("append min=%s"%_equip)
                cur.execute(_sql_str)
                mylogger.debug("_equipments_all is %s"%_equipments_all[0])


            _sql_str = "select bays from aisettingtable_camera_mem where cameraID='%s' and cmosID=%d" % (_dic_info["sn"], _cmos)
            if 0 == cur.execute(_sql_str):
                mylogger.warning('0=' + _sql_str)
                return
            (_bays,) = cur.fetchone()
            if None == _bays:
                mylogger.warning("bays = none")
                return
        except Exception, e:
            mylogger.error(_sql_str+str(e))
            if 1 != cur.connection.open:
                mylogger.error("cur.connection.open = %d" % (cur.connection.open))
                cur = get_a_sql_cur_forever(mylogger)
            return
        #if None == _equipments_all1:

        _equipments = set(_equipments_all)
        del _equipments_all
        _ret = 0

        mylogger.debug("_equipments length is %d" % (len(_equipments)))
        for _equip in _equipments:

            try:
                _bays_status = []

                _sql_str = "select cameraID,bay,CarportStatus from spacestatustable where (cameraID,bay) " \
                           "in (select cameraID,bay from aisettingtable_bay_mem where ctrlEquipment='%s')"%_equip
                if 0 != cur.execute(_sql_str):
                    _bayss = sorted(cur.fetchall())
                    for _bayss1 in _bayss:
                        _bays_status.append(_bayss1[2])
                for i in range(2,7):
                    _sql_str = "select cameraID,bay,CarportStatus from spacestatustable where (cameraID,bay) " \
                               "in (select cameraID,bay from aisettingtable_bay_mem where ctrlEquipment%d='%s')" % (i, _equip)
                    if 0 != cur.execute(_sql_str):
                        _bayss = sorted(cur.fetchall())
                        #print _bayss
                        for _bayss1 in _bayss:
                            _bays_status.append(_bayss1[2])

                if 0 == len(_bays_status):
                    mylogger.warning('0=' + _sql_str)
                    continue
                mylogger.debug("bay status is %s with %s"%(_bays_status, _equip))
                _ret += update_lamp(_equip, _bays_status)
            except Exception,e:
                mylogger.error(str(e))
                mylogger.warning(_sql_str)
        if 0 != _ret:
            try:
                cur.execute("update spacestatustable set Lamp_changeTime=%d where cameraID='%s' and cmosID=%d"
                            % (_timeSec,_dic_info["sn"], _cmos))
            except Exception, e:
                mylogger.error(str(e))
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
    #sqlite3_cur, sqlite3_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 135, %d,'%s')" % (os.getpid(), __file__, time.time(),ServerID))
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