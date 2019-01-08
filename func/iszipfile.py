#!/usr/bin/python
import cgi, os, shutil
import zipfile

if zipfile.is_zipfile('1.zip'):
    print "is"
    zip0 = zipfile.ZipFile('1.zip', 'r')
    #zip0.setpassword('123456')
    try:
        info0 = zip0.namelist()
        info1 = zip0.infolist()
        zip0.extractall("/tmp/ai")
    except Exception,e:
        print e

    print 'ok'
    print info0
else:
    print 'not'