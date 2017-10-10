import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from QF_Strategy import *
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
    # D = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(curr_pair) + "&count=" + str(bars) + "&candleFormat=" + str(rep) +"&granularity=" + str(tf)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    time.sleep(1)
    if rep == "midpoint":
        for i in range(len(data["candles"])):
            # D.append(data["candles"][bars - i - 1][STRT])
            O.append(data["candles"][bars - i - 1][STRO])
            H.append(data["candles"][bars - i - 1][STRH])
            L.append(data["candles"][bars - i - 1][STRL])
            C.append(data["candles"][bars - i - 1][STRC])
        if ohlc == "ohlc":
            return O, H, L, C
        elif ohlc == "hlc":
            return H, L, C
        elif ohlc == "c":
            # return D, C
            return C
    else:
        for i in range(len(data["candles"])):
            CB.append(data["candles"][bars - i - 1][STRCB])
            CA.append(data["candles"][bars - i - 1][STRCA])
        if ohlc == "c":
            return CB, CA

# New Version
# def GetPrices(sym, tf, bars, ohlc):
#     h = {'Authorization' : LIVE_ACCESS_TOKEN}
#     main_url = "https://api-fxpractice.oanda.com/v1/candles?"
#     sym_url = "instrument=" + str(sym)
#     if isinstance(bars, (int, float)):
#         num_url = "&count=" + str(bars)
#     else:
#         num_url = "&start=" + str(bars[0]) + "&end=" + str(bars[1]) 
#     if 'a' in ohlc or 'b' in ohlc:
#         form_url = "&candleFormat=bidask"
#         p = [[] for i in range(9)]
#     else:
#         form_url = "&candleFormat=midpoint"
#         p = [[] for i in range(5)]
#     tf_url = "&granularity=" + str(tf)
#     url = main_url + sym_url + num_url + form_url + tf_url
#     r = requests.get(url, headers=h)     
#     data = json.loads(r.text)
#     time.sleep(1)
#     if 'a' in ohlc or 'b' in ohlc:
#         for i in range(len(data["candles"])):
#             p[0].append(data["candles"][bars - i - 1][STRT])
#             p[1].append(data["candles"][bars - i - 1][STROB])
#             p[2].append(data["candles"][bars - i - 1][STROA])
#             p[3].append(data["candles"][bars - i - 1][STRHB])
#             p[4].append(data["candles"][bars - i - 1][STRHA])
#             p[5].append(data["candles"][bars - i - 1][STRLB])
#             p[6].append(data["candles"][bars - i - 1][STRLA])
#             p[7].append(data["candles"][bars - i - 1][STRCB])
#             p[8].append(data["candles"][bars - i - 1][STRCA])
#         if ohlc == "ohlcba":
#             return p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]
#         elif ohlc == "hlcba":
#             return p[3], p[4], p[5], p[6], p[7], p[8]
#         elif ohlc == "cba":
#             return p[7], p[8]
#         elif ohlc == "dohlcba":
#             return p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]
#         elif ohlc == "dhlcba":
#             return p[0], p[3], p[4], p[5], p[6], p[7], p[8]
#         elif ohlc == "dcba":
#             return p[0], p[7], p[8]
#     else:
#         for i in range(len(data["candles"])):
#             p[0].append(data["candles"][bars - i - 1][STRT])
#             p[1].append(data["candles"][bars - i - 1][STRO])
#             p[2].append(data["candles"][bars - i - 1][STRH])
#             p[3].append(data["candles"][bars - i - 1][STRL])
#             p[4].append(data["candles"][bars - i - 1][STRC])
#         if ohlc == "ohlc":
#             return p[1], p[2], p[3], p[4], 
#         elif ohlc == "hlc":
#             return p[2], p[3], p[4]
#         elif ohlc == "c":
#             return p[4]
#         elif ohlc == "dohlc":
#             return p[0], p[1], p[2], p[3], p[4] 
#         elif ohlc == "dhlc":
#             return p[0], p[2], p[3], p[4] 
#         elif ohlc == "dc":
#             return p[0], p[4]

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


TOD = {
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


BBB1 = {
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

BBB2 = {
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

BBB3 = {
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
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0, "Z": 0, "Max 4": 0, "Min 4": 0, "Max 16": 0, "Min 16": 0,
    "Eulow": 0, "Euhigh": 0, "Aslow": 0, "Ashigh": 0, "Seslow": 0, "Seshigh": 0, "Wklow": 0, "Wkhigh": 0}, 
    "GBP_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0, "Z": 0, "Max 4": 0, "Min 4": 0, "Max 16": 0, "Min 16": 0,
    "Eulow": 0, "Euhigh": 0, "Aslow": 0, "Ashigh": 0, "Seslow": 0, "Seshigh": 0, "Wklow": 0, "Wkhigh": 0}, 
    "USD_CAD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0, "Z": 0, "Max 4": 0, "Min 4": 0, "Max 16": 0, "Min 16": 0,
    "Eulow": 0, "Euhigh": 0, "Aslow": 0, "Ashigh": 0, "Seslow": 0, "Seshigh": 0, "Wklow": 0, "Wkhigh": 0},
    "AUD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0, "Z": 0, "Max 4": 0, "Min 4": 0, "Max 16": 0, "Min 16": 0,
    "Eulow": 0, "Euhigh": 0, "Aslow": 0, "Ashigh": 0, "Seslow": 0, "Seshigh": 0, "Wklow": 0, "Wkhigh": 0}, 
    "NZD_USD": {
    "Z100": 0, "Z101": 0, "Z102": 0, "Z210": 0, "Z211": 0, "Z212": 0, "Z500": 0, "Z501": 0, "Z502": 0, 
    "SMA100": 0, "SMA101": 0, "SMA102": 0, "SMA103": 0, "SMA500": 0, "SMA501": 0, "SMA502": 0, "SMA503": 0, 
    "SMA210": 0, "SMA211": 0, "SMA212": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0, "Z": 0, "Max 4": 0, "Min 4": 0, "Max 16": 0, "Min 16": 0,
    "Eulow": 0, "Euhigh": 0, "Aslow": 0, "Ashigh": 0, "Seslow": 0, "Seshigh": 0, "Wklow": 0, "Wkhigh": 0}
}

PriceAction = {
    "EUR_USD": {
    "AtWkLow": 0, "AtWkHigh": 0, "AtSesLow": 0, "AtSesHigh": 0, "Doji": 0, "SMA10Bounce": 0, "SMA21Bounce": 0, "BullEngulfing": 0,
    "BearEngulfing": 0, "InsidebarBreakUp": 0, "InsidebarBreakDown": 0, "BullKeyReversal": 0, "BearKeyReversal": 0,
    "UpDoji": 0, "DownDoji": 0},
    "GBP_USD": {
    "AtWkLow": 0, "AtWkHigh": 0, "": 0, "ATR": 0, "s": 0, "r": 0},
    "USD_CAD": {
    "AtWkLow": 0, "AtWkHigh": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0},
    "AUD_USD": {
    "AtWkLow": 0, "AtWkHigh": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0},
    "NZD_USD": {
    "AtWkLow": 0, "AtWkHigh": 0, "SMA213": 0, "ATR": 0, "s": 0, "r": 0}
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

def Get_Z(c, p):
    ma = SMA(c, p, 0)
    sd = STDEV(c, p, 0)
    return (c[0] - ma)/sd

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