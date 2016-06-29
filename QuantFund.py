# This script handles what should run, when it should run and with what starting parameters
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
from QF_Strategy import *
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]
hr = [2,6,10,14,18,22]
dt_PPB =  datetime.now()
dt_PPB = dt_PPB.replace(minute=2, second=0,microsecond=1)
while dt_PPB < datetime.now():
    dt_PPB += timedelta(minutes=5)

dt_MAC =  datetime.now()
dt_MAC = dt_MAC.replace(minute=3, second=0,microsecond=1)
while not dt_MAC.hour in hr:
    dt_MAC += timedelta(hours=1)

dt_BusRide =  datetime.now()
dt_BusRide = dt_BusRide.replace(minute=2, second=0,microsecond=1)
while dt_BusRide.hour != 21:
    dt_BusRide += timedelta(hours=1)

dt_IntraTrend =  datetime.now()
dt_IntraTrend = dt_IntraTrend.replace(minute=2, second=0,microsecond=1)
while dt_IntraTrend < datetime.now():
    dt_IntraTrend += timedelta(minutes=15)

account_id = 229783
account_id2 = 406207
account_id3 = 836663
account_id4 = 167051
main_log = "QF.txt"
fl_strat1 = "PPBreakout_Log2.txt" 
fl_strat2 = "MAC_Log.txt"
fl_strat3 = "BusRide_Log.txt"
fl_strat4 = "IntraTrend_Log.txt"
first_run = True

while True:
    if datetime.now() > dt_PPB:
        file = open(main_log,'a')
        file.write("Running PPB " + str(datetime.now()) +"\n")
        file.close()
        PivotPointBreakout(account_id, Sec, 100, fl_strat1)
        file = open(main_log,'a')
        file.write("PPB complete " + str(datetime.now()) +"\n")
        file.close()
        dt_PPB += timedelta(minutes=5)
        dt_PPB = dt_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_MAC:
        file = open(main_log,'a')
        file.write("Running MAC " + str(datetime.now()) +"\n")
        file.close()
        MovingAverageContrarian(account_id2, Sec, 100, fl_strat2)
        file = open(main_log,'a')
        file.write("MAC complete " + str(datetime.now()) +"\n")
        file.close()
        dt_MAC += timedelta(hours=4)
        dt_MAC = dt_MAC.replace(minute=1, second=1, microsecond=1)
    elif datetime.now() > dt_BusRide:
        file = open(main_log,'a')
        file.write("Running BusRide " + str(datetime.now()) +"\n")
        file.close()
        BusRide(account_id3, Sec, 100, fl_strat3)
        file = open(main_log,'a')
        file.write("BusRide complete " + str(datetime.now()) +"\n")
        file.close()
        dt_BusRide += timedelta(hours=24)
        dt_BusRide = dt_BusRide.replace(minute=2, second=0, microsecond=1)
    if datetime.now() > dt_IntraTrend:
        file = open(main_log,'a')
        file.write("Running IntraTrend " + str(datetime.now()) +"\n")
        file.close()
        IntraTrend(account_id4, Sec, 100, fl_strat4)
        file = open(main_log,'a')
        file.write("IntraTrend complete " + str(datetime.now()) +"\n")
        file.close()
        dt_IntraTrend += timedelta(minutes=15)
        dt_IntraTrend = dt_IntraTrend.replace(second=3, microsecond=1)
    time.sleep(1)