import ConfigParser
import os
import shutil
import sys
import time
import tarfile

import wtclib
import glob

def get_a_sql_cur_forever(db_name=None):
    global mylogger
    while True:
        if None == db_name:
            (_cur, conn_err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        else:
            (_cur, conn_err) = wtclib.get_a_sql_cur("../conf/conf.conf", db_name)
        if None != _cur:
            break
        else:
            mylogger.info(conn_err)
            time.sleep(20)
    return _cur, conn_err


if __name__ == '__main__':
    if not os.path.isdir("../log/rmfilelog"):
        try:
            os.mkdir("../log/rmfilelog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/rmfilelog/rmfile.log")
    mylogger.info("start running")

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "file_save")
    if "root_dir" in conf_dict:
        root_dir = conf_dict["root_dir"]
    else:
        #s = os.getcwd()
        #root_dir = s[:s[0:s.rfind('/')].rfind('/')]
        #del s
        root_dir = "../.."
    if "fullsize_pic_save_days" in conf_dict and conf_dict["fullsize_pic_save_days"].isdigit():
        fullsize_days = int(conf_dict["fullsize_pic_save_days"])
    else:
        fullsize_days = 30
    if "ai_littlesize_pic_save_days" in conf_dict  and conf_dict["ai_littlesize_pic_save_days"].isdigit():
        aisize_days = int(conf_dict["ai_littlesize_pic_save_days"])
    else:
        aisize_days = 30

    if "video_save_days" in conf_dict and conf_dict["video_save_days"].isdigit():
        video_days = int(conf_dict["video_save_days"])
    else:
        video_days = 30

    hdd_free_GB = 300
    if "hdd_free_gb" in conf_dict  and conf_dict["hdd_free_gb"].isdigit():
        hdd_free_GB = int(conf_dict["hdd_free_gb"])
    if hdd_free_GB < 300:
        hdd_free_GB = 300
    del conf_dict

    #timet = time.time()

    #dirs = os.listdir(os.getcwd())
    #print dirs
    sql_dir = os.path.join(root_dir, "ai/sql_log")
    if not os.path.isdir(sql_dir):
        try:
            os.mkdir(sql_dir)
        except Exception, e:
            mylogger.error(str(e))
            os._exit(1)

    local = time.localtime(time.time() - 24 * 3600)

    timenow = time.localtime()
    while True:
        hddinfo = os.statvfs("/")
        if not os.path.isdir(root_dir):
            time.sleep(3600)
            continue
        mylogger.info("HDD free %d GB" % (hddinfo.f_bfree * hddinfo.f_bsize / 1024 / 1024 / 1024))
        if hddinfo.f_bfree*hddinfo.f_bsize/1024/1024/1024 < hdd_free_GB:
            if os.path.isdir(root_dir+'/ai/save_img'):
                for snpath, dayname, filenames in os.walk(root_dir+'/ai/save_img'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname)/10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath,dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time() - _rm_time))
                        time.sleep(10)
                    """
                    oldtime = time.localtime(time.time()-aisize_days*24*3600)
                    daystr = "%04d%02d%02d"%(oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
                    for daypath in dir_sort:
                        if daypath < daystr:
                            shutil.rmtree(snpath+'/'+daypath)
                        else:
                            break
                    """
            if os.path.isdir(root_dir+'/ai/save_log'):
                for snpath, dayname, filenames in os.walk(root_dir+'/ai/save_log'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname)/10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath,dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time() - _rm_time))
                        time.sleep(10)


            snpath = os.path.join(root_dir, 'ai/sql_log')
            if os.path.isdir(snpath):
                filenames = os.listdir(snpath)
                mylogger.info("remove ai/sql_log/ files")
                if len(filenames) > 10:
                    dir_sort = sorted(filenames)
                    for i in range(len(filenames) / 10):
                        os.remove(os.path.join(snpath, dir_sort[i]))
                        time.sleep(2)
                    """
                    oldtime = time.localtime(time.time()-aisize_days*24*3600)
                    daystr = "%04d%02d%02d"%(oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
                    for daypath in dir_sort:
                        if daypath < daystr:
                            shutil.rmtree(snpath+'/'+daypath)
                    """
            snpath = os.path.join(root_dir, 'ai/jpg')
            if os.path.isdir(snpath):
                filenames = os.listdir(snpath)
                mylogger.info("remove ai/jpg/ files")
                if len(filenames) > 10:
                    dir_sort = sorted(filenames)
                    for i in range(len(filenames) / 10):
                        os.remove(os.path.join(snpath, dir_sort[i]))
                        time.sleep(2)

            if os.path.isdir(root_dir+ '/re/save_orig_yuv'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/save_orig_yuv'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time() - _rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/save_orig_jpg'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/save_orig_jpg'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time() - _rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/save_no_result_yuv'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/save_no_result_yuv'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/save_no_result_jpg'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/save_no_result_jpg'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/jpg'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/jpg'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/yuv'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/yuv'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)

            if os.path.isdir(root_dir+ '/re/un_jpg'):
                for snpath, dayname, filenames1 in os.walk(root_dir+'/re/un_jpg'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(filenames1) > 10:
                    filenames = sorted(filenames1)
                    for i in range(len(filenames1)-10):
                        os.remove(os.path.join(snpath, filenames[i]))
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)
            if os.path.isdir(root_dir+ '/re/un_yuv'):
                for snpath, dayname, filenames in os.walk(root_dir+'/re/un_yuv'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 10:
                    dir_sort = sorted(dayname)
                    for i in range(len(dayname) / 10):
                        _rm_time = time.time()
                        shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                        mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                        time.sleep(10)

            if os.path.isdir(root_dir+ '/video'):
                for snpath, dayname, filenames in os.walk(root_dir+'/video'):
                    mylogger.info(snpath)
                    print dayname
                    break
                if len(dayname) > 8:
                    try:
                        dir_sort = sorted(dayname)
                        for i in range(len(dayname) / 8):
                            _rm_time = time.time()
                            shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                            mylogger.info("rm %s, use %f sec" % (dir_sort[i], time.time()-_rm_time))
                            time.sleep(10)

                        del dir_sort
                    except Exception, e:
                        mylogger.error(str(e))

        del hddinfo

        if os.path.isdir(root_dir+ '/orig'):
            for snpath, dayname, filenames in os.walk(root_dir+'/orig'):
                mylogger.info(snpath)
                print dayname
                break
            if len(dayname) > 10:
                dir_sort = sorted(dayname)
                for i in range(len(dayname) / 10):
                    shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                    mylogger.info("rm %s" % dir_sort[i])
                    time.sleep(10)

                    del dir_sort
                del snpath, dayname, filenames
        snpath = '../log/'
        if os.path.isdir(snpath):
            _filename = "ucmq_log_*.log"
            _find_file = glob.glob(snpath+_filename)
            if len(_find_file) > 2:
                dir_sort = sorted(_find_file)
                for i in range(len(_find_file) - 2):
                    os.remove(dir_sort[i])
                    mylogger.info("remove "+dir_sort[i])


        while True:
            timeCur = time.localtime()
            if timeCur.tm_mday != timenow.tm_mday:
                timenow = timeCur
                break
            else:
                local = time.localtime(time.time() - 180 * 24 * 3600)
                if 1 == local.tm_hour:
                    cur, conn = get_a_sql_cur_forever('alglog')
                    cur.execute("show tables")
                    _tables = sorted(cur.fetchall())
                    _int_old = int('%d%02d%02d' % (local.tm_year, local.tm_mon, local.tm_mday))
                    for _table in _tables:
                        if 'ailog' in _table[0]:
                            try:
                                _int1 = int(_table[0][5:])
                                if _int1 < _int_old:
                                    cur.execute("drop table %s" % _table[0])
                            except Exception, e:
                                mylogger.error(str(e))
                            continue
                        if 'video_log' in _table[0]:
                            try:
                                _int1 = int(_table[0][10:])
                                if _int1 < _int_old:
                                    cur.execute("drop table %s" % _table[0])
                            except Exception, e:
                                mylogger.error(str(e))
                    conn.close()
                del local, cur, conn
                hddinfo = os.statvfs("/")
                mylogger.info("HDD free %d GB" % (hddinfo.f_bfree * hddinfo.f_bsize / 1024 / 1024 / 1024))
                if hddinfo.f_bfree * hddinfo.f_bsize / 1024 / 1024 / 1024 < 200:
                    if os.path.isdir(root_dir + '/video'):
                        for snpath, dayname, filenames in os.walk(root_dir + '/video'):
                            mylogger.info(snpath)
                            #print dayname
                            break
                        if 0 != len(dayname):
                            try:
                                dir_sort = sorted(dayname)
                                for i in range(len(dayname) / 2):
                                    _rm_time = time.time()
                                    shutil.rmtree(os.path.join(snpath, dir_sort[i]))
                                    _rm_end_time = time.time()
                                    mylogger.info("rm %s, use %f sec" % (dir_sort[i], _rm_end_time-_rm_time))

                                    if hddinfo.f_bfree * hddinfo.f_bsize / 1024 / 1024 / 1024 > 200:
                                        break
                                    time.sleep(10)
                            except Exception, e:
                                mylogger.error(str(e))
                            finally:

                                del dir_sort,dayname
                del hddinfo

            time.sleep(3500)
