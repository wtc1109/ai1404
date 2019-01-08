import MySQLdb

test = MySQLdb.connect(db="testdb", host="localhost", user="root", passwd="123456")
print test
cur = test.cursor()
cur.execute("insert student values(3,'sfe2', 'm');")
aa = cur.execute("select name from student")
print cur.fetchmany(aa)
try:
    conn2 = MySQLdb.connect(db="testdb1", host="localhost", user="root", passwd="123456")
except Exception, e:
    print e
""" """
try:
    conn3 = MySQLdb.connect(host="localhost", user="root", passwd="123456")

except Exception, e:
    print e
print "conn3"
cur1 = conn3.cursor()
#cur1.execute("create database if not exists mydb;")
conn3.select_db("mydb")
#cur1.execute("create table mdhv(id int, ip char(32), plate char(16));")
try:
    cur1.execute("""insert into mdhv values(1,'sfe', 'm');""")
except Exception, e:
    print e
#    cur1.execute("show database")
#    print cur1.fetchall()
#    cur1.execute("""drop database if exists"""+"mydb")
a1 = cur1.execute("select ip from mdhv")
print cur1.fetchmany(a1)

#
print "aaa"
#print cur1.fetchmany(1)
#print conn2