import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import sys

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

SL = 0.001
TP = 0.001
n = 50
dt = datetime.strptime('January 22 16  9:30', '%B %d %y %H:%M')
name = "PPBreakout_Log.txt"
LowerPP = 0
UpperPP = 0

i = 0
bars = 95
h = {'Authorization' : ACCESS_TOKEN}
url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=96&candleFormat=midpoint&granularity=M5"
r = requests.get(url, headers=h)     
data = json.loads(r.text)
def Date(index):
    return data["candles"][index][STRT]
def Open(index):
    return data["candles"][index][STRO]
def High(index):
    return data["candles"][index][STRH]
def Low(index):
    return data["candles"][index][STRL]
def Close(index):
    return data["candles"][index][STRC]
def Volume(index):
    return data["candles"][index][STRV]

level = 1.0860
cls = []

for i in range(0,bars):
    cls.append(Close(i))

a = np.array(cls)
Hgh = (max(a))
Lw = (min(a))

inc = (Hgh-Lw)/100
lvl_2_Chart = []
# print inc
mgn = 0.000025
mgnret = 0.0002
for j in range(0,99):
    level = Lw + j*inc  
    sum_vol_up = 0.0
    sum_vol_dwn = 0.0
    sum_can_up = 0.0
    sum_can_dwn = 0.0
    price_Chart = []
    lvl_Chart = []   
    for i in range(0,bars):
        if (Close(i) > level and Close(i) < level + mgn) and ((Close(i-1)/Close(i)-1 > mgnret and Close(i+1)/Close(i)-1 > mgnret) or (Close(i-1)/Close(i)-1 < -mgnret and Close(i+1)/Close(i)-1 < -mgnret)):
            sum_can_up = sum_can_up + 1
            sum_vol_up = sum_vol_up + Volume(i)
        elif (Close(i) < level and Close(i) > level - mgn) and ((Close(i-1)/Close(i)-1 > mgnret and Close(i+1)/Close(i)-1 > mgnret) or (Close(i-1)/Close(i)-1 < -mgnret and Close(i+1)/Close(i)-1 < -mgnret)):
            sum_can_dwn = sum_can_dwn + 1
            sum_vol_dwn = sum_vol_dwn + Volume(i)
        # if (Close(i) > level and Close(i) < level + mgn) or (Low(i) > level and Low(i) < level + mgn) or (High(i) > level and High(i) < level + mgn):
        #     sum_can_up = sum_can_up + 1
        #     sum_vol_up = sum_vol_up + Volume(i)
        # elif (Close(i) < level and Close(i) > level - mgn) or (Low(i) < level and Low(i) > level - mgn) or (High(i) < level and High(i) > level - mgn):
        #     sum_can_dwn = sum_can_dwn + 1
        #     sum_vol_dwn = sum_vol_dwn + Volume(i)
    # if sum_vol_dwn == 0 or sum_vol_up == 0:
    #     prop = prop + 1 
    # else:
    #     prop =  sum_can_up/(sum_can_up + sum_can_dwn)
    # if prop > 0.75 or prop < 0.25:   
    if sum_can_up + sum_can_dwn >= 1:    
        lvl_2_Chart.append(float(level))

# i = 0
# h = {'Authorization' : ACCESS_TOKEN}
# url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=96&candleFormat=midpoint&granularity=M5"
# r = requests.get(url, headers=h)     
# data = json.loads(r.text)
# def Close(index):
#     return data["candles"][index][STRC]

# plt.plot(lvl_Chart,'ro')

for x in lvl_2_Chart:
    lvl_Chart = []
    for i in range(0,95):
        lvl_Chart.append(float(x))
    plt.plot(lvl_Chart)

for i in range(0,95):
    price = Close(i)
    price_Chart.append(float(price))

plt.plot(price_Chart)
plt.plot(lvl_Chart)
plt.ylim(1.079,1.084)
plt.show()