
#coding=utf8

import os,time,socket,fcntl,struct
import cgi, cgitb, shutil,MySQLdb, re, json,time,os
from itertools import chain
from PIL import ImageDraw,Image
import requests
import sqlite3,chardet,sys,binascii
import ConfigParser
from python_coordZero_outputPath import python_axing_inputNode_outList
import socket
try:
    import cPickle as pickle
except ImportError:
    import pickle

import logging

import socket



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



host_ip=get_ip_addr('eth0')

cf = ConfigParser.ConfigParser()
cf.read('../searchPath/src/conf.ini')
ctrl_server_ip2 = cf.get('ctrl','ctrl_addr')



msg = ''

#定期删除照片函数
def deldir(dir,ctime):
    files = os.listdir(dir)
    for file in files:
        filePath= dir+file
        if os.path.isfile(filePath):
            last1 = os.stat(filePath).st_mtime
            timet =time.time()-ctime
            if (timet>last1):
                os.remove(filePath)



form = cgi.FieldStorage()


print "Content-type:application/json\n\n"

timet=time.time()
if "cameraID" in form.keys():
    cameraID = form["cameraID"].value
    cameraID = cameraID.upper()

else:
    # cameraID = '1805430051'
    cameraID = None

if "bayID" in form.keys():
    bayID = form["bayID"].value
    bayID=int(bayID)


else:
    # bayID=1
    bayID=None

if "parkID" in form.keys():
    parkID = form["parkID"].value
    parkID=int(parkID)
else:
    # parkID =1
    parkID=None

if "CurBayName" in form.keys():
    CurBayName = form["CurBayName"].value
    CurBayName = CurBayName.upper()

else:
    # CurBayName = '72'
    CurBayName = None

if "searchPointID" in form.keys():
    searchPointID = form["searchPointID"].value

else:
    # searchPointID = '398'
    searchPointID=None

if "CurBayZone" in form.keys():
    CurBayZone = form["CurBayZone"].value.decode('utf8')

else:
    # CurBayZone=u'一层停车场'.encode('gb2312')
    # CurBayZone='6'
    CurBayZone=None






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
    conn2 = MySQLdb.connect(host=ctrl_server_ip2, user="bluecardsoft", passwd="#$%_BC13439677375", db="park",charset='gb2312')
    conn2.autocommit(1)
    cur2 = conn2.cursor()
except Exception, e:
    cur2 = None
    print json.dumps({'code':'500',"error":e[1]})





_msg=0

