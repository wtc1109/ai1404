import ConfigParser
import json
import os
import sys
import time

import pika

import wtclib

if not os.path.isdir("../log/reret"):
    try:
        os.mkdir("../log/reret")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        os._exit()
mylogger = wtclib.create_logging("../log/reret/re2filter.log")
mylogger.info("start running")
while True:
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
    if None != cur:
        break
    else:
        mylogger.info("can not connect to db and sleep 20")
        time.sleep(20)
"""
cur.execute("insert into ReFilterTable(Spaceid, cameraID, cmosID)values('123456', '1315', 0)")
cur.execute("update ReFilterTable set PlateNumber1='wfbi' where Spaceid='123456'")
cur.execute("update ReFilterTable set PlateNumber1=NULL where Spaceid='123456'")
"""
"""
_pid = os.getpid()
try:
    cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                "'python %s &', 300, %d)"%(_pid, __file__, (time.time())))
except Exception, e:
    mylogger.error(str(e)+time.asctime())
"""


msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

pre_similar_table = ['0DQ','8BRH',
                     'S53','2Z',
                     'T71','PRF',
                     'PRF','6G',
                     '4A']

def match_same_process(cur, FilterSql, ReoutSql):
    cur.execute()

def match_process(src, dst):
    i = -1
    cnt = 0
    for cc in src:
        i += 1
        if cc == dst[i]:
            cnt += 1
            continue
        for list1 in pre_similar_table:
            if cc in list1 and dst[i] in list1:
                cnt += 1
                break
    return cnt


def same_match_filter(filterTable):
    return 1


