# This file handles all dictionaries, datetime calculations and order functions
# May also handle data functions used for Optimizer
import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from QF_Strategy import *
# from QF_Optimizer import *
from datetime import datetime, timedelta
import time
import sys
import smtplib

hr = [0,4,8,12,16,20]

##########################################################################################################
#                                                Prices                                                  #
##########################################################################################################

def Get_Price(curr_pair, tf, bars, ohlc, rep):
    O = []
    H = []
    L = []
    C = []
    OB = []
    HB = []
    LB = []
    CB = []
    OA = []
    HA = []
    LA = []
    CA = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(curr_pair) + "&count=" + str(bars) + "&candleFormat=" + str(rep) +"&granularity=" + str(tf)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    time.sleep(1)
    if rep == "midpoint":
        for i in range(len(data["candles"])):
            O.append(data["candles"][bars - i - 1][STRO])
            H.append(data["candles"][bars - i - 1][STRH])
            L.append(data["candles"][bars - i - 1][STRL])
            C.append(data["candles"][bars - i - 1][STRC])
        if ohlc == "ohlc":
            return O, H, L, C
        elif ohlc == "hlc":
            return H, L, C
        elif ohlc == "c":
            return C
    else:
        for i in range(len(data["candles"])):
            CB.append(data["candles"][bars - i - 1][STRCB])
            CA.append(data["candles"][bars - i - 1][STRCA])
        if ohlc == "c":
            return CB, CA

##########################################################################################################
#                                           Email & Reports                                              #
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
			o = []
			c = []
			h = {'Authorization' : LIVE_ACCESS_TOKEN}
			url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(sec[i]) + "&count=3&candleFormat=midpoint&granularity=D"
			r = requests.get(url, headers=h)     
			data = json.loads(r.text)
			for i in range(len(data["candles"])):
				o.append(data["candles"][3 - i - 1][STRO])
				c.append(data["candles"][3 - i - 1][STRC])
			time.sleep(1)
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
#                                             Dictionaries                                               #
##########################################################################################################

Analysis = {
    "Analysis_Type": {"Param1": 0, "Param2": 0, "Param3": 0, "Param4": 0, "Param5": 0}
}

Strat = {
    "PPB": {
    "InitialBalance": 0, "DailyPl": "", "Vol": 0, "Stop": 0
    },
    "IT": {
    "InitialBalance": 0, "DailyPl": "", "Vol": 0, "Stop": 0
    }
}

