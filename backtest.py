from array import *
from Settings import LIVE_ACCESS_TOKEN, ACCOUNT_ID_QF, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import numpy as np
import matplotlib.pyplot as plt
from Backtest_Objects import *
from datetime import datetime, timedelta
import os
from numpy import genfromtxt
import math
import requests
import json
from array import *

h = {'Authorization' : LIVE_ACCESS_TOKEN}
url = "https://api-fxtrade.oanda.com/v1/accounts/406207/trades?count=100"
r = requests.get(url, headers=h)     
data = json.loads(r.text)
print data

h = {'Authorization' : LIVE_ACCESS_TOKEN}
url = "https://api-fxtrade.oanda.com/v1/accounts/406207/transactions?count=100"
r = requests.get(url, headers=h)     
data = json.loads(r.text)
print data

# # st = "2012-01-01"
# # en = "2016-08-01"
# # end_dt = FindDateRange(st, 24)
# Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]
# # a = Download_Prices("GBP_USD", "M15", "2012-01-01", "2016-01-01")
# p = Get_Prices("EUR_USD", "H4", "2012-01-01", "2016-01-01")
# # sec = raw_input("Name:")
# # # os.remove(file_str)
# ma = pMa(p[3,:],50)
# sd = pStd(p[3,:],50)
# mas = pMa(p[3,:],20)
# sds = pStd(p[3,:],20)
# ub = np.zeros(len(p[3,:]))
# lb = np.zeros(len(p[3,:]))
# ubs = np.zeros(len(p[3,:]))
# lbs = np.zeros(len(p[3,:]))
# ubb = np.zeros(len(p[3,:]))
# lbb = np.zeros(len(p[3,:]))
# EUR_USD = PriceAction("EUR_USD", p[0,:], p[1,:], p[2,:], p[3,:])
# EUR_USD.Trends()
# EUR_USD.Candlesticks()
# EUR_USD.MAC()
# EUR_USD.SupportResistance()
# # GBP_USD.Chart()
# Account_Chart = []
# Open_Order = 0
# Carry_Price = 0.0
# Lots = 1000
# Account = 1000
# Starting_Balance = Account
# last_entry = 0
# last_trade = 0
# Open_Units = 0
# Open_Trade = False
# Trade_Counter = 0
# new_entry = False
# # buys = np.zeros(len(EUR_USD.close))
# # sells = np.zeros(len(EUR_USD.close))
# # buysl = []
# # sellsl = []
# # buytp = []
# # selltp = []
# # for i in range(len(EUR_USD.close)-12):
# # 	for j in range(len(EUR_USD.zerosdwn[:,0])):
# # 		if EUR_USD.ubb[1,i] == 1:
# # 			sells[i] = 1
# # 			mx = 0
# # 			for k in range(12):
# # 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# # 			mn = 2
# # 			for k in range(12):
# # 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# # 			sellsl.append(mx)
# # 			selltp.append(mn)
# # 		if EUR_USD.lbb[1,i] == 1:
# # 			buys[i] = 1 
# # print sum(buys), sum(sells)
# # buys = np.zeros(len(EUR_USD.close))
# # sells = np.zeros(len(EUR_USD.close))
# # buysl = []
# # sellsl = []
# # buytp = []
# # selltp = []
# # for i in range(len(EUR_USD.close)-12):
# # 	for j in range(len(EUR_USD.zerosdwn[:,0])):
# # 		if EUR_USD.ubb[1,i] == 1 and EUR_USD.ubb[1,i-1] == 0:
# # 			sells[i] = 1
# # 			mx = 0
# # 			for k in range(12):
# # 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# # 			mn = 2
# # 			for k in range(12):
# # 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# # 			sellsl.append(mx)
# # 			selltp.append(mn)
# # 		if EUR_USD.lbb[1,i] == 1 and EUR_USD.lbb[1,i-1] == 0:
# # 			buys[i] = 1 
# # 			mx = 0
# # 			for k in range(12):
# # 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# # 			mn = 2
# # 			for k in range(12):
# # 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# # 			buysl.append(mn)
# # 			buytp.append(mx)
# # print sum(buys), sum(sells)
# # buys = np.zeros(len(EUR_USD.close))
# # sells = np.zeros(len(EUR_USD.close))
# # buysl = []
# # sellsl = []
# # buytp = []
# # selltp = []
# # for i in range(len(EUR_USD.close)-12):
# # 	for j in range(len(EUR_USD.zerosdwn[:,0])):
# # 		if EUR_USD.ubb[1,i] == 0 and EUR_USD.ubb[1,i-1] == 1:
# # 			sells[i] = 1
# # 			mx = 0
# # 			for k in range(12):
# # 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# # 			mn = 2
# # 			for k in range(12):
# # 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# # 			sellsl.append(mx)
# # 			selltp.append(mn)
# # 		if EUR_USD.lbb[1,i] == 0 and EUR_USD.lbb[1,i-1] == 1:
# # 			buys[i] = 1 
# # 			mx = 0
# # 			for k in range(12):
# # 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# # 			mn = 2
# # 			for k in range(12):
# # 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# # 			buysl.append(mn)
# # 			buytp.append(mx)
# # print sum(buys), sum(sells)
# buys = np.zeros(len(EUR_USD.close))
# sells = np.zeros(len(EUR_USD.close))
# buysl = []
# sellsl = []
# buytp = []
# selltp = []

# for i in range(len(EUR_USD.close)-12):
# 	for j in range(len(EUR_USD.zerosdwn[:,0])):
# 		if EUR_USD.ubb[1,i] == 1 and EUR_USD.zerosdwn[j,i] == 1:
# 			sells[i] = 1
# 			mx = 0
# 			for k in range(12):
# 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# 			mn = 2
# 			for k in range(12):
# 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# 			sellsl.append(mx)
# 			selltp.append(mn)
# 		if EUR_USD.lbb[1,i] == 1 and EUR_USD.zerosup[j,i] == 1:
# 			buys[i] = 1 
# 			mx = 0
# 			for k in range(12):
# 				mx = max(EUR_USD.high[i+k]/EUR_USD.close[i]-1, mx)
# 			mn = 2
# 			for k in range(12):
# 				mn = min(EUR_USD.low[i+k]/EUR_USD.close[i]-1, mn)
# 			buysl.append(mn)
# 			buytp.append(mx)
# buysl = np.array(buysl)
# sellsl = np.array(sellsl)
# buytp = np.array(buytp)
# selltp = np.array(selltp)
# print np.percentile(buytp,5), np.percentile(buytp,25), np.percentile(buytp,50), np.percentile(buytp,75), np.percentile(buytp,95)
# print np.percentile(buysl,5), np.percentile(buysl,25), np.percentile(buysl,50), np.percentile(buysl,75), np.percentile(buysl,95)
# print np.percentile(selltp,5), np.percentile(selltp,25), np.percentile(selltp,50), np.percentile(selltp,75), np.percentile(selltp,95)
# print np.percentile(sellsl,5), np.percentile(sellsl,25), np.percentile(sellsl,50), np.percentile(sellsl,75), np.percentile(sellsl,95)
# print sum(buys), sum(sells)

