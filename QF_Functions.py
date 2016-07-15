# This file handles all dictionaries, datetime calculations and order functions
# May also handle data functions used for Optimizer
import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STRV, STRCO, PWD
import httplib
import urllib
from QF_Strategy import *
from QF_Optimizer import *
from datetime import datetime, timedelta
import time
import sys
import smtplib

def Get_Price(curr_pair, tf, bars, ohlc):
    O = []
    H = []
    L = []
    C = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(curr_pair) + "&count=" + str(bars) + "&candleFormat=midpoint&granularity=" + str(tf)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    for i in range(len(data["candles"])):
        O.append(data["candles"][bars - i - 1][STRO])
        H.append(data["candles"][bars - i - 1][STRH])
        L.append(data["candles"][bars - i - 1][STRL])
        C.append(data["candles"][bars - i - 1][STRC])
    time.sleep(1)
    if ohlc == "ohlc":
        return O, H, L, C
    elif ohlc == "hlc":
        return H, L, C
    elif ohlc == "c":
        return C
hr = [2,6,10,14,18,22]

##########################################################################################################
#                                                                                                        #
#                                           Email & Reports                                              #
#                                                                                                        #
##########################################################################################################

def Report(report_temp, account_id, access_token):
    sec = ["EUR_USD", "GBP_USD", "USD_JPY", "USD_CAD", "AUD_USD", "NZD_USD"]
    if report_temp == "DailyReport":
        dt_now = str(datetime.now())
        dat = "Daily Report on " + str(account_id) + " as of " + str(dt_now[:10]) + "\n" 
        p = []
        j = 0
        vals = ["units", "instrument", "side", "avgPrice"]
        h = {'Authorization' : access_token}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/positions"
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        if chk.find("positions") != -1:
            for positions in data2["positions"]:
                p.append([])
                for i in range(len(vals)):
                    p[j].append(positions[vals[i]])
                j += 1
        dat = dat + "\n# -----      Open Positions     ----- #  \n"
        for news in p:
            if news[1] not in sec:
                sec.append(news[1])
            o, h, l, c = Get_Price(news[1], "D", 3, "ohlc")
            if news[2] == "sell":
                pl = str(round(100*(float(news[3])/c[0] - 1), 2)) + "%"
            elif news[2] == "buy":
                pl = str(round(100*(c[0]/float(news[3]) - 1), 2)) + "%"
            for items in news:
                dat = dat + " " + str(items)
            dat = dat + " " + pl
            dat = dat + str("\n")
            sec[i], c[0]/o[1] - 1 

        p = []
        j = 0
        vals = ["title", "impact", "currency"]
        h = {'Authorization' : access_token}
        url = "https://api-fxtrade.oanda.com/labs/v1/calendar?period=86400"
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        if chk.find("title") != -1:
            for positions in data2:
                p.append([])
                for i in range(len(vals)):
                    p[j].append(positions[vals[i]])
            j += 1

        dat = dat + "\n# -----        Market News      ----- #  \n"
        for news in p:
            for items in news:
                dat = dat + " " + str(items)
            dat = dat + str("\n")
        dat = dat + str("\n")

        p = []
        j = 0
        vals = ["accountName", "balance", "unrealizedPl", "marginUsed", "marginAvail", "openTrades", "openOrders", "accountCurrency"]
        h = {'Authorization' : access_token}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id)
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        for i in range(len(vals)):
            p.append(data2[vals[i]])

        dat = dat + "\n# -----       Account Info      ----- #  \n"
        for items in p:
            dat = dat + " " + str(items)
        dat = dat + str("\n")

        dat = dat + "\n# -----       Market Moves      ----- #  \n"

        for i in range(len(sec)):
            o, h, l, c = Get_Price(sec[i], "D", 3, "ohlc")
            dat = dat + " " + str(sec[i]) + " " + str(round(c[0]-o[1],5)) + "\n"
        return dat

def SendEmail(from_addr, pwd, to_addr, subject, message):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(from_addr, pwd)
    problems = server.sendmail(from_addr, to_addr, message)
    server.quit()

def AccountInfo(account_id, access_token):
    dat = []
    rang = ["accountId", "accountName", "balance", "unrealizedPl", 
    "realizedPl", "marginUsed", "marginAvail", "openTrades", 
    "openOrders", "marginRate", "accountCurrency"]
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    for i in range(len(rang)):
        dat.append(data[rang[i]])
    print dat
    time.sleep(1)

