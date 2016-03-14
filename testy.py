import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import xml.etree.ElementTree as ET

# r = requests.get("http://www.forexfactory.com/ffcal_week_this.xml")
# root = ET.fromstring(r.text)
# dat_Fila = []
# for country in root.iter('event'):
# 	dat = []
# 	for t in country:
# 		dat.append(t.text)
# 	dat_Fila.append(dat)
# root = ""
# r = ""
# dat_Fila = []
# dat = []

# name = "report.txt"
# file = open(name,'a')
# file.write("|| ---------- EUR ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "EUR":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.write("\n" + "|| ---------- GBP ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "GBP":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.write("\n" + "|| ---------- CAD ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "CAD":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.write("\n" + "|| ---------- JPY ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "JPY":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.write("\n" + "|| ---------- AUD ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "AUD":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.write("\n" + "|| ---------- NZD ---------- || " + "\n" + "\n")
# for i in range(0,len(dat_Fila)-1):
# 	if dat_Fila[i][1] == "NZD":
# 		file.write(str(dat_Fila[i][0]) + " \n")
# 		file.write(str(dat_Fila[i][2]) + " - " + str(dat_Fila[i][3]) + " \n")
# 		file.write("Previous: " + str(dat_Fila[i][6]) + "\n")
# 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# file.close()

from datetime import datetime, timedelta
dt =  datetime.now()
dt = dt.replace(minute=2, second=0,microsecond=1)
dt = dt + timedelta(hours=1)
print dt
d_t = "March 9 16 6:02"

print d_t
dt = datetime.strptime(d_t, '%B %d %y %H:%M')
print dt

# import smtplib
# name = "PPBreakout_Log2.txt"
# fp = open(name, 'rb')
# msg = fp.read()
# fp.close()

# server = smtplib.SMTP('smtp.gmail.com:587')
# server.starttls()
# server.login(usr,pw)
# server.sendmail(email_fr, email_to, msg)
# server.quit()