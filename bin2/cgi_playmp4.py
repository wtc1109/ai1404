import os,time
import cgi, cgitb, shutil

form = cgi.FieldStorage()

"""
fp = open("/tmp/mp42.txt", "a+")
try:    
    #post1 = form.file.read()
    for key1 in form.keys():
        fp.write("key=%s,val=%s\n"%(key1,form[key1]))

    #fp.write(post1)
    fp.write("\n\n\n")
except Exception,e:
    fp.write(str(e))
fp.close()
"""

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>HVPD video</title>
</head>
<body>
"""
if "video" in form.keys() and os.path.exists("../%s"%(form["video"].value)):
    print """<video controls><source src="../%s" type="video/mp4"></video>"""%(form["video"].value)
else:
    print "NO video"
print "</body> </html>"