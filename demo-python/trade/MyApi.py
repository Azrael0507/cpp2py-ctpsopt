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
#OrderInfo
INSTRID=configins['orderinfo']['instrid']
PRICETYPE=configins['orderinfo']['pricetype']
DIR=configins['orderinfo']['dir']
OFFSET=configins['orderinfo']['offset']
HEDGE=configins['orderinfo']['hedge']
PRICE=float(configins['orderinfo']['price'])
VOLUME=int(configins['orderinfo']['volume'])


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
#结算单确认函数，每日交易前，需要首先进行结算单确认，否则报单被拒
	def ReqSettleCf(self):
		settleconfirm=api.CThostFtdcSettlementInfoConfirmField()
		settleconfirm.BrokerID=BROKERID
		settleconfirm.InvestorID=USERID
		self.tapi.ReqSettlementInfoConfirm(settleconfirm, 0)
		PrintSendName("ReqSettleCf")




#报单录入函数
	def ReqOrIn(self):
		Orderfield = api.CThostFtdcInputOrderField()
		Orderfield.BrokerID=BROKERID
		Orderfield.InvestorID=USERID
		Orderfield.InstrumentID=INSTRID
		Orderfield.OrderRef="001"
		Orderfield.OrderPriceType=PRICETYPE
		Orderfield.Direction=DIR
		Orderfield.CombOffsetFlag=OFFSET
		Orderfield.CombHedgeFlag=HEDGE
		Orderfield.LimitPrice=PRICE
		Orderfield.VolumeTotalOriginal=VOLUME
		Orderfield.TimeCondition=api.THOST_FTDC_TC_GFD
		Orderfield.VolumeCondition=api.THOST_FTDC_VC_AV
		Orderfield.ContingentCondition=api.THOST_FTDC_CC_Immediately
		Orderfield.ForceCloseReason=api.THOST_FTDC_FCC_NotForceClose
		Orderfield.IsAutoSuspend=0
		Orderfield.IsSwapOrder=0
		Orderfield.UserForceClose=0
		self.tapi.ReqOrderInsert(Orderfield,0)
		PrintSendName("ReqOrderInsert")

#报单撤销函数
	def ReqOrDel(self, ExchangeID, OrderSysID):
		pDelOrder=api.CThostFtdcInputOrderActionField()
		pDelOrder.BrokerID=BROKERID
		pDelOrder.InvestorID=USERID
		pDelOrder.UserID=USERID
		pDelOrder.ExchangeID=ExchangeID
		pDelOrder.ActionFlag=api.THOST_FTDC_AF_Delete
		pDelOrder.OrderSysID=OrderSysID
		self.tapi.ReqOrderAction(pDelOrder, 0)
		PrintSendName("ReqOrderAction")


	

def PrintSendName(sendname):
	print("send", sendname, "ok")