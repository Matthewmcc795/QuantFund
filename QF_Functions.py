# This file handles all dictionaries, datetime calculations and order functions
# May also handle data functions used for Optimizer
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from QF_Strategy import *
from QF_Optimizer import *
from datetime import datetime, timedelta
import time
import sys

hr = [2,6,10,14,18,22]

##########################################################################################################
#                                                                                                        #
#                                             Dictionaries                                               #
#                                                                                                        #
##########################################################################################################

Positions = {
    "PPB": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "MAC": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "BusRide": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "IT": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "CS": {
    "EUR_USD": 0, "GBP_USD": 0, "GBP_CHF": 0, "GBP_CAD": 0, "EUR_CAD": 0, 
    "GBP_AUD": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0}
}

PPB = {
    "ATR": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "SL": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0
    }, 
}

MAC = {
    "Z": {"EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0}
}

PP = {
    "S2": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "S1": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "PP": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "R1": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "R2": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "Update": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "Position": {
    "EUR_USD": "", "GBP_USD": "", "USD_CAD": "", "AUD_USD": "", "NZD_USD": "", "USD_CHF": "", "GBP_CHF": "", 
    "EUR_GBP": "", "GBP_CAD": "", "NZD_CAD": "", "AUD_CHF": "", "EUR_CAD": "", "GBP_AUD": "", "NZD_CHF": "", 
    "AUD_NZD": "", "CAD_CHF": "", "EUR_AUD": "", "GBP_NZD": "", "EUR_CHF": "", "EUR_NZD": "", "AUD_CAD": ""}
}

IT = {
    "SMA50": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "TP": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "SL": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "BEP": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "BEV": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "counter": {
    "EUR_USD": -1, "GBP_USD": -1, "USD_CAD": -1, "AUD_USD": -1, "NZD_USD": -1, "USD_CHF": -1, "GBP_CHF": -1, 
    "EUR_GBP": -1, "GBP_CAD": -1, "NZD_CAD": -1, "AUD_CHF": -1, "EUR_CAD": -1, "GBP_AUD": -1, "NZD_CHF": -1, 
    "AUD_NZD": -1, "CAD_CHF": -1, "EUR_AUD": -1, "GBP_NZD": -1, "EUR_CHF": -1, "EUR_NZD": -1, "AUD_CAD": -1}
}

##########################################################################################################
#                                                                                                        #
#                                              Date/Time                                                 #
#                                                                                                        #
##########################################################################################################
def Get_dt(strat):
	if strat == "dt_Intraday_PPB":
		dt_Intraday_PPB =  datetime.now()
		dt_Intraday_PPB = dt_Intraday_PPB.replace(minute=2, second=0,microsecond=1)
		while dt_Intraday_PPB < datetime.now():
		    dt_Intraday_PPB += timedelta(minutes=5)
		return dt_Intraday_PPB
	elif strat == "dt_Intraday_MAC":
		dt_Intraday_MAC =  datetime.now()
		dt_Intraday_MAC = dt_Intraday_MAC.replace(minute=3, second=0,microsecond=1)
		while dt_Intraday_MAC < datetime.now():
		    dt_Intraday_MAC += timedelta(minutes=15)
		return dt_Intraday_MAC
	elif strat == "dt_Intraday_BusRide":
		dt_Intraday_BusRide =  datetime.now()
		dt_Intraday_BusRide = dt_Intraday_BusRide.replace(minute=2, second=0,microsecond=1)
		while dt_Intraday_BusRide < datetime.now():
		    dt_Intraday_BusRide += timedelta(minutes=15)
		return dt_Intraday_BusRide
	elif strat == "dt_Intraday_IntraTrend":
		dt_Intraday_IntraTrend =  datetime.now()
		dt_Intraday_IntraTrend = dt_Intraday_IntraTrend.replace(minute=2, second=0,microsecond=1)
		while dt_Intraday_IntraTrend < datetime.now():
		    dt_Intraday_IntraTrend += timedelta(minutes=15)
		return dt_Intraday_IntraTrend
	elif strat == "dt_Swing_PPB":
		dt_Swing_PPB =  datetime.now()
		dt_Swing_PPB = dt_Swing_PPB.replace(minute=2, second=0,microsecond=1)
		while dt_Swing_PPB.hour != 21:
		    dt_Swing_PPB  += timedelta(hours=1)
		return dt_Swing_PPB
	elif strat == "dt_Swing_MAC":
		dt_Swing_MAC =  datetime.now()
		dt_Swing_MAC = dt_Swing_MAC.replace(minute=3, second=0,microsecond=1)
		while not dt_Swing_MAC.hour in hr:
		    dt_Swing_MAC += timedelta(hours=1)
		return dt_Swing_MAC
	elif strat == "dt_Swing_BusRide":
		dt_Swing_BusRide =  datetime.now()
		dt_Swing_BusRide = dt_Swing_BusRide.replace(minute=2, second=0,microsecond=1)
		while dt_Swing_BusRide.hour != 21:
		    dt_Swing_BusRide += timedelta(hours=1)
		return dt_Swing_BusRide
	elif strat == "dt_Swing_IntraTrendD":
		dt_Swing_IntraTrendD =  datetime.now()
		dt_Swing_IntraTrendD = dt_Swing_IntraTrendD.replace(minute=2, second=0,microsecond=1)
		while dt_Swing_IntraTrendD.hour != 21:
		    dt_Swing_IntraTrendD += timedelta(minutes=15)
		return dt_Swing_IntraTrendD
	elif strat == "dt_Swing_IntraTrendW":
		dt_Swing_IntraTrendW =  datetime.now()
		dt_Swing_IntraTrendW = dt_Swing_IntraTrendW.replace(minute=2, second=0,microsecond=1)
		while dt_Swing_IntraTrendW.hour != 21 and dt_Swing_IntraTrendW.weekday() == 0:
		    dt_Swing_IntraTrendW += timedelta(hours=1)
		return dt_Swing_IntraTrendW
	elif strat == "dt_Intraday_CableSnap":
		dt_Intraday_CableSnap =  datetime.now()
		dt_Intraday_CableSnap = dt_Intraday_CableSnap.replace(minute=2, second=0,microsecond=1)
		while dt_Intraday_CableSnap < datetime.now():
		    dt_Intraday_CableSnap += timedelta(minutes=15)
		return dt_Intraday_CableSnap
	elif strat == "dt_Swing_CableSnap":
		dt_Swing_CableSnap =  datetime.now()
		dt_Swing_CableSnap = dt_Swing_CableSnap.replace(minute=2, second=0,microsecond=1)
		while dt_Swing_CableSnap.hour != 21:
		    dt_Swing_CableSnap  += timedelta(hours=1)
		return dt_Swing_CableSnap

##########################################################################################################
#                                                                                                        #
#                                               Orders                                                   #
#                                                                                                        #
##########################################################################################################

# def OpenLimitOrder(Account_Num, instrument, units, order_type, price, order_side, Take_Profit, Stop_Loss):
#     conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
#     headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
#     file = open(name,'a')
#     file.write("Sending order... " + "\n")
#     file.close()
#     params = urllib.urlencode({
#         "instrument" : str(instrument),
#         "units" : units,
#         "type" : order_type,
#         "price" : price,
#         "side" : order_side,
#         "takeProfit": Take_Profit,
#         "stopLoss": Stop_Loss
#     })
#     conn.request("POST", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
#     response = conn.getresponse().read()
#     file = open(name,'a')
#     file.write(response + "\n")
#     file.close()

def UpdateStopLoss(Account_Num, trade_ID, Stop_Loss, file_str):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    params = urllib.urlencode({"stopLoss": Stop_Loss})
    file = open(file_str,'a')
    file.write("Updating Stop Loss ... " + "\n")
    file.close()
    conn.request("PATCH", "/v1/accounts/" + str(Account_Num) + "/trades/" + str(trade_ID), params, headers)
    response = conn.getresponse().read()
    file = open(file_str,'a')
    file.write(response + "\n")
    file.close()
    time.sleep(1)

def ClosePositions(Account_Num, sec, file_str):
    file = open(file_str,'a')
    file.write("Closing positions... " + "\n")
    file.close()
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/positions/" + sec
    r = requests.delete(url, headers=h)     
    time.sleep(1)

def GetOpenTrades(Account_Num, sec):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h) 
    time.sleep(1)    
    return json.loads(r.text)

def OpenMarketOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss, file_str):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    file = open(file_str,'a')
    file.write("Sending order... " + "\n")
    file.close()
    params = urllib.urlencode({
        "instrument" : str(instrument),
        "units" : units,
        "type" : order_type,
        "side" : order_side,
        "takeProfit": Take_Profit,
        "stopLoss": Stop_Loss
    })
    conn.request("POST", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
    response = conn.getresponse().read()
    file = open(file_str,'a')
    file.write(response + "\n")
    file.close()
    time.sleep(1)

def GetOpenUnits(account_id, sec, sec_list):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/positions"
    r = requests.get(url, headers=h)     
    data2 = json.loads(r.text)
    chk = str(data2)
    Units = 0
    if chk.find("positions") != -1:
        for positions in data2["positions"]:
            if sec[:3] == "USD" or sec[-3:] == "USD":
                if positions["instrument"] == sec:
                    Units = positions["units"]
            else:
                ticker_string1 = sec[:3] + "USD"
                ticker_string2 = sec[-3:] + "USD"
                if ticker_string1 not in sec_list:
                    ticker_string1 = "USD" + sec[:3]
                elif ticker_string2 not in sec_list:
                    ticker_string2 = "USD" + sec[-3:]
                if positions["instrument"] == ticker_string1 or positions["instrument"] == ticker_string2 or positions["instrument"] == sec:
                    Units += positions["units"]                   
    time.sleep(1)
    return Units

def GetOpenTradeIDs(Account_Num, sec):
    trd_ids = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h)
    for positions in Open_Trades["trades"]:
        trd_ids.append(positions["id"])
    time.sleep(1)    
    return trd_ids

def SaveToLog(file_name, msg):
    file = open(file_name,'a')
    file.write(msg + " " + str(datetime.now()) +"\n")
    file.close()
