#!/usr/bin/python
import cgi, os, shutil
import zipfile



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
        try:
            zip0.extractall("/tmp/ai")
            ret = -2
        except:
            zip0.setpassword('123987')
            zip0.extractall("/tmp/ai")
            os.system("chmod -R 777 /tmp/ai/")
            #os.system("chmod -R 777 /tmp/ai/" + upgrade)
            if 0 == os.fork():
                os.close(1)
                os.system("/tmp/ai/"+upgrade)

    return ret


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