# -*- coding: utf-8 -*-
from MySpi import *
import soptthosttraderapi as api
import configparser

configins=configparser.ConfigParser()
configins.read('config.ini')
#Addr
FrontAddr=configins['network']['tradefront']
#AuthInfo
APPID=configins['authinfo']['appid']
AUTHCODE=configins['authinfo']['authcode']
#LoginInfo
BROKERID=configins['baseinfo']['brokerid']
USERID=configins['baseinfo']['userid']
PASSWORD=configins['baseinfo']['password']


class CTradeApi(api.CThostFtdcTraderApi):
	def __init__(self):
		self.tspi=''
		self.tapi=''
		self.result=''
		self.starttime=''

	def start(self):
		self.tapi=api.CThostFtdcTraderApi.CreateFtdcTraderApi()
		self.tspi=CTradeSpi(self)
		self.tapi.RegisterFront(FrontAddr)
		self.tapi.RegisterSpi(self.tspi)
		self.tapi.SubscribePrivateTopic(api.THOST_TERT_RESTART)
		self.tapi.SubscribePublicTopic(api.THOST_TERT_RESTART)
		self.tapi.Init()

	def ReqAuth(self):
		authfield = api.CThostFtdcReqAuthenticateField()
		authfield.BrokerID=BROKERID
		authfield.UserID=USERID
		authfield.AppID=APPID
		authfield.AuthCode=AUTHCODE
		self.tapi.ReqAuthenticate(authfield,0)
		PrintSendName("ReqAuthenticate")

	def ReqLogin(self):
		loginfield = api.CThostFtdcReqUserLoginField()
		loginfield.BrokerID=BROKERID
		loginfield.UserID=USERID
		loginfield.Password=PASSWORD
		loginfield.UserProductInfo="python dll"
		self.tapi.ReqUserLogin(loginfield,0)
		PrintSendName("ReqUserLogin")

def PrintSendName(sendname):
	print("send", sendname, "ok")