PPB = {
    "ATR": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "SL": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}, 
    "TP": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "Units": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "Open": {
    "EUR_USD": datetime.now(), "GBP_USD": datetime.now(), "USD_CAD": datetime.now(), "AUD_USD": datetime.now(), "NZD_USD": datetime.now(), "USD_CHF": datetime.now(), "GBP_CHF": datetime.now(), 
    "EUR_GBP": datetime.now(), "GBP_CAD": datetime.now(), "NZD_CAD": datetime.now(), "AUD_CHF": datetime.now(), "EUR_CAD": datetime.now(), "GBP_AUD": datetime.now(), "NZD_CHF": datetime.now(), 
    "AUD_NZD": datetime.now(), "CAD_CHF": datetime.now(), "EUR_AUD": datetime.now(), "GBP_NZD": datetime.now(), "EUR_CHF": datetime.now(), "EUR_NZD": datetime.now(), "AUD_CAD": datetime.now()},
    "Status": {
    "EUR_USD": "", "GBP_USD": "", "USD_CAD": "", "AUD_USD": "", "NZD_USD": "", "USD_CHF": "", "GBP_CHF": "", 
    "EUR_GBP": "", "GBP_CAD": "", "NZD_CAD": "", "AUD_CHF": "", "EUR_CAD": "", "GBP_AUD": "", "NZD_CHF": "", 
    "AUD_NZD": "", "CAD_CHF": "", "EUR_AUD": "", "GBP_NZD": "", "EUR_CHF": "", "EUR_NZD": "", "AUD_CAD": ""},
    "Op": {
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

Optimizer = {
    "EUR_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "GBP_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "USD_CAD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "AUD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "NZD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0} 
}

Indicators = {
    "EUR_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "GBP_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "USD_CAD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "AUD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "NZD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}
}

PriceAction = {
    "EUR_USD": {
    "SMA10Bounce": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "GBP_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "USD_CAD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "AUD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}, 
    "NZD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}
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
    "Units": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0},
    "Open": {
    "EUR_USD": datetime.now(), "GBP_USD": datetime.now(), "USD_CAD": datetime.now(), "AUD_USD": datetime.now(), "NZD_USD": datetime.now(), "USD_CHF": datetime.now(), "GBP_CHF": datetime.now(), 
    "EUR_GBP": datetime.now(), "GBP_CAD": datetime.now(), "NZD_CAD": datetime.now(), "AUD_CHF": datetime.now(), "EUR_CAD": datetime.now(), "GBP_AUD": datetime.now(), "NZD_CHF": datetime.now(), 
    "AUD_NZD": datetime.now(), "CAD_CHF": datetime.now(), "EUR_AUD": datetime.now(), "GBP_NZD": datetime.now(), "EUR_CHF": datetime.now(), "EUR_NZD": datetime.now(), "AUD_CAD": datetime.now()},
    "Status": {
    "EUR_USD": "", "GBP_USD": "", "USD_CAD": "", "AUD_USD": "", "NZD_USD": "", "USD_CHF": "", "GBP_CHF": "", 
    "EUR_GBP": "", "GBP_CAD": "", "NZD_CAD": "", "AUD_CHF": "", "EUR_CAD": "", "GBP_AUD": "", "NZD_CHF": "", 
    "AUD_NZD": "", "CAD_CHF": "", "EUR_AUD": "", "GBP_NZD": "", "EUR_CHF": "", "EUR_NZD": "", "AUD_CAD": ""},
    "Op": {
    "EUR_USD": 0, "GBP_USD": 0, "USD_CAD": 0, "AUD_USD": 0, "NZD_USD": 0, "USD_CHF": 0, "GBP_CHF": 0, 
    "EUR_GBP": 0, "GBP_CAD": 0, "NZD_CAD": 0, "AUD_CHF": 0, "EUR_CAD": 0, "GBP_AUD": 0, "NZD_CHF": 0, 
    "AUD_NZD": 0, "CAD_CHF": 0, "EUR_AUD": 0, "GBP_NZD": 0, "EUR_CHF": 0, "EUR_NZD": 0, "AUD_CAD": 0}
}

##########################################################################################################
#                                              Date/Time                                                 #
##########################################################################################################
def Get_dt(strat):
    if strat == "dt_PPB":
        dt_PPB =  datetime.now()
        dt_PPB = dt_PPB.replace(minute=0, second=0,microsecond=1)
        while dt_PPB < datetime.now():
            dt_PPB += timedelta(minutes=5)
        return dt_PPB
    elif strat == "dt_IT":
        dt_IT =  datetime.now()
        dt_IT = dt_IT.replace(minute=0, second=0,microsecond=1)
        while dt_IT < datetime.now():
            dt_IT += timedelta(minutes=15)
        return dt_IT
    elif strat == "dt_MAC":
        dt_MAC =  datetime.now()
        dt_MAC = dt_MAC.replace(minute=0, second=0,microsecond=1)
        while not dt_MAC.hour in hr:
            dt_MAC += timedelta(hours=1)
        return dt_MAC
    elif strat == "MainReport":
        dt_report =  datetime.now()
        dt_report = dt_report.replace(minute=0, second=0,microsecond=1)
        while dt_report.hour not in [5,17]:
            dt_report  += timedelta(hours=1)
        return dt_report
    elif strat == "WeeklyReport":
        dt_report =  datetime.now()
        dt_report = dt_report.replace(minute=0, second=0,microsecond=1)
        while dt_report.hour != 17 and dt_report.weekday != 4:
            dt_report  += timedelta(hours=1)
        return dt_report
    elif strat == "dt_Daily":
        dt_report =  datetime.now()
        dt_report = dt_report.replace(minute=0, second=0,microsecond=1)
        while dt_report.hour != 17:
            dt_report  += timedelta(hours=1)
        return dt_report
    elif strat == "dt_SessionPrep":
        dt_report =  datetime.now()
        dt_report = dt_report.replace(minute=0, second=0,microsecond=1)
        while dt_report.hour != 5:
            dt_report  += timedelta(hours=1)
        return dt_report


##########################################################################################################
#                                               Orders                                                   #
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
    file.write("Updating Stop Loss ... " + str(datetime.now()) + "\n")
    file.close()
    conn.request("PATCH", "/v1/accounts/" + str(Account_Num) + "/trades/" + str(trade_ID), params, headers)
    response = conn.getresponse().read()
    file = open(file_str,'a')
    file.write(response + "\n")
    file.close()
    time.sleep(1)

def ClosePositions(Account_Num, sec, file_str, access_token):
    file = open(file_str,'a')
    file.write("Closing positions... " + str(datetime.now()) + "\n")
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
    file.write("Sending order... " + str(datetime.now()) + "\n")
    file.close()
    if Take_Profit == 0.0 and Stop_Loss == 0.0: 
        params = urllib.urlencode({
            "instrument" : str(instrument),
            "units" : units,
            "type" : order_type,
            "side" : order_side})
    else:
        params = urllib.urlencode({
            "instrument" : str(instrument),
            "units" :   units,
            "type" : order_type,
            "side" : order_side,
            "takeProfit": Take_Profit,
            "stopLoss": Stop_Loss})
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

def GetAccountBalance(account_id, access_token):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    return data["balance"]

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


##########################################################################################################
#                                              Indicators                                                #
##########################################################################################################

def Get_Pivot_Points(sec, curr_price):
    if curr_price >= PP["R2"][sec]:
        PP["Position"][sec] = "R2"
    elif curr_price >= PP["R1"][sec] and curr_price < PP["R2"][sec]:
        PP["Position"][sec] = "R1-R2"
    elif curr_price >= PP["PP"][sec] and curr_price < PP["R1"][sec]:
        PP["Position"][sec] = "PP-R1"
    elif curr_price >= PP["S1"][sec] and curr_price < PP["PP"][sec]:
        PP["Position"][sec] = "S1-PP"
    elif curr_price >= PP["S2"][sec] and curr_price < PP["S1"][sec]:
        PP["Position"][sec] = "S2-S1"
    elif curr_price < PP["S2"][sec]:
        PP["Position"][sec] = "S2"
    pos = PP["Position"][sec]
    if pos == "R2":
        s, r = PP[pos][sec], 2*curr_price
    elif pos == "S2":
        s, r = 0, PP[pos][sec]
    elif pos != "":
        s, r = PP[pos[:2]][sec], PP[pos[-2:]][sec]
    return s, r

def TR(h,l,yc):
    x = h-l
    y = abs(h-yc)
    z = abs(l-yc)
    if y <= x >= z:
        TR = x
    elif x <= y >= z:
        TR = y
    elif x <= z >= y:
        TR = z
    return TR

def TrueRanges(h, l, c):
    tr = []
    tr.append(0)
    for i in range(1, len(c)):
        tr.append(TR(h[i], l[i], c[i-1]))
    return tr

def ROC(c):
    roc = []
    for i in range(len(c)):
        roc.append(c[i]/c[0] - 1)
    return roc

def Get_ATR(h, l, c, sec):
    if PPB["ATR"][sec] == 0:
        return ATR(h,l,c)
    else:
        PPB["ATR"][sec] = (PPB["ATR"][sec]*13 + TR(h[0], l[0], c[1]))/14
        return PPB["ATR"][sec]

def ATR(h, l, c):
    p = 98
    TrueRanges = 0.0
    ATR_val = 0
    while p > 84:
        TrueRanges = TrueRanges + TR(h[p], l[p], c[p+1])
        p -= 1
    ATR_val = TrueRanges/14
    while p >= 0:
        ATR_val = (ATR_val*13 + TR(h[p], l[p], c[p+1]))/14
        p -= 1
    return ATR_val

def SMA(c, n, offset):
    sma_val = 0.0
    for i in range(n):
        sma_val += c[i + offset]
    return sma_val/n

def STDEV(c, n, offset):
    ma = SMA(c, n, offset)
    sd_val = 0.0
    for i in range(n):
        sd_val += (ma - c[i + offset])**2 
    return (sd_val/(n-1))**(0.5)

def CORREL(c1, c2):
    ma1 = SMA(c1,len(c1))
    ma2 = SMA(c2,len(c2))
    for i in range(len(c1)):
        exy += (c1[i] - ma1)*(c2[i]-ma2)
    exy = exy/len(c1)