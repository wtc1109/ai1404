
#coding=utf8
import os,time,socket,fcntl,struct
import cgi, cgitb, shutil,MySQLdb, re, json,time,os
from itertools import chain
import sqlite3,chardet,sys,binascii
import urllib



try:
    import cPickle as pickle
except ImportError:
    import pickle


import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('../searchPath/src/conf.ini')


ctrl_server_ip2 = cf.get('ctrl','ctrl_addr')



def getjpg(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html



ctime=time.time()

def get_ip_addr(ifname):
    global mylogger
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    except Exception, e:
        mylogger.error(str(e))
        return None
    return addr


def deldir(dir,datatime01):
    files = os.listdir(dir)
    for file in files:
        filePath= dir+file

        if os.path.isfile(filePath):

            last1 = os.stat(filePath).st_mtime
            if (datatime01>last1):
                os.remove(filePath)

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)  # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)  # Compiles a regex.
    for item in collection:
        match = regex.search(item)  # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


form = cgi.FieldStorage()

print "Content-type:application/json\n\n"



if "plate_in" in form.keys():
    plate = form["plate_in"].value
    if plate !='nolpr':
        plate = plate.upper()
    # plate = str(plate)


else:
    plate= 'nolpr'



if "page" in form.keys():
    page=form['page'].value
    try:
        page=int(page)
        if page<1:
            page=1
    except Exception as e:
        page=1



else:
    page=1

try:
    conn = MySQLdb.connect(host='localhost', user="bluecardsoft", passwd="#$%_BC13439677375", db="AlgReturndb2")
    conn.autocommit(1)
    cur = conn.cursor()

except Exception, e:
    cur = None
    print json.dumps({'code':500,'error':e[1]})

try:
    conn2 = MySQLdb.connect(host=ctrl_server_ip2, user="bluecardsoft", passwd="#$%_BC13439677375", db="park",charset='gb2312')
    conn2.autocommit(1)
    cur2 = conn2.cursor()
except Exception, e:
    cur2 = None
    print json.dumps({'code':500,'error':e[1]})


_dict1={}
_ret = 0

