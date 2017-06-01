import requests
import hashlib
import random
import time
import codecs
import json
def write_to_log(str,baseurl):
    fw = codecs.open(baseurl+'hotline.log','a','gbk')
    try:
        fw.write(str)
    except Exception as e:
        raise e
    finally:
        fw.close()
def load(filename):
    with codecs.open(filename,'r',encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data
class HotLineManger(object):
    def __init__(self,baseurl):
        self.user = None
        self.password = None
        self.session = requests.session()
        self.sessionId = None
        self.userId = None
        self.userlist=load(baseurl+'hotlineConf.json')['userList']
    def hasemp(self,empname):
        return empname in self.userlist
    def login(self,empname):
        self.user = self.userlist[empname][0]
        self.password = self.userlist[empname][1]
        loginUrl = 'http://211.151.35.102/?json={"Command":"Action","Action":"Login","ActionID":"%s","ExtenType":"Local","Password":"%s","BusyType":"0","Monitor":true,"User":"%s"}&_=1491824202704' % (\
            "Logoff"+str(random.random()),self.password,self.user)
        res = self.session.get(loginUrl)
        if res.status_code==200:
            resdict = res.json()
            if resdict['Succeed']:
                self.sessionId= resdict['SessionID']
                self.userId = resdict['UserID']
                return True
        return False
    def logout(self,empname):
        if not self.login(empname) :
            return False
        logoffUrl = 'http://211.151.35.102/?json={"Command":"Action","Action":"Logoff","ActionID":"%s","QueueRemove":true,"User":"%s","PBX":"1.1.1.107","Account":"N000000006707","SessionID":"%s"}&_=1491900093154' % ( \
        "Logoff" + str(random.random()), self.userId, self.sessionId)
        logoffUrl1 = 'http://a1.7x24cc.com/chatSseAction?Action=SessionClose&AgentId=%s&callback=jQuery172009474883891740071_1491899986675' % \
                     self.userId
        r2 = self.session.get(logoffUrl)
        r3 = self.session.get(logoffUrl1)
        if r2.status_code==200 and r3.status_code==200:
            r2Json = r2.json()
            if r2Json['Succeed']:
                return True
        return False
