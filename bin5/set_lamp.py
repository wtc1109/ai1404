import ConfigParser
import Queue
import json
import math
import os
import socket
import sys
import threading
import time
import urllib
import urllib2
import datetime
import MySQLdb
import pika
import wtclib
import random,shutil

"""receive ucmq messages and download the files to local
"""
DIRECTION_SAVE_FILES = "/tmp/waiting/"
#DIRECTION_SAVE_FILES = "../../waiting/"
THREAD_NUM = 10 #how many threads

gQueues = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)

def get_mysql_cur():
    global mylogger
    while True:
        (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != cur:
            break
        else:
            mylogger.info("can not connect to db and sleep 20")
            time.sleep(20)
    return cur


class setting_cgi_lamp(threading.Thread):
    def __init__(self, idnum):
        self.__id = idnum
        self.__timet = time.time()
        self.__downloadOKCnt = 0
        self.__downloadErrCnt = 0
        self.__logger = wtclib.create_logging('../log/airet/set_lamp%d.log' % idnum)
        threading.Thread.__init__(self)

    def run(self):
        global gQueues, gQueue_ret

        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            _timet_in = time.time()
            _recv_dict = json.loads(_recv_json)

            if time.time() - self.__timet > 30:
                self.__timet = time.time()
                self.__logger.info("sum=%d, ok=%d, err=%d in 30sec"
                                   % (self.__downloadOKCnt + self.__downloadErrCnt, self.__downloadOKCnt,
                                      self.__downloadErrCnt))
                self.__downloadOKCnt = 0
                self.__downloadErrCnt = 0


            step = 1
            _err = "OK"
            try:
                socket.setdefaulttimeout(1)
                _ret1, _err = wtclib.http_get_cgi_msg2device({"Lamp": _recv_dict['Lamp']}, ip=_recv_dict['ip'],
                                                            cgi_name="setting")
                step = _ret1
            except Exception, e:
                step = -1
                self.__logger.warning(str(e) +' '+ _recv_dict['sn'])
                _err = str(e)
            finally:
                if 1 == _ret1:
                    self.__downloadOKCnt += 1
                else:
                    self.__downloadErrCnt += 1
                _ret_dic = {"ret": step, "id": self.__id,'error':_err}

                _recv_dict.update(_ret_dic)
                gQueue_ret.put(json.dumps(_recv_dict))

                self.__logger.debug("child end  id=" + str(self.__id) + " time=" + str(time.time())+" use %f"%(time.time()-_timet_in))


if __name__ == '__main__':
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    #mylogger = create_logging("downfilelog/Mthread.log")
    mylogger = wtclib.create_logging("../log/airet/Mlamp.log")
    mylogger.info("start running")
    gThread_using_flag = []

    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = setting_cgi_lamp(i)
        thread.start()
    cur = get_mysql_cur()
    if None == cur:
        mylogger.error("config fail with db")
        os._exit()

    _timet_slow = time.time()
    while True:
        _sleep = 1.0
        Cur_qsize = gQueue_ret.qsize()
        rec_json_buff = []
        _timet_Sec = int(time.time())
        for i in range(Cur_qsize):
            try:
                rec_json = gQueue_ret.get(block=False)
                _dic = json.loads(rec_json)
                gThread_using_flag[_dic["id"]] = 1
                cur.execute(
                    "update lamp_change set LampRenewTimet=%d,working=0 where cameraID='%s'" % (_timet_Sec, _dic['sn']))
                if 1 == _dic['ret']:
                    cur.execute("update lamp_change set priority_new=0 where cameraID='%s'" % (_dic['sn']))
                    cur.execute("update lampsettingtablemem set LampStatus='%s', LampRenewTimet=%d "
                                "where equipmentID='%s'"%(_dic['Lamp'], _timet_Sec, _dic['equit']))
                    mylogger.info("%s Lamp now is %s" % (_dic['sn'], _dic['Lamp']))
                else:
                    cur.execute(
                        "update lamp_change set priority_new=%d where cameraID='%s'" % (_dic['priority']-1, _dic['sn']))
                    mylogger.info("%s %s Lamp thread%d set to %s fail %s" % (
                        _dic['sn'], _dic['ip'], _dic['id'], _dic['Lamp'], _dic['error']))
                    _sleep = 0.5
            except IOError, Queue.Empty:
                pass

        try:
            if 0 != cur.execute("select * from lamp_change where priority_new>3 and working=0 ORDER BY "
                                "priority_new DESC,LampRenewTimet ASC LIMIT %d"%THREAD_NUM):
                _cameras = cur.fetchall()
                for _camera in _cameras:
                    _dic = {"sn":_camera[2],'Lamp':_camera[4],'ip':_camera[5],'equit':_camera[6],'priority':_camera[7]}
                    _done = 1
                    for i in range(THREAD_NUM):
                        if 0 != gThread_using_flag[i]:
                            gQueues[i].put_nowait(json.dumps(_dic))
                            gThread_using_flag[i] = 0
                            _done = 0
                            break
                    if 0 != _done:
                        break
                if 0 != _done:
                    _sleep = 0.5
        except Exception,e:
            mylogger.error(str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_mysql_cur(mylogger)

        if time.time() - _timet_slow > 10:
            _timet_slow = time.time()
            try:
                if 0 != cur.execute("select * from lamp_change where priority_new>0 and LampRenewTimet < %d and "
                                    "working=0 ORDER BY priority_new DESC,LampRenewTimet ASC LIMIT %d"%(_timet_slow-60, THREAD_NUM)):

                    _cameras = sorted(cur.fetchall())
                    for _camera in _cameras:
                        _dic = {"sn": _camera[2], 'Lamp': _camera[4], 'ip': _camera[5],'equit':_camera[6],'priority':_camera[7]}
                        _done = 1
                        for i in range(THREAD_NUM):
                            if 0 != gThread_using_flag[i]:
                                gQueues[i].put_nowait(json.dumps(_dic))
                                gThread_using_flag[i] = 0
                                _done = 0
                                break
                        if 0 != _done:
                            break
            except Exception, e:
                mylogger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    cur = get_mysql_cur(mylogger)

        time.sleep(_sleep)