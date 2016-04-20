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

Sec.append("EUR_GBP")
Sec.append("EUR_CAD")
Sec.append("EUR_AUD")
Sec.append("EUR_NZD")

Sec.append("GBP_AUD")
Sec.append("GBP_NZD")
Sec.append("GBP_CAD")

Sec.append("AUD_CAD")
Sec.append("AUD_NZD")

Sec.append("NZD_CAD")
Portfolio = np.zeros((len(Sec)-1,1500))


for j in range(0,len(Sec)-1):
	buy_win_stoch = np.zeros((len(Sec)-1,1500))
	buy_loss_stoch = np.zeros((len(Sec)-1,1500))
	sell_win_stoch = np.zeros((len(Sec)-1,1500))
	sell_loss_stoch = np.zeros((len(Sec)-1,1500))
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

	s = Stochastic(h, l, c, 10, 2, "K")

	for i in range(0,1500):
		lvl_min = round(o[i],2)
		lvl_max = round(o[i],2) + 0.01
		pp = (h[i]+l[i]+c[i])/3
		sell_tp = 2*pp - h[i]
		buy_tp = 2*pp - l[i]
		sl = o[i]
		if c[i] > lvl_max:
			if l[i+1] < sl:
				win = win + lots*(sl - c[i])
				buy_loss_stoch[j,i] = float(s[i])
			elif h[i+1] > buy_tp:
				win = win + lots*(buy_tp - c[i])
				buy_win_stoch[j,i] = float(s[i])
			elif l[i+2] < sl:
				win = win + lots*(sl - c[i])
				buy_loss_stoch[j,i] = float(s[i])
			elif h[i+2] > buy_tp:
				win = win + lots*(buy_tp - c[i])
				buy_win_stoch[j,i] = float(s[i])
		elif c[i] < lvl_min:
			if h[i+1] > sl:
				win = win - lots*(sl - c[i])
				sell_loss_stoch[j,i] = float(s[i])
			elif l[i+1] < sell_tp:
				win = win - lots*(sell_tp - c[i])
				sell_win_stoch[j,i] = float(s[i])
			elif h[i+2] > sl:
				win = win - lots*(sl - c[i])
				sell_loss_stoch[j,i] = float(s[i])
			elif l[i+2] < sell_tp:
				win = win - lots*(sell_tp - c[i])
				sell_win_stoch[j,i] = float(s[i])
	Portfolio[j,i] = win
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

print sell_win_stoch
print sell_loss_stoch
print buy_win_stoch
print buy_loss_stoch

for j in range(0,len(Sec)-1):
	x_array = []
	y_array = []
	# print sell_win_stoch
	for i in range(0, 500):
		# print Portfolio[j,i]
		# print sell_win_stoch[j,i]
		if Portfolio[j,i] > 0 and sell_win_stoch[j,i] > 0:
			x_array.append(float(Portfolio[j,i]))
			y_array.append(float(sell_win_stoch[j,i]))
	# print x_array
	# print y_array
	sr = SimpleRegression(x_array,y_array)
	print sr[0], sr[1] 


	plt.plot(Portfolio[j,:], label=str(Sec[j]))	
# plt.plot(Portfolio.mean(axis=0), label=str(Sec[j]))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylim(0, 500)
plt.show()

# plt.plot(sell_win_stoch)
# plt.ylim(0, 1)
# plt.show()


# n, bins, patches = plt.hist(buy_loss_stoch, 20, normed=1, facecolor='green', alpha=0.75)

# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([0, 100, 0, 0.03])
# plt.grid(True)

# plt.show()

# n, bins, patches = plt.hist(sell_win_stoch, 20, normed=1, facecolor='green', alpha=0.75)

# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([0, 100, 0, 0.03])
# plt.grid(True)

# plt.show()

# n, bins, patches = plt.hist(buy_win_stoch, 20, normed=1, facecolor='green', alpha=0.75)

# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([0, 100, 0, 0.03])
# plt.grid(True)

# plt.show()