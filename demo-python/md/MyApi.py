# -*- coding: utf-8 -*-
from MySpi import *
import soptthostmduserapi as MDapi
import csv
import configparser

configins=configparser.ConfigParser()
configins.read('config.ini')

#Addr
FrontAddr=configins['network']['mdfront']
#AuthInfo
APPID=configins['authinfo']['appid']
AUTHCODE=configins['authinfo']['authcode']
#LoginInfo
BROKERID=configins['baseinfo']['brokerid']
USERID=configins['baseinfo']['userid']
PASSWORD=configins['baseinfo']['password']
#mddata
MDID=configins['mddata']['mdid'].split(',')
print(MDID)

class CMDApi(MDapi.CThostFtdcMdApi):
    def __init__(self):
        self.mdspi=''
        self.mdapi=''

    def start(self):
        self.mdapi=MDapi.CThostFtdcMdApi.CreateFtdcMdApi()
        self.mdspi=CFtdcMdSpi(self)
        self.mdapi.RegisterFront(FrontAddr)
        self.mdapi.RegisterSpi(self.mdspi)
        self.mdapi.Init()
    
    def ReqLogin(self):
        loginfield = MDapi.CThostFtdcReqUserLoginField()
        loginfield.BrokerID=BROKERID
        loginfield.UserID=USERID
        loginfield.Password=PASSWORD
        loginfield.UserProductInfo="python dll"
        self.mdapi.ReqUserLogin(loginfield,0)
    
    def ReqDepthMD(self):
        for i in range(len(MDID)):
            MDID[i]=MDID[i].encode('utf-8')
        ret=self.mdapi.SubscribeMarketData(MDID,len(MDID))
