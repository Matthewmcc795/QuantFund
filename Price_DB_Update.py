import pyodbc
import pypyodbc
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO

SecID = []
Bars = 5000
n = 100
Sec_Count = 1

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"
conn = pypyodbc.win_connect_mdb(file_Name)
cur = conn.cursor()

cur.execute("SELECT Ticker] FROM Securities")
results = cur.fetchall()
for i in range(0,Sec_Count):
    x1 = str(results[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    SecID.append(float(z1))

h = {'Authorization' : ACCESS_TOKEN}
url = ACCOUNT_DOMAIN + "instrument=EUR_USD&count=" + str(Bars) + "&candleFormat=midpoint&granularity=D"
r = requests.get(url, headers=h)     
data = json.loads(r.text)

def Date(index):
    return data["candles"][5000-index][strT]
def Open(index):
    return data["candles"][5000 - index][STRO]
def High(index):
    return data["candles"][5000 - index][STRH]
def Low(index):
    return data["candles"][5000 - index][STRL]
def Close(index):
    return data["candles"][5000 - index][STRC]

cur.execute("SELECT [Day] FROM D1_Price WHERE [Ticker] = 'EUR_USD' ORDER BY [Day] DESC")
resultsd = cur.fetchall()
for i in range(0,n):
    x1 = str(resultsd[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    Dates.append(float(z1))
laststr = Dates(0, 0)

for i in range(0,n-1) n - 1:
    if Date(i) = laststr:
        q = i

for j in range(0,n - q - 1):
	cur.execute('''INSERT INTO D1_Price(ID,Day,Ticker,Open,High,Low,Close) 
	VALUES(?,?,?,?,?,?,?)''',(ID,Date(j),"EUR_USD",Open(j),High(j),Low(j),Close(j)))

cur.commit()

cur.close()
conn.commit()
conn.close()