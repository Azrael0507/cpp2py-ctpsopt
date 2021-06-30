# -*- coding: utf-8 -*-
from MyApi import *
import soptthostmduserapi as MDapi

class CFtdcMdSpi(MDapi.CThostFtdcMdSpi):

    def __init__(self,mdapi):
        MDapi.CThostFtdcMdSpi.__init__(self)
        self.mdapi=mdapi
        
    def OnFrontConnected(self) -> "void":
        print ("OnFrontConnected")
        self.mdapi.ReqLogin()
        
    def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print (f"OnRspUserLogin, SessionID={pRspUserLogin.SessionID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}")
        self.mdapi.ReqDepthMD()

    def OnRtnDepthMarketData(self, pDepthMarketData: 'CThostFtdcDepthMarketDataField') -> "void":
        print ("OnRtnDepthMarketData")

        DealTooMax(pDepthMarketData)

        mdlist=([pDepthMarketData.TradingDay,\
        pDepthMarketData.InstrumentID,\
        pDepthMarketData.LastPrice,\
        pDepthMarketData.PreSettlementPrice,\
        pDepthMarketData.PreClosePrice,\
        pDepthMarketData.PreOpenInterest,\
        pDepthMarketData.OpenPrice,\
        pDepthMarketData.HighestPrice,\
        pDepthMarketData.LowestPrice,\
        pDepthMarketData.Volume,\
        pDepthMarketData.Turnover,\
        pDepthMarketData.OpenInterest,\
        pDepthMarketData.ClosePrice,\
        pDepthMarketData.SettlementPrice,\
        pDepthMarketData.UpperLimitPrice,\
        pDepthMarketData.LowerLimitPrice,\
        pDepthMarketData.PreDelta,\
        pDepthMarketData.CurrDelta,\
        pDepthMarketData.UpdateTime,\
        pDepthMarketData.UpdateMillisec,\
        pDepthMarketData.BidPrice1,\
        pDepthMarketData.BidVolume1,\
        pDepthMarketData.AskPrice1,\
        pDepthMarketData.AskVolume1,\
        pDepthMarketData.AveragePrice])
        print (mdlist)

    def OnRspSubMarketData(self, pSpecificInstrument: 'CThostFtdcSpecificInstrumentField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspSubMarketData")
        print ("InstrumentID=",pSpecificInstrument.InstrumentID)
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)

#深度行情处理异常值
def DealTooMax(mddata):
    maxprice = 1e+15
    minprice = -1e+15
    if((mddata.SettlementPrice > maxprice) or (mddata.PreSettlementPrice < minprice)):
        mddata.SettlementPrice=0