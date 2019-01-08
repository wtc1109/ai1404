import json
import os
import socket
import sys
import time
import urllib
import urllib2

import wtclib

if __name__ == '__main__':
    mylog = wtclib.create_logging("../log/userjpg.log")
    (val, _ucmq_url) = wtclib.get_ucmq_url("userjpg")
    if 0 == val:
        mylog.info("can not get a ucmq url"+_ucmq_url)
        os._exit()
    s = os.getcwd()
    mylog.info("userjpg start")
    _top_top = s[:s[0:s.rfind('/')].rfind('/')]
    if not os.path.isdir("/tmp/userjpg"):
        os.mkdir("/tmp/userjpg")
    _top_top = "/tmp"

    socket.setdefaulttimeout(10)
    while True:
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
            mylog.debug("userjpg msg:"+ret_str)
            continue

        mylog.debug("mq="+mq_str[1])
        try:
            _recv_dict = json.loads(mq_str[1])
        except:
            continue

        if not "sn" in _recv_dict:
            mylog.debug("recv msg="+mq_str[1]+" no sn in")
            continue


        if not "CMOS" in _recv_dict or not type(_recv_dict["CMOS"])==int:
            _cmos = 0
        else:
            _cmos = _recv_dict["CMOS"]

        _url_addr = "http://" + _recv_dict["ip"] + "/images/user%d.jpg"%_cmos
        _file_name = _top_top + '/userjpg/' + _recv_dict["sn"] + "_%d.jpg"%_cmos
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




