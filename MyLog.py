#coding=utf-8
import time
import os

def write_loginfo(ologdir, logname, timeinfo, logdict):
    timestr = time.strftime(timeinfo)
    logdir = '%s/%s' % (ologdir,timestr)
    if not os.path.isdir(logdir):
        try:
            os.makedirs(logdir)
        except Exception,x:
            pass
    fname = "%s.%s.log" % (logname,timestr)
    fhandle = file( "%s/%s"%(logdir,fname), "a")
    loginfo = "%s [WlwReqHead:%s]~~[WlwReqBody:%s]~~[CardReqMsg:%s]~~[Url:%s]~~[CardRspMsg:%s]~~[WlwRspMsg:%s]\n" % (time.strftime('%Y-%m-%d %H:%M:%S'),logdict.get("WlwReqHead",""),logdict.get("WlwReqBody",""),logdict.get("CardReqMsg",""),logdict.get("Url",""),logdict.get("CardRspMsg",""),logdict.get("WlwRspMsg",""))
    fhandle.write(loginfo)
    fhandle.close()

if __name__ == '__main__':
    t1 = time.time()
    write_loginfo("/tmp/logs", 'test', '%Y%m%d', 'liupengc\n')
    t2 = time.time()
    print t2-t1
