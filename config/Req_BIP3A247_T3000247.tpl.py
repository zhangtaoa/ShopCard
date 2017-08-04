<%
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

splitMsg="#@$"
httpMethod = "POST"

xmlBody = dict_info["WlwReqBody"]

busiType = get_node_value(xmlBody,"BusiType")
pCardType = get_node_value(xmlBody,"PCardType")
loginType = get_node_value(xmlBody,"LoginType")
loginNo = get_node_value(xmlBody,"LoginNo")
busiCode = get_node_value(xmlBody,"BusiCode")
bizType = get_node_value(xmlBody,"BizType")
oprType = get_node_value(xmlBody,"OprType")
optSeq = get_node_value(xmlBody,"OptSeq")
oprNum = get_node_value(xmlBody,"SerialNumber")

#url = "http://10.255.254.94:8012/promotionrest/v1/pcardrest/pcardReceive/%s" % loginNo
url = "http://10.255.201.198:8902/i/gray/inner/promotionrest/v1/pcardrest/pcardReceive/%s" % loginNo
#url = "http://10.255.201.198:8902/promotionrest/v1/pcardrest/pcardReceive/%s" % loginNo
#url = "http://127.0.0.1:63000/i/gray/inner/promotionrest/v1/pcardrest/pcardReceive/%s" % loginNo

reqMsg = """{"busiCode": "","busiType": "%s","channelId": "%s","loginNo": "%s","loginType": "%s","oprType": "%s","optSeq": "%s","pCardType": "%s","serialNumber":"%s"}""" % (busiType,bizType,loginNo,loginType,oprType,optSeq,pCardType,oprNum)

%>${httpMethod}${splitMsg}${url}${splitMsg}${reqMsg}