import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
from Backtest_Objects import *

Sec = []
# Sec.append("EUR_USD")
Sec.append("GBP_USD")
# Sec.append("USD_CAD")
# Sec.append("AUD_USD")
Sec.append("NZD_USD")

i = 0
bars = 95

def Tail(cl,op,lo):
    if cl>op:
        return op-lo
    else:
        return cl-lo
def Wick(cl,op,hi):
    if cl>op:
        return hi-op
    else:
        return hi-cl
for i in range(0,2):
    print Sec[i]
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/v1/accounts/5801231/trades?instrument=" + str(Sec[i])
    r = requests.get(url, headers=h)     
    data2 = json.loads(r.text)
    print data2
    for positions in data2["trades"]:
        Open_Units = positions["id"]
        print Open_Units


    conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": DEMO_ACCESS_TOKEN}
    params = urllib.urlencode({"stopLoss": "0.5"})
    conn.request("PATCH", "/v1/accounts/5801231/trades/" + str(Open_Units), params, headers)
    response = conn.getresponse().read()
    print response

# h = {'Authorization' : DEMO_ACCESS_TOKEN}
# url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=96&candleFormat=midpoint&granularity=M15"

# r = requests.get(url, headers=h)     
# data = json.loads(r.text)
# def Date(index):
#     return data["candles"][index][STRT]
# def Open(index):
#     return data["candles"][index][STRO]
# def High(index):
#     return data["candles"][index][STRH]
# def Low(index):
#     return data["candles"][index][STRL]
# def Close(index):
#     return data["candles"][index][STRC]
# def Volume(index):
#     return data["candles"][index][STRV]

# st = "2016-01-25"
# en = "2016-02-03"
# Ticker = "EUR_USD"
# tf = "M15"

# price_Chart = []
# piv = []
# mgnret = 0.0005
# sum_avg = 0.0
# o = pOpen(Ticker, tf, st,  en)
# h = pHigh(Ticker, tf, st,  en)
# l = pLow(Ticker, tf, st,  en)
# c = pClose(Ticker, tf, st,  en)
# std = pStd(c,16)
# sp = 20

# w = []
# t = []
# for i in range(sp,len(c)-sp-2):
#     w.append(Wick(c[i],o[i],h[i]))
#     t.append(Tail(c[i],o[i],l[i]))
# w_tp = np.array(w)
# t_tp = np.array(t)
# w_ma = pMa(w_tp,16)
# w_std = pStd(w_tp,16)
# t_ma = pMa(t_tp,16)
# t_std = pStd(t_tp,16)


# for i in range(1,min(len(c),len(t_ma))):
#     flt = True
#     price = c[i]
#     price_Chart.append(float(price))
    # if (c[i-1]/c[i]-1 > mgnret and c[i+1]/c[i]-1 > mgnret) or (c[i-2]/c[i]-1 > mgnret and c[i+2]/c[i]-1 > mgnret):
    #     piv.append(c[i])
    # if (c[i-1]/c[i]-1 < -mgnret and c[i+1]/c[i]-1 < -mgnret) or (c[i-2]/c[i]-1 < -mgnret and c[i+2]/c[i]-1 < -mgnret):
    #     piv.append(c[i])
    # for j in range(1,2*sp):
    #     sum_avg = sum_avg + c[i-sp+j] 
    # sum_avg = sum_avg/(2*sp)

    # for j in range(1,2*sp):
    #     if c[i-sp+j] > sum_avg +0.001 and c[i-sp+j] < sum_avg -0.001:
    #         flt = False
    #         break 
    # if (c[i-sp]/c[i]-1 < -mgnret and c[i+sp]/c[i]-1 < -mgnret and flt == True ):
    #     piv.append(c[i])

    # if Wick(c[i],o[i],h[i]) > w_ma[i] + 3*w_std[i]:
    #     piv.append(c[i])
#     if (t_tp[i] + t_tp[i-1]+ t_tp[i-2])/3 > t_ma[i] + t_std[i]:
#         piv.append(c[i])
#     else:
#         piv.append(0)


# plt.plot(price_Chart)
# plt.plot(piv, 'r^')
# plt.ylim(min(c)-0.002,max(c)+0.002)
# plt.show()

# threshold = 0.5
# learning_rate = 0.1
# weights = [0, 0, 0]
# training_set = [((1, 0, 0), 1), ((1, 0, 1), 1), ((1, 1, 0), 1), ((1, 1, 1), 0)]

# def dot_product(values, weights):
#     return sum(value * weight for value, weight in zip(values, weights))

# while True:
#     print('-' * 60)
#     error_count = 0
#     for input_vector, desired_output in training_set:
#         print(weights)
#         result = dot_product(input_vector, weights) > threshold
#         error = desired_output - result
#         if error != 0:
#             error_count += 1
#             for index, value in enumerate(input_vector):
#                 weights[index] += learning_rate * error * value
#     if error_count == 0:
#         break