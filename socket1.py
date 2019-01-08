import socket
import fcntl
import struct
import uuid

def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    print addr
    mac1 = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac2 = ":".join([mac1[e:e+2] for e in range(0,11,2)])
    print mac2
if __name__ == '__main__':
    get_ip_addr("eth0")
    get_ip_addr("lo")