if (cur2 !=None and cameraID != None and bayID !=None and parkID !=None and CurBayZone!=None):

    code=200
    _dict={}
    #查询停车场区域名字和照片
    _al = cur2.execute("select Name,img from park where ID=%s"%parkID)

    if _al!=0:
        parkINname,parkImage= cur2.fetchone()
        parkINname= parkINname.encode('utf8')
        # print 'parkImage....',parkImage


    # 查询停车场区域照片
    _al = cur2.execute('select x,y,Name from space where controlservernumber=%s and pointid=%s'%(cameraID,bayID))
    if _al!=0:
        end_x,end_y,bayName,=cur2.fetchone()





        _al = cur2.execute('select id from park where name="%s"' % CurBayZone)
        if _al!=0:
            CurBayZon, = cur2.fetchone()




        #查询用户输入的车位x,y坐标
        if CurBayName:
            _al = cur2.execute('select x,y,name from space where name like "%{}" and parkid={}'.format(CurBayName,parkID))
        else:
            _al = cur2.execute('select x,y,name from space where  name like "%{}" and parkid={}'.format(searchPointID,parkID))


        if _al==0:
            start_x = 0
            start_y = 0
            code = '300'
            UserbayName='00000'
            msg = u'输入车位号不存在，请重新输入'
            ret=[]
            page=0




        if _al!=0:
            # start_x, start_y= cur2.fetchone()
            ret= cur2.fetchall()
            start_x=ret[page-1][0]
            start_y=ret[page-1][1]
            UserbayName=ret[page-1][2]
            # print 'ret....',ret
            # print 'start_x,y.......',start_x,start_y
            # print 'end_x,y.......',end_x,end_y




        try:
            #到src目录下执行ｃ代码生成ｔｘｔ路线文件,执行完后在转回到当前路径.
            os.chdir('../searchPath/src')
            os.popen('./bmp_to_txt')
            os.chdir('../../cgi-bin')


            im = Image.open('../searchPath/src/ppimg_img_%s.jpg'%parkID)
            im01=Image.open('../searchPath/img/qi.png')
            im02=Image.open('../searchPath/img/zhong.png')
        except Exception as e:
            _dict = {'code': '500', 'msg': u'载入图片有误'}
            _msg = 1
        # print e

        if _msg==0:
            try:
                if CurBayZon!=parkID:
                    start_x=0
                    start_y=0
                    code='302'
                    page=1
                    ret=[0]
                    msg= u'请到{}在导航'.format(parkINname.decode('utf8'))
                try:

                    ls = python_axing_inputNode_outList.main(start_x,start_y,end_x,end_y,'../searchPath/src/ppimg_DanseImg_%d.txt'%parkID)

                except Exception as e:
                    ls=[]

                # 设置路线宽度
                wh = im.size[1] * 0.015

                ClList = []
                for i in ls:
                    i[0] = i[0] * int(im.size[0])
                    i[1] = i[1] * int(im.size[1])
                    i = list(i)
                    ClList.append(i)


                CloseList=[]
                for i in ClList:
                    i=tuple(i)
                    CloseList.append(i)


                # 导航图片尺寸大小
                size_w = int(im.size[0] / 20)
                size_h = int(im.size[0] / 20 * 1.26)
                # size_h = int(im.size[0] / 20)





                # 进行绘制图像保存到指定文件下
                start_x=start_x * int(im.size[0])
                start_y=start_y * int(im.size[1])

                end_x=end_x * int(im.size[0])
                end_y=end_y * int(im.size[1])
                if start_x<0:
                    start_x=0
                    start_y=0
                draw = ImageDraw.Draw(im)


                #进行判断起终图片位置进行调整
                start_x0=start_x
                start_y0=start_y
                end_x0=end_x
                end_y0=end_y
                if start_x == 0 and start_y == 0:
                    start_x0=size_w//2
                    start_y0=size_h
                if start_x == 0 and start_y == 0:
                    start_size_x = 0
                    start_size_y = 0
                start_size_x = int(start_x - size_w // 2)
                start_size_y = int(start_y - size_h)
                if start_size_x < 0 and start_size_y < 0:
                    start_size_x = 0
                    start_size_y = 0
                if start_size_y < 0:
                    start_size_y = 0
                    start_y0=size_h


                #绘制终点图片位置
                end_size_x=int(end_x-size_w//2)
                end_size_y=int(end_y-size_h)
                if end_size_y<0:
                    end_size_y=0
                    end_y0 = size_h
                if end_size_y>im.size[1]:
                    end_size_y=im.size[1]


                # 进行更改起点、终点图片尺寸
                img01 = im01.resize((size_w, size_h))
                img02 = im02.resize((size_w, size_h))

                #如果给的坐标没有数据或这是一个数据只画一个终点图片
                if ls != [] and len(ls) != 1:
                    #绘制起点线
                    draw.line((start_x0,start_y0,CloseList[0][0]+wh//2-wh//5,CloseList[0][1]), (128,128,128), width=int(wh))
                    draw.ellipse((start_x0-wh//2,start_y0-wh//2,start_x0+wh//2,start_y0+wh//2), (128,128,128))
                    draw.ellipse((CloseList[0][0]+wh//2-wh//5-wh//2,CloseList[0][1]-wh//2,CloseList[0][0]+wh//2-wh//5+wh//2,CloseList[0][1]+wh//2), (128,128,128))
                    # 绘制终点线
                    draw.line((end_x0, end_y0, CloseList[len(CloseList) - 1][0], CloseList[len(CloseList) - 1][1]),
                              (128, 128, 128), width=int(wh))
                    draw.ellipse((end_x0 - wh // 2, end_y0 - wh // 2, end_x0 + wh // 2, end_y0 + wh // 2),
                                 (128, 128, 128))



                    #沿路线画圆。修饰划线连接处断开的缺陷
                    for i in CloseList:
                        draw.ellipse((i[0]-wh//2,i[1]-wh//2,i[0]+wh//2,i[1]+wh//2),'red')

                    # 绘制导航信息

                    draw.line(CloseList, 'red', width=int(wh))



                    #把导航图片粘贴到停车场图片下
                    #绘制起点图片位
                    draw.bitmap((start_size_x, start_size_y), img01,(78,204,122))
                    #绘制终点坐标
                    draw.bitmap((end_size_x,end_size_y),img02,'red')
                else:

                    draw.ellipse((start_size_x+size_w//2-wh//2, start_size_y+size_h-wh//2,start_size_x+size_w//2+wh//2, start_size_y+size_h+wh//2),'red')
                    draw.ellipse((end_size_x+size_w//2-wh//2, end_size_y+size_h-wh//2,end_size_x+size_w//2+wh//2, end_size_y+size_h+wh//2),'red')
                    draw.line((start_size_x+size_w//2, start_size_y+size_h,end_size_x+size_w//2, end_size_y+size_h),'red',width=int(wh))
                    # 绘制起点图片位
                    draw.bitmap((start_size_x, start_size_y), img01, (78, 204, 122))
                    # 绘制终点坐标
                    draw.bitmap((end_size_x, end_size_y), img02, 'red')




                #绘制完的图片存放的指定位置
                im.save('../searchPath/tmp_img/ppimg_img_%s_%s_%s_%s.jpg'%(parkID,CurBayName,bayName,page))

                os.chdir('../searchPath/tmp_img/')
                os.popen('chmod 666 *')
                os.chdir('../../cgi-bin')

                #判断该路径下文件创建时间 超过120秒的进行删除
                deldir('../searchPath/tmp_img/',120)

                _dict={'code':code,'parkInName':parkINname,'parkID':parkID,'bayName':bayName,
                       'GisName':'/searchPath/tmp_img/ppimg_img_%s_%s_%s_%s.jpg'%(parkID,CurBayName,bayName,page),
                       'msg':msg,'page':page,'page_max':len(ret),'UserbayName':UserbayName}

            except Exception as e:
                _dict={'code':'500','msg':'数据出错'}



    else:
        _dict = {'code': '403', 'msg': u'传入坐标信息有误'}
else:
    _dict={'code':'403','msg':u'传入参数有误'}
timet2=time.time()
timet3=timet2-timet
_dict['time']=timet3

print json.dumps(_dict,encoding='utf8',ensure_ascii=False).encode('utf8')


