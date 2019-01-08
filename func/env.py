import os, time, sys
import ConfigParser
import json
import MySQLdb
import psutil, signal, socket, struct
import datetime
import tarfile, zipfile, random,glob
import datetime

_day1 = datetime.datetime.now()-datetime.timedelta(days=1)
_cameras = (['123',1],['123',2],['123',3])
_ca = sorted(_cameras)
_find_file = glob.glob('env.*')
_dic1 = {"ip":'123','sd':'fg'}
_dic1.update({'ip':'456','gh':234})
for _d1 in _dic1:
    pass
_files = os.listdir('../')
i1 = 13/4*4
ss1 = "1w3"
_path, _file = os.path.split('/tmp/war/123')
_filen, _ext = os.path.splitext(_file)
ss2 = ss1.upper()
plate='1139'
len1 = len("1ch80" and plate)
plate1 = (('123',),('adsf',),(23,),('adf',),(234,),('egrt',))
p1 = list(plate1)
for i in range(5):
    _bay=random.randint(1,3)
_str = datetime.datetime.now()

_path, _file = os.path.split("/tmp/wa/123.jpg")
video_def_dictH = ((1920,25),(1600,40),(1280,50),(1056,64),(864,96),(640,128),(576, 200))
video_def_dictL = ((1920, 8), (1600, 16), (1280, 32), (1056, 48), (864, 64), (640, 96), (576, 128))
ptr = video_def_dictL
_max_def = 1200

for vdef in ptr:
    if _max_def > vdef[0]:
        _max_rtsp_client = vdef[1]
        break
pc_mem = psutil.virtual_memory()
hddinfo = os.statvfs(".")
ii = 0
strii = "%03dj"%ii
print strii.isdigit()
dict1 = {"r":10,"g":'s','b':'sdfsdf'}
for keys in dict1:
    print keys
cf = ConfigParser.ConfigParser()
#cf.read(home + "/ucmq.ini")
cf.read("conf.conf")
secs = cf.sections()
opts = cf.options("ucmq")
print opts
if "ucmq" in secs:
    print "ucmq in"
if "server_addr" in opts:
    print "server_addr in"
#kvs = cf.items("ucmq")
#print kvs

str_val = cf.get("ucmq", "server_addr")
int_val = cf.getint("ucmq", "server_port")
print "str=", str_val
print "int=", int_val
if not "server" in secs:
    cf.add_section("server")
cf.set("server", "http_listen_port", 88010)
if not "wtc" in secs:
    cf.add_section("wtc")
cf.set("wtc", "mydb", "system")
cf.write(open("conf.conf","w"))

_sn = "1 2 3 4 5 6 7 8 9 10"
_snp = _sn.split(" ")
_ssn = "%s"%[_snp[i] for i in range(4)]
_equipID = min("171243005", "171243006")

en = zipfile.is_zipfile("hvpd_update_file_2017121802.zip")
zip0 = zipfile.ZipFile("hvpd_update_file_2017121802.zip",'r')
info0 = zip0.namelist()
for filen in info0:
    file_sp = filen.split('/')
    if "upgrade" in file_sp:
        print "123"
    if "upgrade.sh" in file_sp:
        print "sdf"
en1 = zipfile.is_zipfile("env.rar")
en2 = tarfile.is_tarfile("hvpd_update_file_2017121802.tar.gz")
tar2 = tarfile.open("hvpd_update_file_2017121802.tar.gz")
info2 = tar2.getnames()
for filen in info2:
    file_sp = filen.split('/')
    if "upgrade" in file_sp:
        print "123"
    if "upgrade.sh" in file_sp:
        print "sdf"
def check_ip_is_ok(ip_addr):
    try:
        sin = socket.inet_aton(ip_addr)
    except (Exception) as e:
        return -1
    ip_splite = ip_addr.split('.')
    ip_len = len(ip_splite)
    if 4 == ip_len or 6 == ip_len:
        return 0
    else:
        return -2
filename = __file__
try:
    sin = socket.inet_aton("192.168.1")
except (Exception) as e:
    print e

_ip = "192.168.1.2"
ret = check_ip_is_ok(_ip)
ip_splite = _ip.split('.')
sint = struct.unpack('>I', bytes(sin))
print sint
num_ip = socket.ntohl(struct.unpack('I',socket.inet_aton("192.168.1.2"))[0])
_specials = [[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7]]
for _sp in _specials:
    if _sp[2] == 4:
        break
print _sp[4]
a1 = int("0a",16)
path1 = os.getcwd()
env = os.environ
strt=time.asctime()
stat = os.stat("conf.conf")
cti = time.ctime(stat.st_mtime)
mti = datetime.date.fromtimestamp(stat.st_mtime).isoformat()

prog = 'python /home/w/PycharmProjects/linuxpython/multi_ucmq5.py &'
print len(prog)
sp1 = prog.split(' ')
print sp1[len(sp1)-1]
s = os.getcwd()
pids1 = psutil.pids()
for pid1 in pids1:
    p = psutil.Process(pid1)
    print "pid=%d, pname=%s"%(pid1, p.name())
    if "python" == p.name()[:6]:
        print "python"
        os.kill(pid1, signal.SIGKILL)
path = s[:s[0:s.rfind('/')].rfind('/')]

str1 = "%Y-%M-%D"
per=0
print len(str1)
print type(str1)
a1 = str1[len(str1)-1]
_dicR = {'R':80,'G':0, 'B':0, 'T':100}
_dicG = {'R':0,'G':80, 'B':0, 'T':100}
_dicB = {'R':0,'G':0, 'B':80, 'T':100, "te":"teest"}
_dic2 = {'T1':json.dumps(_dicR), 'T2':json.dumps(_dicG), 'T3':json.dumps(_dicB)}
rgb = json.dumps(_dic2)
_dic_rgb = json.loads(rgb)
a3 = sys._getframe().f_lineno
print "line:"+str(a3)
a2 = str(type(_dicB["te"]))
print a2
if not type(_dicB["R"])==int:
    print type(_dicB["R"])
print type(_dicB["R"])
while True:
    per += str1[per:].find('%')
    if per < 0:
       break
    per2 = str1[per+2:].find('%')
    print str1[per+1:per+2]
    if per2 < 0:
        print str1[per+2:]
    else:
        print str1[per+2:per+2+per2]
    per += 2
    if per >= len(str1):
        break
print env['HOME']
home = env['PWD']
pos = home.rfind("/")
root_dir = home[0:pos]
#os.mkdir("/home/bluecard/hvpdgi")
stat = os.stat("/tmp/")
cti = time.ctime(stat.st_ctime)
