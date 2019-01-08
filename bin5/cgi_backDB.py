import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<title>BackupDB</title>
</head>
<body>
"""
os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 hvpd3db2 > ../sqlback")
#os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 algreturndb2 | gzip > ../sqlback.gz")
if os.path.exists("../sqlback"):
    os.system("cd ..;zip -P 123654 sqlback.zip sqlback")
    os.remove("../sqlback")
if os.path.exists("../sqlback.zip"):
    print "<br />Backup database is OK"
    print """<p><a href="/sqlback.zip">Download this file for backup</a></p><p>Also this file can be used for recovery, next time</p>"""
else:
    print "backup database is false"
print "</body> </html>"