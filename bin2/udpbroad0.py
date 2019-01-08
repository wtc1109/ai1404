import binascii
import fcntl
import json
import os
import socket
import struct
import sys
import time

from M2Crypto.EVP import Cipher

import wtclib

ENCRYPT_OP = 1
DECRYPT_OP = 0
hex1= binascii.a2b_hex("abcd")
hex2 = ord(hex1[0])
iv = '\0' * 16  # init not used for aes_128_ecb
PRIVATE_KEY = "hsylgwk-2012aaaa"
RECEIVE_PORT = '8803'
UDP_BROADCAST_PORT = 9981
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
    return logger
"""

def Encrypt(data):

    cipher = Cipher(alg='aes_128_ecb', key=PRIVATE_KEY, iv=iv, op=ENCRYPT_OP)
    buf = cipher.update(data)
    buf = buf + cipher.final()
    del cipher

    output = ''
    for i in buf:
        output += '%02X' % (ord(i))
    return output

def Udp_broadcast(addr, port):
    global mylogger
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    addr1 = ("255.255.255.255", port)
    local_IP = (addr, 0)
    sock.bind(local_IP)
    _serverID = wtclib.get_serverID()
    while True:
        struct_time = time.localtime()
        time_str = '%d-%02d-%02d %02d:%02d:%02d' % (struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday,
                                                    struct_time.tm_hour, struct_time.tm_min, struct_time.tm_sec)
        time_strF = str(time.time())
        msg = {"AISERVERIP": addr, "AIport": RECEIVE_PORT, "timenow": time_str, "timstr": time_strF, \
               "sec": Encrypt(time_strF), "AIsn": _serverID, "AIHW": "AIBC", "VERSION": "1.00", "Online": "3"}
        js_msg = json.dumps(msg)
        try:
            sock.sendto(js_msg, addr1)
        except Exception, e:
            mylogger.error(str(e)+' '+js_msg)

        mylogger.info("udp broadcast0:" + js_msg+" @ "+addr)
        time.sleep(10)




def get_ip_addr(ifname):
    global mylogger
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    except Exception, e:
        mylogger.error(str(e))
        return None
    return addr

if __name__ == '__main__':
    global mylogger
    if not os.path.isdir("../log/udplog"):
        try:
            os.mkdir("../log/udplog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit(0)

    mylogger = wtclib.create_logging("../log/udplog/udpbroad0.log")
    mylogger.info("start running")
    addr = get_ip_addr("eth0")
    if None == addr:
        mylogger.error("eth0 addr is None")
        os._exit(0)
    cnt = 10
    while True:

        Udp_broadcast(addr, UDP_BROADCAST_PORT)
        time.sleep(3)

        mylogger.error("udp broadcast is running, and nerver here")


