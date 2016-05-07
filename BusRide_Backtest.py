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

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

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
	time.sleep(0.25)
	h = pHigh(Ticker, tf1, st, en)
	time.sleep(0.25)
	l = pLow(Ticker, tf1, st, en)
	time.sleep(0.25)
	c = pClose(Ticker, tf1, st,  en)
	time.sleep(0.25)
	d = pDate(Ticker, tf1, st, en)
	hr = pHour(d)
	win = 100.0
	lots = 500 

	hh = HighestHigh(c,20)
	ll = LowestLow(c,20)
	hhs = HighestHigh(c,5)
	lls = LowestLow(c, 5)

	for i in range(0, len(hh[0,:])):
		if hh[0,i] == c[i]:
			hh_array[j,i] = 1

	for i in range(0, len(ll[0.:])):
		if ll[0,i] == c[i]:
			ll_array[j,i] = 1

	

	# for i in range(20,1500):
	# 	lvl_min = round(o[i],2)
	# 	lvl_max = round(o[i],2) + 0.01
	# 	pp = (h[i]+l[i]+c[i])/3
	# 	sell_tp = 2*pp - h[i]
	# 	buy_tp = 2*pp - l[i]
	# 	sl = o[i]
	# 	if c[i] > lvl_max:
	# 		if l[i+1] < sl:
	# 			win = win + lots*(sl - c[i])
	# 			buy_loss_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 			# print float((c[i]-ma[i])/sd[i])
	# 		elif h[i+1] > buy_tp:
	# 			win = win + lots*(buy_tp - c[i])
	# 			buy_win_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 		elif l[i+2] < sl:
	# 			win = win + lots*(sl - c[i])
	# 			buy_loss_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 		elif h[i+2] > buy_tp:
	# 			win = win + lots*(buy_tp - c[i])
	# 			buy_win_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 	elif c[i] < lvl_min:
	# 		if h[i+1] > sl:
	# 			win = win - lots*(sl - c[i])
	# 			sell_loss_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 		elif l[i+1] < sell_tp:
	# 			win = win - lots*(sell_tp - c[i])
	# 			sell_win_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 		elif h[i+2] > sl:
	# 			win = win - lots*(sl - c[i])
	# 			sell_loss_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 		elif l[i+2] < sell_tp:
	# 			win = win - lots*(sell_tp - c[i])
	# 			sell_win_stoch[j,i] = float((c[i]-ma[i])/sd[i])
	# 	Portfolio[j,i] = win
	# print "Short"
	# a = np.array(sell_win_stoch)
	# print "Sell Win =" + str(np.median(a))
	# a = np.array(sell_loss_stoch)
	# print "Sell Loss =" + str(np.median(a))
	# print "Buy"
	# a = np.array(buy_win_stoch)
	# print "Buy Win =" + str(np.median(a))
	# a = np.array(buy_loss_stoch)
	# print "Buy Loss =" + str(np.median(a))

# cnt_1 = 0
# cnt_2 = 0
# cnt_3 = 0
# cnt_4 = 0
# cnt_t = 0
# for j in range(0,len(Sec)-1):
# 	for i in range(0,500):
# 		if sell_win_stoch[j,i] < -1:
# 			cnt_1 += 1
# 		elif sell_win_stoch[j,i] < 0 and sell_win_stoch[j,i] > -1:
# 			cnt_2 += 1
# 		elif sell_win_stoch[j,i] > 0 and sell_win_stoch[j,i] < 1:
# 			cnt_3 += 1
# 		elif sell_win_stoch[j,i] > 1: 
# 			cnt_4 += 1

# 		if sell_win_stoch[j,i] != 0:
# 			cnt_t +=1
# # print cnt_1, cnt_2, cnt_3, cnt_4, cnt_t
# print float(cnt_1)/cnt_t, float(cnt_2)/cnt_t, float(cnt_3)/cnt_t, float(cnt_4)/cnt_t
