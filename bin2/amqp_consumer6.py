import MySQLdb
import pika
import time,datetime
import json
import psutil
import urllib2
import os, sys
import requests
import wtclib
import random
import sysv_ipc
import struct,binascii
import threading,thread
import Queue
from PIL import ImageDraw, Image
import glob


AI_settings = {}
title_queue = Queue.Queue(maxsize=5)
result_queue = Queue.Queue(maxsize=5)
draw_queue = Queue.Queue(maxsize=5)

class sync_data_from_HDD(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/ai_shell/sync.log')
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret
        self.__logger.info("Sync start")

        sync_cur = get_a_sql_cur_forever(self.__logger)
        try:
            _sql_str = "select max(set_time) from aisettingtable"
            sync_cur.execute(_sql_str)
            _datetime, = sync_cur.fetchone()
            if None == _datetime:
                _datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _sql_str = "TRUNCATE TABLE aisettingtablemem"
            sync_cur.execute(_sql_str)
            _sql_str = "insert into aisettingtablemem select * from aisettingtable"
            sync_cur.execute(_sql_str)
            _sql_str = "SELECT * FROM aisettingtable"
            _a1 = sync_cur.execute(_sql_str)
            if 0 != _a1:
                self.__logger.info("Init get %d ai settings"%_a1)
                _settings = sync_cur.fetchall()
                for _setting in _settings:
                    AI_settings.update({_setting[0]:[info for info in _setting]})
        except Exception,e:
            self.__logger.error(str(e))
            self.__logger.error(_sql_str)
            if 'MySQL server has gone away' in str(e):
                sync_cur = get_a_sql_cur_forever(self.__logger)
        NEW_daybook_create = 1
        conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "db")
        if "ai_daybook_en" in conf_dict:
            AI_daybook_en = int(conf_dict["ai_daybook_en"])
        else:
            AI_daybook_en = 0
        if 0 != AI_daybook_en:
            create_daybook_log_table()
            create_daybook_log_table(24 * 3600)
        while True:
            try:
                _sql_str = "select * from aisettingtable where set_time >'%s'"%_datetime
                _a1 = sync_cur.execute(_sql_str)
                if 0 != _a1:
                    self.__logger.info("Update %d ai settings" % _a1)
                    _new_settings = sync_cur.fetchall()
                    for _new_set in _new_settings:
                        _sql_str = "replace into aisettingtablemem select * from aisettingtable where " \
                                   "cameraID='%s' and cmosID=%d"%(_new_set[0],_new_set[1])
                        sync_cur.execute(_sql_str)
                        AI_settings.update({_new_set[0]: [info for info in _new_set]})
                    _sql_str = "select max(set_time) from aisettingtable"
                    sync_cur.execute(_sql_str)
                    _datetime, = sync_cur.fetchone()
                else:
                    self.__logger.debug("None setting need update")
                if 0 != AI_daybook_en:
                    localtime1 = time.localtime()
                    if 0 == NEW_daybook_create and localtime1.tm_hour > 12:
                        create_daybook_log_table(24 * 3600)
                        NEW_daybook_create = 1
                    if 0 != NEW_daybook_create and localtime1.tm_hour <= 12:
                        NEW_daybook_create = 0
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    sync_cur = get_a_sql_cur_forever(self.__logger)
            time.sleep(5)
                #finally:

class insert_aiout_title(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/ai_shell/title.log')
        threading.Thread.__init__(self)
    def run(self):
        self.__logger.info("title start")
        title_cur = get_a_sql_cur_forever(self.__logger)
        ServerID = wtclib.get_serverID()
        _sql_str = "insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, " \
                   "'python %s &', 360, %d,'%s')" % (os.getpid(), __file__, time.time(), ServerID)
        try:
            title_cur.execute(_sql_str)
        except Exception,e:
            self.__logger.error(str(e))
        wdi_time30sec  = int(time.time())/32

        title_update_dict = {}
        while True:
            try:
                msg = title_queue.get(block=True)
                _dic_info = json.loads(msg)
                self.__logger.info("receive tile " + _dic_info["cam_id"])
                _title_time_Sec = int(time.time())
                _new_32sec = _title_time_Sec/32
                if wdi_time30sec != _new_32sec:
                    wdi_time30sec = _new_32sec
                    _sql_str = "update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(),ServerID)
                    title_cur.execute(_sql_str)
                    self.__logger.info(_sql_str)

                if _dic_info["cam_id"] in title_update_dict:
                    if _title_time_Sec - title_update_dict[_dic_info["cam_id"]] < 10:
                        self.__logger.debug("not need title update with %s"%_dic_info["cam_id"])
                        continue
                    title_update_dict[_dic_info["cam_id"]] = _title_time_Sec
                else:
                    title_update_dict.update({_dic_info["cam_id"]:_title_time_Sec})


                _sql_str = "insert into aiouttable(cameraID,cmosID)values('%s',%d)ON DUPLICATE KEY UPDATE LatestUpdate=now()" \
                           % (_dic_info["cam_id"], _dic_info["CMOS"])
                title_cur.execute(_sql_str)
                _sql_str = "insert into aiouttable2(cameraID,cmosID)values('%s',%d)ON DUPLICATE KEY UPDATE LatestUpdate=now();" \
                           % (_dic_info["cam_id"], _dic_info["CMOS"])
                title_cur.execute(_sql_str)
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    title_cur = get_a_sql_cur_forever(self.__logger)
            #time.sleep(5)
                #finally:

class insert_aiout_result(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/ai_shell/result.log')
        threading.Thread.__init__(self)
    def run(self):
        global AIOUT_CH, Backup_ai_jpg

        self.__logger.info("result start")
        time.sleep(6)
        conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "db")
        if "ai_daybook_en" in conf_dict:
            AI_daybook_en = int(conf_dict["ai_daybook_en"])
        else:
            AI_daybook_en = 0
        del conf_dict

        if 0 != AI_daybook_en:
            log_cur = get_a_sql_cur_forever(self.__logger, 'alglog')
        result_cur = get_a_sql_cur_forever(self.__logger)

        try:

            _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
            if "ai_shell" in _dic1:
                _version = _dic1["ai_shell"]
            else:
                stat = os.stat(__file__)
                _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
                del stat
            result_cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai_shell','%s')"
                        "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
            result_cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai','1.01')"
                        "ON DUPLICATE KEY UPDATE version='1.01'")


            del _version, _dic1
        except Exception, e:
            self.__logger.error(str(e))
            result_cur = get_a_sql_cur_forever(self.__logger)

        while True:

            try:
                msg = result_queue.get(block=True)
                _cam_id1, = struct.unpack("32s", msg[:32])
                _cam_id = str(_cam_id1.strip('\0'))[:-1]


                pic1, slot1 = struct.unpack("128sB", msg[32:161])
                _ai_pic = str(pic1.strip('\0'))

                del _cam_id1,  pic1

                # print binascii.hexlify(msg1[0][164:257])
                _slot_count, = struct.unpack("b", msg[160:161])
                _regionOut = struct.unpack('24i', msg[164:260])
                # print binascii.hexlify(msg1[0][260:264])
                _region_confidence = struct.unpack('3b', msg[260:263])
                # print binascii.hexlify(msg1[0][264:280])
                _state1 = struct.unpack('3i', msg[264:276])
                _car_count, = struct.unpack('b', msg[276:277])
                # print binascii.hexlify(msg1[0][280:376])
                _car_coord = struct.unpack('24i', msg[280:376])
                # print binascii.hexlify(msg1[0][376:380])
                _is_cross_line = struct.unpack('3b', msg[376:379])
                # print binascii.hexlify(msg1[0][380:572])
                _vlpr_coord = struct.unpack('48i', msg[380:572])
                # print binascii.hexlify(msg1[0][572:580])
                _slot_vlpr_confidence = struct.unpack('6b', msg[572:578])
                del msg
                body = json.dumps({"cam_id":_cam_id,"CMOS":0})
                _carPos = []
                _platePos = []
                _parkingLine = []
                _state = [1]*3
                for i in range(3):
                    _carPos.append(
                        [_car_coord[8 * i], _car_coord[8 * i + 1], _car_coord[8 * i + 6], _car_coord[8 * i + 7]])
                    if 1 != _state1[i]:
                        _state[i] = 0

                del _car_coord, _state1
                for i in range(6):
                    _platePos.append(
                        [_vlpr_coord[8 * i], _vlpr_coord[8 * i + 1], _vlpr_coord[8 * i + 6], _vlpr_coord[8 * i + 7]])
                del _vlpr_coord
                for i in range(24):
                    _parkingLine.append(_regionOut[i])
                del _regionOut

                try:
                    self.__logger.info("start sql with %s %s"%(_cam_id,_ai_pic))
                    _filename = _ai_pic[_ai_pic.rfind('/') + 1:]
                    _sql_str = "update aiouttable set pic_full_name='%s',LatestUpdate=now(),CarCount=%d,parking1State=%d," \
                               "parking2State=%d,parking3State=%d,parking1IsCrossLine=%d,parking2IsCrossLine=%d,parking3IsCrossLine=%d," \
                               % (_filename, _slot_count, _state[0], _state[1], _state[2], _is_cross_line[0],
                                  _is_cross_line[1], _is_cross_line[2])

                    _sql_str += "parkingLine1LTx=%d,parkingLine1LTy=%d,parkingLine1RTx=%d,parkingLine1RTy=%d," \
                                "parkingLine1LBx=%d,parkingLine1LBy=%d,parkingLine1RBx=%d,parkingLine1RBy=%d," \
                                "parkingLine2LTx=%d,parkingLine2LTy=%d,parkingLine2RTx=%d,parkingLine2RTy=%d," \
                                "parkingLine2LBx=%d,parkingLine2LBy=%d,parkingLine2RBx=%d,parkingLine2RBy=%d," \
                                "parkingLine3LTx=%d,parkingLine3LTy=%d,parkingLine3RTx=%d,parkingLine3RTy=%d," \
                                "parkingLine3LBx=%d,parkingLine3LBy=%d,parkingLine3RBx=%d,parkingLine3RBy=%d," \
                                % (_parkingLine[0], _parkingLine[1], _parkingLine[2], _parkingLine[3],
                                   _parkingLine[4], _parkingLine[5], _parkingLine[6], _parkingLine[7],
                                   _parkingLine[8], _parkingLine[9], _parkingLine[10], _parkingLine[11],
                                   _parkingLine[12], _parkingLine[13], _parkingLine[14], _parkingLine[15],
                                   _parkingLine[16], _parkingLine[17], _parkingLine[18], _parkingLine[19],
                                   _parkingLine[20], _parkingLine[21], _parkingLine[22], _parkingLine[23])
                    _sql_str += "parkingLine1Confidence=%d,parkingLine2Confidence=%d,parkingLine3Confidence=%d," \
                                "Car1posLTx=%d,Car1posLTy=%d,Car1posRBx=%d,Car1posRBy=%d," \
                                "Car2posLTx=%d,Car2posLTy=%d,Car2posRBx=%d,Car2posRBy=%d," \
                                "Car3posLTx=%d,Car3posLTy=%d,Car3posRBx=%d,Car3posRBy=%d," \
                                % (_region_confidence[0], _region_confidence[1], _region_confidence[2],
                                   _carPos[0][0], _carPos[0][1], _carPos[0][2], _carPos[0][3],
                                   _carPos[1][0], _carPos[1][1], _carPos[1][2], _carPos[1][3],
                                   _carPos[2][0], _carPos[2][1], _carPos[2][2], _carPos[2][3])
                    _sql_str += "plate1posLTx=%d,plate1posLTy=%d,plate1posRBx=%d,plate1posRBy=%d," \
                                "plate2posLTx=%d,plate2posLTy=%d,plate2posRBx=%d,plate2posRBy=%d," \
                                "plate3posLTx=%d,plate3posLTy=%d,plate3posRBx=%d,plate3posRBy=%d," \
                                "plate4posLTx=%d,plate4posLTy=%d,plate4posRBx=%d,plate4posRBy=%d," \
                                "plate5posLTx=%d,plate5posLTy=%d,plate5posRBx=%d,plate5posRBy=%d," \
                                "plate6posLTx=%d,plate6posLTy=%d,plate6posRBx=%d,plate6posRBy=%d," \
                                % (_platePos[0][0], _platePos[0][1], _platePos[0][2], _platePos[0][3],
                                   _platePos[1][0], _platePos[1][1], _platePos[1][2], _platePos[1][3],
                                   _platePos[2][0], _platePos[2][1], _platePos[2][2], _platePos[2][3],
                                   _platePos[3][0], _platePos[3][1], _platePos[3][2], _platePos[3][3],
                                   _platePos[4][0], _platePos[4][1], _platePos[4][2], _platePos[4][3],
                                   _platePos[5][0], _platePos[5][1], _platePos[5][2], _platePos[5][3])
                    _sql_str += "platePos1Confidence=%d,platePos2Confidence=%d,platePos3Confidence=%d," \
                                "platePos4Confidence=%d,platePos5Confidence=%d,platePos6Confidence=%d " \
                                "where cameraID='%s'" \
                                % (_slot_vlpr_confidence[0], _slot_vlpr_confidence[1], _slot_vlpr_confidence[2],
                                   _slot_vlpr_confidence[3], _slot_vlpr_confidence[4], _slot_vlpr_confidence[5],
                                   _cam_id)

                    result_cur.execute(_sql_str)

                    _sql_str = "update aiouttable2 set pic_full_name='%s',LatestUpdate=now(),CarCount=%d,parking1State=%d," \
                               "parking2State=%d,parking3State=%d,parking1IsCrossLine=%d,parking2IsCrossLine=%d,parking3IsCrossLine=%d," \
                               % (_filename, _slot_count, _state[0], _state[1], _state[2], _is_cross_line[0],
                                  _is_cross_line[1], _is_cross_line[2])

                    _sql_str += "parkingLine1LTx=%d,parkingLine1LTy=%d,parkingLine1RTx=%d,parkingLine1RTy=%d," \
                                "parkingLine1LBx=%d,parkingLine1LBy=%d,parkingLine1RBx=%d,parkingLine1RBy=%d," \
                                "parkingLine2LTx=%d,parkingLine2LTy=%d,parkingLine2RTx=%d,parkingLine2RTy=%d," \
                                "parkingLine2LBx=%d,parkingLine2LBy=%d,parkingLine2RBx=%d,parkingLine2RBy=%d," \
                                "parkingLine3LTx=%d,parkingLine3LTy=%d,parkingLine3RTx=%d,parkingLine3RTy=%d," \
                                "parkingLine3LBx=%d,parkingLine3LBy=%d,parkingLine3RBx=%d,parkingLine3RBy=%d," \
                                % (_parkingLine[0] * 8192 / 500, _parkingLine[1] * 8192 / 500,
                                   _parkingLine[2] * 8192 / 500, _parkingLine[3] * 8192 / 500,
                                   _parkingLine[4] * 8192 / 500, _parkingLine[5] * 8192 / 500,
                                   _parkingLine[6] * 8192 / 500, _parkingLine[7] * 8192 / 500,
                                   _parkingLine[8] * 8192 / 500, _parkingLine[9] * 8192 / 500,
                                   _parkingLine[10] * 8192 / 500, _parkingLine[11] * 8192 / 500,
                                   _parkingLine[12] * 8192 / 500, _parkingLine[13] * 8192 / 500,
                                   _parkingLine[14] * 8192 / 500, _parkingLine[15] * 8192 / 500,
                                   _parkingLine[16] * 8192 / 500, _parkingLine[17] * 8192 / 500,
                                   _parkingLine[18] * 8192 / 500, _parkingLine[19] * 8192 / 500,
                                   _parkingLine[20] * 8192 / 500, _parkingLine[21] * 8192 / 500,
                                   _parkingLine[22] * 8192 / 500, _parkingLine[23] * 8192 / 500)
                    _sql_str += "parkingLine1Confidence=%d,parkingLine2Confidence=%d,parkingLine3Confidence=%d," \
                                "Car1posLTx=%d,Car1posLTy=%d,Car1posRBx=%d,Car1posRBy=%d," \
                                "Car2posLTx=%d,Car2posLTy=%d,Car2posRBx=%d,Car2posRBy=%d," \
                                "Car3posLTx=%d,Car3posLTy=%d,Car3posRBx=%d,Car3posRBy=%d," \
                                % (_region_confidence[0], _region_confidence[1], _region_confidence[2],
                                   _carPos[0][0] * 8192 / 500, _carPos[0][1] * 8192 / 500, _carPos[0][2] * 8192 / 500,
                                   _carPos[0][3] * 8192 / 500,
                                   _carPos[1][0] * 8192 / 500, _carPos[1][1] * 8192 / 500, _carPos[1][2] * 8192 / 500,
                                   _carPos[1][3] * 8192 / 500,
                                   _carPos[2][0] * 8192 / 500, _carPos[2][1] * 8192 / 500, _carPos[2][2] * 8192 / 500,
                                   _carPos[2][3] * 8192 / 500)
                    _sql_str += "plate1posLTx=%d,plate1posLTy=%d,plate1posRBx=%d,plate1posRBy=%d," \
                                "plate2posLTx=%d,plate2posLTy=%d,plate2posRBx=%d,plate2posRBy=%d," \
                                "plate3posLTx=%d,plate3posLTy=%d,plate3posRBx=%d,plate3posRBy=%d," \
                                "plate4posLTx=%d,plate4posLTy=%d,plate4posRBx=%d,plate4posRBy=%d," \
                                "plate5posLTx=%d,plate5posLTy=%d,plate5posRBx=%d,plate5posRBy=%d," \
                                "plate6posLTx=%d,plate6posLTy=%d,plate6posRBx=%d,plate6posRBy=%d," \
                                % (_platePos[0][0] * 8192 / 500, _platePos[0][1] * 8192 / 500,
                                   _platePos[0][2] * 8192 / 500, _platePos[0][3] * 8192 / 500,
                                   _platePos[1][0] * 8192 / 500, _platePos[1][1] * 8192 / 500,
                                   _platePos[1][2] * 8192 / 500, _platePos[1][3] * 8192 / 500,
                                   _platePos[2][0] * 8192 / 500, _platePos[2][1] * 8192 / 500,
                                   _platePos[2][2] * 8192 / 500, _platePos[2][3] * 8192 / 500,
                                   _platePos[3][0] * 8192 / 500, _platePos[3][1] * 8192 / 500,
                                   _platePos[3][2] * 8192 / 500, _platePos[3][3] * 8192 / 500,
                                   _platePos[4][0] * 8192 / 500, _platePos[4][1] * 8192 / 500,
                                   _platePos[4][2] * 8192 / 500, _platePos[4][3] * 8192 / 500,
                                   _platePos[5][0] * 8192 / 500, _platePos[5][1] * 8192 / 500,
                                   _platePos[5][2] * 8192 / 500, _platePos[5][3] * 8192 / 500)
                    _sql_str += "platePos1Confidence=%d,platePos2Confidence=%d,platePos3Confidence=%d," \
                                "platePos4Confidence=%d,platePos5Confidence=%d,platePos6Confidence=%d " \
                                "where cameraID='%s'" \
                                % (_slot_vlpr_confidence[0], _slot_vlpr_confidence[1], _slot_vlpr_confidence[2],
                                   _slot_vlpr_confidence[3], _slot_vlpr_confidence[4], _slot_vlpr_confidence[5],
                                   _cam_id)

                    result_cur.execute(_sql_str)
                    if 0 != AI_daybook_en:
                        self.__logger.debug("AI daybook")
                        localtime1 = time.localtime()
                        ailog_table = "ailog%d%02d%02d" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)

                        del localtime1
                        _sql_str = "insert into %s(aijpgname,JpgLatestUpdate,cameraID,cmosID,CarCount,parking1State," \
                                   "parking2State,parking3State,parking1IsCrossLine,parking2IsCrossLine,parking3IsCrossLine," \
                                   "parkingLine1LTx,parkingLine1LTy,parkingLine1RTx,parkingLine1RTy," \
                                   "parkingLine1LBx,parkingLine1LBy,parkingLine1RBx,parkingLine1RBy," \
                                   "parkingLine2LTx,parkingLine2LTy,parkingLine2RTx,parkingLine2RTy," \
                                   "parkingLine2LBx,parkingLine2LBy,parkingLine2RBx,parkingLine2RBy," \
                                   "parkingLine3LTx,parkingLine3LTy,parkingLine3RTx,parkingLine3RTy," \
                                   "parkingLine3LBx,parkingLine3LBy,parkingLine3RBx,parkingLine3RBy," \
                                   "parkingLine1Confidence,parkingLine2Confidence,parkingLine3Confidence," \
                                   "Car1posLTx,Car1posLTy,Car1posRBx,Car1posRBy," \
                                   "Car2posLTx,Car2posLTy,Car2posRBx,Car2posRBy," \
                                   "Car3posLTx,Car3posLTy,Car3posRBx,Car3posRBy," \
                                   "plate1posLTx,plate1posLTy,plate1posRBx,plate1posRBy," \
                                   "plate2posLTx,plate2posLTy,plate2posRBx,plate2posRBy," \
                                   "plate3posLTx,plate3posLTy,plate3posRBx,plate3posRBy," \
                                   "plate4posLTx,plate4posLTy,plate4posRBx,plate4posRBy," \
                                   "plate5posLTx,plate5posLTy,plate5posRBx,plate5posRBy," \
                                   "plate6posLTx,plate6posLTy,plate6posRBx,plate6posRBy," \
                                   "platePos1Confidence,platePos2Confidence,platePos3Confidence," \
                                   "platePos4Confidence,platePos5Confidence,platePos6Confidence" \
                                   ")values('%s',now(),'%s',0,%d,%d,%d,%d, %d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d," \
                                   "%d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d, %d,%d,%d,%d," \
                                   "%d,%d,%d,%d, %d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d," \
                                   "%d,%d,%d,%d,%d,%d,%d,%d, %d,%d,%d,%d,%d,%d)" \
                                   % (ailog_table, _filename, _cam_id,  _slot_count, _state[0],
                                      _state[1], _state[2],
                                      _is_cross_line[0], _is_cross_line[1], _is_cross_line[2],
                                      _parkingLine[0], _parkingLine[1], _parkingLine[2], _parkingLine[3],
                                      _parkingLine[4], _parkingLine[5], _parkingLine[6], _parkingLine[7],
                                      _parkingLine[8], _parkingLine[9], _parkingLine[10], _parkingLine[11],
                                      _parkingLine[12], _parkingLine[13], _parkingLine[14], _parkingLine[15],
                                      _parkingLine[16], _parkingLine[17], _parkingLine[18], _parkingLine[19],
                                      _parkingLine[20], _parkingLine[21], _parkingLine[22], _parkingLine[23],
                                      _region_confidence[0], _region_confidence[1], _region_confidence[2],
                                      _carPos[0][0], _carPos[0][1], _carPos[0][2], _carPos[0][3],
                                      _carPos[1][0], _carPos[1][1], _carPos[1][2], _carPos[1][3],
                                      _carPos[2][0], _carPos[2][1], _carPos[2][2], _carPos[2][3],
                                      _platePos[0][0], _platePos[0][1], _platePos[0][2], _platePos[0][3],
                                      _platePos[1][0], _platePos[1][1], _platePos[1][2], _platePos[1][3],
                                      _platePos[2][0], _platePos[2][1], _platePos[2][2], _platePos[2][3],
                                      _platePos[3][0], _platePos[3][1], _platePos[3][2], _platePos[3][3],
                                      _platePos[4][0], _platePos[4][1], _platePos[4][2], _platePos[4][3],
                                      _platePos[5][0], _platePos[5][1], _platePos[5][2], _platePos[5][3],
                                      _slot_vlpr_confidence[0], _slot_vlpr_confidence[1], _slot_vlpr_confidence[2],
                                      _slot_vlpr_confidence[3], _slot_vlpr_confidence[4], _slot_vlpr_confidence[5])
                        try:
                            log_cur.execute(_sql_str)
                        except Exception, e:
                            self.__logger.error("log_cur:"+str(e))
                            if 'MySQL server has gone away' in str(e):
                                log_cur = get_a_sql_cur_forever(self.__logger, 'alglog')
                        self.__logger.info("end sql")
                        if '1' == Backup_ai_jpg:
                            draw_queue.put(json.dumps({"cam_id":_cam_id,"aifile":_filename, "now":time.time()}))
                except Exception, e:
                    self.__logger.error(_sql_str)
                    self.__logger.error(str(e))
                    self.__logger.error(body)
                    if 'MySQL server has gone away' in str(e):
                        result_cur = get_a_sql_cur_forever(self.__logger)
                    continue
                del _ai_pic,_carPos,_parkingLine,_platePos,_sql_str
            except Exception,e:
                self.__logger.error(str(e))
                continue

            try:
                self.__logger.debug("rabbitmq publish:AIout " + body)
                AIOUT_CH.basic_publish(body=body, exchange="AiOut.tr", properties=msg_props,
                                       routing_key="place queue")
            except Exception,e:
                self.__logger.error(str(e))
                self.__logger.error(body)
                AIOUT_CH = get_placeOUT_rabbitmq_channel()

