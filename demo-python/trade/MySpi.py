# -*- coding: utf-8 -*-
from MyApi import *
import datetime
import time
import os
import sys
import soptthosttraderapi as api


class CTradeSpi(api.CThostFtdcTraderSpi):
	myapi=''
	def __init__(self,myapi):
		api.CThostFtdcTraderSpi.__init__(self)
		self.myapi=myapi
		self.orderhash={}
		self.tradehash={}
		self.positionhash={}
		self.tradeseq=0
		
	def OnFrontConnected(self) -> "void":
		print ("receive OnFrontConnected")
		self.myapi.ReqAuth()
		
	def OnRspAuthenticate(self, pRspAuthenticateField: 'CThostFtdcRspAuthenticateField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":	
		PrintReName("OnRspAuthenticate")
		PrintReMsg(pRspInfo)
		self.myapi.ReqLogin()
		
	def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		PrintReName("OnRspUserLogin")
		print ("ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
		self.myapi.ReqSettleCf()

#结算单确认回调函数，确认完毕后进入报单
	def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm: 'CThostFtdcSettlementInfoConfirmField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		PrintReName("OnRspSettlementInfoConfirm")
		print ("ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
		self.myapi.ReqOrIn()

#报单插入对应的4组不同的回调函数
	def OnRspOrderInsert(self, pInputOrder: 'CThostFtdcInputOrderField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		PrintReName("OnRspOrderInsert")
		print ("ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
	

	def OnErrRtnOrderInsert(self, pInputOrder: 'CThostFtdcInputOrderField', pRspInfo: 'CThostFtdcRspInfoField') -> "void":
		PrintReName("OnErrRtnOrderInsert")
		print ("ErrorMsg=", pRspInfo.ErrorMsg)
	
	def OnRtnOrder(self, pOrder: 'CThostFtdcOrderField' ) -> "void":
		PrintReName("OnRtnOrder")
		print ("investorid=", pOrder.InvestorID , "orderstatus=", pOrder.OrderStatus, "OrderSysID", pOrder.OrderSysID)
		print ("investorid=", pOrder.InvestorID , "ExchangeID=", pOrder.ExchangeID, "OrderSysID", pOrder.OrderSysID)
		exchangeid = pOrder.ExchangeID
		sysid = pOrder.OrderSysID
		self.myapi.ReqOrDel(exchangeid, sysid)

	def OnRtnTrade(self, pTrade: 'CThostFtdcTradeField' ) -> "void":
		PrintReName("OnRtnTrade")
		print ("investorid=", pTrade.InvestorID , "TradeID=", pTrade.TradeID, "OrderSysID", pTrade.OrderSysID)

#报单操作单独对应的两组两组函数
	def OnRspOrderAction(self, pInputOrderAction: 'CThostFtdcInputOrderActionField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		PrintReName("pInputOrderAction")
		print ("ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)	
	
	def OnErrRtnOrderAction(self, pOrderAction: 'CThostFtdcOrderActionField', pRspInfo: 'CThostFtdcRspInfoField') -> "void":
		PrintReName("OnErrRtnOrderAction")
		print ("ErrorMsg=", pRspInfo.ErrorMsg)	
		

#静态处理方法内容
#打印排错返错信息
def PrintReMsg(pRspInfo):
	if pRspInfo is not None:
		print ("ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
	else:
		print ("ErrorID= null ErrorMsg= null")
		return 1

def PrintReName(rename):
	print("receive", rename)