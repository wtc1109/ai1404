import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<title>RecoveryDB</title>
</head>
<body>
"""
#os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 algreturndb2 > ../sqlback")
#os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 algreturndb2 | gzip > ../sqlback.gz")
if os.path.exists("../sqlback.zip"):
    os.system("cd ..;unzip -P 123654 sqlback.zip")

if os.path.exists("../sqlback"):
    os.system("mysqldump -ubluecardsoft -p#$%_BC13439677375 algreturndb2 > ../sqlback2")
    os.system("mysql -ubluecardsoft -p#$%_BC13439677375 algbackup < ../sqlback2")
    os.remove("../sqlback2")
    os.system("mysql -ubluecardsoft -p#$%_BC13439677375 algreturndb2 < ../sqlback")
    os.remove("../sqlback")
    print "<br />Backup database is OK"
    
else:
    print "backup database is false"
print "</body> </html>"