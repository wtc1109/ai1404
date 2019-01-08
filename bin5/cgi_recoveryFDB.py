#!/usr/bin/python
import cgi, cgitb, os, shutil
import tarfile, zipfile
import multiprocessing

def check_zipfile_firmware(fi):
    os.system("cd /tmp;unzip -P 123654 %s"%fi)
    os.remove(fi)
    if os.path.exists("/tmp/sqlback"):
        os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 hvpd3db2 > ../sqlback")
        os.system("mysql -ubluecardsoft -p#$%_BC13439677375 hvpd2db2_backup < ../sqlback")
        os.remove("../sqlback")
        os.system("mysql -ubluecardsoft -p#$%_BC13439677375 hvpd3db2 < /tmp/sqlback")
        os.remove("/tmp/sqlback")
        return 0

    return -1


form = cgi.FieldStorage()

fileitem = form['filename']

if fileitem.filename:
    try:
        fn = os.path.basename(fileitem.filename)
        firmware ="/tmp/"+fn
        open(firmware, 'wb').write(fileitem.file.read())
        message = "The file " + fn + " was uploaded successfully"
        if zipfile.is_zipfile(firmware):
            if 0 == check_zipfile_firmware(firmware):
                message += " zipfile is OK"
            else:
                message += " zipfile is false code"
                os.remove(firmware)
        else:
            message += " and NOT ZIP for recovery DATABASE"
            os.remove(firmware)

    except Exception, e:
        message = str(e)
        pass

else:
    message = "No file was uploaded"

print "Content-type:text/html\n\n"
print """<html>
<body>
<p>%s</p>
</body>
</html>
"""%message