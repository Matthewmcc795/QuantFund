import pypyodbc
import requests
import time
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO

start_time = time.time()

last_update = 0
Sec = []

# Cycle through Daily, H4, M5 etc. 

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
Str_SQL1 = []
Str_SQL2 = [] 

cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'D';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

cur.execute("SELECT [Str_SQL1] FROM Connections WHERE [Time_Frame] = 'D';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL1.append(z2)

cur.execute("SELECT [Str_SQL2] FROM Connections WHERE [Time_Frame] = 'D';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL2.append(z2)

for j in range(0,70):
    print Sec[j]
    h = {'Authorization' : ACCESS_TOKEN}
    r = requests.get(URL[j], headers=h)     
    data = json.loads(r.text)
    def Date(index):
        return data["candles"][999-index][STRT]
    def Open(index):
        return data["candles"][999-index][STRO]
    def High(index):
        return data["candles"][999-index][STRH]
    def Low(index):
        return data["candles"][999-index][STRL]
    def Close(index):
        return data["candles"][999-index][STRC]

    #cur.execute("SELECT * FROM D_Price WHERE [Ticker] = %s ORDER BY [Day] ASC" % Sec[j])
    print("SELECT * FROM D_Price WHERE [Ticker] = %s ORDER BY [Day] ASC" % Sec[j])
    results = cur.fetchall()
    x = str(results[0])
    print x
    y = x[3:]
    z = y[:len(y)-3]
    for i in range(0,100):
        if z == str(Date(i)):
            last_update = i 

# Check for each 1000 items in feed if it's the same in the DB


cur.close()
conn.commit()
conn.close()

print("--- %s seconds ---" % (time.time() - start_time))