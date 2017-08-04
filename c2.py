#coding=utf-8
import requests

hmsg = '''<?xml version='1.0' encoding='UTF-8'?><InterBOSS><Version>0100</Version><TestFlag>0</TestFlag><BIPType><BIPCode>BIP3A228</BIPCode><ActivityCode>T3000234</ActivityCode><ActionCode>0</ActionCode></BIPType><RoutingInfo><OrigDomain>BOSS</OrigDomain><RouteType>00</RouteType><Routing><HomeDomain>BOSS</HomeDomain><RouteValue>998</RouteValue></Routing></RoutingInfo><TransInfo><SessionID>UMPPBIP3A228201404121546311170</SessionID><TransIDO>UMPPT3000206201404121546311171</TransIDO><TransIDOTime>20140412154631</TransIDOTime></TransInfo></InterBOSS>'''
bmsg = '''<?xml version="1.0" encoding="UTF-8"?><InterBOSS><SvcCont><![CDATA[<?xml version="1.0" encoding="UTF-8"?><PcardReceiveReq><BusiType>hf01</BusiType><PCardType>001</PCardType><LoginType>0</LoginType><LoginNo>18701184076</LoginNo><BusiCode></BusiCode><BizType>22</BizType><OprType>2</OprType><OptSeq>1020170407850188997187862528_1320170407850188997309890560_99</OptSeq><OprNum>UMMP1231234213434324</OprNum></PcardReceiveReq>]]></SvcCont></InterBOSS>'''
#url="http://218.206.190.10:7701/Trans/Receiver"
#url="http://127.0.0.1:3001/Shop/Trans/Receiver"
url="http://127.0.0.1:51800/esbWS/services/roamServ"
payload = {'xmlhead': hmsg, 'xmlbody': bmsg}
#headers = {'Content-Type': 'multipart/form-data'}
files = {'xmlhead': ('', hmsg), 'xmlbody': ('', bmsg)}
#r = requests.post(url, data=payload)
#r = requests.post(url, files=(('xmlhead', hmsg), ('xmlbody', bmsg)))
r = requests.post(url, files=files)
print r.headers
print r.text
