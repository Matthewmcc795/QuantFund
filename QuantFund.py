import requests
import json
from array import *
from Settings import CSTokens, LIVE_ACCESS_TOKEN
from QF_Strategy import *
from QF_Functions import *
from QF_Optimizer import *
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

QFSec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]

QFMACSec = ["GBP_USD", "EUR_CAD", "GBP_AUD", "GBP_NZD", "GBP_CAD", "EUR_GBP", "AUD_CAD"]
# QFSec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD", "USD_CHF", "NZD_CHF",
#         "EUR_GBP", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", 
#         "AUD_CAD", "NZD_CAD", "AUD_NZD", "EUR_CHF", "GBP_CHF", "CAD_CHF", "AUD_CHF"]
QFPort = [229783, 406207, 836663, 167051, 306386, 816622]
QFTraget = [1.0, 1.0, 1.0]
QFLimit = [1.0, 1.0, 1.0]
QFVol = 100
QFBBBVol = 500
QFMACVol = 1000
# Strat["PPB"]["Vol"] = 100
# Strat["IT"]["Vol"] = 100


TOD_Params = {}
TOD_Params['AUD_NZD'] = {'Buy': [5], 'Sell': [13]}
TOD_Params['GBP_AUD'] = {'Buy': [7], 'Sell': [6, 12, 18]}
TOD_Params['AUD_CAD'] = {'Buy': [4, 23], 'Sell': [13, 20]}
TOD_Params['EUR_CAD'] = {'Buy': [13, 23], 'Sell': [10]}
TOD_Params['EUR_NZD'] = {'Buy': [3], 'Sell': [5, 15]}
TOD_Params['EUR_GBP'] = {'Buy': [2, 5, 18, 22], 'Sell': []}
TOD_Params['GBP_USD'] = {'Buy': [2, 15], 'Sell': [6, 10]}
TOD_Params['AUD_USD'] = {'Buy': [1, 4, 17], 'Sell': [14, 20]}
TOD_Params['EUR_USD'] = {'Buy': [1, 15], 'Sell': [10]}
TOD_Params['USD_CAD'] = {'Buy': [], 'Sell': [2, 17]}
TOD_Params['GBP_NZD'] = {'Buy': [], 'Sell': [4, 10, 23]}
TOD_Params['NZD_USD'] = {'Buy': [4, 14, 19], 'Sell': [10]}
TOD_Params['GBP_CAD'] = {'Buy': [8], 'Sell': [6, 11, 18, 21]}
TOD_Params['EUR_AUD'] = {'Buy': [13, 20], 'Sell': [1, 10]}
TOD_Params['NZD_CAD'] = {'Buy': [4, 8, 23], 'Sell': []}
TOD_Sec = TOD_Params.keys()

main_log = "QF.txt"
# fl_strat1 = "PPB_Log.txt" 
# fl_strat2 = "MAC_Log.txt"
# fl_strat3 = "IT_Log.txt"
fl_strat4 = "TOD_Log.txt"

# dt_Main_Report = Get_dt("MainReport")
dt_PPB = Get_dt("dt_PPB")
dt_IT = Get_dt("dt_IT")
# dt_BBB1 = Get_dt("dt_MAC")
# dt_BBB2 = Get_dt("dt_MAC")
# dt_BBB3 = Get_dt("dt_MAC")
# dt_MAC = Get_dt("dt_MAC")
d = datetime.now()
dt_TOD = Get_dt("dt_TOD")

df_TOD = datetime.now()

dt_TOD = df_TOD.replace(minute=0, second=0,microsecond=1) + timedelta(hours=1)
        # dt_TOD += timedelta(hours=1)
        # dt_TOD = dt_TOD.replace(minute=0, second=1, microsecond=1)

dt_Daily = Get_dt("dt_Daily")
dt_SessionPrep = Get_dt("dt_SessionPrep")
dt_M5_Optimizer = dt_PPB - timedelta(minutes=1)
dt_M15_Optimizer = dt_IT - timedelta(minutes=1)

Intraday_PPB_tf = ["M5", "M15", "D"]
UpdatePivotPoints(QFSec)
LoadIndicators(QFSec,"M5")
LoadIndicators(QFSec,"M15")
UpdateAccountBalance(QFPort[1], "PPB")
UpdateAccountBalance(QFPort[2], "IT")

