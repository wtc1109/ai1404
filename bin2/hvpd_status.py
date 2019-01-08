import urllib, urllib2, time
from HTMLParser import HTMLParser
data_link = []
tr_start = False
"""usr get method to get a ucmq msg from server"""
class MyHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global tr_start, data_link
        #print "<%s>"%tag
        if 'tr' == tag and tr_start == False:
            tr_start = True
        if 'input' == tag and True == tr_start:
            dic_val = dict(attrs)
            try:
                val = dic_val["value"]
                data_link.append(val)
            except:
                pass
    def handle_endtag(self, tag):
        global tr_start
        #print "</%s>"%tag
        if 'tr' == tag:
            tr_start = False

    def handle_startendtag(self, tag, attrs):
        #print "<%s/>"%tag
        pass
    def handle_data(self, tag):
        global tr_start
        #print "data=", tag
        if True == tr_start:
            data_link.append(tag)

def html2dict(htmls):
    parser = MyHtmlParser()
    parser.feed(htmls)
    #print parser
    #print data_link
    dic2 = {}
    for i in range(len(data_link) / 2):
        msg = data_link[2 * i].strip(' ')
        msg = msg.strip('\n')
        msg = msg.strip('\r')
        msg = msg.strip(':')
        if '' == msg:
            continue
            #    print r'%x'%msg
        dic = {msg: data_link[2 * i + 1]}
        dic2.update(dic)
    return dic2

def get_hvpd_status(url):
    global data_link
    try:
        res_data = urllib2.urlopen(url)
        res = res_data.read()
        #print res
        res_data.close()
        urllib.urlcleanup()
        data_link = []
        return html2dict(res)
    except Exception, e:
        print url + str(e)
        return None