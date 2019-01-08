import ConfigParser
import os
import time

from bin import wtclib


def get_save_days():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("conf.conf")
    except Exception, e:
        mylogger.error(str(e)+ ' read')
        return {"ret":0,"err":str(e)}
    secs = cf.sections()
    try:
        opts = cf.options("file_save")
    except Exception, e:
        mylogger.error(str(e) + ' file_save')
        return {"ret": 0, "err": str(e)}

    try:
        root_dir = cf.get("file_save", "root_dir")
        fullsize_days = cf.getint("file_save", "fullsize_pic_save_days")
        aisize_days = cf.getint("file_save", "ai_littlesize_pic_save_days")
    except Exception, e:
        mylogger.error(str(e) + ' get ucmq')
        return {"ret": 0, "err": str(e)}
    return {"ret":1, "root_dir": root_dir, "fullsizeD": fullsize_days, "aisizeD": aisize_days}

if __name__ == '__main__':
    if not os.path.isdir("rmfilelog"):
        try:
            os.mkdir("rmfilelog")
        except Exception, e:
            print e
            os._exit()
    mylogger = wtclib.create_logging("rmfilelog/rmfile.log")
    mylogger.info("start running")
    conf = get_save_days()
    if 0 == conf["ret"]:
        root_dir = os.environ["HOME"]+"/hvpd/"
        fullsize_days = 10
        aisize_days = 30
    else:
        root_dir = conf["root_dir"]
        if not os.path.isabs(root_dir):
            root_dir = os.environ["HOME"]+'/'+root_dir
        fullsize_days = conf["fullsizeD"]
        aisize_days = conf["aisizeD"]
    timet = time.time()
    local = time.localtime(timet)
    #dirs = os.listdir(os.getcwd())
    #print dirs

    timenow = time.localtime()
    while True:

        if not os.path.isdir(root_dir):
            time.sleep(3600)
            continue
        for dirpath, dirname, filenames in os.walk(root_dir):
            print dirpath
            print dirname
            #print filenames
            break
        for path in dirname:
            if os.path.isdir(dirpath+'/'+path + '/ai'):
                for snpath, dayname, filenames in os.walk(dirpath+'/'+path+'/ai'):
                    print snpath
                    print dayname
                    break

                oldtime = time.localtime(time.time()-aisize_days*24*3600)
                daystr = "%04d%02d%02d"%(oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
                for daypath in dayname:
                    if daypath < daystr:
                        os.removedirs(snpath+'/'+daypath)
            if os.path.isdir(dirpath+'/'+path + '/re'):
                for snpath, dayname, filenames in os.walk(dirpath+'/'+path+'/re'):
                    print snpath
                    print dayname
                    break

                oldtime = time.localtime(time.time()-fullsize_days*24*3600)
                daystr = "%04d%02d%02d"%(oldtime.tm_year, oldtime.tm_mon, oldtime.tm_mday)
                for daypath in dayname:
                    if daypath < daystr:
                        os.removedirs(snpath+'/'+daypath)

        while True:
            timeCur = time.localtime()
            if timeCur.tm_mday != timenow.tm_mday:
                timenow = timeCur
                break
            else:
                time.sleep(3600)
