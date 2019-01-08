import os, time
import wtclib


if __name__ == '__main__':
    local = time.localtime()
    _today  = "%d-%02d-%02d %02d%02d%02d -b yan"%(local.tm_year, local.tm_mon, local.tm_mday,local.tm_hour,local.tm_min,local.tm_sec)
    _dic = {"createdb":"%s"%_today, "ai2filter":"%s"%_today,"ai2getyuv":"%s"%_today,"ai2lamp":"%s"%_today,
            "aifilter":"%s"%_today, "configfiles":"%s"%_today,"downloadpic":"%s"%_today,"ledplayer":"%s"%_today,
            "ai_shell": "%s" % _today,"re_shell": "%s" % _today}
    wtclib.set_user_config_from_dict("bin/aisoftversion.ini", "version", _dic)


