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
import matplotlib.mlab as mlab

sec = input("Select Currency:")
# Sec = []
# Sec.append("EUR_USD")
# Sec.append("GBP_USD")
# Sec.append("USD_CAD")
# Sec.append("AUD_USD")
# Sec.append("NZD_USD")

Portfolio = np.zeros((len(Sec)-1,1900))
buy_win_stoch = np.zeros((len(Sec)-1,1900))
buy_loss_stoch = np.zeros((len(Sec)-1,1900))
sell_win_stoch = np.zeros((len(Sec)-1,1900))
sell_loss_stoch = np.zeros((len(Sec)-1,1900))
hh_array = np.zeros((len(Sec)-1,1900))
ll_array = np.zeros((len(Sec)-1,1900))
hh_ll_array = np.zeros((len(Sec)-1,1900))
ll_hh_array = np.zeros((len(Sec)-1,1900))

for j in range(0, len(Sec)-1):

	st = "2010-01-01"
	en = "2016-02-01"
	Ticker = Sec[j]
	tf1 = "D"
	Account = 100

	o = pOpen(Ticker, tf1, st, en)
	time.sleep(1)
	h = pHigh(Ticker, tf1, st, en)
	time.sleep(1)
	l = pLow(Ticker, tf1, st, en)
	time.sleep(1)
	c = pClose(Ticker, tf1, st,  en)
	time.sleep(1)
	d = pDate(Ticker, tf1, st, en)
	win = 100.0
	lots = 500 

	for i in range(20,1500):
		lvl_min = round(o[i],2)
		lvl_max = round(o[i],2) + 0.01
		pp = (h[i]+l[i]+c[i])/3
		sell_tp = 2*pp - h[i]
		buy_tp = 2*pp - l[i]
		sl = o[i]
		if c[i] > lvl_max:
			if l[i+1] < sl:
				win = win + lots*(sl - c[i])
			elif h[i+1] > buy_tp:
				win = win + lots*(buy_tp - c[i])
			elif l[i+2] < sl:
				win = win + lots*(sl - c[i])
			elif h[i+2] > buy_tp:
				win = win + lots*(buy_tp - c[i])
		elif c[i] < lvl_min:
			if h[i+1] > sl:
				win = win - lots*(sl - c[i])
			elif l[i+1] < sell_tp:
				win = win - lots*(sell_tp - c[i])
			elif h[i+2] > sl:
				win = win - lots*(sl - c[i])
			elif l[i+2] < sell_tp:
				win = win - lots*(sell_tp - c[i])
		Portfolio[j,i] = win