def msg_consumer(channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        global cur, mylogger, channelOut, msg_props

        _timeSec = int(time.time())
        """
        global _pid
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
        """
        mylogger.debug("msg recv" + body)
        try:
            _dic_info = json.loads(body)
        except Exception, e:
            mylogger.warning(str(e))
            mylogger.warning("len = %d"%len(body))
            mylogger.warning("json.loads "+body)
            return
        if "quit" in _dic_info:
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()
            mylogger.debug("quit")
        mylogger.debug(body)
        if not "cam_id" in _dic_info:
            mylogger.info("not cam_id in _dic_info")
            return
        if not "plateGet" in _dic_info:
            mylogger.info("not plateGet in _dic_info")
            return

        if not "CMOS" in _dic_info:
            mylogger.info("not CMOS in _dic_info")
            return

        if not type(_dic_info["CMOS"])==int:
            mylogger.debug("not type CMOS is int")
            return
        if not type(_dic_info["plateGet"])==int:
            mylogger.debug("not type plateGet is int")
            return
        _cmos = _dic_info["CMOS"]
        if _cmos > 1:
            mylogger.error("CMOS=%d"%_cmos)
            return

        if 0 == _cmos :
            if(_dic_info["plateGet"] > 3 or _dic_info["plateGet"] < 1):
                mylogger.info("CMOS=%d and plate=%d"%(_cmos,_dic_info["plateGet"]))
                return
            else:
                _Reoffset = (_dic_info["plateGet"]-1)*4+2

        if 1 == _cmos :
            if(_dic_info["plateGet"] > 6 or _dic_info["plateGet"] < 4):
                mylogger.info("CMOS=%d and plate=%d"%(_cmos,_dic_info["plateGet"]))
                return
            else:
                _Reoffset = (_dic_info["plateGet"] - 4) * 4+2

        _sql_str = "select * from ReOutTable where cameraID='%s' and cmosID=%d"%(_dic_info["cam_id"], _cmos)
        if 0 == cur.execute(_sql_str):
            mylogger.debug("0="+_sql_str)
            return
        try:
            _re_out = cur.fetchmany(1)[0]
        except:
            mylogger.debug("read select * from ReOutTable = 0")
            return
        _hvpd = _dic_info["cam_id"]


        try:
            _spaceID = _dic_info["cam_id"]+str(_dic_info["plateGet"])
            if 0 == cur.execute("select * from ReFilterTable where Spaceid='%s'"%_spaceID):
                cur.execute("insert into ReFilterTable(Spaceid, cameraID, cmosID)values('%s', '%s', %d)"
                            %((_dic_info["cam_id"]+str(_dic_info["plateGet"])), _dic_info["cam_id"], _cmos))
            _ReFilterInfo = cur.fetchmany(cur.execute("select * from ReFilterTable where Spaceid='%s'"%_spaceID))[0]
            if None == _re_out[_Reoffset+1]:# no plate here
                _ret = 0
                for i in range(8):
                    if None == _ReFilterInfo[4+i*6] and 0 != _ReFilterInfo[3+i*6]:  #same with no plate
                        cur.execute("update ReFilterTable set sameCnt%d=%d,matchCnt%d=%d,sameTimet%d=%d,matchTimet%d=%d "
                                    "where Spaceid='%s'"%(i+1, _ReFilterInfo[5+i*6],i+1, _ReFilterInfo[6+i*6],
                                                          i+1, _timeSec,i+1, _timeSec, _spaceID))
                        _ret = 1    #found a no plate, so update
                        break
                if 0 == _ret:
                    for i in range(8):
                        if 0 == _ReFilterInfo[3+i*4]:#find a empty buffer
                            cur.execute("update ReFilterTable set inuse%d=1,PlateNumber%d=NULL, sameCnt%d=1,matchCnt%d=1,sameTimet%d=%d,matchTimet%d=%d "
                                        "where Spaceid='%s'"%(i+1, i+1,i+1,i+1, i+1, _timeSec, i+1,_timeSec,_spaceID))
                            _ret = 11
                            break
                    if 11 != _ret:#all is inuse
                        _matchtimet = []
                        for i in range(8):
                            _matchtimet.append(_ReFilterInfo[6*i+8])#delete the oldest match
                        _insert = _matchtimet.index(min(_matchtimet))
                        cur.execute("update ReFilterTable set PlateNumber%d=NULL, sameCnt%d=1,matchCnt%d=1,sameTimet%d=%d,matchTimet%d=%d "
                                    "where Spaceid='%s'" % (_insert+1, _insert+1, _insert+1, _insert+1, _timeSec,  _insert+1, _timeSec, _spaceID))
            else:
                match_same_process(cur, _ReFilterInfo, _re_out)
                _ret = 0
                for i in range(8):  #same and match
                    if 0 != _ReFilterInfo[6*i+3] and _re_out[_Reoffset+1] == _ReFilterInfo[6*i+4]:
                        cur.execute("update ReFilterTable set sameCnt%d=%d,sameTimet%d=%d,matchCnt%d=%d,matchTimet%d=%d "
                                    "where Spaceid='%s'" % (i+1, _ReFilterInfo[6*i+5], i+1, _timeSec, i+1, _ReFilterInfo[6*i+6], i+1, _timeSec,_spaceID))
                        _ret = 1
                        continue
                    if match_process(_re_out[_Reoffset+1], _ReFilterInfo[6*i+4])>3:
                        cur.execute("update ReFilterTable set matchCnt%d=%d,matchTimet%d=%d "
                                    "where Spaceid='%s'" % (i + 1, _ReFilterInfo[6 * i + 5], i + 1, _timeSec, _spaceID))
                        _ret = 1
                        continue
                if 0 == _ret:
                    _insert = 10
                    for i in range(8):
                        if 0 == _ReFilterInfo[6*i+3]:
                            _insert = i
                            break
                    if 10 != _insert:
                        cur.execute("update ReFilterTable set inuse%d=1, PlateNumber%d='%s', sameCnt%d=1, matchCnt%d=1,"
                                    "sameTimet%d=%d, matchTimet%d=%d where Spaceid='%s'"
                                    % (_insert + 1, _insert + 1,_re_out[_Reoffset+1], _insert + 1, _insert + 1, _insert + 1, _timeSec, _insert + 1,_timeSec, _spaceID))
                    else:
                        _matchtimet = []
                        for i in range(8):
                            _matchtimet.append(_ReFilterInfo[6 * i + 8])
                        _insert = _matchtimet.index(min(_matchtimet))
                        cur.execute("update ReFilterTable set inuse%d=1, PlateNumber%d='%s', sameCnt%d=1, matchCnt%d=1,"
                                    "sameTimet%d=%d, matchTimet%d=%d where Spaceid='%s'"
                                    % (
                                        _insert + 1, _insert + 1, _re_out[_Reoffset + 1], _insert + 1, _insert + 1, _insert + 1, _timeSec,
                                        _insert + 1, _timeSec, _spaceID))
            _ReFilterInfo = cur.fetchmany(cur.execute("select * from ReFilterTable where Spaceid='%s'"%_spaceID))[0]
            _insert = same_match_filter(_ReFilterInfo)

            if 0 == cur.execute("select * from ReOutFilterTable where cameraID='%s' and cmosID=%d"%(_dic_info["cam_id"], _cmos)):
                cur.execute("insert into ReOutFilterTable(cameraID, cmosID)values('%s',%d)"%(_dic_info["cam_id"], _cmos))
            cur.execute("update ReOutFilterTable")


            msg = json.dumps({"sn": _hvpd, "CMOS": _cmos})
            try:
                mylogger.debug("basic_publish:"+msg)
                channelOut.basic_publish(body=msg, exchange="ReOut.filter", properties=msg_props,routing_key="hola")
            except Exception, e:
                channel.basic_cancel(consumer_tag="hello-consumer2")
                channel.stop_consuming()
                mylogger.error("channelOut Error "+str(e))

        except:
            mylogger.error("end")
            pass
        return


if __name__ == '__main__':
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "reoutmq_server_addr" in conf_dict:
        _mq_host = conf_dict["reoutmq_server_addr"]
    else:
        _mq_host = wtclib.get_ip_addr1("eth0")
    if "reoutmq_server_port" in conf_dict:
        _mq_port = int(conf_dict["reoutmq_server_port"])
    else:
        _mq_port = 5672
    if "reoutmq_exchange" in conf_dict:
        _mq_exchange = conf_dict["reoutmq_exchange"]
    else:
        _mq_exchange = "ReOut.tr"
    if "reoutmq_user_name" in conf_dict:
        _mq_user_name = conf_dict["reoutmq_user_name"]
    else:
        _mq_user_name = "user1"
    if "reoutmq_passwd" in conf_dict:
        _mq_passwd = conf_dict["reoutmq_passwd"]
    else:
        _mq_passwd = "9876543"
    if "reoutmq_vhost" in conf_dict:
        _mq_vhost = conf_dict["reoutmq_vhost"]
    else:
        _mq_vhost = "OutTrig"

    while True:
        while True:
            try:
                credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
                conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials)
                conn_broker = pika.BlockingConnection(conn_params)

                break
            except Exception, e:
                mylogger.info(str(e))
                time.sleep(2)
        while True:
            try:
                channel = conn_broker.channel()
                # channel.exchange_declare(exchange="AiOut",exchange_type="fanout", passive=False, durable=False, auto_delete=True)
                channel.queue_declare(queue="refilter")
                channel.queue_bind(queue="refilter", exchange=_mq_exchange)
                break
            except Exception, e:
                mylogger.info(str(e))
                time.sleep(20)
        channelOut = conn_broker.channel()

        channelOut.exchange_declare(exchange="ReOut.filter", exchange_type="fanout",
                                    passive=False, durable=False, auto_delete=True)
        channel.basic_consume(msg_consumer, queue="refilter", consumer_tag="filter")

        try:
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))
            try:
                channelOut.close()
            except Exception, e:
                mylogger.error(str(e))
