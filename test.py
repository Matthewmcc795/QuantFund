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

ticker = "USD_JPY"
st = "2014-06-01"
en = "2015-03-01"
tf1 = "D"
c = pClose(ticker, tf1, st,  en)
plt.plot(c, label=str(ticker))
plt.legend(bbox_to_anchor=(1.5, 1), loc='upper left', borderaxespad=0.)
plt.ylim(min(c)/1.005, max(c)*1.005)
plt.show()
