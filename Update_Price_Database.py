import pypyodbc
import requests
import time
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO

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
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
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

    cur.execute(Str_SQL1[j])
    results = cur.fetchall()
    x = str(results[0])
    y = x[3:]
    z = y[:len(y)-3]
    for i in range(0,100):
        if z == str(Date(i)):
            last_update = i 

    if last_update > 0 :
        print "Updating...."
        cur.execute(Str_SQL2[j])
        results = cur.fetchall()
        x1 = str(results[0])
        y2 = x1[1:]
        z2 = y2[:len(y2)-2]

        for i in range(1,last_update+1):
            cur.execute('''INSERT INTO D_Price (ID,Day,Ticker,Open,High,Low,Close) 
            VALUES(?,?,?,?,?,?,?)''',(int(z2)+i,Date(last_update - i),str(Sec[j]),Open(last_update - i),High(last_update - i),Low(last_update - i),Close(last_update - i)))
        
        print "Update complete"
    else:
        print str(Sec[j]) + " is up to date"
cur.commit()

URL = []
Str_SQL1 = []
Str_SQL2 = [] 

cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'H4';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

cur.execute("SELECT [Str_SQL1] FROM Connections WHERE [Time_Frame] = 'H4';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL1.append(z2)

cur.execute("SELECT [Str_SQL2] FROM Connections WHERE [Time_Frame] = 'H4';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL2.append(z2)

for j in range(0,70):
    print Sec[j]
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
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

    cur.execute(Str_SQL1[j])
    results = cur.fetchall()
    x = str(results[0])
    y = x[3:]
    z = y[:len(y)-3]
    for i in range(0,100):
        if z == str(Date(i)):
            last_update = i 

    if last_update > 0 :
        print "Updating...."
        cur.execute(Str_SQL2[j])
        results = cur.fetchall()
        x1 = str(results[0])
        y2 = x1[1:]
        z2 = y2[:len(y2)-2]

        for i in range(1,last_update+1):
            cur.execute('''INSERT INTO H4_Price (ID,Day,Ticker,Open,High,Low,Close) 
            VALUES(?,?,?,?,?,?,?)''',(int(z2)+i,Date(last_update - i),str(Sec[j]),Open(last_update - i),High(last_update - i),Low(last_update - i),Close(last_update - i)))
        
        print "Update complete"
    else:
        print str(Sec[j]) + " is up to date"
cur.commit()

URL = []
Str_SQL1 = []
Str_SQL2 = [] 

cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'H1';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

cur.execute("SELECT [Str_SQL1] FROM Connections WHERE [Time_Frame] = 'H1';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL1.append(z2)

cur.execute("SELECT [Str_SQL2] FROM Connections WHERE [Time_Frame] = 'H1';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL2.append(z2)

for j in range(0,70):
    print Sec[j]
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
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

    cur.execute(Str_SQL1[j])
    results = cur.fetchall()
    x = str(results[0])
    y = x[3:]
    z = y[:len(y)-3]
    for i in range(0,100):
        if z == str(Date(i)):
            last_update = i 

    if last_update > 0 :
        print "Updating...."
        cur.execute(Str_SQL2[j])
        results = cur.fetchall()
        x1 = str(results[0])
        y2 = x1[1:]
        z2 = y2[:len(y2)-2]

        for i in range(1,last_update+1):
            cur.execute('''INSERT INTO H1_Price (ID,Day,Ticker,Open,High,Low,Close) 
            VALUES(?,?,?,?,?,?,?)''',(int(z2)+i,Date(last_update - i),str(Sec[j]),Open(last_update - i),High(last_update - i),Low(last_update - i),Close(last_update - i)))
        
        print "Update complete"
    else:
        print str(Sec[j]) + " is up to date"
cur.commit()

URL = []
Str_SQL1 = []
Str_SQL2 = [] 

cur.execute("SELECT [URL_U] FROM Connections WHERE [Time_Frame] = 'M5';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    URL.append(z2)

cur.execute("SELECT [Str_SQL1] FROM Connections WHERE [Time_Frame] = 'M5';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL1.append(z2)

cur.execute("SELECT [Str_SQL2] FROM Connections WHERE [Time_Frame] = 'M5';")
results = cur.fetchall()

for i in range(0,70):
    x1 = str(results[i])
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    Str_SQL2.append(z2)

for j in range(0,70):
    print Sec[j]
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
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

    cur.execute(Str_SQL1[j])
    results = cur.fetchall()
    x = str(results[0])
    y = x[3:]
    z = y[:len(y)-3]
    for i in range(0,100):
        if z == str(Date(i)):
            last_update = i 

    if last_update > 0 :
        print "Updating...."
        cur.execute(Str_SQL2[j])
        results = cur.fetchall()
        x1 = str(results[0])
        y2 = x1[1:]
        z2 = y2[:len(y2)-2]

        for i in range(1,last_update+1):
            cur.execute('''INSERT INTO M5_Price (ID,Day,Ticker,Open,High,Low,Close) 
            VALUES(?,?,?,?,?,?,?)''',(int(z2)+i,Date(last_update - i),str(Sec[j]),Open(last_update - i),High(last_update - i),Low(last_update - i),Close(last_update - i)))
        
        print "Update complete"
    else:
        print str(Sec[j]) + " is up to date"
cur.commit()

cur.close()
conn.commit()
conn.close()

print("--- %s seconds ---" % (time.time() - start_time))