# print Strat["PPB"]["InitialBalance"]
# print Strat["IT"]["InitialBalance"]
# PA = PriceAction(QFSec)
# MM = MoneyManagement(QFSec)
while True:
    d = datetime.now()
    ###############################################################################
    #                                QF - Day Trade                               #
    ###############################################################################
    # if datetime.now() > dt_PPB:
    #     SaveToLog(main_log, "Running PPB")
    #     PivotPointBreakout(QFPort[1], QFSec, QFVol, Intraday_PPB_tf, fl_strat1)
    #     SaveToLog(main_log, "Intraday_PPB complete")
    #     dt_PPB += timedelta(minutes=5)
    #     dt_PPB = dt_PPB.replace(second=0, microsecond=1)
    # if datetime.now() > dt_IT:
    #     SaveToLog(main_log, "Running IntraTrend")
    #     IntraTrend(QFPort[2], QFSec, QFVol, "M15", fl_strat3)
    #     SaveToLog(main_log, "IntraTrend complete")
    #     dt_IT += timedelta(minutes=15)
    #     dt_IT = dt_IT.replace(second=0, microsecond=1)
    ###############################################################################
    #                               QF - Swing Trade                              #
    ###############################################################################
    # if datetime.now() > dt_MAC:
    #     SaveToLog(main_log, "Running MAC")
    #     MovingAverageContrarian(QFPort[0], QFMACSec, QFMACVol, "H4", fl_strat2)
    #     SaveToLog(main_log, "MAC complete")
    #     dt_MAC += timedelta(hours=4)
    #     dt_MAC = dt_MAC.replace(minute=0, second=1, microsecond=1)
    # if datetime.now() > dt_BBB1:
    #     SaveToLog(main_log, "Running BBB 10")
    #     BollingerBandBreakout1(QFPort[2], QFSec, QFBBBVol, "H4", fl_strat3)
    #     SaveToLog(main_log, "Running BBB 10 complete")
    #     dt_BBB1 += timedelta(hours=4)
    #     dt_BBB1 = dt_BBB1.replace(minute=0, second=1, microsecond=1)
    # if datetime.now() > dt_BBB2:
    #     SaveToLog(main_log, "Running BBB 50")
    #     BollingerBandBreakout2(QFPort[3], QFSec, QFBBBVol, "H4", fl_strat3)
    #     SaveToLog(main_log, "Running BBB 50 complete")
    #     dt_BBB2 += timedelta(hours=4)
    #     dt_BBB2 = dt_BBB2.replace(minute=0, second=1, microsecond=1)
    # if datetime.now() > dt_BBB3:
    #     SaveToLog(main_log, "Running BBB 200")
    #     BollingerBandBreakout3(QFPort[4], QFSec, QFBBBVol, "H4", fl_strat3)
    #     SaveToLog(main_log, "Running BBB 200 complete")
    #     dt_BBB3 += timedelta(hours=4)
    #     dt_BBB3 = dt_BBB3.replace(minute=0, second=1, microsecond=1)
    if datetime.now() > dt_TOD:
        SaveToLog(main_log, "Running TOD")
        TimeofDay(QFPort[4], TOD_Sec, 100, "H1", fl_strat4)
        SaveToLog(main_log, "Running BBB 200 complete")
        dt_TOD += timedelta(hours=1)
        dt_TOD = dt_TOD.replace(minute=0, second=1, microsecond=1)
    ###############################################################################
    #                                 Optimizer                                   #
    ###############################################################################
    if datetime.now() > dt_M15_Optimizer:
        SaveToLog(main_log, "Running M15 Optimizer")
        t = datetime.now()
        UpdateOpenUnits(QFSec, QFPort[1], "PPB")
        UpdateOpenUnits(QFSec, QFPort[2], "IT")
        LoadIndicators(QFSec,"M5")
        LoadIndicators(QFSec,"M15")
        ManageMoney(QFPort[1], "PPB", QFTraget[0], QFLimit[0])
        ManageMoney(QFPort[2], "IT", QFTraget[1], QFLimit[1])
        dt_M15_Optimizer += timedelta(minutes=15)
        dt_M15_Optimizer = dt_M15_Optimizer.replace(second=1, microsecond=1)
        SaveToLog(main_log, "M15 Optimizer runtime: " + str(datetime.now() - t))
    elif datetime.now() > dt_M5_Optimizer:
        SaveToLog(main_log, "Running PPB Optimizer")
        t = datetime.now()
        UpdateOpenUnits(QFSec, QFPort[1], "PPB")
        ManageMoney(QFPort[1], "PPB", QFTraget[0], QFLimit[0])
        LoadIndicators(QFSec,"M5")
        dt_M5_Optimizer += timedelta(minutes=5)
        dt_M5_Optimizer = dt_M5_Optimizer.replace(second=1, microsecond=1)
        SaveToLog(main_log, "M5 Optimizer runtime: " + str(datetime.now() - t))
    if datetime.now() > dt_Daily:
        SaveToLog(main_log, "Running Daily Updates")
        t = datetime.now()
        UpdatePivotPoints(QFSec)
        UpdateAccountBalance(QFPort[1], "PPB")
        UpdateAccountBalance(QFPort[2], "IT")
        dt_Daily += timedelta(hours=24)
        dt_Daily = dt_Daily.replace(minute=0, second=0, microsecond = 1)
        SaveToLog(main_log, "Daily Updates runtime: " + str(datetime.now() - t))
    if d.weekday() == 4 and d.hour == 16 and d.minute > 50:
        for i in range(len(QFSec)):
            ClosePositions(QFPort[0], QFSec[i], fl_strat1, LIVE_ACCESS_TOKEN)
            ClosePositions(QFPort[1], QFSec[i], fl_strat2, LIVE_ACCESS_TOKEN)
            ClosePositions(QFPort[2], QFSec[i], fl_strat3, LIVE_ACCESS_TOKEN)
        time.sleep(3600)
    time.sleep(1)