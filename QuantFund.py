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
dt_PPB += timedelta(hours=1)

dt_MAC =  datetime.now()
dt_MAC = dt_MAC.replace(minute=3, second=0,microsecond=1)
while not dt_MAC.hour in hr:
    dt_MAC += timedelta(hours=1)

dt_BusRide =  datetime.now()
dt_BusRide = dt_BusRide.replace(minute=2, second=0,microsecond=1)
while dt_BusRide.hour != 21
    dt_BusRide += timedelta(hours=1)

account_id = 229783
account_id2 = 406207
account_id3 = 4
name_strat1 = "PPBreakout_Log2.txt" 
name_strat2 = "MAC_Log.txt"
name_strat3 = "BusRide_Log.txt"
first_run = True

while True:
    if datetime.now() > dt_PPB:
    	PivotPointBreakout(account_id, Sec, 200)
	    dt_PPB += timedelta(minutes=5)
	    dt_PPB = dt_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_MAC:
    	MovingAverageContrarian(account_id2, Sec, 100)
        dt_MAC += timedelta(hours=4)
        dt_MAC = dt_MAC.replace(minute=1, second=1, microsecosnd=1)
    elif datetime.now() > dt_BusRide:
			BusRide(account_id3, Sec, 100)
		dt_BusRide += timedelta(hours=24)
		dt_BusRide = dt_BusRide.replace(minute=2, second=0, microsecond=1)
    time.sleep(1)