# basebuy = np.zeros((2,len(EUR_USD.close)))
# basesell = np.zeros((2,len(EUR_USD.close)))
# basebuypl = np.zeros((2,len(EUR_USD.close)))
# basesellpl = np.zeros((2,len(EUR_USD.close)))

# for i in range(len(EUR_USD.close)):
# 	if Open_Order == 0:
# 		Carry_Price = EUR_USD.close[i-1]
# 		if buys[i] and i - last_entry > 5:
# 			basebuy[0,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = 1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i]*(1-0.013)
# 			Take_Profit = EUR_USD.close[i]*(1+0.00734)
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 		elif sells[i] and i - last_entry > 5:
# 			basesell[0,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = -1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i]*(1+0.018)
# 			Take_Profit = EUR_USD.close[i]*(1-0.00823)
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 	elif Open_Order == 1:
# 		if EUR_USD.high[i] > Take_Profit:
# 			basebuy[0,i] = -1
# 			basebuypl[0,i] = (Take_Profit-Open_Price)
# 			Account = Starting_Balance + (Take_Profit-Open_Price)* Lots
# 			Open_Order = 0
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Stop_Loss:
# 			basebuy[0,i] = -1
# 			basebuypl[0,i] = -(Open_Price-Stop_Loss)
# 			Account = Starting_Balance -  (Open_Price-Stop_Loss)* Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.high[i] < Take_Profit and EUR_USD.low[i] > Stop_Loss:
# 			Account = Starting_Balance + (Carry_Price - Open_Price) * Lots
# 	elif Open_Order == -1:
# 		if EUR_USD.high[i] > Stop_Loss:
# 			basesell[0,i] = -1
# 			basesellpl[0,i] = -(Stop_Loss-Open_Price)
# 			Account = Starting_Balance - (Stop_Loss-Open_Price) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Take_Profit:
# 			basesell[0,i] = -1
# 			basesellpl[0,i] = (Open_Price-Take_Profit)
# 			Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] > Take_Profit and EUR_USD.high[i] < Stop_Loss:
# 			Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
# 	Account_Chart.append(Account)
# print sum(basesell[0,:]), sum(basebuy[0,:])
# sellpl = []
# buypl = []
# for i in range(len(EUR_USD.close)):
# 	if basesellpl[0,i] != 0:
# 		sellpl.append(basesellpl[0,i])
# 	if basebuypl[0,i] != 0:
# 		buypl.append(basebuypl[0,i])
# print len(sellpl), len(buypl)
# plt.plot(sellpl,'x')
# plt.show()
# plt.plot(buypl,'x')
# plt.show()



# # plt.plot(Account_Chart)
# # plt.show()
# # a = np.zeros(len(EUR_USD.close))
# # for i in range(len(EUR_USD.close)):
# # 	if i in [0,700,1800,3200,3800,5400]:
# # 		a[i] = EUR_USD.close[i]
# # plt.plot(a)
# # plt.plot(EUR_USD.close)
# # plt.show()
# # wicks_dat = []
# # wicks_dat2 = []
# # wicks_dat3 = []
# # wicks_dat4 = []
# # wicks_dat5 = []
# # wicks_dat6 = []
# # tails_dat = []
# # tails_dat2 = []
# # tails_dat3 = []
# # tails_dat4 = []
# # tails_dat5 = []
# # tails_dat6 = []
# # wicks = np.array(wicks)
# # tails = np.array(tails)
# # wicks_val = pMa(wicks, 20)
# # tails_val = pMa(tails, 20)
# # wicks_ma = pMa(wicks_val, 50)
# # tails_ma = pMa(tails_val, 50)
# # wicks_sd = pStd(wicks_val, 50)
# # tails_sd = pStd(tails_val, 50)
# # wub = wicks_ma + 1.96*wicks_sd
# # wlb = wicks_ma - 1*wicks_sd
# # tub = tails_ma + 1.96*tails_sd
# # tlb = tails_ma - 1*tails_sd

# # for i in range(50,len(EUR_USD.close)):
# #     if ubb[i] == 1:
# #         wicks_dat.append(wicks[i])
# #         wicks_dat2.append(wicks_ma[i])
# #     if ubb[i] == 0 and lbb[i] == 0:
# #         try:
# #             wicks_dat3.append(float(wicks[i]))
# #             wicks_dat4.append(float(wicks_ma[i]))
# #         except ValueError:
# #             wicks_dat3.append(0)
# #             wicks_dat4.append(0)
# #     if lbb[i] == 1:
# #         wicks_dat5.append(wicks[i])
# #         wicks_dat6.append(wicks_ma[i])
# #     if ubb[i] == 1:
# #         tails_dat.append(tails[i])
# #         tails_dat2.append(tails_ma[i])
# #     if ubb[i] == 0 and lbb[i] == 0:
# #         try:
# #             tails_dat3.append(float(tails[i]))
# #             tails_dat4.append(float(tails_ma[i]))
# #         except ValueError:
# #             tails_dat3.append(0)
# #             tails_dat4.append(0)
# #     if lbb[i] == 1:
# #         tails_dat5.append(tails[i])
# #         tails_dat6.append(tails_ma[i])
# # wicks_dat = np.array(wicks_dat)
# # wicks_dat2 = np.array(wicks_dat2)
# # wicks_dat3 = np.array(wicks_dat3)
# # wicks_dat4 = np.array(wicks_dat4)
# # wicks_dat5 = np.array(wicks_dat5)
# # wicks_dat6 = np.array(wicks_dat6)
# # print sum(wicks_dat)/len(wicks_dat), sum(wicks_dat2)/len(wicks_dat2)
# # print np.nansum(wicks_dat3)/len(wicks_dat3), sum(wicks_dat4)/len(wicks_dat4)
# # print sum(wicks_dat5)/len(wicks_dat5), sum(wicks_dat6)/len(wicks_dat6)
# # tails_dat = np.array(tails_dat)
# # tails_dat2 = np.array(tails_dat2)
# # tails_dat3 = np.array(tails_dat3)
# # tails_dat4 = np.array(tails_dat4)
# # tails_dat5 = np.array(tails_dat5)
# # tails_dat6 = np.array(tails_dat6)
# # print sum(tails_dat)/len(tails_dat), sum(tails_dat2)/len(tails_dat2)
# # print np.nansum(tails_dat3)/len(tails_dat3), sum(tails_dat4)/len(tails_dat4)
# # print sum(tails_dat5)/len(tails_dat5), sum(tails_dat6)/len(tails_dat6)

