import socket

host = "13"
port = 9981
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
addr1 = ("192.168.7.255", port)
#sock.bind(addr1)
try:
    sock.sendto("asfhu", addr1)
except Exception, e:
    print e