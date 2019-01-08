import logging
from logging.handlers import RotatingFileHandler
import ConfigParser
import MySQLdb
import time,sys, socket, fcntl, struct
import urllib, urllib2, time, json, requests
import sqlite3

"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET"""
def create_logging(filename):
    Rthandler = RotatingFileHandler(filename, maxBytes=204800, backupCount=50)
    Rthandler.setLevel(logging.INFO)  #write files info
    formatter = logging.Formatter('%(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.basicConfig(level=logging.NOTSET, format="%(filename)s [Line=%(lineno)s] %(levelname)s %(message)s")       #write to stdio all
    logger = logging.getLogger(filename)
    logger.addHandler(Rthandler)
    return logger


def get_ip_addr1(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    return addr

def get_ip_addr2():
    #name1 = socket.gethostname()
    _info = socket.gethostbyname_ex(socket.gethostname())
    return _info

def get_user_config_ret_dict(file_in, sec_in):
    cf = ConfigParser.ConfigParser()
    cf.read(file_in)
    secs = cf.sections()
    val = 0
    if not sec_in in secs:
        return {}
    opts = cf.options(sec_in)
    dict_ret = {}
    for opti in opts:
        dict_ret.update({opti:cf.get(sec_in, opti)})
    return dict_ret

def set_user_config_from_dict(file_in, sec_in, dict_in):
    cf = ConfigParser.ConfigParser()
    cf.read(file_in)
    secs = cf.sections()
    val = 0
    if not sec_in in secs:
        cf.add_section(sec_in)
    for opti in dict_in:
        cf.set(sec_in, opti, dict_in[opti])
    try:
        cf.write(open(file_in, "w"))
    except Exception, e:
        return str(e)
    return 0


def get_a_sql_cur(conf_file,dbn="AlgReturndb2"):
    conf_dict = get_user_config_ret_dict(conf_file, "db")

    if "location" in conf_dict:
        DB_host = conf_dict["location"]
    else:
        DB_host = "localhost"
    if "user_name" in conf_dict:
        DB_user = conf_dict["user_name"]
    else:
        DB_user = "bluecardsoft"
    if "user_passwd" in conf_dict:
        DB_passwd = conf_dict["user_passwd"]
    else:
        DB_passwd = "#$%_BC13439677375"
    if "name" in conf_dict:
        DB_name = conf_dict["name"]
    else:
        DB_name = dbn

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
                cur.execute("create database %s"%DB_name)
                cur.execute("use %s"%DB_name)

            except Exception, e:
                print str(e) + " in line: " + str(sys._getframe().f_lineno) + '@' + __file__
                return None, str(e) + ' connect'
    cur.execute("use " + DB_name)
    return cur, conn

def get_ucmq_setup_info():
    conf_dict = get_user_config_ret_dict("../conf/conf.conf", "ucmq")

    if "server_addr" in conf_dict:
        addr = conf_dict["server_addr"]
    else:
        addr = get_ip_addr1("eth0")
    if "server_port" in conf_dict:
        portstr = conf_dict["server_port"]
    else:
        portstr = "8803"
    if "download_file_mq_name" in conf_dict:
        name = conf_dict["download_file_mq_name"]
    else:
        name = "downloadmq"
    return addr,portstr, name

def get_ucmq_url(mq_name):

    addr,portstr,name = get_ucmq_setup_info()
    if None == mq_name:
        mq_name = name
    test_data = {'name': mq_name, 'opt': 'get', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url


def get_ucmq_status_url(mq_name):
    addr, portstr,name = get_ucmq_setup_info()
    if None == mq_name:
        mq_name = name
    test_data = {'name': mq_name, 'opt': 'status_json', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url

def get_ucmq_reset_url(mq_name):
    addr, portstr,name = get_ucmq_setup_info()
    if None == mq_name:
        mq_name = name
    test_data = {'name': mq_name, 'opt': 'reset', 'ver': '2'}
    test_data_encode = urllib.urlencode(test_data)
    _ucmq_url = "http://"+ addr +":"+ portstr +"/?" + test_data_encode
    return 1, _ucmq_url

def http_get_cgi_msg2device(dict_msg, ip, cgi_name):

    requrl = "http://"+ ip + "/cgi-bin/" + cgi_name +".cgi"
    res_data = urllib2.Request(requrl, data=dict_msg)
    str_info = urllib.urlencode(dict_msg)
    try:
        resp = urllib.urlopen(res_data.get_full_url(), data=str_info)
        #res = resp.read()

        resp.close()
        #res1 = res.split("\r\n")
        if 200 == resp.code:
            return 1,"%d"%resp.code
        else:
            return 0,"%d"%resp.code
    except Exception, e:
        return 0, str(e)


def http_post_file2device(filename, ip, cgi_name):
    url = "http://" + ip+"/cgi-bin/"+cgi_name
    try:
        files = {"filename": ("123.zip", open(filename, "rb"))}
        r = requests.post(url=url, files=files, timeout=2)
        print r
        if 200 == r.status_code:
            return 200
        else:
            return 502
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)


def get_sqlite_cur(DBname):
    try:
        conn = sqlite3.connect(DBname)
        conn.isolation_level = None
        cur = conn.cursor()
    except:
        conn = sqlite3.connect()
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("create database %s"%DBname)
        cur.execute("use %s"%DBname)
    return cur, conn

def get_a_sqlite3_cur_forever(mylog, DBname):
    while True:
        (_cur, _conn) = get_sqlite_cur(DBname)
        if None != _cur:
            break
        else:
            mylog.info(_conn)
            time.sleep(20)
    return _cur, _conn


def make_serverID():
    fstab = open("/etc/fstab", 'r')
    uuid_i = int(time.time()) % 1000
    while True:
        fs_tab = fstab.readline()
        if '#' == fs_tab[0]:
            continue
        if 0 == len(fs_tab):
            break
        if fs_tab.find("UUID") >= 0:
            uuid_s = fs_tab.find('=')
            uuid_e = fs_tab.find('-')
            uuid_h = fs_tab[uuid_s + 1:uuid_e]
            try:
                uuid_i = int(uuid_h, 16)
                uuid_i %= 1000
                break
            except:
                continue
    fstab.close()
    local_t = time.localtime()
    _sid = "%02d%02d890%03d"%(local_t.tm_year-2000,local_t.tm_mon,uuid_i)
    return _sid

def get_serverID():
    _dict = get_user_config_ret_dict("../conf/id.conf", "system")
    if not "serverid" in _dict:
        serverID = make_serverID()
        _dict.update({"serverid":serverID})
        set_user_config_from_dict("../conf/id.conf", "system", _dict)
    else:
        serverID = _dict["serverid"]
    return serverID

