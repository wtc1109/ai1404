import json
import socket
import MySQLdb
import struct
import time
import fcntl


UDP_RECEIVE_PORT = 10001


def get_sql_tables():
    ret_val = True
    while ret_val:
        try:
            conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="AlgReturndb2")
 #           cur = conn.cursor()
            ret_val = False
        except:
            time.sleep(10)

    return conn

def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    return addr

def update_sql(msg, addr, cur):
    dic = json.loads(msg)
    try:
        sn = dic['sn']
    except:
        return
    port = dic['port']
    orig = cur.execute("select sn from AIctrlTable where sn = "+sn)
    print orig
    if 0 == orig:
        insert_info = "insert into AIctrlTable (sn, LedCtrl_Selected) values"+"('%s', 0)"%sn
        cur.execute(insert_info)
    orig = cur.execute("select * from AIctrlTable")
    print cur.fetchmany(orig)

def udp_receive_msg(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    addr1 = (addr, UDP_RECEIVE_PORT)
    sock.bind(addr1)

    try:
        buff, addr_r = sock.recvfrom(2048)
    except Exception, e:
        print e
    return (buff, addr_r)

if __name__ == '__main__':
    conn = get_sql_tables()
    conn.autocommit(1)
    cur = conn.cursor()
    ip_addr = get_ip_addr('eth0')
    buff, addr_new = udp_receive_msg(ip_addr)
    update_sql(buff, addr_new, cur)
    cur.close()

