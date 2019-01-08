import ConfigParser
import Queue
import json
import math
import os
import socket
import sys
import threading
import time
import urllib
import urllib2
import datetime
import MySQLdb
import pika
import wtclib,random

if __name__ == '__main__':
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
    _a1 = cur.execute("select * from aisettingtable_camera")
    _cameras = cur.fetchall()
    for _camera in _cameras:
        cur.execute("update aisettingtable_bay set equipmentID='%s',parking_line1RTx=30,parking_line1LBy=80,"
                    "parking_line1RBx=30,parking_line1RBy=80 where cameraID='%s'"%(_camera[0],_camera[0]))
    _a1 = cur.execute("select * from aisettingtable_camera_mem")
    if 0 == _a1:
        cur.execute("insert into aisettingtable_camera_mem(cameraID,cmosID,bays)select cameraID,cmosID,bays from aisettingtable_camera")

    if 0 == cur.execute("select * from aisettingtable_bay"):
        for _camera in _cameras:
            for i in range(_camera[2]):
                cur.execute("insert into aisettingtable_bay_mem(cameraID,cmosID,bay)values('%s',%d,%d)" % (
                    _camera[0], _camera[1], i + 1))
                cur.execute("insert into aisettingtable_bay(cameraID,cmosID,bay)values('%s',%d,%d)" % (
                    _camera[0], _camera[1], i + 1))

    if 0 == cur.execute("select * from aisettingtable_bay_mem") :
        cur.execute(
            "insert into aisettingtable_bay_mem(cameraID,cmosID,bay,equipmentID,parking_line1LTx,parking_line1LTy,\
            parking_line1RTx,parking_line1RTy,parking_line1LBx,parking_line1LBy,parking_line1RBx,parking_line1RBy,\
            set_time,set_timet,need_plate,Event1Flag,Event2Flag) select * from aisettingtable_bay")

    cur.execute("insert into aiouttable_bay(cameraID,cmosID,bay) select cameraID,cmosID,bay from aisettingtable_bay_mem")
    cur.execute("update aiouttable_bay set CarposRBx=20,CarposRBy=30,plate1posRBx=15,plate1posRBy=20")
    cur.execute("insert into aiouttable_camera(cameraID,cmosID) select cameraID,cmosID from aisettingtable_camera")
    cur.execute("update aiouttable_camera set pic_full_name='/123.jpg'")
    #os._exit(0)


    """"""
