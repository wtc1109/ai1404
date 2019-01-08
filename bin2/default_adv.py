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

if __name__ == '__main__':
    sqlite_cur, hvpd_conn = get_sqlite_cur("adv_set.db")
    _sql = "create table if not exists setting(" \
           "name char(32) primary key," \
           "val char(128)" \
           ");"
    sqlite_cur.execute(_sql)
    """ the only way to check sqlite3,if data in, is fetchall,and len(o) > 1 
    _sql = "select name from setting"
    _a1 = sqlite_cur.execute(_sql)
    _on = sqlite_cur.fetchall()
    print _a1
    _sql = "insert into setting(name, val)values('1234','sfa')"
    sqlite_cur.execute(_sql)
    _sql = "select * from setting"
    _a1 = sqlite_cur.execute(_sql)
    _on = sqlite_cur.fetchall()
    print _a1
"""