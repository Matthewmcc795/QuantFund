import pypyodbc
import requests
import json
from array import *

last_update = 0
Sec = []
URL = []
Str_SQL1 = []
Str_SQL2 = [] 

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

cur.execute("SELECT [URL_U] FROM Connections")
results = cur.fetchall()
for i in range(0,70):
	x1 = str(results[i])
	y2 = x1[3:]
	z2 = y2[:len(y2)-3]
	URL.append(z2)
	print z2

cur.execute("SELECT [Str_SQL1] FROM Connections")
results = cur.fetchall()
for i in range(0,70):
	x1 = str(results[i])
	y2 = x1[3:]
	z2 = y2[:len(y2)-3]
	Str_SQL1.append(z2)
	print z2

cur.execute("SELECT [Str_SQL2] FROM Connections")
results = cur.fetchall()
for i in range(0,70):
	x1 = str(results[i])
	y2 = x1[3:]
	z2 = y2[:len(y2)-3]
	Str_SQL2.append(z2)
	print z2
cur.close()
conn.commit()
conn.close()