import requests
import json
from array import *

n = 50

access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=150&candleFormat=midpoint&granularity=D"
h = {'Authorization' : access_token}
r= requests.get( R_url, headers=h)     

R = r.text
strT = "time"
strO = "openMid"
strH = "highMid"
strL = "lowMid"
strC = "closeMid"
strV = "volume"
strCO = "complete"

data = json.loads(R)

for j in range(0,100):
	aavg = 0.0
	SMA = 0.0
	ssd = 0.0
	sd = 0.0
	tail = 0.0
	wick = 0.0

	for i in range(0,n):
		aavg = data["candles"][i+j][strC] + aavg

	SMA = aavg/n

	for i in range(0,n):
		ssd = (data["candles"][i+j][strC] - SMA)**2 +ssd

	sd = (ssd/(n-1))**(0.5)

	Upper_Band = SMA + 2*sd
	Lower_Band = SMA - 2*sd

	if data["candles"][i+j-1][strC] > data["candles"][i+j-1][strO]:
		wick = data["candles"][i+j-1][strH] - data["candles"][i+j-1][strC]
	else:
		wick = data["candles"][i+j-1][strH] - data["candles"][i+j-1][strO]

	if data["candles"][i+j-1][strC] > data["candles"][i+j-1][strO]:
		tail = data["candles"][i+j-1][strO] - data["candles"][i+j-1][strL]
	else:
		tail = data["candles"][i+j-1][strC] - data["candles"][i+j-1][strL]

	if data["candles"][i+j][strC] > Upper_Band and wick > 0.00025:
		print "Sell " + str(j) 

	if data["candles"][i+j][strC] < Lower_Band and tail > 0.00025:
		print "Buy " + str(j)