class draw_jpg_lines(threading.Thread):
    def __init__(self, idnum):

        self.__logger = wtclib.create_logging('../log/ai_shell/draw.log')
        threading.Thread.__init__(self)
    def run(self):
        self.__logger.info("draw start")
        draw_cur = get_a_sql_cur_forever(self.__logger)

        while True:
            try:
                msg = draw_queue.get(block=True)
                _dic_info = json.loads(msg)
                self.__logger.info("draw " + _dic_info["aifile"] + " with " + _dic_info["cam_id"])
                if time.time() - _dic_info['now'] < 0.5:
                    time.sleep(0.5)#sleep and wait the jpg file is there for draw

                localtime1 = time.localtime()
                _path = "../../ai/jpg/%d%02d%02d/%02d/%s/"%(localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday,
                                                                4*(localtime1.tm_hour/4),_dic_info["cam_id"])
                (_file,_ext)=os.path.splitext(str(_dic_info["aifile"]))
                _filename = "%s*.jpg"%_file
                _find_file = glob.glob(_path+_filename)
                if 0 == len(_find_file) :
                    self.__logger.info("find None with " + _path+_filename)
                    continue
                if len(_find_file) > 1 :
                    self.__logger.info("%d file "%len(_find_file)+_find_file[0])
                    continue

                _sql_str = "select * from  aiouttable where cameraID='%s'" % (_dic_info["cam_id"])
                if 0 == draw_cur.execute(_sql_str):
                    continue
                _info = draw_cur.fetchone()
                self.__logger.info("draw " + _find_file[0])
                img = Image.open(_find_file[0])
                draw = ImageDraw.Draw(img)
                for i in range(_info[4]):
                    if 1 == _info[5+i]:
                        draw.line((_info[38+4*i],_info[39+4*i],_info[40+4*i],_info[39+4*i]), fill=0xFF)
                        draw.line((_info[38+4*i], _info[39+4*i], _info[38+4*i], _info[41+4*i]), fill=0xFF)
                        draw.line((_info[38+4*i], _info[41+4*i], _info[40+4*i], _info[41+4*i]), fill=0xFF)
                        draw.line((_info[40+4*i], _info[39+4*i], _info[40+4*i], _info[41+4*i]), fill=0xFF)
                    draw.line((_info[11 + 8 * i], _info[12 + 8 * i], _info[13 + 8 * i], _info[14 + 8 * i]), fill=0xFFFFFF)
                    draw.line((_info[11 + 8 * i], _info[12 + 8 * i], _info[15 + 8 * i], _info[16 + 8 * i]), fill=0xFFFFFF)
                    draw.line((_info[13 + 8 * i], _info[14 + 8 * i], _info[17 + 8 * i], _info[18 + 8 * i]), fill=0xFFFFFF)
                    draw.line((_info[15 + 8 * i], _info[16 + 8 * i], _info[17 + 8 * i], _info[18 + 8 * i]), fill=0xFFFFFF)

                if 1 == _info[8] and 1 == _info[9]:
                    draw.line((_info[13], _info[14], _info[17], _info[18]),fill=0xFF)  # red
                    draw.line((_info[19], _info[20], _info[23], _info[24]),fill=0xFF)
                if 1 == _info[10] and 1 == _info[9]:
                    draw.line((_info[21], _info[22], _info[25], _info[26]),fill=0xFF)  # red
                    draw.line((_info[27], _info[28], _info[31], _info[32]),fill=0xFF)
                for i in range(_info[4]*2):
                    if 0 == _info[50+4*i] and 0 == _info[51+4*i] and 0 == _info[52+4*i] and 0 == _info[53+4*i]:
                        continue
                    draw.line((_info[50 + 4 * i], _info[51 + 4 * i], _info[52 + 4 * i], _info[51 + 4 * i]), fill=0xFF00)#green
                    draw.line((_info[50 + 4 * i], _info[51 + 4 * i], _info[50 + 4 * i], _info[53 + 4 * i]), fill=0xFF00)
                    draw.line((_info[50 + 4 * i], _info[53 + 4 * i], _info[52 + 4 * i], _info[53 + 4 * i]), fill=0xFF00)
                    draw.line((_info[52 + 4 * i], _info[51 + 4 * i], _info[52 + 4 * i], _info[53 + 4 * i]), fill=0xFF00)
                img.save(_find_file[0])
                del draw, img, localtime1
            except Exception, e:
                self.__logger.error(_sql_str)
                self.__logger.error(str(e)+' %s'%_find_file[0])
                if 'MySQL server has gone away' in str(e):
                    draw_cur = get_a_sql_cur_forever(self.__logger)



