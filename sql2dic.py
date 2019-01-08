import ConfigParser

import MySQLdb
import MySQLdb.cursors


def get_a_sql_cur(conf_file):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(conf_file)
    except Exception, e:
        return None, str(e)+' db'
    secs = cf.sections()
    try:
        opts = cf.options("db")
    except Exception, e:
        return None, str(e)+' db'
    try:
        DB_host = cf.get("db", "location")
        DB_user = cf.get("db", "user_name")
        DB_passwd = cf.get("db", "user_passwd")
        DB_name = cf.get("db", "name")
    except Exception, e:
        return None, str(e)+' get db'
    while True:
        try:
            conn = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_passwd, db=DB_name, cursorclass=MySQLdb.cursors.DictCursor)
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except Exception, e:
            return None, str(e) + ' connect'
    cur.execute("use " + DB_name)
    return cur, "OK"

if __name__ == '__main__':
    (cur, str1) = get_a_sql_cur("conf.conf")
    ret = cur.execute("select * from defaultXspace")
    ret2 = cur.fetchmany(1)
    print ret2