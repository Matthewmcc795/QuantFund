import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import numpy as np
import pypyodbc
import matplotlib.pyplot as plt
from Backtest_Objects import *
import pandas as pd
from matplotlib.finance import candlestick2_ochl

# Sec = []
# Sec.append("EUR_USD")
# Sec.append("GBP_USD")
# Sec.append("USD_CAD")
# Sec.append("AUD_USD")
# Sec.append("NZD_USD")

# Sec.append("EUR_GBP")
# Sec.append("EUR_CAD")
# Sec.append("EUR_AUD")
# Sec.append("EUR_NZD")

# Sec.append("GBP_AUD")
# Sec.append("GBP_NZD")
# Sec.append("GBP_CAD")

# Sec.append("AUD_CAD")
# Sec.append("AUD_NZD")

# Sec.append("NZD_CAD")

# Portfolio_Cash = 0.0
# Portfolio_Holdings = 0.0
# Buy_Signals = []
# Sell_Signals = []
# CloseBuy_Signals = []
# CloseSell_Signals = []

st = "2015-01-01"
end_dt = "2016-02-01"
Ticker = "GBP_USD"
tf1 = "M15"

# Portfolio = np.zeros((1,5000))
en = FindDateRange(st, 24*4)
Account = 100
while np.busday_count(en, end_dt) > 30:

	o = pOpen(Ticker, tf1, st, en)
	h = pHigh(Ticker, tf1, st, en)
	l = pLow(Ticker, tf1, st, en)
	c = pClose(Ticker, tf1, st,  en)
	d = pDate(Ticker, tf1, st, en)
	ib = InsideBar(h,l)
	Market_Open = np.zeros((1, len(h)))
	ma = pMa(c,50)
	hr = pHour(d)
	mn = pMinute(d)
	for i in range(0,len(h)-1):
		if hr[i] == 5 and mn[i] == 0:
			Market_Open[0,i] = 1

	Lvls = np.zeros((2, len(h)))
	lvl_min = []
	lvl_max = []
	for i in range(0, len(h)-1):
		if Market_Open[0,i] == 1:
			for j in range(0,4*2):
				lvl_min.append(c[i-j])
				lvl_max.append(c[i-j])
			for j in range(0,4*4):
				Lvls[0,i+j] = max(lvl_max)
				Lvls[1,i+j] = min(lvl_min)
			lvl_min = []
			lvl_max = []

	# plt.plot(Lvls[0,:])
	# plt.plot(Lvls[1,:])
	# plt.ylim(1.4,1.6)
	# plt.show()	

	ret = []
	for i in range(0,len(h)):
		if Lvls[1,i] == 0 and  Lvls[1,i-1] == 0:
			break_count = 0
		else:
			if c[i] < Lvls[1,i] and  c[i-1] > Lvls[1,i-1] and break_count < 3:
				for j in range(0,12):
					ret.append(c[i+j]/c[i]-1)
				plt.plot(ret)
				ret = []
				break_count += 1
	# for i in range(0,len(h)):
	# 	if Market_Open[0,i-2] == 1 and c[i-2]/o[i-2] -1 < 0 and c[i-1]/o[i-1] -1 > 0 and  c[i]/c[i-2] - 1 < 0:
	# 		for j in range(0,12):
	# 			ret.append(c[i+j]-c[i])
	# 		plt.plot(ret)
	# 		ret = []
	st = en
	en = FindDateRange(en, 24*4)
plt.ylim(-0.01,0.01)
plt.show()