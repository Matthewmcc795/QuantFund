import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def H4_Prices(curr_pair):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=D"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def M5_Prices(curr_pair):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=m5"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def H4_to_D(h4_price):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=m5"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def D_Prices(curr_pair):
    h4 = H4_Prices(curr_pair)
    D = H4_to_D(h4)
    return D

def Get_ATR(sec,lst_ATR):
	h_prices = []
	l_prices = []
	c_prices = []
	h = {'Authorization' : LIVE_ACCESS_TOKEN}
	url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + sec + "&count=5&candleFormat=midpoint&granularity=M15"
	r = requests.get(url, headers=h)     
	data = json.loads(r.text)
	for x in data["candles"]:
		h_prices.append(x[STRH])
		l_prices.append(x[STRL])
		c_prices.append(x[STRC])
	lst_ATR[i] = (lst_ATR[i]*13 + TR(h_prices[0], l_prices[0], c_prices[1]))/14

def Get_Pivot_Points(sec):
	h_prices = []
	l_prices = []
	c_prices = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + sec + "&count=2&candleFormat=midpoint&granularity=D"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
	for x in data["candles"]:
		h_prices.append(x[STRH])
		l_prices.append(x[STRL])
		c_prices.append(x[STRC])
    PP_val = (h[1] + l[1] + c[1])/3
    S1_val = 2*PP_val - h[1]
    R1_val = 2*PP_val - l[1]
	return PP_val, S1_val, R1_val

def ATR(index):
    p = 98
    TrueRanges = 0.0
    ATR_val = 0
    while p > 84:
        TrueRanges = TrueRanges + TR(MHigh(p),MLow(p),MClose(p+1))
        p -= 1
    ATR_val = TrueRanges/14
    while p >= 0:
        ATR_val = (ATR_val*13 + TR(MHigh(p),MLow(p),MClose(p+1)))/14
        p -= 1
    return ATR_val

lst_ATR[i] = ATR(0)

PP[i], S1[i], R1[i] = Get_Pivot_Points(sec)

# Signal Generating Functions
# Input price arrays and indicator values
# Output boolean values

def Strategy_Manager(Account_Number, Security, Strategy):
	if Strategy == "PivotPointBreakout" and (Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8)):
	# For a given account number and security check if open order policy is met
	# For a strategy check if stats are in order (For now just make sure the hours are good. )
		return True
	else:
		return False

def Order_Checker(SL, TP, mrkt_pr, Strategy):
	if Strategy == "PivotPointBreakout":
	# For a given account number and security check if open order policy is met
	# For a strategy check if stats are in order (For now just make sure the hours are good. )
        if abs(TP- mrkt_pr)/abs(SL- mrkt_pr) < 2.835 and abs(TP- mrkt_pr)/abs(SL- mrkt_pr) > 0.485:
            if abs(TP- mrkt_pr) < 78 and abs(TP- mrkt_pr) > 25:
                if abs(SL- mrkt_pr) < 30 and abs(SL- mrkt_pr) > 5:
                    return True
        else:
            return False

def Manage_Trades(account_num, sec,mrkt_pr,Strategy):

	# Make sure that orders can't swap back 

	# Ex, if a candle breaks the 2nd condition and I've moved it to BE + ATR. Then,
	# if on the next candle it's within that limit then the SL might change back to BE
	if Strategy == "PivotPointBreakout":
	    h = {'Authorization' : LIVE_ACCESS_TOKEN}
	    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_num) + "/trades?instrument=" + sec
	    r = requests.get(url, headers=h)     
	    data2 = json.loads(r.text)
	    chk = str(data2)
	    time.sleep(1)
	    
	    if chk.find("id") != -1:
	        for positions in data2["trades"]:
	            trd_ID = positions["id"]
	            trd_entry = float(positions["price"])
	            trd_side = positions["side"]
	            if trd_side == "buy":
	                if mrkt_pr > trd_entry + lst_ATR[i]/2:
	                    SL = round(trd_entry + 0.00001,5)
	                    UpdateStopLoss(229783, trd_ID, SL)
	                    lst_SL[i] = SL                   
	                elif mrkt_pr > trd_entry + lst_ATR[i]:
	                    SL = round(max(lst_SL, lst_price[i] - lst_ATR[i]) + 0.00001,5)
	                    UpdateStopLoss(229783, trd_ID, SL)
	                    lst_SL[i] = SL
	            elif mrkt_pr == "sell":
	                if mrkt_pr < trd_entry - lst_ATR[i]/2:
	                    SL = round(trd_entry - 0.00001,5)
	                    UpdateStopLoss(229783, trd_ID, SL)
	                    lst_SL[i] = SL
	                elif mrkt_pr < trd_entry - lst_ATR[i]:
	                    SL = round(min(lst_SL, lst_price[i] + lst_ATR[i]) - 0.00001,5)
	                    UpdateStopLoss(229783, trd_ID, SL)
	                    lst_SL[i] = SL


def PivotPointBreakout(m5_price):
    if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
        if M5Close(0) < R1[i] and M5Close(1) < R1[i] and M5Close(2) > R1[i]:
            SL = round(M5Close(0) + lst_ATR[i] + 0.00001,5)
            TP = round(M5Close(0) - lst_ATR[i]*3 - 0.00001,5)
            OpenOrder(229783, Sec[i], 200, "market", "sell", TP, SL)
            lst_SL[i] = SL
        elif M5Close(0) > S1[i] and M5Close(1) > S1[i] and M5Close(2) < S1[i]:
            SL = round(M5Close(0) - lst_ATR[i] - 0.00001,5)
            TP = round(M5Close(0) + lst_ATR[i]*3 + 0.00001,5)
            OpenOrder(229783, Sec[i], 200, "market", "buy", TP, SL)
            lst_SL[i] = SL
    lst_price[i] = M5Close(0)

                        
