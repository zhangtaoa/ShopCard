#coding=utf-8
import requests

hmsg = '''<?xml version='1.0' encoding='UTF-8'?><InterBOSS><Version>0100</Version><TestFlag>0</TestFlag><BIPType><BIPCode>BIP3A247</BIPCode><ActivityCode>T3000247</ActivityCode><ActionCode>0</ActionCode></BIPType><RoutingInfo><OrigDomain>BOSS</OrigDomain><RouteType>00</RouteType><Routing><HomeDomain>UMMP</HomeDomain><RouteValue>998</RouteValue></Routing></RoutingInfo><TransInfo><SessionID>UMPPBIP3A228201404121546311170</SessionID><TransIDO>UMPPT3000206201404121546311171</TransIDO><TransIDOTime>20140412154631</TransIDOTime></TransInfo></InterBOSS>'''
bmsg = '''<?xml version="1.0" encoding="UTF-8"?><InterBOSS><SvcCont><![CDATA[<?xml version="1.0" encoding="UTF-8"?><PcardReceiveReq><BusiType>hf01</BusiType><PCardType>002</PCardType><LoginType>0</LoginType><LoginNo>13754845522</LoginNo><BusiCode></BusiCode><BizType>00</BizType><OprType>2</OprType><OptSeq>1020170715886097739899344896_1320170715886094639996207104_351</OptSeq><SerialNumber>UMMP1111111111110007</SerialNumber></PcardReceiveReq>]]></SvcCont></InterBOSS>'''

#url="http://218.206.190.10:7701/Trans/Receiver"
#url="http://127.0.0.1:3001/Shop/Trans/Receiver"
#url="http://127.0.0.1:61500/shop/Pcard"
url="http://127.0.0.1:51800/shop/Pcard"
payload = {'xmlhead': hmsg, 'xmlbody': bmsg}
#headers = {'Content-Type': 'multipart/form-data'}
files = {'xmlhead': ('', hmsg), 'xmlbody': ('', bmsg)}
#r = requests.post(url, data=payload)
#r = requests.post(url, files=(('xmlhead', hmsg), ('xmlbody', bmsg)))
r = requests.post(url, files=files)
print r.headers
print r.text