if None != cur and None != cur2:

    _cameraAll = []

    timt2 = time.time() - 120

    deldir('../searchPath/tmp_db/',timt2)


    try:
        f = open('../searchPath/tmp_db/%s.txt'%plate, 'rb')
        msg = pickle.load(f)
        f.close()
    except Exception as e:
        msg=[]



    file= os.path.exists('../searchPath/tmp_db/%s.db'%plate)

    if {'plate':plate,"page":page} not in msg :
        # print 'print mysql................'

        for i in range(1, 4):
            _a1 = cur.execute("select Plate%dNumber from reoutfiltertable where length(Plate%dNumber)>=5"%(i, i))
            if 0 != _a1:
                _plateAll = cur.fetchall()

                _plateAll = list(set(chain.from_iterable(_plateAll)))

                _plateSearchOuts = set(fuzzyfinder(plate, _plateAll))


                if 0 != len(_plateSearchOuts):
                    for _plateOut in _plateSearchOuts:

                        _al = cur.execute("select cameraID from reoutfiltertable where Plate%dNumber='%s'" % (i,_plateOut))
                        if _al != 0:
                            _cameras = sorted(cur.fetchall())
                            for _camera in _cameras:
                                _cameraAll.append([_camera[0], i, _plateOut])
        page2=''
        if page >= len(_cameraAll):
            page2 = page
            page = len(_cameraAll)






        if _cameraAll ==[]:
            _dict1={'code':404,'error':u'没有该车牌'}

        else:


            _a1 = cur.execute("select ip from onlinehvpdstatustablemem where cameraID='%s'"%_cameraAll[page-1][0])



            if 0 != _a1:
                _ip, = cur.fetchone()
            else:
                _ip = '127.0.0.1'

            resjpg = urllib.urlopen('http://%s/images/orig0.jpg' % _ip).read()
            _jpg=open('../searchPath/tmp_img/%s.jpg'%_cameraAll[page-1][0],'wb')
            _jpg.write(resjpg)
            _jpg.close()


            if 0 != cur2.execute('select count(*) from park'):
                parkAll, = cur2.fetchone()

                parkAll = int(parkAll)

            if 0 != cur2.execute('select Name from park'):
                park_names = cur2.fetchall()
                park_dict = {}
                num = 1
                for i in park_names:
                    j = i[0].encode('utf8').decode('utf8').encode('utf8')
                    park_dict['parkName%s' % num] = j
                    num += 1
            try:
                f = open('../searchPath/tmp_db/%s-parkname.txt' %plate, 'wb')
                d = pickle.dump(park_dict,f)
                f.close()
            except Exception as e:
                msg = []




            _a1 = cur2.execute("select X,Y,NAME,ParkID from space where ControlServerNumber=%s and PointID=%d"%(_cameraAll[page-1][0], _cameraAll[page-1][1]))
            if 0 != _a1:
                _pos = cur2.fetchone()

                if None in _pos:
                    _ret=1

                if _ret == 0:

                    msg.append({'plate': plate, "page": page})

                    if page2:
                        msg.append({'plate': plate, "page": page2})

                    f = open('../searchPath/tmp_db/%s.txt' % plate, 'w+')
                    pickle.dump(msg, f)
                    f.close()





                    try:
                        timt = time.time()
                        conn3 = sqlite3.connect('../searchPath/tmp_db/%s.db' % (plate))
                        cur3 = conn3.cursor()

                    except Exception, e:
                        cur3 = None
                        print 'sqlite3 DB' + str(e)

                    try:
                        cur3.execute('''
                                                                   create table msg(
                                                                   plate char(10) not null,
                                                                   cameraID char(20) not null, 
                                                                   bayID int,
                                                                   bayname char(10),
                                                                   img char(100),
                                                                   parkid int(10),
                                                                   parkInname varchar(20) ,
                                                                   page_max int(10),
                                                                   page int(15),
                                                                   parkAll int(5), 
                                                                   primary key(bayID,cameraID)
                                                                   )
                                                                       ''')
                    except Exception as e:
                        pass

                    if file == False:
                        for j in _cameraAll:
                            cur3.execute(
                                'insert into msg(cameraID,bayid,plate) values(%s,"%s","%s")' % (j[0], j[1], j[2].decode('gbk').encode('utf8')))
                    # print 'cameraAll.....',_cameraAll
                    cur3.execute('update msg set img="/searchPath/tmp_img/%s.jpg" where (cameraID=%s and bayid="%d")' % (_cameraAll[page-1][0], str(_cameraAll[page-1][0]),int(_cameraAll[page-1][1])))
                    cur3.execute('update msg set parkID=%s where (cameraID=%s and bayid="%d")'%(_pos[3],_cameraAll[page-1][0],int(_cameraAll[page-1][1])))
                    cur3.execute('update msg set bayname="%s" where (cameraID="%s" and bayid="%d")'%(_pos[2],_cameraAll[page-1][0],int(_cameraAll[page-1][1])))
                    cur3.execute('update msg set parkAll=%s  where (cameraID=%s and bayid="%d")'%(parkAll,_cameraAll[page-1][0],int(_cameraAll[page-1][1])))



                    if 0 != cur2.execute("select Name from park where ID=%d"%(_pos[3])):

                        park_name, = cur2.fetchone()
                        park_name= park_name.encode('utf8')

                        cur3.execute('update msg set parkInname="%s",page_max=%s,page=%s where (cameraID=%s and bayid="%d")'%(park_name,len(_cameraAll),page,_cameraAll[page-1][0],int(_cameraAll[page-1][1])))

                    conn3.commit()
                    conn3.close()
                    ctime2 = time.time()
                    ctime3 = ctime2 - ctime



                    _dict1 = {'code':200,'plate': _cameraAll[page-1][2].decode('gbk'), 'page': page, 'page_max': len(_cameraAll),
                              'img': '/searchPath/tmp_img/%s.jpg'%_cameraAll[page-1][0],
                              'parkInName': park_name, 'parkID': _pos[3], 'bayName': _pos[2],
                              'cameraID': _cameraAll[page-1][0], 'bayID': _cameraAll[page-1][1],'parkAll':parkAll,'time':ctime3}
                    nu = 1
                    for  v in park_dict.values():
                        _dict1['park_name%s' % nu] = v
                        nu += 1


                elif _ret ==1:
                    _dict1 = {'code':404,'error':u'定位坐标或车位号数据不存在'}
            else:
                _dict1={'code':404,'error':u'定位坐标或车位号数据不存在'}

    else:
        # print 'print sqlite................'



        try:
            f = open('../searchPath/tmp_db/%s-parkname.txt' % plate, 'rb')
            park_dict = pickle.load(f)
            f.close()
        except Exception as e:
            msg = []

        try:

            conn3 = sqlite3.connect('../searchPath/tmp_db/%s.db' % (plate))
            cur3 = conn3.cursor()

        except Exception, e:
            cur3 = None
            print 'sqlite3 DB' + str(e)

        try:
            cur3.execute('select * from msg')
            ret = cur3.fetchall()
            if ret:

                if page >= len(ret):
                    page = len(ret)
                ctime2 = time.time()
                ctime3 = ctime2 - ctime

                page=page-1
                _dict1 = {'code':200,'plate':ret[page][0],'img':ret[page][4],
                          'parkInName':ret[page][6],'parkID':ret[page][5],
                          'bayName':ret[page][3],'cameraID':ret[page][1],'bayID':ret[page][2],
                          'page_max':ret[page][7],'page':page+1,'parkAll':ret[page][9],
                          'time':ctime3

                          }
                nu=1
                for v in park_dict.values():
                    _dict1['park_name%s' % nu] = v
                    nu += 1



            else:
                _dict1 = {'code':500,'error':u'sqlite查询数据失败'}
        except Exception as e:
            _dict1 = {'code':e}
        conn3.commit()
        conn3.close()

    print json.dumps(_dict1, encoding='utf8', ensure_ascii=False).encode('utf8')



