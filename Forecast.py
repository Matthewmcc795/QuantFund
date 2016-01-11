import requests
import json
from array import *
import matplotlib.pyplot as plt
import numpy as np
import pypyodbc

access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e"
R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=100&candleFormat=midpoint&granularity=D"
h = {'Authorization' : access_token}
r= requests.get( R_url, headers=h)     

strT = "time"
strO = "openMid"
strH = "highMid"
strL = "lowMid"
strC = "closeMid"
strV = "volume"
strCO = "complete"

data = json.loads(r.text)

def Open(index):
    return data["candles"][100 - index][strO]
def High(index):
    return data["candles"][100 - index][strH]
def Low(index):
    return data["candles"][100 - index][strL]
def Close(index):
    return data["candles"][100 - index][strC]

n = 100
p = 0
cntr = 11

UpperBand = []
UpperBand1 = []
LowerBand = []
LowerBand1 = []

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"
conn = pypyodbc.win_connect_mdb(file_Name)  
cur = conn.cursor()

#cur.execute(u"""CREATE TABLE Forecast_Data (ID INTEGER PRIMARY KEY, N String, R Double)""")
#cur.commit()

cur.execute("SELECT [P] FROM Bands_Data WHERE [Per] = 75 ORDER BY [N] ASC")
results = cur.fetchall()
for i in range(0,10):
    x1 = str(results[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    UpperBand.append(float(z1))

cur.execute("SELECT [P] FROM Bands_Data WHERE [Per] = 25 ORDER BY [N] ASC")
results = cur.fetchall()
for i in range(0,10):
    x1 = str(results[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    LowerBand.append(float(z1)) 

ID = 1
for j in range(0,10):
    upr = 0
    lwr = 0
    for i in range(0,10):
        upr = upr + Close(10-i+j)*(1+UpperBand[j])
        lwr = lwr + Close(10-i+j)*(1+LowerBand[j])
    LowerBand1.append(lwr/10)
    UpperBand1.append(upr/10)

plt.plot(LowerBand1)
plt.plot(UpperBand1)
plt.ylim(1.05,1.12)
plt.show()