import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import numpy as np
import pypyodbc
import matplotlib.pyplot as plt
from Backtest_Objects import *
import pandas as pd
from matplotlib.finance import candlestick2_ochl
import matplotlib.mlab as mlab
import smtplib

account_id = 229783
h = {'Authorization' : LIVE_ACCESS_TOKEN}
url =   "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/alltransactions"
r = requests.get(url, headers=h)
print r.headers["Location"]
