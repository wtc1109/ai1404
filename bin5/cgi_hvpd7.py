import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>GBK HVPD</title>
</head>
<body>
"""


print """<table><tr><td></td><td></td></tr>"""
localtime1 = time.localtime()
_hours = localtime1.tm_hour/4*4
_path = "../aijpgs/save_img/%d%02d%02d/%d"%(localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday, _hours)
_cameras = os.listdir(_path)

for _camera in _cameras:
    _camera_path = os.path.join(_path,_camera)
    if not os.path.isdir(_camera_path):
        continue
    _files = sorted(os.listdir(_camera_path))
    _file1 = _files[len(_files) - 1]
    print """<tr><td><img src="%s/%s"/></td><td>%s</td></tr>"""%(_camera_path, _file1, _camera)


print "</table></body> </html>"