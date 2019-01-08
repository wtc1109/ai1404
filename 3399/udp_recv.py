import sqlite3, time, threading, socket
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


class Udp_broadcast_receiver(threading.Thread):
    def __init__(self, ip):
        self.__ip = ip
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, mylog
        _udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ADDR = (self.__ip, 9982)
        while True:
            try:
                _udp_sock.bind(ADDR)
                break
            except Exception, e:
                mylog.debug("UDP bind Error %s,"%self.__ip + str(e))
                time.sleep(10)
        udp_cnt = 0
        _udp_sock.settimeout(60)

        while True:
            try:
                (data, addr) = _udp_sock.recvfrom(1024)
            except Exception, e:
                mylog.warning("udp receive " + str(e))
                # time.sleep(10)
                continue
            mylog.debug(data)


            msg = "nothing"
            _udp_sock.sendto(msg, addr)

if __name__ == '__main__':
    sqlite_cur, hvpd_conn = get_sqlite_cur("udpd.db")
    _sql = "create table if not exists hvpdOnline(" \
           "cameraID char(32) primary key," \
           "neighbor_camera char(32)," \
           "ip char(20)," \
           "connect_timet int," \
           "connect_time datetime" \
           ");"
    sqlite_cur.execute(_sql)