def GetTransactions(account_id, maxid):
    dat = []
    dat.append([])
    j = 0
    rang_Mkt_Ord = ["stopLossPrice", "takeProfitPrice", "accountBalance", "price", "side", "instrument", "tradeOpened", "interest", "time", "units", "id", "pl"]
    rang_Trans_Funds = ["reason", "accountBalance", "amount", "time", "id"]
    rang_Stop_Filled = ["tradeId", "accountBalance", "price", "side", "instrument", "interest", "time", "units", "id", "pl"]
    rang_Take_Profit_Filled = ["tradeId", "accountBalance", "price", "side", "instrument", "interest", "time", "units", "id", "pl"]
    rang_Trade_Close = ["tradeId", "accountBalance", "price", "side", "instrument", "interest", "time", "units", "id", "pl"]
    rang_Trade_Update = ["stopLossPrice", "takeProfitPrice", "tradeId", "instrument", "time", "units", "id"]
    rang_Daily_Int = ["accountBalance", "instrument", "interest", "time", "id"]
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    if maxid == "":
        url =   "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/transactions?count=500"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        for trans in data["transactions"]:
            if str(trans["type"]) == "MARKET_ORDER_CREATE":
                dat.append([])
                for i in range(len(rang_Mkt_Ord)):
                    dat[j].append(str(trans[rang_Mkt_Ord[i]]))
                j += 1
            elif str(trans["type"]) == "TRANSFER_FUNDS":
                dat.append([])
                for i in range(len(rang_Trans_Funds)):
                    dat[j].append(str(trans[rang_Trans_Funds[i]]))
                j += 1
            elif str(trans["type"]) == "STOP_LOSS_FILLED":
                dat.append([])
                for i in range(len(rang_Stop_Filled)):
                    dat[j].append(str(trans[rang_Stop_Filled[i]]))
                j += 1
            elif str(trans["type"]) == "TAKE_PROFIT_FILLED":
                dat.append([])
                for i in range(len(rang_Take_Profit_Filled)):
                    dat[j].append(str(trans[rang_Take_Profit_Filled[i]]))
                j += 1
            elif str(trans["type"]) == "TRADE_CLOSE":
                dat.append([])
                for i in range(len(rang_Trade_Close)):
                    dat[j].append(str(trans[rang_Trade_Close[i]]))
                j += 1
            # elif str(trans["type"]) == "TRADE_UPDATE":
            #   for i in range(len(rang_Trade_Update)):
            #       dat[0].append(str(trans[rang_Trade_Update[i]]))
            # elif str(trans["type"]) == "DAILY_INTEREST":
            #   for i in range(len(rang_Daily_Int)):
            #       dat[0].append(str(trans[rang_Daily_Int[i]]))            
        time.sleep(60)
    return dat

def TransactionHistory(account_id, end_dt):
    dt, minid = GetTransactions(account_id, "")
    dt = datetime.strptime(dt, '%Y-%m-%d')
    end_dt = datetime.strptime(end_dt, '%Y-%m-%d')
    print 1
    while dt > end_dt:
        time.sleep(60)
        dt, minid = GetTransactions(account_id, minid)
        dt = datetime.strptime(dt, '%Y-%m-%d')
    print "Complete"

def pYear(dt):
    return int(dt[:4])

def pMonth(dt):
    mnth = dt[:7]
    return int(mnth[len(mnth)-2:])

def pDay(dt):
    return int(dt[len(dt) -2:])

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
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0} 
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

ITD = {
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

ITW = {
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

Banzai = {
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
    "counter": {"GBP_JPY": 0, "USD_JPY": 0, "AUD_JPY": 0}
}

CSIntraday = {
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

CSSwing = {
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
    elif strat == "dt_Intraday_Banzai":
        dt_Intraday_Banzai =  datetime.now()
        dt_Intraday_Banzai = dt_Intraday_Banzai.replace(minute=2, second=0,microsecond=1)
        while dt_Intraday_Banzai < datetime.now():
            dt_Intraday_Banzai += timedelta(minutes=15)
        return dt_Intraday_Banzai
    elif strat == "dt_Swing_CableSnap":
        dt_Swing_CableSnap =  datetime.now()
        dt_Swing_CableSnap = dt_Swing_CableSnap.replace(minute=2, second=0,microsecond=1)
        while dt_Swing_CableSnap.hour != 21:
            dt_Swing_CableSnap  += timedelta(hours=1)
        return dt_Swing_CableSnap
    elif strat == "DailyReport":
        dt_report =  datetime.now()
        dt_report = dt_report.replace(minute=2, second=0,microsecond=1)
        while dt_report.hour != 21:
            dt_report  += timedelta(hours=1)
        return dt_report

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

def UpdateStopLoss(Account_Num, trade_ID, Stop_Loss, file_str, access_token):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": access_token}
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

def ClosePositions(Account_Num, sec, file_str, access_token):
    file = open(file_str,'a')
    file.write("Closing positions... " + "\n")
    file.close()
    h = {'Authorization' : access_token}
    url =   "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/positions/" + sec
    r = requests.delete(url, headers=h)     
    time.sleep(1)

def GetOpenTrades(Account_Num, sec, access_token):
    h = {'Authorization' : access_token}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h) 
    time.sleep(1)    
    return json.loads(r.text)

def OpenMarketOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss, file_str, access_token):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": access_token}
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

def GetOpenUnits(account_id, sec, sec_list, access_token):
    h = {'Authorization' : access_token}
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
                ticker_str1 = sec[:3] + "USD"
                ticker_str2 = sec[-3:] + "USD"
                if ticker_str1 not in sec_list:
                    ticker_str1 = "USD" + sec[:3]
                elif ticker_str2 not in sec_list:
                    ticker_str2 = "USD" + sec[-3:]
                if positions["instrument"] == ticker_str1 or positions["instrument"] == ticker_str2 or positions["instrument"] == sec:
                    Units += positions["units"]               
    time.sleep(1)
    return Units

def GetOpenTradeIDs(Account_Num, sec, access_token):
    trd_ids = []
    h = {'Authorization' : access_token}
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