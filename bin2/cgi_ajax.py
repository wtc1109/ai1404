#coding=gbk
import os,time,socket,fcntl,struct
import cgi, cgitb, shutil, json

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
_dict1 = {}
for key in form.keys():
    _dict1.update({key:form[key].value})

print "Content-type:text/html\n\n"
print json.dumps(_dict1)
#