# # plt.plot(wicks_val,'b')
# # # plt.show()
# # # plt.plot(tails,'r')
# # # plt.plot(loc)
# # # plt.show()
# # plt.plot(wub,'r')
# # # plt.plot(wlb)
# # plt.show()
# for i in range(1,len(EUR_USD.close)):
# 	if ubb[i] == 1 and ubb[i-1] == 0:
# 		chtdat = np.zeros((20,100))
# 		if i < 50:
# 			st = i
# 		else:
# 			st = 50
# 		for j in range(100):
# 			chtdat[0,j] = EUR_USD.close[i+j-st]
# 			chtdat[1,j] = ma[i+j-st] + 1.96*sd[i+j-st]
# 			if EUR_USD.BearishRev[0,i+j] == 1:
# 				chtdat[2,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[1,i+j] == 1:
# 				chtdat[3,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[2,i+j] == 1:
# 				chtdat[4,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[3,i+j] == 1:
# 				chtdat[5,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[0,i+j] == 1:
# 				chtdat[6,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[1,i+j] == 1:
# 				chtdat[7,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[2,i+j] == 1:
# 				chtdat[8,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[3,i+j] == 1:
# 				chtdat[9,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[0,i+j] == 1:
# 				chtdat[10,j] = EUR_USD.close[i+j-st]	
# 			if EUR_USD.BearishMom[1,i+j] == 1:
# 				chtdat[11,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[2,i+j] == 1:
# 				chtdat[12,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[3,i+j] == 1:
# 				chtdat[13,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[0,i+j] == 1:
# 				chtdat[14,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[1,i+j] == 1:
# 				chtdat[15,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[2,i+j] == 1:
# 				chtdat[16,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[3,i+j] == 1:
# 				chtdat[17,j] = EUR_USD.close[i+j-st]
# 		# print round(max(chtdat[0,:]),2)
# 		# print round(min(chtdat[0,:]),2)
# 		# print 100*(round(max(chtdat[0,:]),2) - round(min(chtdat[0,:]),2))
# 	if ubb[i-1] == 1 and ubb[i] == 0:
# 		chtdat = np.zeros((20,100))
# 		if i < 50:
# 			st = i
# 		else:
# 			st = 50
# 		for j in range(100):
# 			chtdat[0,j] = EUR_USD.close[i+j-st]
# 			chtdat[1,j] = ma[i+j-st] + 1.96*sd[i+j-st]
# 			if EUR_USD.BearishRev[0,i+j] == 1:
# 				chtdat[2,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[1,i+j] == 1:
# 				chtdat[3,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[2,i+j] == 1:
# 				chtdat[4,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishRev[3,i+j] == 1:
# 				chtdat[5,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[0,i+j] == 1:
# 				chtdat[6,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[1,i+j] == 1:
# 				chtdat[7,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[2,i+j] == 1:
# 				chtdat[8,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishRev[3,i+j] == 1:
# 				chtdat[9,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[0,i+j] == 1:
# 				chtdat[10,j] = EUR_USD.close[i+j-st]	
# 			if EUR_USD.BearishMom[1,i+j] == 1:
# 				chtdat[11,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[2,i+j] == 1:
# 				chtdat[12,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BearishMom[3,i+j] == 1:
# 				chtdat[13,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[0,i+j] == 1:
# 				chtdat[14,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[1,i+j] == 1:
# 				chtdat[15,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[2,i+j] == 1:
# 				chtdat[16,j] = EUR_USD.close[i+j-st]
# 			if EUR_USD.BullishMom[3,i+j] == 1:
# 				chtdat[17,j] = EUR_USD.close[i+j-st]
	
# 	# if lbb[i] == 1 and lbb[i-1] == 0:
# 		# plt.plot(chtdat[0,:])
# 		# plt.plot(chtdat[1,:])
# 		# # plt.plot(chtdat[2,:],'rx')
# 		# # plt.plot(chtdat[3,:],'rx')
# 		# # plt.plot(chtdat[4,:],'rx')
# 		# plt.plot(chtdat[5,:],'rx')
# 		# # plt.plot(chtdat[6,:],'gx')
# 		# # plt.plot(chtdat[7,:],'gx')
# 		# # plt.plot(chtdat[8,:],'gx')
# 		# plt.plot(chtdat[9,:],'gx')
# 		# # plt.plot(chtdat[10,:],'ro')
# 		# # plt.plot(chtdat[11,:],'ro')
# 		# plt.plot(chtdat[12,:],'ro')
# 		# # plt.plot(chtdat[13,:],'ro')
# 		# # plt.plot(chtdat[14,:],'go')
# 		# # plt.plot(chtdat[15,:],'go')
# 		# plt.plot(chtdat[16,:],'go')
# 		# # plt.plot(chtdat[17,:],'go')
# 		# for i in range(len(sr[:,0])):
# 		# 	plt.plot(sr[i,:],'y')
# 		# plt.plot(srb,'yo')
# 		# plt.ylim(min(chtdat[0,:]),max(chtdat[0,:]))
# 		# plt.show()
# print sum(srlb), sum(srub)
# # for j in range(len(EUR_USD.BearishRev[:,40])):
# # 	print EUR_USD.BearishRev[j,181+8]
# # for j in range(len(EUR_USD.BullishRev[:,40])):
# # 	print EUR_USD.BullishRev[j,181+8]
# # for j in range(len(EUR_USD.BearishMom[:,40])):
# # 	print EUR_USD.BearishMom[j,181+8]
# # for j in range(len(EUR_USD.BullishMom[:,40])):
# # 	print EUR_USD.BullishMom[j,181+8]
# Account_Chart = []
# Open_Order = 0
# Carry_Price = 0.0
# Lots = 1000
# n = 30
# Account = 1000
# Starting_Balance = Account
# last_entry = 0
# last_trade = 0
# Open_Units = 0
# Open_Trade = False
# Trade_Counter = 0
# new_entry = False
# bullrevma_1 = pMa(EUR_USD.BullishRev[0,:],12)
# bullrevma_2 = pMa(EUR_USD.BullishRev[1,:],12)
# bullrevma_3 = pMa(EUR_USD.BullishRev[2,:],12)
# bullrevma_4 = pMa(EUR_USD.BullishRev[3,:],12)
# bearrevma_1 = pMa(EUR_USD.BearishRev[0,:],12)
# bearrevma_2 = pMa(EUR_USD.BearishRev[1,:],12)
# bearrevma_3 = pMa(EUR_USD.BearishRev[2,:],12)
# bearrevma_4 = pMa(EUR_USD.BearishRev[3,:],12)
# bullrevma = EUR_USD.BullishRev.sum(axis=0)
# bearrevma = EUR_USD.BearishRev.sum(axis=0)
# bullrevma = pMa(bullrevma,12)
# bearrevma = pMa(bearrevma,12)
# # plt.plot(bullrevma_1)
# # plt.plot(bullrevma_2)
# # plt.plot(bullrevma_3)
# # plt.plot(bullrevma_4)
# # plt.plot(bullrevma)
# # plt.plot(bearrevma_1)
# # plt.plot(bearrevma_2)
# # plt.plot(bearrevma_3)
# # plt.plot(bearrevma_4)
# # plt.plot(bearrevma)
# # plt.show()