def get_a_sql_cur_forever(mylog, db_name=None):
    while True:
        if None == db_name:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        else:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf", dbn=db_name)
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur




def create_daybook_log_table(_timet=None):
    global mylogger
    if None == _timet:
        localtime1 = time.localtime()
    else:
        localtime1 = time.localtime(time.time()+_timet)
    try:
        while True:
            (cur, conn) = wtclib.get_a_sql_cur("../conf/conf.conf", dbn='alglog')
            if None != cur:
                break
            else:
                mylogger.info(conn)
                time.sleep(20)
        cur.execute("create table if not exists ailog%d%02d%02d("
                "aijpgname varchar(128) primary key,"
                "JpgLatestUpdate DATETIME,"
                "cameraID varchar(24), "
                "cmosID tinyint,"
                "CarCount tinyint, "
                "parking1State tinyint, "
                "parking2State tinyint, "
                "parking3State tinyint, "
                "parking1IsCrossLine tinyint, "
                "parking2IsCrossLine tinyint, "
                "parking3IsCrossLine tinyint,"
                "parkingLine1LTx smallint default 0, "
                "parkingLine1LTy smallint default 0, "
                "parkingLine1RTx smallint default 0, "
                "parkingLine1RTy smallint default 0, "
                "parkingLine1LBx smallint default 0, "
                "parkingLine1LBy smallint default 0, "
                "parkingLine1RBx smallint default 0, "
                "parkingLine1RBy smallint default 0, "
                "parkingLine2LTx smallint default 0, "
                "parkingLine2LTy smallint default 0, "
                "parkingLine2RTx smallint default 0, "
                "parkingLine2RTy smallint default 0, "
                "parkingLine2LBx smallint default 0, "
                "parkingLine2LBy smallint default 0, "
                "parkingLine2RBx smallint default 0, "
                "parkingLine2RBy smallint default 0, "
                "parkingLine3LTx smallint default 0, "
                "parkingLine3LTy smallint default 0, "
                "parkingLine3RTx smallint default 0, "
                "parkingLine3RTy smallint default 0, "
                "parkingLine3LBx smallint default 0, "
                "parkingLine3LBy smallint default 0, "
                "parkingLine3RBx smallint default 0, "
                "parkingLine3RBy smallint default 0, "
                "parkingLine1Confidence smallint, "
                "parkingLine2Confidence smallint, "
                "parkingLine3Confidence smallint, "
                "Car1posLTx smallint, "
                "Car1posLTy smallint, "
                "Car1posRBx smallint, "
                "Car1posRBy smallint, "
                "Car2posLTx smallint, "
                "Car2posLTy smallint, "
                "Car2posRBx smallint, "
                "Car2posRBy smallint, "
                "Car3posLTx smallint, "
                "Car3posLTy smallint, "
                "Car3posRBx smallint, "
                "Car3posRBy smallint, "

                "plate1posLTx smallint, "
                "plate1posLTy smallint, "
                "plate1posRBx smallint, "
                "plate1posRBy smallint, "
                "plate2posLTx smallint, "
                "plate2posLTy smallint, "
                "plate2posRBx smallint, "
                "plate2posRBy smallint, "
                "plate3posLTx smallint, "
                "plate3posLTy smallint, "
                "plate3posRBx smallint, "
                "plate3posRBy smallint, "
                "plate4posLTx smallint, "
                "plate4posLTy smallint, "
                "plate4posRBx smallint, "
                "plate4posRBy smallint, "
                "plate5posLTx smallint, "
                "plate5posLTy smallint, "
                "plate5posRBx smallint, "
                "plate5posRBy smallint, "
                "plate6posLTx smallint, "
                "plate6posLTy smallint, "
                "plate6posRBx smallint, "
                "plate6posRBy smallint, "
                "platePos1Confidence smallint, "
                "platePos2Confidence smallint, "
                "platePos3Confidence smallint, "
                "platePos4Confidence smallint, "
                "platePos5Confidence smallint, "
                "platePos6Confidence smallint, "

                "reyuv1name varchar(128),"
                "plate1Number varchar(32),"
                "plate1confidence smallint,"
                "plate1brightness smallint,"
                "plate1stable smallint,"
                "stableplate1number varchar(32),"
                "plate1updateTimet DATETIME, "
                "reyuv2name varchar(128),"
                "plate2Number varchar(32),"
                "plate2confidence smallint,"
                "plate2brightness smallint,"
                "plate2stable smallint,"
                "stableplate2number varchar(32),"
                "plate2updateTimet DATETIME, "
                "reyuv3name varchar(128),"
                "plate3Number varchar(32),"
                "plate3confidence smallint,"
                "plate3brightness smallint,"
                "plate3stable smallint,"
                "stableplate3number varchar(32),"
                "plate3updateTimet DATETIME, "
                "LampStatus varchar(32)"
                ")engine=MyISAM" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday))
        conn.close()
    except Exception,e:
        mylogger.error(str(e))

