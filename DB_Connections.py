import pyodbc
import pypyodbc
import requests
import json
from array import *

Sec = []

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

strT = "time"
strO = "openMid"
strH = "highMid"
strL = "lowMid"
strC = "closeMid"
strV = "volume"
strCO = "complete"

conn = pypyodbc.win_connect_mdb(file_Name)  
file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"
cur = conn.cursor()

#cur.execute(u"""CREATE TABLE W_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
#cur.commit()

cur.execute("SELECT [Ticker] FROM Securities")
results = cur.fetchall()
for i in range(0,70):
	x1 = str(results[i])
	y2 = x1[3:]
	z2 = y2[:len(y2)-3]
	Sec.append(z2)

#cur.execute(u"""CREATE TABLE D_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
#cur.commit()

p = 0 
for j in range(0,70):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=1000&candleFormat=midpoint&granularity=D"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][999-index][strT]
	def Open(index):
	    return data["candles"][999-index][strO]
	def High(index):
	    return data["candles"][999-index][strH]
	def Low(index):
	    return data["candles"][999-index][strL]
	def Close(index):
	    return data["candles"][999-index][strC]

	for i in range(1,1000):
	   cur.execute('''INSERT INTO D_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 999*(j+1)
cur.commit()

#cur.execute(u"""CREATE TABLE H4_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
#cur.commit()

p = 0 
for j in range(0,70):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=H4"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][999-index][strT]
	def Open(index):
	    return data["candles"][999-index][strO]
	def High(index):
	    return data["candles"][999-index][strH]
	def Low(index):
	    return data["candles"][999-index][strL]
	def Close(index):
	    return data["candles"][999-index][strC]

	for i in range(1,1000):
	   cur.execute('''INSERT INTO H4_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 999*(j+1)

#cur.execute(u"""CREATE TABLE H1_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
cur.commit()

p = 0 
for j in range(0,70):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=H1"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][999-index][strT]
	def Open(index):
	    return data["candles"][999-index][strO]
	def High(index):
	    return data["candles"][999-index][strH]
	def Low(index):
	    return data["candles"][999-index][strL]
	def Close(index):
	    return data["candles"][999-index][strC]

	for i in range(1,1000):
	   cur.execute('''INSERT INTO H1_Price(ID,Day,Ticker,Open,High,Low,Close) 
	  VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 999*(j+1)
cur.commit()

#cur.execute(u"""CREATE TABLE M5_Price (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)""")
#cur.commit()

p = 0 
for j in range(0,70):
	print(Sec[j])
	access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
	R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[j]) +"&count=5000&candleFormat=midpoint&granularity=M5"
	h = {'Authorization' : access_token}
	r= requests.get( R_url, headers=h)     
	data = json.loads(r.text)

	def Date(index):
	    return data["candles"][999-index][strT]
	def Open(index):
	    return data["candles"][999-index][strO]
	def High(index):
	    return data["candles"][999-index][strH]
	def Low(index):
	    return data["candles"][999-index][strL]
	def Close(index):
	    return data["candles"][999-index][strC]

	for i in range(1,1000):
		cur.execute('''INSERT INTO M5_Price(ID,Day,Ticker,Open,High,Low,Close) 
		VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	p = 999*(j+1)
cur.commit()

cur.close()
conn.commit()
conn.close()