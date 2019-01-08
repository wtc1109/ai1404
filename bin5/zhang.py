import json
import os
import socket
import sys
import time
import urllib
import urllib2

import wtclib

if __name__ == '__main__':
    mylog = wtclib.create_logging("../log/zhang.log")
    (val, _ucmq_url) = wtclib.get_ucmq_url("zhang")
    if 0 == val:
        mylog.info("can not get a ucmq url"+_ucmq_url)
        os._exit()
    s = os.getcwd()
    mylog.info("zhang start")


    _top_top = s[:s[0:s.rfind('/')].rfind('/')] + "/zhang/"
    if not os.path.isdir(_top_top):
        os.mkdir(_top_top)

    fileCnt = 0
    socket.setdefaulttimeout(10)

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "ucmq")
    if "server_addr" in conf_dict:
        _ip = conf_dict["server_addr"]
    else:
        _ip = wtclib.get_ip_addr1("eth0")
    userjpgMQ_reset_url = "http://%s:8803/?opt=reset&ver=2&name=zhang"%_ip
    try:
        res_data = urllib2.urlopen(userjpgMQ_reset_url)
        res = res_data.read()
        res_data.close()
    except Exception, e:
        mylog.debug(str(e))

    _timeSecOld = int(time.time())
    _mkdir = 0
    oldtime = time.localtime(_timeSecOld)
    daystr = "%04d%02d%02d/" % (oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
    _top_day = _top_top + daystr
    if not os.path.isdir(_top_day):
        os.mkdir(_top_day)
    while True:
        _timeSec = int(time.time())

        oldtime = time.localtime()
        if 0 == oldtime.tm_hour :
            if 0 == _mkdir:
                _mkdir = 1
                daystr = "%04d%02d%02d/" % (oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
                _top_day = _top_top + daystr
                if not os.path.isdir(_top_day):
                    os.mkdir(_top_day)
        else:
            _mkdir = 0

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
            mylog.debug("@%d zhang msg:"%(time.time())+ret_str)
            continue

        mylog.debug("mq="+mq_str[1])
        try:
            _recv_dict = json.loads(mq_str[1])
        except:
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
        if not "pcl_result_01" in _recv_dict or not "pcl_result_02" in _recv_dict or not "pcl_result_03" in _recv_dict:
            continue


        _url_addr = "http://" + _recv_dict["ip"] + "/images/test.yuv"
        _file_name = _top_day + _recv_dict["sn"] + "/%d_%s_%s_%s.yuv"%(_timeSec,_recv_dict["pcl_result_01"]
                                                                          , _recv_dict["pcl_result_02"],_recv_dict["pcl_result_03"])

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
                mylog.info("download ok "+_file_name)