MSG_send_error_cnt = 0

def clear_reset_AI():
    global msgsnd_ipc, mylogger, MSG_send_error_cnt
    try:
        mylogger.error("killall AI")
        os.system("killall AI")

        while True:
            try:
                msgsnd_ipc.receive(block=False,type=0)
            except Exception,e:
                mylogger.error(str(e))
                break
        time.sleep(0.5)
        cmd1 = "./AI &"
        thread.start_new_thread(python_cmd, (cmd1,))
        MSG_send_error_cnt = 0
        mylogger.error("restart AI")
        time.sleep(5)
        os.system("rabbitmqctl purge_queue place.in")
    except Exception,e:
        mylogger.error(str(e))

rabbitmq_publish_timet = int(time.time())

def msg_consumer(channel, method, header, body):
    global mylogger,  msg_props, interval_sec,AIOUT_CH,msgsnd_ipc, msgrcv_ipc,MSG_send_error_cnt,rabbitmq_publish_timet
    mylogger.info("receive mq")
    channel.basic_ack(delivery_tag=method.delivery_tag)
    _timeSec = int(time.time())
    #wdi()

    mylogger.info("mq ack" + body)
    try:
        _dic_info = json.loads(body)
    except Exception, e:
        mylogger.warning(str(e))
        mylogger.warning("len=%d"%len(body))
        mylogger.warning("msg="+body)
        return
    if "quit" in _dic_info:
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()
        mylogger.debug("quit")
    #mylogger.debug(body)
    if not "cam_id" in _dic_info:
        mylogger.debug("not cam_id in _dic_info")
        mylogger.debug("rabbitmq publish:AIout " + body)
        try:
            AIOUT_CH.basic_publish(body=body, exchange="AiOut.tr", properties=msg_props,
                                   routing_key="place queue")
        except Exception,e:
            mylogger.error(str(e))
            AIOUT_CH = get_placeOUT_rabbitmq_channel()
        rabbitmq_publish_timet = int(time.time())
        return
    if not "time_now" in _dic_info:
        mylogger.warning("no time_now:%s"%body)
    else:
        if _timeSec - _dic_info["time_now"] > 5 :
            if _timeSec - rabbitmq_publish_timet > 8:
                mylogger.info("%s timeout,where now is %d, msg time is %d"%(_dic_info["cam_id"],_timeSec,_dic_info["time_now"]))
                _timeout_dic = {"msg": "mq time=%d, now is %d, %d seconds late" % (
                _dic_info["time_now"], _timeSec, _timeSec - _dic_info["time_now"])}
                _timeout_str = json.dumps(_timeout_dic)
                mylogger.debug("rabbitmq publish:AIout " + _timeout_str)
                title_queue.put(body)
                try:
                    AIOUT_CH.basic_publish(body=_timeout_str, exchange="AiOut.tr", properties=msg_props,
                                           routing_key="place queue")
                except Exception, e:
                    mylogger.error(str(e))
                    AIOUT_CH = get_placeOUT_rabbitmq_channel()
                rabbitmq_publish_timet = int(time.time())
            return

    if not "CMOS" in _dic_info:
        mylogger.debug("not CMOS in _dic_info")
        return
    if not type(_dic_info["CMOS"])==int:
        mylogger.debug("not type CMOS is int")
        return
    _cmos = _dic_info["CMOS"]
    #mylogger.info("befor queue.put")


    mylogger.info("start pack")
    try:
        cam_id = str("%s%d"%(_dic_info["cam_id"],_cmos))
        if str(_dic_info["cam_id"]) not in AI_settings:
            mylogger.warning(str(_dic_info["cam_id"]) + ' not is aisetting')
            return
        title_queue.put(body)
        _ai_setting = AI_settings[str(_dic_info["cam_id"])]

        slot_count = _ai_setting[3]
        slot_install = _ai_setting[4]
        slot_bitmap = _ai_setting[5]
        is_manual = _ai_setting[6]

        slot_region = [_ai_setting[i]*5 for i in range(7,31)]  # ; // 12

        pic_type = 1  # ; //
        pic_w = 500  # ; //
        pic_h = 500  # ;
        del _ai_setting

        region0 = struct.pack('24i', *[slot_region[i] for i in range(24)])

        msg0 = struct.pack('32s128s4b', cam_id, str(_dic_info['pic_full_name']), slot_count, slot_install, slot_bitmap, is_manual)
        #print binascii.hexlify(msg0)
        msg2 = struct.pack('3i', pic_type, pic_w, pic_h)
        msg = msg0 + region0 + msg2
        mylogger.info("end pack")
        #q2 = sysv_ipc.MessageQueue(16842753, flags=sysv_ipc.IPC_CREAT)

        try:
            msgsnd_ipc.send(msg, type=0xa004)
        except Exception, e:
            mylogger.error(str(e))
            MSG_send_error_cnt += 1
            if MSG_send_error_cnt > 30:
                clear_reset_AI()
            return
        #q3 = sysv_ipc.MessageQueue(50397185, flags=sysv_ipc.IPC_CREAT)
        del slot_region,msg0,msg,msg2,region0
        _sleepCnt = 120
        mylogger.info("start recv")
        while _sleepCnt > 0:
            time.sleep(0.045)
            try:
                msg1 = msgrcv_ipc.receive(block=False, type=0xa005)
                """
                _cam_id1, = struct.unpack("32s", msg1[0][:32])
                _cam_id2 = str(_cam_id1.strip('\0'))
                if 0 != cmp(_cam_id2, cam_id):
                    mylogger.warning("send ID is %s, receive ID is %s" % (cam_id, _cam_id2))
                else:
                    break
                """
                break
            except Exception,e:
                #mylogger.debug(str(e))
                pass
            _sleepCnt -= 1

        mylogger.info("recv end with %d ms"%((120-_sleepCnt)*45))
        if _sleepCnt > 0:
            result_queue.put(msg1[0])

        else:
            mylogger.warning("AI ipc recv None in 5 seconds and cnt=%d"%MSG_send_error_cnt)
            body = json.dumps({"aimsg":"receive timeout"})
            MSG_send_error_cnt += 1
            if MSG_send_error_cnt > 30:
                clear_reset_AI()
            mylogger.debug("rabbitmq publish:AIout " + body)
            AIOUT_CH.basic_publish(body=body, exchange="AiOut.tr", properties=msg_props,
                               routing_key="place queue")
            rabbitmq_publish_timet = int(time.time())

    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(body)
        AIOUT_CH = get_placeOUT_rabbitmq_channel()

    mylogger.info("end process")
    return


