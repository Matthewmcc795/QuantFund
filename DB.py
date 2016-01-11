import pyodbc
import pypyodbc
import requests
import json
from array import *

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
Sec.append("USD_JPY")
Sec.append("USD_CAD")
Sec.append("USD_CHF")

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

strT = "time"
strO = "openMid"
strH = "highMid"
strL = "lowMid"
strC = "closeMid"
strV = "volume"
strCO = "complete"

#pypyodbc.win_create_mdb(file_Name)

conn = pypyodbc.win_connect_mdb(file_Name)  
file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"
cur = conn.cursor()

cur.execute(u"""CREATE TABLE M5_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")

p = 0 
for j in range(0,7):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=M5"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][5000-index][strT]
	def Open(index):
	    return data["candles"][5000-index][strO]
	def High(index):
	    return data["candles"][5000-index][strH]
	def Low(index):
	    return data["candles"][5000-index][strL]
	def Close(index):
	    return data["candles"][5000-index][strC]

	for i in range(1,5000):
	   cur.execute('''INSERT INTO M5_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 4999*(j+1)
cur.commit()

cur.execute(u"""CREATE TABLE H4_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")

p = 0 
for j in range(0,7):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=H4"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][5000-index][strT]
	def Open(index):
	    return data["candles"][5000-index][strO]
	def High(index):
	    return data["candles"][5000-index][strH]
	def Low(index):
	    return data["candles"][5000-index][strL]
	def Close(index):
	    return data["candles"][5000-index][strC]

	for i in range(1,5000):
	   cur.execute('''INSERT INTO H4_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 4999*(j+1)


cur.execute(u"""CREATE TABLE H1_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
cur.commit()

p = 0 
for j in range(0,7):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=H1"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][5000-index][strT]
	def Open(index):
	    return data["candles"][5000-index][strO]
	def High(index):
	    return data["candles"][5000-index][strH]
	def Low(index):
	    return data["candles"][5000-index][strL]
	def Close(index):
	    return data["candles"][5000-index][strC]

	for i in range(1,5000):
	   cur.execute('''INSERT INTO H1_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 4999*(j+1)

cur.commit()
cur.close()
conn.commit()
conn.close()