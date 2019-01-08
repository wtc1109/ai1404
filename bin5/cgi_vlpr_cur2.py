import os,time
import glob, socket, struct, fcntl,stat

def get_ip_addr(ifname):
    global mylogger
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    except Exception, e:
        print e
        return None
    return addr

if __name__ == '__main__':
    print "Content-type:text/html\n\n"
    print """<html>
            <head>
            <meta content="text/html;charset=gbk" http-equiv="content-type">
            <title>VLPR bays</title>
            </head>
            <body>
            """
    local = time.localtime(time.time() - 24 * 3600)
    _yesterday = "%d%02d%02d" % (local.tm_year, local.tm_mon, local.tm_mday)
    try:
        for snpath, dayname, filenames in os.walk('../rejpgs/save_orig_jpg/'):
            if _yesterday in dayname:

                _jpg_tar = "../rejpgs/un_jpg/%s_un_jpg1.tar" % _yesterday
                if os.path.isfile(_jpg_tar):
                    os.remove(_jpg_tar)
                _yuv_tar = "../rejpgs/un_yuv/%s_un_yuv1.tgz" % _yesterday
                if os.path.isfile(_yuv_tar):
                    os.remove(_yuv_tar)

                _jpg_tar = "../rejpgs/save_no_result_jpg/%s_no_result_jpg1.tar" % _yesterday
                if os.path.isfile(_jpg_tar):
                    os.remove(_jpg_tar)
                _yuv_tar = "../rejpgs/save_no_result_yuv/%s_no_result_yuv1.tgz" % _yesterday
                if os.path.isfile(_yuv_tar):
                    os.remove(_yuv_tar)


                fp = open("cmd.sh",'wr')
                fp.write("cd /home/bluecard/hvpd/re/un_jpg \ntar cf %s_un_jpg1.tar %s &\n"% (_yesterday, _yesterday))
                fp.write("cd ../un_yuv \ntar czf %s_un_yuv1.tgz %s &\n" % (_yesterday, _yesterday))
                fp.write("cd ../save_no_result_jpg \ntar cf %s_no_result_jpg1.tar %s &\n" % (_yesterday, _yesterday))
                fp.write("cd ../save_no_result_yuv \ntar czf %s_no_result_yuv1.tgz %s &\n" % (_yesterday, _yesterday))
                fp.write("exit 1")
                fp.close()
                os.chmod("cmd.sh", stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
                os.system("./cmd.sh >/dev/null")

                addr = get_ip_addr("eth0")
                if None == addr:
                    print "</body> </html>"
                    os._exit(0)

                print "yesterday VLPR Suspicious analysis by bays<br>"

                print """<p><a href="../rejpgs/un_jpg/%s_un_jpg1.tar">Suspicious JPEG</a></p>
                <p><a href="../rejpgs/un_yuv/%s_un_yuv1.tgz">Suspicious YUV</a></p>
                <p><a href="../rejpgs/save_no_result_jpg/%s_no_result_jpg1.tar">No result JPEG</a></p>
                <p><a href="../rejpgs/save_no_result_yuv/%s_no_result_yuv1.tgz">No result YUV</a></p>"""\
                      % (_yesterday, _yesterday, _yesterday, _yesterday)
                print """<table><tr><td width="155"></td><td width="65"></td><td width="115"></td><td width="115"></td><td width="155"></td><td></td></tr>"""
                print "<tr><td>SN</td><td>Bay</td>" \
                      "<td><a href='http://%s/rejpgs/un_jpg/%s/' target='_blank'>Suspicious</a></td>" \
                      "<td><a href='http://%s/rejpgs/save_no_result_jpg/%s/' target='_blank'>No result</a></td>" \
                      "<td><a href='http://%s/rejpgs/save_orig_jpg/%s/' target='_blank'>All</a></td>" \
                      "<td>OK Percent</td></tr>" % (addr, _yesterday, addr, _yesterday, addr, _yesterday)
                print "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
                _day_path = '../rejpgs/un_jpg/%s' % _yesterday
                _day_path2 = '../rejpgs/save_orig_jpg/%s' % _yesterday
                _day_path3 = '../rejpgs/save_no_result_jpg/%s' % _yesterday
                for snpath1, _sns, filenames1 in os.walk(_day_path2):
                    break
                _len1_sum = 0
                _len2_sum = 0
                _len3_sum = 0
                _bays = 0
                _sns1 = sorted(_sns)
                for sn in _sns1:
                    for i in range(1, 4):
                        _find_files2 = glob.glob("%s/%s/%d_*.jpg" % (_day_path2, sn, i))
                        _len2 = len(_find_files2)
                        if 0 == _len2:
                            continue
                        _find_files1 = glob.glob("%s/%s/%d_*.jpg" % (_day_path, sn, i))
                        _len1 = len(_find_files1)

                        _find_files3 = glob.glob("%s/%s/%d_*.jpg" % (_day_path3, sn, i))
                        _len3 = len(_find_files3)

                        _len1_sum += _len1
                        _len2_sum += _len2
                        _len3_sum += _len3
                        _bays += 1

                        """
                        print "<tr><td>%s</td><td>%d</td>" \
                              "<td><a href='http://%s/rejpgs/un_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                              "<td><a href='http://%s/rejpgs/save_no_result_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                              "<td><a href='http://%s/rejpgs/save_orig_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                              "<td>%f</td></tr>"\
                              %(sn, i, addr, _yesterday,sn, _len1, addr, _yesterday,sn,
                                _len3,addr, _yesterday,sn, _len2, (100-100.0*(_len1 + _len3)/_len2))
                        """

                        print "<tr><td>%s</td><td>%d</td>" % (sn, i)
                        if 0 == _len1:
                            print "<td>0</td>"
                        else:
                            print "<td><a href='http://%s/rejpgs/un_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                                  % (addr, _yesterday, sn, _len1)
                        if 0 == _len3:
                            print "<td>0</td>"
                        else:
                            print "<td><a href='http://%s/rejpgs/save_no_result_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                                  % (addr, _yesterday, sn, _len3)
                        print "<td><a href='http://%s/rejpgs/save_orig_jpg/%s/%s/' target='_blank'>%d</a></td>" \
                              "<td>%f</td></tr>" % (
                              addr, _yesterday, sn, _len2, (100 - 100.0 * (_len1 + _len3) / _len2))
                print "<tr><td>Sum</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%f</td></tr>" % (
                    _bays, _len1_sum, _len3_sum, _len2_sum, (100.0 - 1.0 * _len1_sum / _len2_sum))
            else:
                print "Yesterday None, or 100% OK"
            break
        print "</table></body> </html>"

    except Exception,e:
        print str(e)
        print "</body> </html>"


