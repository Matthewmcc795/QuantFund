import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# mu, sigma = 100, 15
# x = mu + sigma*np.random.randn(10000)

# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins)
# # the histogram of the data
# n, bins, patches = plt.hist(x, 5, normed=1, facecolor='green', alpha=0.75)


# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
# plt.grid(True)

# plt.show()

hr = [0,4,8,12,16,20]

dt =  datetime.now()
dt = dt.replace(minute=2, second=0,microsecond=1)
while not dt.hour in hr:
	print dt.hour
	dt = dt + timedelta(hours=1)
print dt.hour

# h = {'Authorization' : DEMO_ACCESS_TOKEN}
# url = "https://api-fxpractice.oanda.com/v1/candles?instrument=EUR_USD&start=2016-04-21T13%3A35%3A00Z&end=2016-04-21T14%3A50%3A00Z&granularity=M5"
# r = requests.get(url, headers=h)     
# data = json.loads(r.text)
# # print data
# iterable = (x["closeBid"] for x in data["candles"])
# a = np.fromiter(iterable, np.float, count=-1)

# plt.plot(np.array(a))
# plt.ylim(1.12,1.14)
# plt.show()



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
# # 		file.write("Forecast: " + str(dat_Fila[i][5]) + "\n" + "\n")

# # file.close()
# Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]
# for i in range(0,5):
# #     h = {'Authorization' : LIVE_ACCESS_TOKEN}
# #     url = "https://api-fxtrade.oanda.com/v1/accounts/229783/positions"
# #     r = requests.get(url, headers=h)     
# #     data2 = json.loads(r.text)
# #     chk = str(data2)
# #     if chk.find("instrument") == -1:
# #         Open_Units = 0 
# #     else:
# #         Open_Units = 0
# #         for positions in data2["positions"]:
# #             print positions
# #             if positions["instrument"] == Sec[i]:
# #                 print positions["instrument"]
# #                 Open_Units = positions["units"]
# #                 print positions["units"]
#     h = {'Authorization' : LIVE_ACCESS_TOKEN}
#     url = "https://api-fxtrade.oanda.com/v1/accounts/229783/trades?instrument=" + str(Sec[i])
#     r = requests.get(url, headers=h)     
#     data2 = json.loads(r.text)
#     chk = str(data2)
#     print chk
#     print chk.find("id")
#     if chk.find("id") != -1:
#         for positions in data2["trades"]:
#             print positions
#             trd_ID = positions["id"]
#             trd_entry = positions["price"]
#             trd_side = positions["side"]
#             print trd_ID
#             print trd_entry
#             print trd_side


# # from datetime import datetime, timedelta
# # dt =  datetime.now()
# # dt = dt.replace(minute=2, second=0,microsecond=1)
# # dt = dt + timedelta(hours=1)
# # print dt
# # d_t = "March 9 16 6:02"

# # print d_t
# # dt = datetime.strptime(d_t, '%B %d %y %H:%M')
# # print dt

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