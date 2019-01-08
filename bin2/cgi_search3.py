#coding=gbk
import os,time,socket,fcntl,struct
import cgi, cgitb, shutil

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

form = cgi.FieldStorage()

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>HVPD video</title>
</head>
<body>
"""

print """<img src="http://%s/images/gis1.jpg"/><br>"""%get_ip_addr("eth0")

print "</body> </html>"