# basebuy = np.zeros((2,len(EUR_USD.close)))
# basesell = np.zeros((2,len(EUR_USD.close)))
# basebuypl = np.zeros((2,len(EUR_USD.close)))
# basesellpl = np.zeros((2,len(EUR_USD.close)))

# for i in range(len(EUR_USD.close)):
# 	if Open_Order == 0:
# 		Carry_Price = EUR_USD.close[i-1]
# 		if p[3,i] > ma[i] - 1.96*sd[i] and p[3,i-1] < ma[i-1] - 1.96*sd[i-1] and i - last_entry > 5:
# 			basebuy[0,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = 1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i] - 0.01
# 			Take_Profit = EUR_USD.close[i] + 0.005
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 		elif p[3,i] < ma[i] + 1.96*sd[i] and p[3,i-1] > ma[i-1] + 1.96*sd[i-1] and i - last_entry > 5:
# 			basesell[0,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = -1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i] + 0.01
# 			Take_Profit = EUR_USD.close[i] - 0.005
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 	elif Open_Order == 1:
# 		if EUR_USD.high[i] > Take_Profit:
# 			basebuy[0,i] = -1
# 			basebuypl[0,i] = (Take_Profit-Open_Price)
# 			Account = Starting_Balance + (Take_Profit-Open_Price)* Lots
# 			Open_Order = 0
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Stop_Loss:
# 			basebuy[0,i] = -1
# 			basebuypl[0,i] = -(Open_Price-Stop_Loss)
# 			Account = Starting_Balance -  (Open_Price-Stop_Loss)* Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.high[i] < Take_Profit and EUR_USD.low[i] > Stop_Loss:
# 			Account = Starting_Balance + (Carry_Price - Open_Price) * Lots
# 	elif Open_Order == -1:
# 		if EUR_USD.high[i] > Stop_Loss:
# 			basesell[0,i] = -1
# 			basesellpl[0,i] = -(Stop_Loss-Open_Price)
# 			Account = Starting_Balance - (Stop_Loss-Open_Price) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Take_Profit:
# 			basesell[0,i] = -1
# 			basesellpl[0,i] = (Open_Price-Take_Profit)
# 			Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] > Take_Profit and EUR_USD.high[i] < Stop_Loss:
# 			Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
# 	Account_Chart.append(Account)
# plt.plot(Account_Chart)
# Account_Chart = []
# Open_Order = 0
# Carry_Price = 0.0
# Lots = 1000
# n = 30
# Account = 1000
# Starting_Balance = Account
# last_entry = 0
# last_trade = 0
# Open_Units = 0
# Open_Trade = False
# Trade_Counter = 0
# new_entry = False
# for i in range(len(EUR_USD.close)):
# 	if Open_Order == 0:
# 		Carry_Price = EUR_USD.close[i-1]
# 		if p[3,i] < ma[i] - 1.96*sd[i] and i - last_entry > 5:
# 			basebuy[1,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = 1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i] - 0.01
# 			Take_Profit = EUR_USD.close[i] + 0.005
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 		elif p[3,i] > ma[i] + 1.96*sd[i] and i - last_entry > 5:
# 			basesell[1,i] = 1
# 			Trade_Counter += 1 
# 			Open_Order = -1
# 			Open_Price = EUR_USD.close[i]
# 			Stop_Loss = EUR_USD.close[i] + 0.01
# 			Take_Profit = EUR_USD.close[i] - 0.005
# 			Carry_Price = EUR_USD.close[i]
# 			last_entry = i
# 			new_entry = True
# 	elif Open_Order == 1:
# 		if EUR_USD.high[i] > Take_Profit:
# 			basebuy[1,i] = -1
# 			basebuypl[1,i] = (Take_Profit-Open_Price)
# 			Account = Starting_Balance + (Take_Profit-Open_Price)* Lots
# 			Open_Order = 0
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Stop_Loss:
# 			basebuy[1,i] = -1
# 			basebuypl[1,i] = -(Open_Price-Stop_Loss)
# 			Account = Starting_Balance -  (Open_Price-Stop_Loss)* Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.high[i] < Take_Profit and EUR_USD.low[i] > Stop_Loss:
# 			Account = Starting_Balance + (Carry_Price - Open_Price) * Lots
# 	elif Open_Order == -1:
# 		if EUR_USD.high[i] > Stop_Loss:
# 			basesell[1,i] = -1
# 			basesellpl[1,i] = -(Stop_Loss-Open_Price)
# 			Account = Starting_Balance - (Stop_Loss-Open_Price) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] < Take_Profit:
# 			basesell[1,i] = -1
# 			basesellpl[1,i] = (Open_Price-Take_Profit)
# 			Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
# 			Open_Order = 0 
# 			Starting_Balance = Account
# 		if EUR_USD.low[i] > Take_Profit and EUR_USD.high[i] < Stop_Loss:
# 			Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
# 	Account_Chart.append(Account)
# plt.plot(Account_Chart)
# plt.ylim(500,2000)
# plt.show()
# res = np.zeros((2,2))
# for i in range(len(EUR_USD.close)):
# 	if basebuypl[0,i] != 0:
# 		res[0,0] += 1
# 	if basesellpl[0,i] != 0:
# 		res[1,0] += 1
# 	if basebuypl[1,i] != 0:
# 		res[0,1] += 1
# 	if basesellpl[1,i] != 0:
# 		res[1,1] += 1
# print res[0,0], res[1,0], sum(basebuypl[0,:]), sum(basesellpl[0,:])
# print res[0,1], res[1,1], sum(basebuypl[1,:]), sum(basesellpl[1,:])
# # print Trade_Counter
# # adjbuy = np.zeros((5,len(EUR_USD.close)))
# # adjsell = np.zeros((5,len(EUR_USD.close)))
# # adjbuypl = np.zeros((5,len(EUR_USD.close)))
# # adjsellpl = np.zeros((5,len(EUR_USD.close)))
# # as0 = False
# # as1 = False
# # as2 = False
# # as3 = False
# # as4 = False
# # ab0 = False
# # ab1 = False
# # ab2 = False
# # ab3 = False
# # ab4 = False
# # for i in range(len(EUR_USD.close)):
# # 	if basebuy[0,i] == 1:
# # 		if bullrevma[i] > 0.4:
# # 			adjbuy[0,i] = 1
# # 			ab0 = True
# # 		if bullrevma_1[i] > 0:
# # 			adjbuy[1,i] = 1
# # 			ab1 = True
# # 		if bullrevma_2[i] > 0:
# # 			adjbuy[2,i] = 1
# # 			ab2 = True
# # 		if bullrevma_3[i] > 0:
# # 			adjbuy[3,i] = 1
# # 			ab3 = True
# # 		if bullrevma_4[i] > 0:
# # 			adjbuy[4,i] = 1
# # 			ab4 = True
# # 	if basesell[i] == 1:
# # 		if bearrevma[i] > 0.4:
# # 			adjsell[0,i] = 1
# # 			as0 = True
# # 		if bearrevma_1[i] > 0:
# # 			adjsell[1,i] = 1
# # 			as1 = True
# # 		if bearrevma_2[i] > 0:
# # 			adjsell[2,i] = 1
# # 			as2 = True
# # 		if bearrevma_3[i] > 0:
# # 			adjsell[3,i] = 1
# # 			as3 = True
# # 		if bearrevma_4[i] > 0:
# # 			adjsell[4,i] = 1
# # 			as4 = True
# # 	if basebuy[i] == -1:
# # 		if ab0 == True:
# # 			ab0 == False
# # 			adjbuypl[0,i] = basebuypl[i]
# # 		if ab1 == True:
# # 			ab1 == False
# # 			adjbuypl[1,i] = basebuypl[i]
# # 		if ab2 == True:
# # 			ab2 == False
# # 			adjbuypl[2,i] = basebuypl[i]
# # 		if ab3 == True:
# # 			ab3 == False
# # 			adjbuypl[3,i] = basebuypl[i]
# # 		if ab4 == True:
# # 			ab4 == False
# # 			adjbuypl[4,i] = basebuypl[i]
# # 	if basesell[i] == -1:
# # 		if as0 == True:
# # 			as0 == False
# # 			adjsellpl[0,i] = basesellpl[i]
# # 		if as1 == True:
# # 			as1 == False
# # 			adjsellpl[1,i] = basesellpl[i]
# # 		if as2 == True:
# # 			as2 == False
# # 			adjsellpl[2,i] = basesellpl[i]
# # 		if as3 == True:
# # 			as3 == False
# # 			adjsellpl[3,i] = basesellpl[i]
# # 		if as4 == True:
# # 			as4 == False
# # 			adjsellpl[4,i] = basesellpl[i]
# # 	basebuy[i] = basebuy[i]*EUR_USD.close[i]
# # 	basesell[i] = basesell[i]*EUR_USD.close[i]
# # print sum(basebuy), sum(basesell)
# # print sum(adjbuy[0,:]), sum(adjbuy[1,:]), sum(adjbuy[2,:]), sum(adjbuy[3,:]), sum(adjbuy[4,:])
# # print sum(adjsell[0,:]), sum(adjsell[1,:]), sum(adjsell[2,:]), sum(adjsell[3,:]), sum(adjsell[4,:])	
# # print sum(basebuypl), sum(basesellpl)
# # print sum(adjbuypl[0,:]), sum(adjbuypl[1,:]), sum(adjbuypl[2,:]), sum(adjbuypl[3,:]), sum(adjbuypl[4,:])
# # print sum(adjsellpl[0,:]), sum(adjsellpl[1,:]), sum(adjsellpl[2,:]), sum(adjsellpl[3,:]), sum(adjsellpl[4,:])
# # for k in range(5):
# # 	rets = np.zeros((sum(adjbuy[k,:]),50))
# # 	c = 0
# # 	for i in range(len(EUR_USD.close)):
# # 		if adjbuy[k,i] == 1:
# # 			for j in range(50):
# # 				rets[c,j] = EUR_USD.close[i+j]/EUR_USD.close[i] - 1
# # 			c += 1
# # 	# ret = rets.mean(axis=0)
# # 	# plt.plot(ret)
# # 	for i in range(c):
# # 		plt.plot(rets[i,:])
# # 	plt.show()
# 	# for j in range(len(adjbuy[:,0])):
# 	# 	for i in range(len(EUR_USD.close)):
# 	# 		adjbuy[j,i] = adjbuy[j,i]*EUR_USD.close[i]/0.995
# 	# 		adjsell[j,i] = adjsell[j,i]*EUR_USD.close[i]*1.005
# 		# plt.plot(adjbuy[j,:],'go')
# 		# plt.plot(basebuy,'gx')
# 		# plt.plot(EUR_USD.close,'b')
# 		# plt.show()
# 		# plt.plot(adjsell[j,:],'ro')
# 		# plt.plot(basesell,'rx')
# 		# plt.plot(EUR_USD.close,'b')
# 		# plt.show()
# # plt.plot(basesell,'rx')
# # plt.plot(basebuy,'gx')
# # plt.plot(EUR_USD.close)
# # plt.show()
# # UBData = np.zeros((40,len(p[3,:])))
# # LBData = np.zeros((40,len(p[3,:])))
# # u_cnt = 0
# # l_cnt = 0
# # f_cnt = 0
# # u_brk = []
# # l_brk = []
# # f_brk = []
# # u_stoch	= []
# # l_stoch = []
# # f_stoch = []
# # dist_ub = []
# # dist_lb = []

