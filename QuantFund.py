# This script handles what should run, when it should run and with what starting parameters
import requests
import json
from array import *
from Settings import CSTokens, LIVE_ACCESS_TOKEN
from QF_Strategy import *
from QF_Functions import *
# from QF_Optimizer import *
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
dt_Intraday_PPB = Get_dt("dt_Intraday_PPB")
dt_Intraday_IntraTrend = Get_dt("dt_Intraday_IntraTrend")
dt_Swing_MAC = Get_dt("dt_Swing_MAC")
Intraday_PPB_tf = ["M5", "M15", "D"]

while True:
    d = datetime.now()
    ###############################################################################
    #                                QF - Day Trade                               #
    ###############################################################################
    if datetime.now() > dt_Intraday_PPB:
        SaveToLog(main_log, "Running Intraday_PPB")
        PivotPointBreakout(QFPort[0], QFSec, QFVol, Intraday_PPB_tf, fl_strat1)
        SaveToLog(main_log, "Intraday_PPB complete")
        dt_Intraday_PPB += timedelta(minutes=5)
        dt_Intraday_PPB = dt_Intraday_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_IntraTrend:
        SaveToLog(main_log, "Running Intraday_IntraTrend")
        IntraTrend(QFPort[1], QFSec, QFVol, "M15", fl_strat3)
        SaveToLog(main_log, "Intraday_IntraTrend complete")
        dt_Intraday_IntraTrend += timedelta(minutes=15)
        dt_Intraday_IntraTrend = dt_Intraday_IntraTrend.replace(second=1, microsecond=1)
    ###############################################################################
    #                               QF - Swing Trade                              #
    ###############################################################################
    if datetime.now() > dt_Swing_MAC:
        SaveToLog(main_log, "Running Swing_MAC")
        MovingAverageContrarian(QFPort[2], QFSec, QFVol, "H4", fl_strat2)
        SaveToLog(main_log, "Swing_MAC complete")
        dt_Swing_MAC += timedelta(hours=4)
        dt_Swing_MAC = dt_Swing_MAC.replace(minute=0, second=1, microsecond=1)
    ###############################################################################
    #                                 Optimizer                                   #
    ###############################################################################
    if d.weekday() == 4 and d.hour == 8 and d.minute > 50:
        for i in range(len(sec)):
            ClosePositions(QFPort[0], sec[i], fl_strat1, LIVE_ACCESS_TOKEN)
            ClosePositions(QFPort[1], sec[i], fl_strat3, LIVE_ACCESS_TOKEN)
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