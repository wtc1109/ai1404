import ConfigParser
import os
import requests
import sys
import time
import urllib
import urllib2

import MySQLdb

from bin import wtclib

global mylogger

"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET
def create_logging(filename):
    Rthandler = RotatingFileHandler(filename, maxBytes=204800, backupCount=5)
    Rthandler.setLevel(logging.INFO)  #write files info
    formatter = logging.Formatter('%(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.basicConfig(level=logging.NOTSET)       #write to stdio all
    logger = logging.getLogger(filename)
    logger.addHandler(Rthandler)
    return logger"""

#CGI_DIC = {"upgrade":"upgrage.cgi", "setting":"setting"}
def connect_2_sql():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        mylogger.error(str(e))
        return None
    secs = cf.sections()
    try:
        opts = cf.options("db")
    except Exception, e:
        mylogger.error(str(e)+' db')
        return None
    try:
        _DB_host = cf.get("db", "location")
        _DB_user = cf.get("db", "user_name")
        _DB_passwd = cf.get("db", "user_passwd")
        _DB_name = cf.get("db", "name")
    except Exception, e:
        mylogger.error(str(e)+' get db')
        return None
    cnt = 5
    while True:
        try:
            conn = MySQLdb.connect(host=_DB_host, user=_DB_user, passwd=_DB_passwd, db=_DB_name)
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except:
            cnt -= 1
            if cnt < 0:
                mylogger.warning("can not connect to db")
                cnt = 50
            time.sleep(20)

    return cur
#def load_sql2mem():


def http_sendto_device(msg, sql_info, cgi_name):
    _ip = sql_info[1]
    mylogger.debug("http sendto :" +_ip)
    if None == _ip:
        return

    requrl = "http://"+ _ip + "/cgi-bin/" + cgi_name +".cgi"
    res_data = urllib2.Request(requrl, data=msg)
    str_info = urllib.urlencode(msg)
    try:
        resp = urllib.urlopen(res_data.get_full_url(), data=str_info)
        res = resp.read()
        #print res
        resp.close()
    except Exception, e:
        mylogger.warning(str(e)+' '+requrl)
        pass


def check_sqlMQ_LAMP_msg(cur):
    aa = cur.execute("select * from AIChangeMQ where info='LAMP'")
    allinfo = cur.fetchmany(aa)
    #print "get %d Lamp msgs"%aa
    for a1 in allinfo:
        sn = a1[1]
        ctrlTable = cur.fetchmany(cur.execute("select * from AiSettingTable where sn=" + sn))[0]

        if 0 != ctrlTable[13]:#manual
            http_sendto_device({"led":ctrlTable[15]}, ctrlTable, "setting")
        else:
            bitmap_sn = ctrlTable[9]
            if None == bitmap_sn:
                bitmap_sn = sn
            map_sn = bitmap_sn.split(':')
#            bitmap_strs = []
            space_bitmap = ''
            for map_sn1 in map_sn:
                strInfo = "select ai_out_space_bitmap from AIret_vals where sn=" + map_sn1
#                bitmap_strs.append(cur.fetchmany(cur.execute(strInfo)))

                space_bitmap1 = cur.fetchmany(cur.execute(strInfo))[0]
                #print "bitmap = ", space_bitmap1
                space_bitmap += space_bitmap1[0].lower()
                #print "bitmap lower = ",space_bitmap

            if 0 == ctrlTable[11] or None == ctrlTable[11]:
                LampCtrlSN_name = "defaultXspace"
            else:
                LampCtrlSN_name = ctrlTable[11]
            strInfo = "select output from " + LampCtrlSN_name + " where Flag_used='" + space_bitmap + "'"
            b1 = cur.execute(strInfo)
            mylogger.debug("select output from " +LampCtrlSN_name+str(b1)+ space_bitmap)
            if 0 != b1:
                msg = cur.fetchmany(b1)[0]
                http_sendto_device({"led":msg[0]}, ctrlTable, "setting")

        strInfo = "delete from AIChangeMQ where id=%d"%a1[0]
        cur.execute(strInfo)
        #when the MQ is used, delete it

def check_sql_rephoto_msg(cur):
    aa = cur.execute("select * from AIChangeMQ where info='REPHOTO'")
    allinfo = cur.fetchmany(aa)
    for a1 in allinfo:
        sn = a1[1]
        ctrlTable = cur.fetchmany(cur.execute("select * from AiSettingTable where sn=" + sn))[0]
        http_sendto_device({"rephoto":a1[4]}, ctrlTable, "setting")
        strInfo = "delete from AIChangeMQ where id=%d" % a1[0]
        cur.execute(strInfo)
        strInfo = "delete from AIChangeMQ where id=%d" % a1[0]
        cur.execute(strInfo)


def check_sql_parkingline_msg(cur):
    aa = cur.execute("select * from AIChangeMQ where info='PARKINGLINE'")
    allinfo = cur.fetchmany(aa)
    for a1 in allinfo:
        sn = a1[1]
        ctrlTable = cur.fetchmany(cur.execute("select * from AiSettingTable where sn=" + sn))[0]
        msg = {'parkingline1': a1[4], 'parkingline2': a1[5], 'parkingline3':a1[6]}
        http_sendto_device(msg, ctrlTable, "setting")
        strInfo = "delete from AIChangeMQ where id=%d" % a1[0]
        cur.execute(strInfo)


def http_download_file_device(filename, sql_info, cgi_name):
    _ip = sql_info[1]
    if None == _ip:
        return
    requrl = "http://" + _ip + "/cgi-bin/" + cgi_name + ".cgi"
#    url = "http://192.168.7.185/cgi-bin/update_app.cgi"
    try:
        files = {"file": ("123.zip", open(filename, "rb"))}
    except:
        mylogger.warning("open "+filename+" fail")
        return None
    try:
        r = requests.post(url=requrl, files=files)
    except Exception, e:
        mylogger.warning("post to "+requrl+ str(e))
        return None
    #print r.status_code
    return r.status_code

def check_sql_upgrade_msg(cur):
    aa = cur.execute("select * from AIChangeMQ where info='UPGRADE'")
    allinfo = cur.fetchmany(aa)
    for a1 in allinfo:
        sn = a1[1]
        ctrlTable = cur.fetchmany(cur.execute("select * from AiSettingTable where sn=" + sn))[0]
        filename = a1[4]
        ret = http_download_file_device(filename, ctrlTable, "upgrade")
        if 200 == ret:
            strInfo = "delete from AIChangeMQ where id=%d" % a1[0]
            cur.execute(strInfo)

if __name__ == '__main__':
    global mylogger
    if not os.path.isdir("../log/sqlmqlog"):
        try:
            os.mkdir("../log/sqlmqlog")
        except Exception, e:
            print e
            os._exit()
    mylogger = wtclib.create_logging("../log/sqlmqlog/checksql.log")
    mylogger.info("start running")
    cur = connect_2_sql()
    if None == cur:
        mylogger.error("can not get db")
        sys.exit()
    cnt = 100
    while True:
        #print time.clock()
        check_sqlMQ_LAMP_msg(cur)
        check_sql_rephoto_msg(cur)
        check_sql_parkingline_msg(cur)
        check_sql_upgrade_msg(cur)
        #print time.clock()
        time.sleep(0.5)
        cnt -= 1
        if cnt < 0:
            cnt = 2000
            mylogger.info("checksql is running")
        if 0 == cnt%200:
            mylogger.debug("checksql is running")
