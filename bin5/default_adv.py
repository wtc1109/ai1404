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