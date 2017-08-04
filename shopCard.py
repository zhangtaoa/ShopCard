#coding=utf-8

import os
import sys
import time
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

reload(sys)
sys.setdefaultencoding( "utf-8" )

import MyLog
import MyMako
import cardUtil
import UIPConst

from tornado.options import define, options
define("port",  default=11101, help="run on the given port", type=int)
define("rundir",default='',    help="program dir name",      type=str)

class CardHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        #设置应答请求头
        self.set_header("content-type","multipart/mixed")
		### self.dict_info 在请求的整个处理过程都会存在的
        self.dict_info = {}  # request para info
        self.dict_info["ErrLogPath"] = '%s/errlogs' % (options.rundir,) # 错误日志的目录
        self.dict_info["ErrLogName"] = 'error.%d' % (options.port,) # 错误日志的名称
        self.dict_info["LogPath"] = '%s/logs' % (options.rundir,) # 日志的目录
        self.dict_info["LogName"] = '%d' % (options.port,) # 日志的名称
        ### 19:37 2016/11/4 添加程序监听的端口
        self.dict_info['port'] = '%s' % options.port        
        #print(dir(self.request))
        #print(self.request.connection)
        xmlhead_u8 = self.get_body_argument("xmlhead")
        xmlbody_u8 = self.get_body_argument("xmlbody")
        xmlhead_u = u''
        xmlbody_u = u''

        self.dict_info["WlwReqHead"] = xmlhead_u8
        self.dict_info["WlwReqBody"] = xmlbody_u8

        try:
            xmlhead_u = xmlhead_u8.decode('utf-8')
            xmlbody_u = xmlbody_u8.decode('utf-8')
        except:
            temp_errmsg = UIPConst.ERRMSG % ('2998','Your XML not utf-8')
            self.dict_info["CardRspMsg"] = temp_errmsg
            uip_errmsg = UIPConst.DEFAULTERRMSG % xmlhead_u8
            self.dict_info["WlwRspMsg"] = uip_errmsg
            self.write(uip_errmsg)
            MyLog.write_loginfo(self.dict_info["ErrLogPath"], self.dict_info["ErrLogName"], '%Y%m%d', self.dict_info)
            return self.finish()

        ### 处理报文头，获取交易类型
        bip_code,activity_code = cardUtil.parse_head(xmlhead_u8)
        if bip_code == None or activity_code == None:
           self.dict_info["CardRspMsg"] = "[BIPCode] or [ActivityCode] is None"
           uip_errmsg = UIPConst.DEFAULTERRMSG % xmlhead_u8[0:-12]
           self.dict_info["WlwRspMsg"] = uip_errmsg
           self.write(uip_errmsg)
           MyLog.write_loginfo(self.dict_info["ErrLogPath"], self.dict_info["ErrLogName"], '%Y%m%d', self.dict_info)
           return self.finish()

        self.dict_info["ReqPath"] = '%s/config/Req_%s_%s.tpl.py' % (options.rundir,bip_code,activity_code)
        self.dict_info["RspPath"] = '%s/config/Rsp_%s_%s.tpl.py' % (options.rundir,bip_code,activity_code)

        ### 处理交易,调用miso服务  
        retcode,retmsg = MyMako.runtpl(self.dict_info["ReqPath"],dict_info=self.dict_info)
        #print retcode,retmsg
        if retcode != 0:
            temp_errmsg = UIPConst.ERRMSG % ('2998','Call %s Fail [%s]' % (self.dict_info["ReqPath"],retmsg))
            self.dict_info['CardRspMsg'] = temp_errmsg
            retcode,retmsg = MyMako.runtpl(self.dict_info["RspPath"],dict_info=self.dict_info)
            if retcode != 0:
               retmsg = UIPConst.DEFAULTERRMSG % xmlhead_u8[0:-12]
            uip_errmsg = retmsg
            self.dict_info["WlwRspMsg"] = uip_errmsg
            self.write(uip_errmsg)
            MyLog.write_loginfo(self.dict_info["ErrLogPath"], self.dict_info["ErrLogName"], '%Y%m%d', self.dict_info)
            return self.finish()
        
        ### httpmethod#@$url#@$msg
        req_list = retmsg.split("#@$")
        if len(req_list) == 3:
           method = req_list[0]
           url = req_list[1]
           msg = req_list[2]
        else:
           method = req_list[0]
           url = req_list[1]
           msg = ""

        self.dict_info["CardReqMsg"] = msg
        tsnheaders = {"content-type":"application/json;charset=utf-8",
        	          "cookie":"eshop_token=d0990ff47680b74fb2e882de778cb81a"}

        self.dict_info['Url'] = url
        tsnrequest = tornado.httpclient.HTTPRequest(
                         url=url,
                         method=method,
                         headers=tsnheaders,
                         body=msg,
                         connect_timeout=3,
                         request_timeout=5)
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(tsnrequest, callback=self.on_response)


    def on_response(self,response):
        #print(response.body)
        if response.code != 200:
           temp_errmsg = "Call Http Fail [%s][%s]" % (response.error,response.body)
           self.dict_info["CardRspMsg"] = temp_errmsg
           uip_errmsg = UIPConst.DEFAULTERRMSG % self.dict_info["WlwReqHead"][0:-12]
           self.dict_info["WlwRspMsg"] = uip_errmsg
           MyLog.write_loginfo(self.dict_info["ErrLogPath"], self.dict_info["ErrLogName"], '%Y%m%d', self.dict_info)
           self.write(uip_errmsg)
           return self.finish()

        self.dict_info["CardRspMsg"] = response.body
        retcode,retmsg = MyMako.runtpl(self.dict_info["RspPath"],dict_info=self.dict_info)
        #print retcode,retmsg
        if retcode != 0:
            temp_errmsg = UIPConst.ERRMSG % ('2998','Call %s Fail [%s]' % (self.dict_info['RspPath'], retmsg))
            self.dict_info["WlwRspMsg"] = temp_errmsg
            retcode,retmsg = MyMako.runtpl(self.dict_info["RspPath"],dict_info=self.dict_info)
            if retcode != 0:
               retmsg = UIPConst.DEFAULTERRMSG % self.dict_info['WlwReqHead'][0:-12]
            uip_errmsg = retmsg
            self.dict_info["WlwRspMsg"] = uip_errmsg
            self.write(uip_errmsg)
            MyLog.write_loginfo(self.dict_info["ErrLogPath"], self.dict_info["ErrLogName"], '%Y%m%d', self.dict_info)
            return self.finish()
        self.dict_info["WlwRspMsg"] = retmsg
        MyLog.write_loginfo(self.dict_info["LogPath"], self.dict_info["LogName"], '%Y%m%d', self.dict_info)
        self.write(retmsg)
        return self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    useage = '########################################################\n# python %s --port=ddddd --rundir=abspath \n########################################################\n' % (sys.argv[0],)
    if options.port < 1024 or options.port >65535:
        print "Error:port must in [1025,65535]\n"
        print useage
        sys.exit(1)
    if options.rundir == '' or not os.path.exists(options.rundir):
        print "Error:must enter the rundir and must be existed\n"
        print useage
        sys.exit(1)
    if options.rundir[-1] == '/':
        options.rundir = options.rundir[:-1]

    tornado.httpclient.AsyncHTTPClient.configure(None, max_clients=2048)
    app = tornado.web.Application(handlers=[(r"/shop/Pcard", CardHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
