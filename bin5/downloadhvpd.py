#!/usr/bin/python
import cgi, cgitb, os
import tarfile, zipfile


def check_tarfile_firmware(fi):
    tar2 = tarfile.open(fi)
    info2 = tar2.getnames()
    tar2.close()
    for filen in info2:
        file_sp = filen.split('/')
        if "upgrade" in file_sp:
            return 0
        if "upgrade.sh" in file_sp:
            return 0

    return -1

def check_zipfile_firmware(fi):
    zip0 = zipfile.ZipFile(fi, 'r')
    info0 = zip0.namelist()
    zip0.close()
    for filen in info0:
        file_sp = filen.split('/')
        if "upgrade" in file_sp:
            return 0
        if "upgrade.sh" in file_sp:
            return 0

    return -1

root_dir = os.getcwd()
#_top = root_dir[:root_dir[:root_dir.rfind('/')].rfind('/')]
#firmware1 =_top+"/firmwares/"

form = cgi.FieldStorage()

fileitem = form['filename']

if fileitem.filename:
    try:
        fn = os.path.basename(fileitem.filename)
        #root_dir = os.getcwd()
        #_top = root_dir[:root_dir.rfind('/').rfind('/')]
        firmware ="/home/bluecard/hvpd/firmwares/"+fn
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
os.system("chmod 777 /home/bluecard/hvpd/firmwares/*")
print "Content-type:text/html\n\n"
print """<html>
<body>
<p>%s</p>
</body>
</html>
"""%(message)
