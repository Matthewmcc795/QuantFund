import pypyodbc
import requests
import time
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  

cur = conn.cursor()

cur.execute("DELETE * FROM D_Price")
cur.commit
cur.execute("DELETE * FROM H4_Price")
cur.commit
cur.execute("DELETE * FROM H1_Price")
cur.commit
cur.execute("DELETE * FROM M5_Price")
cur.commit

cur.close()
conn.commit()
conn.close()