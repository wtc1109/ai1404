#import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import os,MySQLdb,time,sys


print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>GBK HVPD</title>
</head>
<body>
"""
try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="AlgReturndb2")
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    cur = None
    print str(e)

#import wtclib
#cur,err = wtclib.get_a_sql_cur("../conf/conf.conf")
if None != cur:
    localtime1 = time.localtime()

    if 0 != cur.execute("select sum(CarCount) from aiouttable"):
        _all_space, = cur.fetchone()
        a1 = cur.execute("select * from bay_using_log where day='%d'"%localtime1.tm_mday)
        print "Get %d hours today<br>"%a1
        if 0 != a1:
            try:
                _logs1 = cur.fetchall()
                _logs = sorted(_logs1)
                x = [_logs[i][1] for i in range(a1)]
                y1 = []
                y2 = []
                for _log in _logs:
                    y1.append(_log[2])
                    y2.append(_log[2]/float(_all_space))
            except Exception, e:
                print e
                print "line: "+str(sys._getframe().f_lineno)
            try:
                #print x
                #print y1
                #print y2
                fig = plt.figure()
                ax1 = fig.add_subplot(111)
                ax1.plot(x, y1, 'b',label='Bays')
                ax1.set_ylabel('Used Bays')
                ax1.set_ylim([min(y1)-1,max(y1)+1])
            except Exception,e:
                print e
                print "line: "+str(sys._getframe().f_lineno)

            try:
                ax2 = ax1.twinx()  # this is the important function
                ax2.plot(x, y2, 'r', label='Percent')
                ax2.set_xlim([min(x)-1, max(x)+1])
                ax2.set_ylabel('100% Percent')
                ax2.set_xlabel('Hour')
                ax1.legend()
                ax2.legend(loc=0)
                plt.savefig("../using.png", format='png')

                #plt.show()
                print """<img src="../using.png" width="800", hight="800" /><br>"""
            except Exception,e:
                print e
                print "line: "+str(sys._getframe().f_lineno)

    localtime1 = time.localtime(time.time()-24*3600)
    a1 = cur.execute("select * from bay_using_log where day='%d'" % localtime1.tm_mday)
    print "Get %d hours yesterday<br>" % a1
    if 0 != a1:
        try:
            _logs1 = cur.fetchall()
            _logs = sorted(_logs1)
            x = [_logs[i][1] for i in range(a1)]
            y1 = []
            y2 = []
            for _log in _logs:
                y1.append(_log[2])
                y2.append(_log[2] / float(_all_space))
        except Exception, e:
            print e
            print "line: " + str(sys._getframe().f_lineno)
        try:
            #print x
            #print y1
            #print y2
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            ax1.plot(x, y1, 'b', label='Bays')
            ax1.set_ylabel('Used Bays')
            ax1.set_ylim([min(y1) - 1, max(y1) + 1])
        except Exception, e:
            print e
            print "line: " + str(sys._getframe().f_lineno)

        try:
            ax2 = ax1.twinx()  # this is the important function
            ax2.plot(x, y2, 'r', label='Percent')
            ax2.set_xlim([min(x)-1, max(x)+1])
            ax2.set_ylabel('100% Percent')
            ax2.set_xlabel('Hour')
            ax1.legend()
            ax2.legend(loc=0)
            plt.savefig("../using1.png", format='png')

            # plt.show()
            print """<img src="../using1.png" width="800", hight="800" /><br>"""
        except Exception, e:
            print e
            print "line: " + str(sys._getframe().f_lineno)


else:
    print """connect DB fault"""

print "</body> </html>"

