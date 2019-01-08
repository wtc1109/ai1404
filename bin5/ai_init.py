import os,wtclib
import time,thread

def python_cmd(cmd):
    #os.system(cmd)
    while True:
        str1 = "@%d"%(os.getpid())
        print cmd + str1
        os.system(cmd)
        #os.system("pause")
        time.sleep(10)

def python_cmd_once(cmd):
    os.system(cmd)

if __name__ == '__main__':
    id1 = wtclib.get_serverID()
    ucmq_dict = wtclib.get_user_config_ret_dict("../ucmq/conf/ucmq.ini", "server")
    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "ucmq")
    eth_addr = wtclib.get_ip_addr1("eth0")
    if "server_addr" in conf_dict and eth_addr != conf_dict["server_addr"]:
        #when set the ucmq server,ucmq is running in other pc
        #wtclib.set_user_config_from_dict("../ucmq/conf/ucmq.ini", "server", {"wtc":eth_addr})
        #path1 = os.getcwd()
        #path2 = path1[0:path1.rfind('/')]
        #cmd1 = path2+"/ucmq/bin/ucmq -c "+path2+"/conf/ucmq.ini -d"
        print "ucmq is running in %s"%conf_dict["server_addr"]
    else:
        if eth_addr != ucmq_dict["http_listen_addr"]:
            wtclib.set_user_config_from_dict("../ucmq/conf/ucmq.ini", "server", {"http_listen_addr": eth_addr})
        cmd2 = "../ucmq/bin/ucmq -c ../ucmq/conf/ucmq.ini &"
        thread.start_new_thread(python_cmd_once, (cmd2,))
        time.sleep(0.5)
        print "ucmq is running in %s"%eth_addr
        #while True:
        #    time.sleep(3600)