# # ma = pMa(p[3,:], 50)
# # sd = pStd(p[3,:], 50)
# # ub = ma + 1*sd
# # lb = ma - 1*sd

# # # act = 0.0
# # # fore = 0.0
# # # cnt = 0
# # # tm = ConvertToTime("1 year")
# # # h = {'Authorization' : DEMO_ACCESS_TOKEN}
# # # url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=GBP&period=" + str(tm)
# # # r = requests.get(url, headers=h)     
# # # data = json.loads(r.text)
# # # for i in range(len(data)):
# # # 	if data[i]['title'] == "Retail Sales (inc Auto Fuel)" and data[i]['currency'] == "GBP":
# # # 		act += float(data[i]['actual']) - float(data[i]['forecast'])
# # # 		# fore += float(data[i]['forecast'])

# # # 		cnt += 1
# # # print act/cnt #, fore/cnt
# # # b = (p[3,i] - lb[i])/(ub[i]-lb[i])
# # # stochk = Stochastic(p[1,:], p[2,:], p[3,:], 13, 5, "K")
# # # stochd = Stochastic(p[1,:], p[2,:], p[3,:], 13, 5, "D")
# # # h = Hammer(p[0,:], p[1,:], p[2,:], p[3,:])
# # # s = ShootingStar(p[0,:], p[1,:], p[2,:], p[3,:])
# # # ud = UpDoji(p[0,:], p[1,:], p[2,:], p[3,:],1)
# # # dd = DownDoji(p[0,:], p[1,:], p[2,:], p[3,:],1)
# # # ibu = InsideBarBreakUp(p[1,:], p[2,:], p[3,:],1)
# # # ibl = InsideBarBreakDown(p[1,:], p[2,:], p[3,:],1)
# # bukr = BullishKeyReversal(p[0,:], p[1,:], p[2,:], p[3,:])
# # bekr = BearishKeyReversal(p[0,:], p[1,:], p[2,:], p[3,:])
# # # roc = ROC(p[3,:], 50)
# # # # Piv = pPivotPoints(p[1,:], p[2,:], p[3,:], p[3,:])
# # # # a = ATR(p[3,:], p[1,:], p[2,:])

