import urllib, urllib2, time, json
import os
import pika
import MySQLdb

"""receive ucmq messages and download the files to local
"""
DIRECTION_SAVE_FILES = os.environ['HOME'] + "/hvcd/"

def Download_file(jstr):
    _dic1 = json.loads(jstr)
    _url = "http://" + _dic1["ip"] + _dic1["location"]
    _file_name = DIRECTION_SAVE_FILES + _dic1["sn"]
    if not os.path.isdir(_file_name):
        try:
            os.mkdir(_file_name)
        except Exception, e:
            print "mkdir"+_filename+str(e)
            if not os.path.isdir(_file_name):
                return

    _localtime1 = time.localtime()
    days = "%s%s" % (str(_localtime1.tm_mon).zfill(2), str(_localtime1.tm_mday).zfill(2))
    _file_name += '/' + days
    if not os.path.isdir(_file_name):
        try:
            os.mkdir(_file_name)
        except Exception, e:
            print "mkdir" + _filename + str(e)
            if not os.path.isdir(_file_name):
                return

    _file_name += '/' + _dic1["pic_sn"] + ".jpg"
    print _file_name
    print _url
#    _url = "http://192.168.7.185/info/hub.c"
    try:
        fd, info = urllib.urlretrieve(_url, _file_name)
    except Exception, e:
        print e
        return
    try:
        length = info.dict["content-length"]
        print info.dict["content-length"]
        return _file_name
    except KeyError, IOError:
        os.remove(_file_name)
        return None

test_data = {'name': 'testmq', 'opt':'get', 'ver':'2'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.19:8803/"

def ucmq_get_msg():
    while True:
        while True:
            try:
                res_data = urllib2.urlopen(requrl + '?' + test_data_encode)
                break
            except urllib2.URLError, e:
                print e
                time.sleep(20)
                continue
        res = res_data.read()
        mq_str = res.split('\n')
        print mq_str[0]
        ret_str = mq_str[0].rstrip('\r')
        if (ret_str == "UCMQ_HTTP_OK"):
            break
        else:
            time.sleep(1)
        res_data.close()
    urllib.urlcleanup()
    return mq_str[1]


def get_a_rabbitmq_channel():
    credentials = pika.PlainCredentials("guest", "guest")
    conn_params = pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    # conn_params = pika.ConnectionParameters(host= "192.168.7.19",port=5672, credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    channel.exchange_declare(exchange="amq", exchange_type="direct",
                             passive=False, durable=True, auto_delete=False)
    return channel


def get_a_sql_cur():
    while True:
        try:
            conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="AlgReturndb2")
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except:
            time.sleep(20)

    return cur

def maybe_add_a_new_device(json_str, cur):
    _dic1 = json.loads(json_str)
    try:
        _ip = _dic1["ip"]
    except:
        return
    try:
        _slave_flag = _dic1["slave"]
    except:
        return

    try:
        _neighbor = _dic1["neighbor"]
    except:
        _neighbor = ''
        pass
    try:
        _bluetooch = _dic1["bluetooch_id"]
    except:
        _bluetooch = ''
        pass
    a1 = cur.execute("select * from AiSettingTable where sn='"+_dic1["sn"]+"'")
    if 0 == a1:
        str_info = "insert into AiSettingTable (sn, ip, slave_flag, neighbor_sn, bluetooth_id, user_set_space," \
                   "installation_space, valid_space_bitmap, LedCtrl_bitmap_sn, " \
                   "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag, ParkingLine1_manual_setup," \
                   "ParkingLine2_manual_setup, ParkingLine3_manual_setup) values" \
                   "('%s', '%s', %d, '%s', '%s', 3, 3, 7, '%s'" % (_dic1["sn"], _ip, _slave_flag, _neighbor, _bluetooch, _dic1["sn"]) \
                   + ", 0, 1, '16:21,38:21,3:88,33:88', '38:21,61:22,33:88,66:88', '61:22,83:23,66:88,95:89')"
        cur.execute(str_info)
    else:
        a1info = cur.fetchmany(a1)
        if (_ip != a1info[0][1]) or (_slave_flag != a1info[0][2]):
            str_info = "update AiSettingTable set ip='%s', slave_flag=%d"%(_ip, _slave_flag)
            if '' != _neighbor:
                str_info += ", neighbor_sn='%s'"%_neighbor
            if '' != _bluetooch:
                str_info += ", bluetooth_id='%s'"%_bluetooch
            str_info += " where sn='%s'"%_dic1["sn"]
            cur.execute(str_info)

    a1 = cur.execute("select * from AiSettingTable where sn='" + _dic1["sn"] + "'")
    return cur.fetchmany(a1)[0]


def make_rabbitmq_msg(json_str, filename, sql):
    _dic = json.loads(json_str)
    try:
        why = _dic["why"]
        info = {"cam_id":_dic["sn"],"pic_full_name":filename,
                "slot_count":sql[5], "is_manual":sql[13],
                "slot_region1":sql[16],"slot_region2":sql[17],
                "slot_region3": sql[18],
                "slot_install":sql[6],
                "slot_bitmap":sql[7], "Pic_type_for":_dic["why"]}
    except:
        info = {"cam_id": _dic["sn"], "pic_full_name": filename,
                "slot_count": sql[5], "is_manual": sql[13],
                "slot_region1": sql[16], "slot_region2": sql[17],
                "slot_region3": sql[18],
                "slot_install": sql[6],
                "slot_bitmap": sql[7]}

    return info

if __name__ == '__main__':

    if not os.path.isdir(DIRECTION_SAVE_FILES):
        try:
            os.mkdir(DIRECTION_SAVE_FILES)
        except Exception, e:
            print e
    channel = get_a_rabbitmq_channel()
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    j = 1000

    cur = get_a_sql_cur()
    sec_start = time.time()
    print time.time()
    while j > 0:
        json_str = ucmq_get_msg()
        try:
            _dic = json.loads(json_str)
        except:
            continue
        try:
            _sn = _dic["sn"]
        except:
            continue
        try:
            _pic_type = _dic["type_for"]
        except:
            continue
        sql_info = maybe_add_a_new_device(json_str, cur)
        _filename = Download_file(json_str)

        if None == _filename:
            print "download file none"
            continue
        if "place" == _pic_type:
            msg = make_rabbitmq_msg(json_str, _filename, sql_info)
            js_msg = json.dumps(msg)
            channel.basic_publish(body=js_msg, exchange="amq", properties=msg_props,
                                  routing_key="test queue")
        else:
            print "file not for place"
        j -= 1
    print time.time(),"start @", sec_start
    exit()