def get_placeOUT_rabbitmq_channel():
    global mylogger
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "aioutmq_server_addr" in conf_dict:
        _mq_host = conf_dict["aioutmq_server_addr"]
    else:
        _mq_host = "localhost"
    if "aioutmq_server_port" in conf_dict:
        _mq_port = int(conf_dict["aioutmq_server_port"])
    else:
        _mq_port = 5672
    if "aioutmq_user_name" in conf_dict:
        _mq_user_name = conf_dict["aioutmq_user_name"]
    else:
        _mq_user_name = "cpf"
    if "aioutmq_passwd" in conf_dict:
        _mq_passwd = conf_dict["aioutmq_passwd"]
    else:
        _mq_passwd = "cpf"
    if "aioutmq_vhost" in conf_dict:
        _mq_vhost = conf_dict["aioutmq_vhost"]
    else:
        _mq_vhost = "OutTrig"


    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="AiOut.tr", exchange_type="fanout",
                             passive=False, durable=False, auto_delete=True)
    return channel




def get_place_rabbitmq_channel():
    global mylogger
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "placemq_server_addr" in conf_dict:
        _mq_host = conf_dict["placemq_server_addr"]
    else:
        _mq_host = "localhost"
    if "placemq_server_port" in conf_dict:
        _mq_port = int(conf_dict["placemq_server_port"])
    else:
        _mq_port = 5672

    if "placemq_user_name" in conf_dict:
        _mq_user_name = conf_dict["placemq_user_name"]
    else:
        _mq_user_name = "guest"
    if "placemq_passwd" in conf_dict:
        _mq_passwd = conf_dict["placemq_passwd"]
    else:
        _mq_passwd = "guest"

    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host='/', credentials=credentials)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    try:
        channel = conn_broker.channel()
        channel.exchange_declare(exchange="place", exchange_type="direct",
                                 passive=False, durable=False, auto_delete=False)
        #channel.exchange_declare(exchange="place",exchange_type="direct", passive=False, durable=False, auto_delete=True)
        channel.queue_declare(queue="place.in")
        channel.queue_bind(queue="place.in", exchange='place',routing_key="place queue")
    except Exception, e:
        mylogger.info(str(e))

    channel.basic_consume(msg_consumer, queue="place.in", consumer_tag="place queue1")
    return channel


