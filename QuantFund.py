# This script handles what should run, when it should run and with what starting parameters
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
# QFSec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD", "USD_CHF", "NZD_CHF",
#         "EUR_GBP", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", 
#         "AUD_CAD", "NZD_CAD", "AUD_NZD", "EUR_CHF", "GBP_CHF", "CAD_CHF", "AUD_CHF"]
QFPort = [229783, 406207, 836663]
QFVol = 100

main_log = "QF.txt"
fl_strat1 = "PPB_Log.txt" 
fl_strat2 = "MAC_Log.txt"
fl_strat3 = "IT_Log.txt"

dt_Main_Report = Get_dt("MainReport")
dt_PPB = Get_dt("dt_PPB")
dt_IT = Get_dt("dt_IT")
dt_MAC = Get_dt("dt_MAC")
dt_PivPts = Get_dt("dt_PivPts")
dt_PPB_Optimizer = dt_PPB - timedelta(minutes=1)
dt_IT_Optimizer = dt_IT - timedelta(minutes=1)

Intraday_PPB_tf = ["M5", "M15", "D"]
UpdatePivotPoints(QFSec)
LoadIndicators(QFSec,"M5")
LoadIndicators(QFSec,"M15")

# PA = PriceAction(QFSec)
# MM = MoneyManagement(QFSec)
while True:
    d = datetime.now()
    ###############################################################################
    #                                QF - Day Trade                               #
    ###############################################################################
    if datetime.now() > dt_PPB:
        SaveToLog(main_log, "Running PPB")
        PivotPointBreakout(QFPort[0], QFSec, QFVol, Intraday_PPB_tf, fl_strat1)
        SaveToLog(main_log, "Intraday_PPB complete")
        dt_PPB += timedelta(minutes=5)
        dt_PPB = dt_PPB.replace(second=1, microsecond=1)
    if datetime.now() > dt_IT:
        SaveToLog(main_log, "Running IntraTrend")
        IntraTrend(QFPort[1], QFSec, QFVol, "M15", fl_strat3)
        SaveToLog(main_log, "IntraTrend complete")
        dt_IT += timedelta(minutes=15)
        dt_IT = dt_IT.replace(second=1, microsecond=1)
    ###############################################################################
    #                               QF - Swing Trade                              #
    ###############################################################################
    if datetime.now() > dt_MAC:
        SaveToLog(main_log, "Running MAC")
        MovingAverageContrarian(QFPort[2], QFSec, QFVol, "H4", fl_strat2)
        SaveToLog(main_log, "MAC complete")
        dt_MAC += timedelta(hours=4)
        dt_MAC = dt_MAC.replace(minute=0, second=1, microsecond=1)
    ###############################################################################
    #                                 Optimizer                                   #
    ###############################################################################
    if datetime.now() > dt_IT_Optimizer:
        t = datetime.now()
        UpdateOpenUnits(QFSec, QFPort[0], "PPB")
        UpdateOpenUnits(QFSec, QFPort[1], "IT")
        LoadIndicators(QFSec,"M5")
        LoadIndicators(QFSec,"M15")
        dt_IT_Optimizer += timedelta(minutes=15)
        dt_IT_Optimizer = dt_IT_Optimizer.replace(second=1, microsecond=1)
        SaveToLog(main_log, "IT Optimizer runtime: " + str(datetime.now() - t))
    elif datetime.now() > dt_PPB_Optimizer:
        t = datetime.now()
        UpdateOpenUnits(QFSec, QFPort[0], "PPB")
        LoadIndicators(QFSec,"M5")
        dt_PPB_Optimizer += timedelta(minutes=5)
        dt_PPB_Optimizer = dt_PPB_Optimizer.replace(second=1, microsecond=1)
        SaveToLog(main_log, "PPB Optimizer runtime: " + str(datetime.now() - t))
    if datetime.now() > dt_PivPts:
        UpdatePivotPoints(QFSec)
    if d.weekday() == 4 and d.hour == 20 and d.minute > 50:
        for i in range(len(QFSec)):
            ClosePositions(QFPort[0], QFSec[i], fl_strat1, LIVE_ACCESS_TOKEN)
            ClosePositions(QFPort[1], QFSec[i], fl_strat3, LIVE_ACCESS_TOKEN)
        time.sleep(3600)
    ###############################################################################
    #                                 Reporting                                   #
    ###############################################################################
    # if datetime.now() > dt_Main_Report:
    #     body = Report("DailyReport", QFPort[0], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0], "QF Report - " + str(QFPort[0]), body)
    #     body = Report("DailyReport", QFPort[1], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0]," QF Report - " + str(QFPort[1]), body)
    #     body = Report("DailyReport", QFPort[2], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0], "QF Report - " + str(QFPort[2]), body)
    #     dt_Main_Report += timedelta(hours=12)
    #     dt_Main_Report = dt_Main_Report.replace(minute=0, second=1, microsecond=1)
    time.sleep(1)