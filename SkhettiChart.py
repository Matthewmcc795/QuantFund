import requests
import json
from array import *
import matplotlib.pyplot as plt
import numpy as np
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import pypyodbc

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

Bars = 5000
I_D = 0   
# for k in range(0,5):
k = 0
h = {'Authorization' : ACCESS_TOKEN}
print "Retrieving Data..."
r = requests.get( ACCOUNT_DOMAIN + "instrument=" + Sec[k] +"&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4", headers=h)     
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

def Inside_Bar(h,l,hp,lp):
    if hp > h and lp < l:
        return True
    else:
        return False

for m in range(0,10):
    n = 50
    last_i = 0
    spacer = 5
  
    for i in range(51,4500):

        chart = []
        # if Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) > High(i-1) and i - last_i > spacer:
        #     for j in range(0,50):
        #         ret = Close(i+j)/Close(i)- 1
        #         chart.append(ret)
        #     last_i = i
        #     plt.plot(chart)
        if Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) < Low(i-1) and i - last_i > spacer:
            for j in range(0,10):
                ret = Close(i+j)/Close(i)- 1
                chart.append(ret)
            last_i = i
            plt.plot(chart)
plt.plot(chart)
plt.ylim(-0.05,0.05)
plt.show()