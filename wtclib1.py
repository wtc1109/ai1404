import logging
from logging.handlers import RotatingFileHandler
import ConfigParser
import MySQLdb
import time,sys
import urllib, urllib2, time, json, requests

"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET"""
def create_logging(filename):
    Rthandler = RotatingFileHandler(filename, maxBytes=204800, backupCount=5)
    Rthandler.setLevel(logging.INFO)  #write files info
    formatter = logging.Formatter('%(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.basicConfig(level=logging.NOTSET, format="%(filename)s [Line=%(lineno)s] %(levelname)s %(message)s")       #write to stdio all
    logger = logging.getLogger(filename)
    logger.addHandler(Rthandler)
    return logger

def get_a_sql_cur(conf_file):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(conf_file)
    except Exception, e:
        return None, str(e)+' db'
    secs = cf.sections()
    try:
        opts = cf.options("db")
    except Exception, e:
        return None, str(e)+' db'
    try:
        DB_host = cf.get("db", "location")
        DB_user = cf.get("db", "user_name")
        DB_passwd = cf.get("db", "user_passwd")
        DB_name = cf.get("db", "name")
    except Exception, e:
        return None, str(e)+' get db'
    while True:
        try:
            conn = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_passwd, db=DB_name)
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except Exception, e:
            try:
                conn = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_passwd)
                conn.autocommit(1)
                cur = conn.cursor()
                cur.execute("create database AlgReturndb2")
                cur.execute("use AlgReturndb2")
            except Exception, e:
                return None, str(e) + ' connect'
    cur.execute("use " + DB_name)
    return cur, "OK"

def get_ucmq_url(mq_name):

    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        return 0, str(e)
    secs = cf.sections()
    try:
        opts = cf.options("ucmq")
    except Exception, e:
        return 0, str(e)+' ucmq'

    try:
        addr = cf.get("ucmq", "server_addr")
        portstr = cf.get("ucmq", "server_port")
        if None == mq_name:
            name = cf.get("ucmq", "download_file_mq_name")
        else:
            name = mq_name
    except Exception, e:
        return 0, str(e)+' get ucmq'
    del cf
    test_data = {'name': name, 'opt': 'get', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url


def get_ucmq_status_url(mq_name):

    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        return 0, str(e)
    secs = cf.sections()
    try:
        opts = cf.options("ucmq")
    except Exception, e:
        return 0, str(e)+' ucmq'

    try:
        addr = cf.get("ucmq", "server_addr")
        portstr = cf.get("ucmq", "server_port")
        if None == mq_name:
            name = cf.get("ucmq", "download_file_mq_name")
        else:
            name = mq_name
    except Exception, e:
        return 0, str(e)+' get ucmq'
    del cf
    test_data = {'name': name, 'opt': 'status_json', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url

def get_ucmq_reset_url(mq_name):

    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        return 0, str(e)
    secs = cf.sections()
    try:
        opts = cf.options("ucmq")
    except Exception, e:
        return 0, str(e)+' ucmq'

    try:
        addr = cf.get("ucmq", "server_addr")
        portstr = cf.get("ucmq", "server_port")
        if None == mq_name:
            name = cf.get("ucmq", "download_file_mq_name")
        else:
            name = mq_name
    except Exception, e:
        return 0, str(e)+' get ucmq'
    del cf
    test_data = {'name': name, 'opt': 'reset', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url

def http_get_cgi_msg2device(dict_msg, ip, cgi_name):

    requrl = "http://"+ ip + "/cgi-bin/" + cgi_name +".cgi"
    res_data = urllib2.Request(requrl, data=dict_msg)
    str_info = urllib.urlencode(dict_msg)
    try:
        resp = urllib.urlopen(res_data.get_full_url(), data=str_info)
        res = resp.read()
        #print res
        resp.close()
    except Exception, e:
        return 0, str(e)
    return 1, "OK"

def http_post_file2device(filename, ip, cgi_name):
    url = "http://" + ip+"/cgi-bin/"+cgi_name
    files = {"filename": ("123.zip", open(filename, "rb"))}
    try:
        r = requests.post(url=url, files=files)
        print r
        if 200 == r.status_code:
            return 200
        else:
            return None
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
