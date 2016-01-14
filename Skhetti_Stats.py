import requests
import json
from array import *
import matplotlib.pyplot as plt
import numpy as np
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import pypyodbc

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
Daze = []
Day_Count = 0


file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  
cur = conn.cursor()
#cur.execute(u"""CREATE TABLE Skhetti_Stats (ID INTEGER PRIMARY KEY, Day String, Test String, Ret Double)""")
cur.execute("SELECT DISTINCT [Day] FROM Backtest_Ret WHERE [Test] = 'BUY MAC H4 EUR_USD and 50 SMA' ;")

Data_Daze = cur.fetchall()
Day_Count = len(Data_Daze)
for x in Data_Daze:
    x1 = str(x)
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Daze.append(z2)

Highs = []
Index_Highs = []
Lows = []
Index_Lows = []

for j in range(0,Day_Count):
	Ret = []
	cur.execute("SELECT [Ret] FROM Backtest_Ret WHERE [Test] = 'BUY MAC H4 EUR_USD and 50 SMA' AND [Day] = " + "'" + Daze[j] + "'" + " ORDER BY [ID] ASC;")
	Ret_Data = cur.fetchall()
	for y in Ret_Data:
		x1 = str(y)
		y2 = x1[1:]
		z2 = y2[:len(y2)-2]
		Ret.append(float(z2))
	a = np.array(Ret)
	Highs.append(max(a))
	Lows.append(min(a))
	Max_indices = np.where(a == max(a))
	Min_indices = np.where(a == min(a))
	IH = str(np.take(Max_indices,[0]))
	IL = str(np.take(Min_indices,[0]))
	IH1 = IH[1:]
	IH2 = IH1[:len(IH1)-1]
	IL1 = IL[1:]
	IL2 = IL1[:len(IL1)-1]
	Index_Highs.append(float(IH2))
	Index_Lows.append(float(IL2))

a = np.array(Highs)
print np.average(a)
print np.std(a)
a = np.array(Lows)
print np.average(a)
print np.std(a)

cur.close()
conn.commit()
conn.close()