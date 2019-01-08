import json
import os
import socket
import sys
import time
import urllib
import urllib2

import wtclib

if __name__ == '__main__':
    mylog = wtclib.create_logging("../log/h264.log")
    (val, _ucmq_url) = wtclib.get_ucmq_url("h264mq")
    if 0 == val:
        mylog.info("can not get a ucmq url"+_ucmq_url)
        os._exit()
    s = os.getcwd()
    mylog.info("H264 start")


    _top_top = s[:s[0:s.rfind('/')].rfind('/')] + "/video/"
    if not os.path.isdir(_top_top):
        os.mkdir(_top_top)

    fileCnt = 0
    socket.setdefaulttimeout(10)
    _timeSecOld = int(time.time())-7200
    while True:
        _timeSec = int(time.time())
        _gmtime = time.localtime(_timeSec)
        if _timeSec - _timeSecOld > 3600:
            _timeSecOld = _timeSec
            oldtime = time.localtime()
            daystr = "%04d%02d%02d/" % (oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
            _top_day = _top_top + daystr
            if not os.path.isdir(_top_day):
                os.mkdir(_top_day)


        try:
            res_data = urllib2.urlopen(_ucmq_url)
            res = res_data.read()
            res_data.close()
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylog.info(str(e))
            time.sleep(20)

            continue

        mq_str = res.split('\n')
        # print mq_str[0]
        ret_str = mq_str[0].rstrip('\r')
        if (ret_str != "UCMQ_HTTP_OK"):
            time.sleep(1)
            mylog.debug("H264mq msg:"+ret_str)
            continue

        mylog.debug("mq="+mq_str[1])
        try:
            _recv_dict = json.loads(mq_str[1])
        except:
            continue

        if not "location" in _recv_dict:
            continue
        if not "ip" in _recv_dict:
            continue

        if not "sn" in _recv_dict:
            mylog.debug("recv msg="+mq_str[1]+" no sn in")
            continue
        if not os.path.isdir(_top_day+_recv_dict["sn"]):
            os.mkdir(_top_day+_recv_dict["sn"])

        if not "CMOS" in _recv_dict or not type(_recv_dict["CMOS"])==int:
            _cmos = 0
        else:
            _cmos = _recv_dict["CMOS"]

        _url_addr = "http://" + _recv_dict["ip"] + _recv_dict["location"]
        _file_name = _top_day + _recv_dict["sn"] + "/%d_%02d%02d%02d.h264"%(_cmos,_gmtime.tm_hour,_gmtime.tm_min,_gmtime.tm_sec)

        step = 1
        try:
            fd, info = urllib.urlretrieve(url=_url_addr, filename=_file_name)
        except Exception, e:
            step = -1
            mylog.warning(str(e) + _url_addr)
        urllib.urlcleanup()
        if step > 0:
            if not "content-length" in info.dict: # if length is 0,so remove the empty file
                os.remove(_file_name)
                mylog.warning("no content-length, download " + _file_name + " failed from "+_url_addr)
            else:
                mylog.debug("download ok "+_file_name)



