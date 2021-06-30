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