# # # d = Doji(p[0,:], p[1,:], p[2,:], p[3,:])
# # # bum = BullishMarubozu(p[0,:], p[1,:], p[2,:], p[3,:])
# # # bem = BearishMarubozu(p[0,:], p[1,:], p[2,:], p[3,:])
# # # lld = LongLeggedDoji(p[0,:], p[1,:], p[2,:], p[3,:])
# # # gs = Gravestone(p[0,:], p[1,:], p[2,:], p[3,:])
# # # df = Dragonfly(p[0,:], p[1,:], p[2,:], p[3,:])
# # # lu = LongUp(p[3,:])
# # # ld = LongDown(p[3,:])
# # # f3 = FallingThree(p[0,:], p[1,:], p[2,:], p[3,:])
# # # r3 = RisingThree(p[0,:], p[1,:], p[2,:], p[3,:])
# # # ms = MorningStar(p[0,:], p[1,:], p[2,:], p[3,:])
# # # es = EveningStar(p[0,:], p[1,:], p[2,:], p[3,:])
# # tws = ThreeWhiteSoldiers(p[3,:])
# # tbc = ThreeBlackCrows(p[3,:])

# # # dr = Doji_Resistance(p[0,:], p[1,:], p[2,:], p[3,:])
# # # ds = Doji_Support(p[0,:], p[1,:], p[2,:], p[3,:])
# # # hw = HighWave(p[0,:], p[1,:], p[2,:], p[3,:])
# # # bue = BullishEngulfing(p[0,:], p[1,:], p[2,:], p[3,:])
# # # bee = BearishEngulfing(p[0,:], p[1,:], p[2,:], p[3,:])
# # # dcc = DarkCloudCover(p[0,:], p[1,:], p[2,:], p[3,:])
# # # bp = BullishPiercing(p[0,:], p[1,:], p[2,:], p[3,:])
# # # buh = BullishHarami(p[0,:], p[1,:], p[2,:], p[3,:])
# # # beh = BearishHarami(p[0,:], p[1,:], p[2,:], p[3,:])

# # # when you're done replace all the c > ub with the test for breaks out and breaks in or the test of above the line
# # plt_dwn_array = []
# # plt_up_array = []
# # up_cnt = 0
# # dwn_cnt = 0
# # up_rets = np.zeros(9)
# # dwn_rets = np.zeros(9)

# # for i in range(20, len(p[3,:])-20):
# # 	if p[3,i] > ub[i] and tws[i] == 1 and p[0,i] > ub[i]:
# # 		up_cnt += 1
# # 		for j in range(0,9):
# # 			plt_up_array.append(p[3,i+j]/p[3,i])
# # 			up_rets[j] += p[3,i+j]/p[3,i]
# # 		# plt.plot(plt_up_array)
# # 		plt_up_array = []
# # # plt.show()
# # up_rets = up_rets/up_cnt
# # print up_rets

# # for i in range(20, len(p[3,:])-20):
# # 	if p[3,i] < lb[i] and tbc[i] == 1 and p[0,i] < lb[i]:
# # 		dwn_cnt += 1
# # 		for j in range(0,9):
# # 			plt_dwn_array.append(p[3,i+j]/p[3,i])
# # 			dwn_rets[j] += p[3,i+j]/p[3,i]
# # 		# plt.plot(plt_dwn_array)
# # 		plt_dwn_array = []
# # # plt.show()
# # dwn_rets = dwn_rets/dwn_cnt
# # print dwn_rets
# # print up_cnt, dwn_cnt
# # plt.plot(up_rets)
# # plt.plot(dwn_rets)
# # plt.show()
# # for i in range(len(p[3,:])):
# # 	# Upper Band
# # 	if p[3,i] > ub[i] and p[3,i-1] < ub[i-1]:
# # 		UBData[0,i] = 1
# # 	if p[3,i] > ub[i]:
# # 		UBData[1,i] = 1
# # 	if dd[i] == 1 and p[3,i] > ub[i] and p[3,i-1] > ub[i-1]:
# # 		UBData[3,i] = 1
# # 	if ibl[i] == 1 and p[3,i] > ub[i] and p[3,i-1] > ub[i-1]:
# # 		UBData[4,i] = 1
# # 	if bekr[i] == 1 and p[3,i] > ub[i] and p[3,i-1] > ub[i-1]:
# # 		UBData[5,i] = 1
# # 	if s[i] == 1 and p[3,i] > ub[i] and p[3,i-1] > ub[i-1]:
# # 		UBData[6,i] = 1
# # 	UBData[7,i] = p[3,i]-ub[i]
# # 	if UBData[1,i] == 1:
# # 		u_cnt += 1
# # 		u_stoch.append(stochk[i])
# # 	if UBData[1,i] == 0 and u_cnt != 0:
# # 		u_brk.append(u_cnt)
# # 		u_cnt = 0
# # 	if p[3,i] > ub[i] and d[i] == 1:
# # 		UBData[8,i] = 1
# # 	if p[3,i] > ub[i] and gs[i] == 1:
# # 		UBData[9,i] = 1
# # 	if p[3,i] > ub[i] and df[i] == 1:
# # 		UBData[10,i] = 1
# # 	if p[3,i] > ub[i] and bum[i] == 1:
# # 		UBData[11,i] = 1
# # 	if p[3,i] > ub[i] and bem[i] == 1:
# # 		UBData[12,i] = 1
# # 	if p[3,i] > ub[i] and lld[i] == 1:
# # 		UBData[13,i] = 1
# # 	if p[3,i] > ub[i] and lu[i] == 1:
# # 		UBData[14,i] = 1
# # 	if p[3,i] > ub[i] and ld[i] == 1:
# # 		UBData[15,i] = 1
# # 	if p[3,i] > ub[i] and f3[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[16,i] = 1
# # 	# Tries one break, then has to try again
# # 	if p[3,i] < ub[i] and f3[i] == 1 and p[0,i] > ub[i] and p[3,i-4] < ub[i-4] and p[0,i-4] > ub[i-4]:
# # 		UBData[17,i] = 1
# # 	if p[3,i] > ub[i] and r3[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[18,i] = 1
# # 	# Tries one break, then has to try again
# # 	if p[3,i] > ub[i] and r3[i] == 1 and p[0,i] < ub[i] and p[3,i-4] > ub[i-4] and p[0,i-4] < ub[i-4]:
# # 		UBData[19,i] = 1
# # 	if p[3,i] > ub[i] and ms[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[20,i] = 1
# # 	# Dips below ub and then returns
# # 	if p[3,i] > ub[i] and ms[i] == 1 and p[3,i-1] < ub[i-1] and p[0,i-2] > ub[i-2] and p[3,i-2] < ub[i-2]:
# # 		UBData[21,i] = 1
# # 	# Morning star takes you above the ub
# # 	if p[3,i] > ub[i] and ms[i] == 1 and p[3,i-1] < ub[i-1] and p[3,i-2] < ub[i-2]:
# # 		UBData[22,i] = 1
# # 	if p[3,i] > ub[i] and es[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[23,i] = 1
# # 	# Broke, doji and then return
# # 	if p[3,i] < ub[i] and es[i] == 1 and p[3,i-1] > ub[i-1] and p[0,i-2] < ub[i-2] and p[3,i-2] > ub[i-2]:
# # 		UBData[24,i] = 1
# # 	# Evening star takes you below the ub
# # 	if p[3,i] < ub[i] and es[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[25,i] = 1
# # 	if p[3,i] > ub[i] and tws[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[26,i] = 1
# # 	# The pattern ends with the 3rd candle breaking the ub
# # 	if p[3,i] > ub[i] and tws[i] == 1 and p[0,i] < ub[i]:
# # 		UBData[27,i] = 1
# # 	if p[3,i] > ub[i] and tbc[i] == 1 and p[3,i-1] > ub[i-1] and p[3,i-2] > ub[i-2]:
# # 		UBData[28,i] = 1
# # 	# The pattern ends with the 3rd candle breaking the ub
# # 	if p[3,i] < ub[i] and tbc[i] == 1 and p[0,i] > ub[i]:
# # 		UBData[29,i] = 1
# # 	if p[3,i] > ub[i] and hw[i] == 1:
# # 		UBData[30,i] = 1
# # 	if p[3,i] > ub[i] and bee[i] == 1:
# # 		UBData[31,i] = 1
# # 	if p[3,i] > ub[i] and bue[i] == 1:
# # 		UBData[32,i] = 1
# # 	if p[3,i] > ub[i] and beh[i] == 1:
# # 		UBData[33,i] = 1
# # 	if p[3,i] > ub[i] and buh[i] == 1:
# # 		UBData[34,i] = 1
# # 	if p[3,i] > ub[i] and bp[i] == 1:
# # 		UBData[35,i] = 1
# # 	if p[3,i] > ub[i] and dcc[i] == 1:
# # 		UBData[36,i] = 1

