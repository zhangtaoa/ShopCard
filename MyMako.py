#coding:utf-8
import os
import time
import mako
from mako.template import Template
from mako import exceptions
from StringIO import StringIO
from mako.runtime import Context

###### 我的mako模版, 在模版中生成字符串,动态加载,使用其他的模版库 ####
###### 模版的后缀必须以  .tpl.py  结束 #####
###### 
""" 需要使用到一个全局变量
    记录已经加载的模版相关信息
    模版文件的编码类型必须是 UTF-8 的编码需要注意.
    g_mako_infos 的 key 是模版的绝对路径名称: /a/b/c/d/aaa.tpl.py
    g_mako_infos的value是一个list: [0:模版文件的修改时间, 1:模版文件的字符串内容, 2:Template obj ]
"""
g_mako_infos = {}

##### 传入模版所在的目录, 
##### 目录中的所有以 .tpl.py的文件 加载到g_mako_infos中  #####
def init_mako_tplinfos(mako_dirpath):
    global g_mako_infos
    ##判断目录是否能够访问
    if os.access(mako_dirpath,os.R_OK) == False:
        return -1, "mako_dirpath %s can't access" % (mako_dirpath,)
    ##如果可以访问继续执行
    if mako_dirpath[-1] == '/':
        mako_dirpath = mako_dirpath[:-1]
    flist = os.listdir(mako_dirpath)
    for f in flist:
        if f.endswith('.tpl.py'):
            mako_fpath = "%s/%s" % (mako_dirpath,f)
            mako_info = g_mako_infos.get(mako_fpath) # list type
            # first read file
            if mako_info is None: 
                # 0:modify time; 1:file content; 2:Template obj 
                g_mako_infos[mako_fpath] = [0,"",None] 
                mako_info = g_mako_infos[mako_fpath]
            
            if os.access(mako_fpath, os.R_OK):
                fmtime = os.path.getmtime(mako_fpath)
                # first read and update need reread!
                # print  mako_info[0],fmtime
                # 如果发现文件有更新, 则 重新加载模版对象;
                if mako_info[0] == 0 or long(fmtime) > long(mako_info[0]):
                    with open(mako_fpath) as fp:
                        try:
                            mako_info[1] = fp.read().decode('utf-8','ignore')
                        except:
                            errstr = 'read and decode %s faild' % (mako_fpath,)
                        unistr = mako_info[1]
                        try:
                            mako_info[2] = Template(unistr)
                            mako_info[0] = fmtime
                        except:
                            errstr = "compile tmmplate %s error %s"  % (mako_fpath,exceptions.text_error_template().render() )
                            #print "ERROR:", errstr
                            return 1, errstr
                # 多个文件的话,全部加载完毕
                #return 0, "OK"
            else:
                return 1, "can't read %s" % (mako_fpath,)   
    return 0, 'init ok contanis %d tmmplates' % (len(g_mako_infos), )

### 运行模版 获取模版的输出 ###
### mako_fpath 模版文件的决定路径 myargs 模版需要的参数 ###
### >>>> 模版执行成功返回  0, outsmg
### >>>> 模版执行成功返回 !0, errmsg
### 将模版的绝对路径传入, 会解析对应的目录中所有的模版



def runtpl(mako_fpath,**myargs):
    global g_mako_infos
    mako_dirpath = os.path.dirname(mako_fpath)
    retcode,retmsg = init_mako_tplinfos(mako_dirpath)
    if retcode != 0:
        return retcode,retmsg
    buf = StringIO()
    #print '>>>>:',g_mako_infos.keys(), len(g_mako_infos)
    #print '>>>>>:',mako_fpath
    
    if g_mako_infos.get(mako_fpath) == None:
        return 1, "Sorry Your %s Not Found"%(mako_fpath)
    try:
        mytemplate = g_mako_infos[mako_fpath][2]
        ctx = Context(buf, **myargs)
        mytemplate.render_context(ctx)
        oustr = buf.getvalue()
        buf.close()
        return 0, oustr
    except:
        errstr = "render tmmplate %s error:%s"  % (mako_fpath,exceptions.text_error_template().render() )
        if not buf.closed:
            buf.close()
        return 1, errstr

if __name__ == '__main__':
    ilist = [111,2222,333,4444,'abcdefg']
    iinfo = {}
    iinfo["ID"] = 1001
    iinfo["NAME"] = 'liupengc'
    
    mako_fpath =  '/chnesb/work/mypy/liupengc/myuip/tpldir/tsninfo.tpl.py'
    mako_fpath =  '/chnesb/uipserver/tpldir/CDRQryReq.tpl.py'
    #mako_fpath =  '/chnesb/uipserver/tpldir/demo.tpl.py'
    #mako_fpath =  '/chnesb/uipserver/tpldir/AuthReq.tpl.py'
    for i in range(1):
        t1 = time.time()
        iinfo["ID"] = iinfo["ID"] + 1
        #iinfo['srv_name'] =  'RealFeeQryReq'
        iinfo['msginfo'] =   '<m:pin><![CDATA[<ROOT><IDItemRange>15810108120</IDItemRange><IdentCode>123</IdentCode><BizType>0701</BizType><TransIDO>1001</TransIDO></ROOT>]]></m:pin>'
        iinfo['msginfo'] =  '''<?xml version="1.0" encoding="UTF-8"?>
                                <ROOT>
                                    <IDItemRange>15810108120</IDItemRange>
                                    <BillMonth>201410</BillMonth>
                                    <TmemType>01</TmemType>
                                    <IdentCode>1234567</IdentCode>
                                    <PwdTempIdentCode>1</PwdTempIdentCode>
                                    <RandTempIdentCode>2</RandTempIdentCode>
                                    <BgnIndex>3</BgnIndex>
                                    <EndIndex>4</EndIndex>
                                    <BizType>0702</BizType>
                                    <TransIDO>999999</TransIDO>
                                </ROOT>
                            '''
        #iinfo['msginfo'] =   '<m:pin><![CDATA[<ROOT><IDValue>15810108120</IDValue><IDType>123</IDType><BizType>0701</BizType><TransIDO>1001</TransIDO></ROOT>]]></m:pin>'
        #ec,em1 = runtpl(mako_fpath,name=ilist,myinfo=iinfo)
        #iinfo['msginfo'] = ''
        retcode,retmsg = runtpl(mako_fpath,name=ilist,myinfo=iinfo)
        t2 = time.time()
        print "retcode=[%d]" % (retcode,)
        print "regmsg=[%s]" % (retmsg,)
        print "costs:>>>>>>:", t2-t1
        print mako_fpath
        #print  iinfo
        #time.sleep(0.5)
        #print em
        #break
    
    
    
