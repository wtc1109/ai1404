#!/usr/bin/python
import cgi, cgitb, os

def remove_old_file(fn):
    #(snpath, dirs, filenames), = os.walk("/home/bluecard/hvpd/prog/conf/")
    for snpath, dirs, filenames in os.walk("/home/bluecard/hvpd/prog/conf/"):
        break
    for files in filenames:
        if 0 == files.find(fn):
            path1 = "/home/bluecard/hvpd/prog/conf/"+files
            os.remove(path1)


form = cgi.FieldStorage()

fileitem = form['filename']
if fileitem.filename:
    remove_old_file("HVCS_parking_address")
    fn = os.path.basename(fileitem.filename)
    if 0 == fn.find("HVCS_region_config"):
        remove_old_file("HVCS_region_config")
    elif 0 == fn.find("HVCS_screen_connect"):
        remove_old_file("HVCS_screen_connect")
    elif 0 == fn.find("HVCS_screen2_connect"):
        remove_old_file("HVCS_screen2_connect")
    elif 0 == fn.find("HVCS_screen_config"):
        remove_old_file("HVCS_screen_config")
    elif 0 == fn.find("HVCS_screen2_config"):
        remove_old_file("HVCS_screen2_config")
    elif 0 == fn.find("HVCS_reserved_parking"):
        remove_old_file("HVCS_reserved_parking")
    elif 0 == fn.find("screenspecialconfigtable"):
        remove_old_file("screenspecialconfigtable")

    open("/home/bluecard/hvpd/prog/conf/"+fn, 'wb').write(fileitem.file.read())
    message = "The file "+fn+" was uploaded successfully"
else:
    message = "No file was uploaded"
os.system("chmod 777 /home/bluecard/hvpd/prog/conf/*")
print "Content-type:text/html\n\n"
print """<html>
<body>
<p>%s</p>
</body>
</html>
"""%message