def python_cmd(cmd):
    str1 = "@%d"%(os.getpid())
    print cmd + str1
    os.system(cmd)
    #os.system("pause")
    time.sleep(0.5)

if __name__ == '__main__':
    if not os.path.isdir("../log/ai_shell"):
        try:
            os.mkdir("../log/ai_shell")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/ai_shell/ai_shell.log")
    mylogger.info("start running")

    _dic1 = wtclib.get_user_config_ret_dict("../conf/conf.conf", "file_save")
    if "backup_ai_jpg" in _dic1:
        Backup_ai_jpg = _dic1["backup_ai_jpg"]
    else:
        Backup_ai_jpg = '0'
    if "backup_re_jpg" in _dic1:
        Backup_re_jpg = _dic1["backup_re_jpg"]
    else:
        Backup_re_jpg = '0'
    del _dic1



    try:
        _pipe = os.popen("ps aux|grep AI")
        _pipe_data = _pipe.read()
        _pipe.close()
        print _pipe_data
        _retV = _pipe_data.strip("\n").split('\n')
        print _retV[0]
        if len(_retV) > 2:
            os.system("killall AI")
            print "kill AI"
        cmd1 = "./ftok &"
        thread.start_new_thread(python_cmd, (cmd1,))
        cmd1 = "./AI &"
        thread.start_new_thread(python_cmd, (cmd1,))
        print "start AI"
        time.sleep(1)
        fp = open('key.txt')
        fpd = fp.read()
        fp.close()
        _dic1 = json.loads(fpd)

        msgsnd_ipc = sysv_ipc.MessageQueue(int(_dic1["send"]), flags=sysv_ipc.IPC_CREAT)
        msgrcv_ipc = sysv_ipc.MessageQueue(int(_dic1["recv"]), flags=sysv_ipc.IPC_CREAT)
        while True:  # clear ipc msg
            time.sleep(1)
            try:
                msgrcv_ipc.receive(block=False, type=0)
            except:
                break
        del fp, fpd, _dic1


        sync_data_from_HDD(1).start()
        insert_aiout_title(2).start()
        insert_aiout_result(3).start()
        if '1' == Backup_ai_jpg:
            draw_jpg_lines(4).start()
        time.sleep(5)
        os.system("rabbitmqctl purge_queue place.in")
        del _pipe, _pipe_data,_retV,cmd1
    except Exception,e:
        mylogger.error(str(e))



    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"


    while True:
        channel = get_place_rabbitmq_channel()
        AIOUT_CH = get_placeOUT_rabbitmq_channel()
        try:
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))

