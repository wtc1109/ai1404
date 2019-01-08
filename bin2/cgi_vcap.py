import os
import time,cgi, cgitb,requests

form = cgi.FieldStorage()
post1 = form.file.read()
fp = open("/tmp/onvif2.txt","a+")
for key1 in form.headers.keys():
    fp.write("key=%s,val=%s\n"%(key1,form.headers[key1]))
fp.write(post1)
fp.write("\n")
url = "http://192.168.7.248/onvif/device_service"
r = requests.post(url=url, headers={"Content-Type":form.headers["content-type"]}, data=post1)
fp.write("*****************\n")
fp.write("Content-Type: " + r.headers["content-type"])
fp.write( r.text)
fp.write("\n\n\n")
fp.close()
print "Content-Type: " + r.headers["content-type"]
print r.text