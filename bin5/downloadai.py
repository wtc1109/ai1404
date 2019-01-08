#!/usr/bin/python
import cgi, cgitb, os, shutil
import tarfile, zipfile
import multiprocessing



def check_tarfile_firmware(fi):
    tar2 = tarfile.open(fi)
    info2 = tar2.getnames()

    ret = -1
    for filen in info2:
        if filen == "upgrade":
            upgrade = "upgrade"
            ret = 0
            break
        elif filen == "upgrade.sh":
            upgrade = "upgrade.sh"
            ret = 0
            break

    if 0 == ret:
        try:
            shutil.rmtree("/tmp/ai")
        except:
            pass
        tar2.extractall("/tmp/ai")
        os.system("chmod 777 -R /tmp/ai/"+upgrade)
        if 0 == os.fork():
            os.close(1)
            os.system("/tmp/ai/" + upgrade)
    return ret

def check_zipfile_firmware(fi):
    zip0 = zipfile.ZipFile(fi, 'r')
    info0 = zip0.namelist()

    ret = -1

    for filen in info0:
        if filen == "upgrade":
            upgrade = "upgrade"
            ret = 0
            break
        elif filen == "upgrade.sh":
            upgrade = "upgrade.sh"
            ret = 0
            break

    if 0 == ret:
        try:
            shutil.rmtree("/tmp/ai")
        except:
            pass
        zip0.extractall("/tmp/ai")
        os.system("chmod 777 /tmp/ai/" + upgrade)
        if 0 == os.fork():
            os.close(1)
            os.system("/tmp/ai/"+upgrade)

    return ret

#ret0 = check_tarfile_firmware("/tmp/linuxpython.tar.gz")
#ret1= check_zipfile_firmware("/tmp/ai.zip")

form = cgi.FieldStorage()

fileitem = form['filename']

if fileitem.filename:
    try:
        fn = os.path.basename(fileitem.filename)
        firmware ="/tmp/"+fn
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