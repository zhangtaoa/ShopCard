# ShopCard
1、此代码主要应用技术为tornado，mako；
2、用途：
   接收中国移动网状网接口的multipart/form-data格式的soap协议数据，进行相关的校验；
   然后根据报文的字段分析业务类别调用不通的模版，生产调用卡券中心的url、method、data数据进行调用
   （卡券中心发布的服务包括http的get、post、delete等，pose的报文格式为json）
   接收卡券中心的业务处理应答报文，从json转成网状网需要的soap multiprocess/mixed返回给网状网
 3、tornado采用异步IO的操作，且潜入mako模版能够处理高并发请求，同时把业务逻辑放在mako模版中进行处理，实现配置化、热加载
