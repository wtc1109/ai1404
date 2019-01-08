#!/usr/bin/python
import cgi, cgitb, os
import tarfile, zipfile


def check_tarfile_firmware(fi):
    tar2 = tarfile.open(fi)
    info2 = tar2.getnames()
    tar2.close()
    for filen in info2:
        if filen == "upgrade":
            return 0
        elif filen == "upgrade.sh":
            return 0
        elif filen == "upgrade.py":
            return 0
    return -1

def check_zipfile_firmware(fi):
    zip0 = zipfile.ZipFile("fi", 'r')
    info0 = zip0.namelist()
    zip0.close()
    for filen in info0:
        if filen == "upgrade":
            return 0
        elif filen == "upgrade.sh":
            return 0
        elif filen == "upgrade.pyc":
            return 0
    return -1

form = cgi.FieldStorage()

fileitem = form['filename']

if fileitem.filename:
    try:
        fn = os.path.basename(fileitem.filename)
        firmware ="//home/bluecard/hvpd/firmwares/"+fn
        open(firmware, 'wb').write(fileitem.file.read())
        message = "The file " + fn + " was uploaded successfully"
        if tarfile.is_tarfile(firmware):
            if 0 == check_tarfile_firmware(firmware):
                message += " tarfile is OK"
            else:
                message += " tarfile is false code"
                os.remove(firmware)
        elif zipfile.is_zipfile(firmware):
            if 0 == check_zipfile_firmware(firmware):
                message += " zipfile is OK"
            else:
                message += " zipfile is false code"
                os.remove(firmware)
        else:
            message += " and NOT filetpye for upgrade"
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