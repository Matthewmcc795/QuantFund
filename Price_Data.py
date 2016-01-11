# classes
import requests
import json
from array import *

access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=USD_CAD&count=5000&candleFormat=midpoint&granularity=H4"
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

def Open(index):
	return data["candles"][index][strO]
def High(index):
	return data["candles"][index][strH]
def Low(index):
	return data["candles"][index][strL]
def Close(index):
	return data["candles"][index][strC]

print Open(1)
print High(1)
print Low(1)
print Close(1)

