import sqlite3

def get_sqlite_cur(DBname):
    try:
        conn = sqlite3.connect(DBname)
        conn.isolation_level = None
        cur = conn.cursor()
    except:
        conn = sqlite3.connect()
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("create database %s"%DBname)
        cur.execute("use %s"%DBname)
    return cur, conn

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<title>All Online</title>
</head>
<body>
"""
if __name__ == '__main__':

    sqlite_cur, hvpd_conn = get_sqlite_cur("imei.db")
    _sql = "select * from online"
    sqlite_cur.execute(_sql)
    _onlines = sqlite_cur.fetchall()
    print "Get %d sn" % len(_onlines)
    print """
        <table><tr>
        <td width="180">SN</td>
        <td width="220">IMEI</td>
        <td>RSSI</td>
        <td>VBatt</td>
        <td width="220">WARNING</td>
        <td>TIME</td></tr>
        """
    for _sn in _onlines:
        print "<tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>"\
              %(_sn[0], _sn[1], _sn[3],_sn[6],_sn[2],_sn[8])


    print "</table></body> </html>"