# # 	# # Lower Band
# # 	if p[3,i] < lb[i] and p[3,i-1] > lb[i-1]:
# # 		LBData[0,i] = 1
# # 	if p[3,i] < lb[i]:
# # 		LBData[1,i] = 1
# # 	if ud[i] == 1 and p[3,i] < lb[i] and p[3,i-1] < lb[i-1]:
# # 		LBData[3,i] = 1
# # 	if ibu[i] == 1 and p[3,i] < lb[i] and p[3,i-1] < lb[i-1]:
# # 		LBData[4,i] = 1
# # 	if bukr[i] == 1 and p[3,i] < lb[i] and p[3,i-1] < lb[i-1]:
# # 		LBData[5,i] = 1
# # 	if h[i] == 1 and p[3,i] < lb[i] and p[3,i-1] < lb[i-1]:
# # 		LBData[6,i] = 1
# # 	LBData[7,i] = p[3,i]-lb[i]
# # 	if LBData[1,i] == 1:
# # 		l_cnt += 1
# # 		l_stoch.append(stochk[i])
# # 	if LBData[1,i] == 0 and l_cnt != 0:
# # 		l_brk.append(l_cnt)
# # 		l_cnt = 0
# # 	if p[3,i] < lb[i] and d[i] == 1:
# # 		LBData[8,i] = 1
# # 	if p[3,i] < lb[i] and gs[i] == 1:
# # 		LBData[9,i] = 1
# # 	if p[3,i] < lb[i] and df[i] == 1:
# # 		LBData[10,i] = 1
# # 	if p[3,i] < lb[i] and bum[i] == 1:
# # 		LBData[11,i] = 1
# # 	if p[3,i] < lb[i] and bem[i] == 1:
# # 		LBData[12,i] = 1
# # 	if p[3,i] < lb[i] and lld[i] == 1:
# # 		LBData[13,i] = 1
# # 	if p[3,i] < lb[i] and lu[i] == 1:
# # 		LBData[14,i] = 1
# # 	if p[3,i] < lb[i] and ld[i] == 1:
# # 		LBData[15,i] = 1
# # 	if p[3,i] < lb[i] and f3[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[16,i] = 1
# # 	# Tries one break, then has to try again
# # 	if p[3,i] < lb[i] and f3[i] == 1 and p[0,i] > lb[i] and p[3,i-4] < lb[i-4] and p[0,i-4] > lb[i-4]:
# # 		LBData[17,i] = 1
# # 	if p[3,i] < lb[i] and r3[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[18,i] = 1
# # 	# Tries one break, then has to try again
# # 	if p[3,i] > lb[i] and r3[i] == 1 and p[0,i] < lb[i] and p[3,i-4] > lb[i-4] and p[0,i-4] < lb[i-4]:
# # 		LBData[19,i] = 1
# # 	if p[3,i] < lb[i] and ms[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[20,i] = 1
# # 	# Dips below lb and then returns
# # 	if p[3,i] > lb[i] and ms[i] == 1 and p[3,i-1] < lb[i-1] and p[0,i-2] > lb[i-2] and p[3,i-2] < lb[i-2]:
# # 		LBData[21,i] = 1
# # 	# Morning star takes you above the lb
# # 	if p[3,i] > lb[i] and ms[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[22,i] = 1
# # 	if p[3,i] < lb[i] and es[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[23,i] = 1
# # 	# Broke, doji and then return
# # 	if p[3,i] < lb[i] and es[i] == 1 and p[3,i-1] > lb[i-1] and p[0,i-2] < lb[i-2] and p[3,i-2] > lb[i-2]:
# # 		LBData[24,i] = 1
# # 	# Evening star takes you below the lb
# # 	if p[3,i] < lb[i] and es[i] == 1 and p[3,i-1] > lb[i-1] and p[3,i-2] > lb[i-2]:
# # 		LBData[25,i] = 1
# # 	if p[3,i] < lb[i] and tws[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[26,i] = 1
# # 	# The pattern ends with the 3rd candle breaking the lb
# # 	if p[3,i] > lb[i] and tws[i] == 1 and p[0,i] < lb[i]:
# # 		LBData[27,i] = 1	
# # 	if p[3,i] < lb[i] and tbc[i] == 1 and p[3,i-1] < lb[i-1] and p[3,i-2] < lb[i-2]:
# # 		LBData[28,i] = 1
# # 	# The pattern ends with the 3rd candle breaking the lb
# # 	if p[3,i] < lb[i] and tbc[i] == 1 and p[0,i] > lb[i]:
# # 		LBData[29,i] = 1
# # 	if p[3,i] < lb[i] and hw[i] == 1:
# # 		LBData[30,i] = 1
# # 	if p[3,i] < lb[i] and bee[i] == 1:
# # 		LBData[31,i] = 1
# # 	if p[3,i] < lb[i] and bue[i] == 1:
# # 		LBData[32,i] = 1
# # 	if p[3,i] < lb[i] and beh[i] == 1:
# # 		LBData[33,i] = 1
# # 	if p[3,i] < lb[i] and buh[i] == 1:
# # 		LBData[34,i] = 1
# # 	if p[3,i] < lb[i] and bp[i] == 1:
# # 		LBData[35,i] = 1
# # 	if p[3,i] < lb[i] and dcc[i] == 1:
# # 		LBData[36,i] = 1

