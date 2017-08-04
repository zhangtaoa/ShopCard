<%
import json
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

############ 获取 xml 报文中节点的值 ###############
def get_node_value(instr="",node_name="None", rfind = 0):
    if instr == None:
        return ""
    s1 = "<%s>"%node_name
    s2 = "</%s>"%node_name
    if rfind == 0:
        f1 = instr.find(s1)
        if f1 == -1:
            return ""
        f1 = f1 + len(s1)
        f2 = instr.find(s2)
        if f2 == -1 or f1>=f2:
            return ""
        return instr[f1:f2]
    else:
        f1 = instr.rfind(s1)
        if f1 == -1:
            return ""
        f1 = f1 + len(s1)
        f2 = instr.rfind(s2)
        if f2 == -1 or f1>=f2:
            return ""
        return instr[f1:f2]
####################################################

xmlHead = dict_info["WlwReqHead"]

#头信息哪些需要重新填写
responseMsg="""<?xml version="1.0" encoding="UTF-8"?><InterBOSS><Version>0100</Version><TestFlag>0</TestFlag><BIPType><BIPCode>{BIPCode}</BIPCode><ActivityCode>{ActivityCode}</ActivityCode><ActionCode>1</ActionCode></BIPType><RoutingInfo>{RoutingInfo}</RoutingInfo><TransInfo><SessionID>{SessionID}</SessionID><TransIDO>{TransIDO}</TransIDO><TransIDOTime>{TransIDOTime}</TransIDOTime><TransIDH>{TransIDO}</TransIDH><TransIDHTime>{SysTime}</TransIDHTime></TransInfo><SNReserve>{SNReserve}</SNReserve>{HeaderResponse}<SvcCont><![CDATA[{ResponseMsg}]]></SvcCont></InterBOSS>"""

bipCode = get_node_value(xmlHead,"BIPCode")
activityCode = get_node_value(xmlHead,"ActivityCode")
routingInfo = get_node_value(xmlHead,"RoutingInfo")
sessionID = get_node_value(xmlHead,"SessionID")
transIDO = get_node_value(xmlHead,"TransIDO")
transIDOTime = get_node_value(xmlHead,"TransIDOTime")
sysTime = time.strftime('%Y%m%d%H%M%S')[:14]
snReserve = get_node_value(xmlHead,"SNReserve")

rspParams = {}
rspParams["BIPCode"] = bipCode
rspParams["ActivityCode"] = activityCode
rspParams["RoutingInfo"] = routingInfo
rspParams["SessionID"] = sessionID
rspParams["TransIDO"] = transIDO
rspParams["TransIDOTime"] = transIDOTime
rspParams["SysTime"] = sysTime
rspParams["SNReserve"] = snReserve
cardResponse = dict_info["CardRspMsg"]
try:
    responseDict = json.loads(cardResponse)
    retCode = responseDict["retCode"]
    retMsg = responseDict["retMsg"]
except:
    retCode = "2998"
    retMsg = "Error!"
    
if retCode == "000000":
    headResponse = """<Response><RspType>2</RspType><RspCode>0000</RspCode><RspDesc>OK</RspDesc></Response>"""
    retCode = "0000"
elif retCode == "2998":
    headResponse = """<Response><RspType>2</RspType><RspCode>2998</RspCode><RspDesc>Error</RspDesc></Response>"""
    retCode = "2999"
    retMsg = "Error"
else:
    headResponse = """<Response><RspType>2</RspType><RspCode>2998</RspCode><RspDesc>Error</RspDesc></Response>"""
    if retCode == "050112":
       retCode = "4701"
    elif retCode == "050122":
       retCode = "4702"
    elif retCode == "050111":
       retCode = "4703"
    elif retCode == "050116":
       retCode = "4704"
    elif retCode == "050121":
       retCode = "4705"
    elif retCode == "050119":
       retCode = "4706"
    elif retCode == "050120":
       retCode = "4707"
    elif retCode == "050115":
       retCode = "3705"
    elif retCode == "050118":
       retCode = "3706"
    elif retCode == "050201":
       retCode = "4708"
    elif retCode == "050114":
       retCode = "3707"
    elif retCode == "050123":
       retCode = "3708"
    elif retCode == "050117":
       retCode = "4709"
    elif retCode == "050113":
       retCode = "4003"

svcMsg="""<PcardReceiveRsp><RspCode>%s</RspCode><RspDesc>%s</RspDesc></PcardReceiveRsp>""" % (retCode,retMsg)

rspParams["HeaderResponse"] = headResponse
rspParams["ResponseMsg"] = svcMsg
output = responseMsg.format(**rspParams)

%>${output}