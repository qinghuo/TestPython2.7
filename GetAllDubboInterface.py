#-- coding:utf-8 --
from kazoo.client import KazooClient
from urllib import unquote
import xlwt
def analysisUrl(url):
    applicationName="unkonwn"
    if -1 !=url.find("&application="):
        cString = url[url.find("&application=") + 13:]
        applicationName = cString[0:cString.find('&')]
    aString = url[url.find("&interface=") + 11:]
    interface = aString[0:aString.find("&")]
    bString = aString[aString.find("&methods=") + 9:]
    methods=bString
    if -1 != bString.find('&'):
        methods = bString[0:bString.find('&')]
    return applicationName,interface,methods

# Create a client and start it
zk = KazooClient(hosts='172.20.1.26:2181')
zk.start()
dubboRootUrl="/dubbo"
dubboServices=zk.get_children(dubboRootUrl)
f=open('tmp.text','w')
f.truncate()
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')
# sheet.write(0, 0, "系统名")
# sheet.write(0, 1, "接口名")
# sheet.write(0, 2, "方法列表")
i=0
for dubboService in dubboServices:
    try:
        if zk.exists(dubboRootUrl+'/'+dubboService+'/providers'):
            childrens=zk.get_children(dubboRootUrl + '/' + dubboService + '/providers')
            if len(childrens)>0:
              applicationName, interface,methods=analysisUrl(str(unquote(childrens[0])))
              print interface+" "+methods
              f.write(interface+" "+methods+'\n')
              sheet.write(i,0,applicationName)
              sheet.write(i, 1, interface)
              sheet.write(i, 2, methods)
              i=i+1
    except Exception as e:
        print  e

f.close()
wbk.save("dubboInterfaces.xls")

# if __name__ == '__main__':
#     test="dubbo://172.20.100.156:18356/com.weidai.mario.merchant.gate.facade.api.ILargeLoanMerchantGateFacade?anyhost=true&application=dubbo-mario-gate&cluster=failfast&default.cluster=failfast&default.retries=0&default.timeout=6000&dubbo=2.5.3&interface=com.weidai.mario.merchant.gate.facade.api.ILargeLoanMerchantGateFacade&methods=largeLoanPushOrder&pid=34333&retries=0&side=provider&timestamp=1517475936566";
#     applicationName, interface, methods = analysisUrl(test)
#     print  applicationName+'\n'
#     print  interface+'\n'
#     print  methods+'\n'