# # 	# # Middle of Band
# # 	if p[3,i] < ub[i] and p[3,i] > lb[i]:
# # 		UBData[2,i] = 1
# # 		LBData[2,i] = 1
# # 	if UBData[2,i] == 1:
# # 		f_cnt += 1
# # 		f_stoch.append(stochk[i])
# # 	if UBData[2,i] == 0 and f_cnt != 0:
# # 		f_brk.append(f_cnt)
# # 		f_cnt = 0
# # print sum(UBData[0,:]), sum(LBData[0,:])
# # print sum(UBData[1,:]), sum(LBData[1,:])
# # print sum(UBData[2,:]), sum(LBData[2,:])
# # print sum(UBData[3,:]), sum(LBData[3,:])
# # print sum(UBData[4,:]), sum(LBData[4,:])
# # print sum(UBData[5,:]), sum(LBData[5,:])
# # print sum(UBData[6,:]), sum(LBData[6,:])
# # print sum(UBData[7,:]), sum(LBData[7,:])
# # print sum(UBData[8,:]), sum(LBData[8,:])
# # print sum(UBData[9,:]), sum(LBData[9,:])
# # print sum(UBData[10,:]), sum(LBData[10,:])
# # print sum(UBData[11,:]), sum(LBData[11,:])
# # print sum(UBData[12,:]), sum(LBData[12,:])
# # print sum(UBData[13,:]), sum(LBData[13,:])
# # print sum(UBData[14,:]), sum(LBData[14,:])
# # print sum(UBData[15,:]), sum(LBData[15,:])
# # print sum(UBData[16,:]), sum(LBData[16,:])
# # print sum(UBData[17,:]), sum(LBData[17,:])
# # print sum(UBData[18,:]), sum(LBData[18,:])
# # print sum(UBData[19,:]), sum(LBData[19,:])
# # print sum(UBData[20,:]), sum(LBData[20,:])
# # print sum(UBData[21,:]), sum(LBData[21,:])
# # print sum(UBData[22,:]), sum(LBData[22,:])
# # print sum(UBData[23,:]), sum(LBData[23,:])
# # print sum(UBData[24,:]), sum(LBData[24,:])
# # print sum(UBData[25,:]), sum(LBData[25,:])
# # print sum(UBData[26,:]), sum(LBData[26,:])
# # print sum(UBData[27,:]), sum(LBData[27,:])
# # print sum(UBData[28,:]), sum(LBData[28,:])
# # print sum(UBData[29,:]), sum(LBData[29,:])
# # print sum(UBData[30,:]), sum(LBData[30,:])
# # print sum(UBData[31,:]), sum(LBData[31,:])
# # print sum(UBData[32,:]), sum(LBData[32,:])
# # print sum(UBData[33,:]), sum(LBData[33,:])
# # print sum(UBData[34,:]), sum(LBData[34,:])
# # print sum(UBData[35,:]), sum(LBData[35,:])
# # print sum(UBData[36,:]), sum(LBData[36,:])
# # # print np.mean(u_stoch), np.mean(l_stoch), np.mean(f_stoch)
# # # print sum(u_brk), len(u_brk), round(float(float(sum(u_brk))/float(len(u_brk))),3)
# # # print u_brk
# # # print sum(l_brk), len(l_brk), round(float(float(sum(l_brk))/float(len(l_brk))),3)
# # # print l_brk
# # # print sum(f_brk), len(f_brk), round(float(float(sum(f_brk))/float(len(f_brk))),3)
# # # print f_brk

# # # ret = []
# # # for i in range(1,len(p[3,:])-1):
# # # 	W = []
# # # 	M = []
# # # 	ret = 0.005
# # # 	temp = []
# # # 	lft_tail = p[3,i]/p[3,i-1]-1
# # # 	rht_tail = p[3,i + 1]/p[3,i]-1
# # # 	angle = math.tan(rht_tail/(lft_tail+0.000001))*180/math.pi
# # # 	if abs(lft_tail-rht_tail) < 0.0001:
# # # 		Test_Data[17, i] = 1
# # # 	ret.append(lft_tail)
# # # 	# if p[3,i-15]/p[3,i-20] - 1 < -ret and p[3,i-10]/p[3,i-15] - 1 > ret and p[3,i-5]/p[3,i-10] - 1 < -ret and p[3,i]/p[3,i-5] - 1 > ret:
# # # 	# 	Test_Data[17, i] = 1
# # # 	# 	for j in range(40):
# # # 	# 		temp.append(p[3,i+j-20]/p[3,i-20])
# # # 	# 	plt.plot(temp)
# # # 	# if p[3,i-1]/p[3,i] - 1 < -ret and p[3,i+1]/p[3,i] - 1 > ret:
# # # 	# 	Test_Data[17, i] = 1
# # # 	# 	for j in range(40):
# # # 	# 		temp.append(p[3,i+j-20]/p[3,i-20])
# # # 	# 		t.append(Test_Data[17,i+j-20]*p[3,i+j-20])
# # # 		# plt.plot(temp)
# # # 	# if p[3,i-15]/p[3,i-20] - 1 > ret and p[3,i-10]/p[3,i-15] - 1 < -ret and p[3,i-5]/p[3,i-10] - 1 > ret and p[3,i]/p[3,i-5] - 1 < -ret:
# # # 	# 	Test_Data[18, i] = 1
# # # 	# 	for j in range(100):
# # # 	# 		temp.append(p[3,i+j-50]/p[3,i-50])
# # # 	# 	plt.plot(temp)