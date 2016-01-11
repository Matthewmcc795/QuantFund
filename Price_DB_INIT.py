import pypyodbc
import requests
import time
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
last_update = 0
Sec = []

# Cycle through Daily, H4, M5 etc. 
start_time = time.time()


file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  

cur = conn.cursor()

cur.execute("SELECT [Ticker] FROM Securities")
results = cur.fetchall()
for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Sec.append(z2)

URL = []

cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'D';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

for j in range(0,70):
	h = {'Authorization' : ACCESS_TOKEN}
	r = requests.get(URL[j], headers=h)     
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

	for i in range(0,1000):
		cur.execute('''INSERT INTO D_Price (ID,Day,Ticker,Open,High,Low,Close) 
		VALUES(?,?,?,?,?,?,?)''',(1000*j+i,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	cur.commit()

URL = []
print "Daily Prices Updated"
cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'H4';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

for j in range(0,70):
	h = {'Authorization' : ACCESS_TOKEN}
	r = requests.get(URL[j], headers=h)     
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

	for i in range(0,1000):
		cur.execute('''INSERT INTO H4_Price (ID,Day,Ticker,Open,High,Low,Close) 
		VALUES(?,?,?,?,?,?,?)''',(1000*j+i,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	cur.commit()

URL = []
print "4 Hourly Prices Updated"
cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'H1';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

for j in range(0,70):
	h = {'Authorization' : ACCESS_TOKEN}
	r = requests.get(URL[j], headers=h)     
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

	for i in range(0,1000):
		cur.execute('''INSERT INTO H1_Price (ID,Day,Ticker,Open,High,Low,Close) 
		VALUES(?,?,?,?,?,?,?)''',(1000*j+i,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	cur.commit()

URL = []
print "Hourly Prices Updated"
cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'M5';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

for j in range(0,70):
	h = {'Authorization' : ACCESS_TOKEN}
	r = requests.get(URL[j], headers=h)     
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

	for i in range(0,1000):
		cur.execute('''INSERT INTO M5_Price (ID,Day,Ticker,Open,High,Low,Close) 
		VALUES(?,?,?,?,?,?,?)''',(1000*j+i,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
	cur.commit()
print "5 Minute Prices Updated"
cur.close()
conn.commit()
conn.close()
print("--- %s seconds ---" % (time.time() - start_time))