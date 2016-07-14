# This script handles what should run, when it should run and with what starting parameters
import requests
import json
from array import *
from Settings import CSTokens, LIVE_ACCESS_TOKEN, MAIL, NREPORT, MREPORT, PWD
from QF_Strategy import *
from QF_Functions import *
from QF_Optimizer import *
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

QFSec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD", "USD_CHF", "NZD_CHF",
        "EUR_GBP", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", 
        "AUD_CAD", "NZD_CAD", "AUD_NZD", "EUR_CHF", "GBP_CHF", "CAD_CHF", "AUD_CHF"]
QFPort = [229783, 406207]
QFVol = 100

CSSec = ["EUR_USD", "GBP_USD", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", "EUR_CHF", "GBP_CHF"]
BanzaiSec = ["GBP_JPY", "AUD_JPY", "USD_JPY"]
CSPort = [836663, 581757]
CSVol = [1000, 500]

main_log = "QF.txt"
fl_strat1 = "Day_Trade_Log.txt" 
fl_strat2 = "Swing_Trade_Log.txt"
fl_strat3 = "CableSnap_Log.txt"

dt_report = Get_dt("DailyReport")
dt_report = datetime.now()
dt_Intraday_PPB = Get_dt("dt_Intraday_PPB")
dt_Intraday_MAC = Get_dt("dt_Intraday_MAC")
dt_Intraday_BusRide = Get_dt("dt_Intraday_BusRide")
dt_Intraday_IntraTrend = Get_dt("dt_Intraday_IntraTrend")
dt_Swing_PPB = Get_dt("dt_Swing_PPB")
dt_Swing_MAC = Get_dt("dt_Swing_MAC")
dt_Swing_BusRide = Get_dt("dt_Swing_BusRide")
dt_Swing_IntraTrendD = Get_dt("dt_Swing_IntraTrendD")
# dt_Swing_IntraTrendW = Get_dt("dt_Swing_IntraTrendW")
dt_Intraday_CableSnap = Get_dt("dt_Intraday_CableSnap")
dt_Intraday_Banzai = Get_dt("dt_Intraday_Banzai")
# dt_Swing_CableSnap = Get_dt("dt_Swing_CableSnap")
Intraday_PPB_tf = ["M5", "M15", "D"]
Swing_PPB_tf = ["D", "D", "W"]

while True:
    ###############################################################################
    #                                QF - Day Trade                               #
    ###############################################################################
    if datetime.now() > dt_Intraday_PPB:
        SaveToLog(main_log, "Running Intraday_PPB")
        PivotPointBreakout(QFPort[0], QFSec, QFVol, Intraday_PPB_tf, fl_strat1)
        SaveToLog(main_log, "Intraday_PPB complete")
        dt_Intraday_PPB += timedelta(minutes=5)
        dt_Intraday_PPB = dt_Intraday_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_MAC:
        SaveToLog(main_log, "Running Intraday_MAC")
        MovingAverageContrarian(QFPort[0], QFSec, QFVol, "M15", fl_strat1)
        SaveToLog(main_log, "Intraday_MAC complete")
        dt_Intraday_MAC += timedelta(minutes=15)
        dt_Intraday_MAC = dt_Intraday_MAC.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_BusRide:
        SaveToLog(main_log, "Running Intraday_BusRide")
        BusRide(QFPort[0], QFSec, QFVol, "M15", fl_strat1)
        SaveToLog(main_log, "Intraday_BusRide complete")
        dt_Intraday_BusRide += timedelta(hours=24)
        dt_Intraday_BusRide = dt_Intraday_BusRide.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_IntraTrend:
        SaveToLog(main_log, "Running Intraday_IntraTrend")
        IntraTrend(QFPort[0], QFSec, QFVol, "M15", fl_strat1)
        SaveToLog(main_log, "Intraday_IntraTrend complete")
        dt_Intraday_IntraTrend += timedelta(minutes=15)
        dt_Intraday_IntraTrend = dt_Intraday_IntraTrend.replace(second=1, microsecond=1)
    ###############################################################################
    #                               QF - Swing Trade                              #
    ###############################################################################
    if datetime.now() > dt_Swing_PPB:
        SaveToLog(main_log, "Running Swing_PPB")
        PivotPointBreakout(QFPort[1], QFSec, QFVol, Swing_PPB_tf, fl_strat2)
        SaveToLog(main_log, "Swing_PPB complete")
        dt_Swing_PPB += timedelta(minutes=5)
        dt_Swing_PPB = dt_Swing_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Swing_MAC:
        SaveToLog(main_log, "Running Swing_MAC")
        MovingAverageContrarian(QFPort[1], QFSec, QFVol, "H4", fl_strat2)
        SaveToLog(main_log, "Swing_MAC complete")
        dt_Swing_MAC += timedelta(hours=4)
        dt_Swing_MAC = dt_Swing_MAC.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Swing_BusRide:
        SaveToLog(main_log, "Running Swing_BusRide")
        BusRide(QFPort[1], QFSec, QFVol, "D", fl_strat2)
        SaveToLog(main_log, "Swing_BusRide complete")
        dt_Swing_BusRide += timedelta(hours=24)
        dt_Swing_BusRide = dt_Swing_BusRide.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Swing_IntraTrendD:
        SaveToLog(main_log, "Running Swing_IntraTrendD")
        IntraTrend(QFPort[1], QFSec, QFVol, "D", fl_strat2)
        SaveToLog(main_log, "Swing_IntraTrendD complete")
        dt_Swing_IntraTrendD += timedelta(hours=24)
        dt_Swing_IntraTrendD = dt_Swing_IntraTrendD.replace(minute=0, second=1, microsecond=1)
    ###############################################################################
    #                            Ultra Short GBP EUR                              #
    ###############################################################################
    if datetime.now() > dt_Intraday_CableSnap:
        SaveToLog(main_log, "Running Intraday_CableSnap")
        CableSnap(CSPort, CSSec, CSVol, "M15", fl_strat3, CSTokens)
        SaveToLog(main_log, "Intraday_CableSnap complete")
        dt_Intraday_CableSnap += timedelta(minutes=15)
        dt_Intraday_CableSnap = dt_Intraday_CableSnap.replace(second=1, microsecond=1)
    ###############################################################################
    #                                Buy USD/JPY                                  #
    ###############################################################################
    if datetime.now() > dt_Intraday_Banzai:
        SaveToLog(main_log, "Running Intraday_Banzai")
        Banzai(CSPort, BanzaiSec, CSVol, "M15", fl_strat3, CSTokens)
        SaveToLog(main_log, "Intraday_Banzai complete")
        dt_Intraday_Banzai += timedelta(minutes=15)
        dt_Intraday_Banzai = dt_Intraday_Banzai.replace(second=1, microsecond=1)
    ###############################################################################
    #                            Optimizer/Reporting                              #
    ###############################################################################
    # if datetime.now() > dt_report:
    #     body = Report("DailyReport", QFPort[0], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0], "Daily Quant Fund Report - " + str(QFPort[0]), body)
    #     body = Report("DailyReport", QFPort[1], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0], "Daily Quant Fund Report - " + str(QFPort[1]), body)
    #     body = Report("DailyReport", CSPort[0], LIVE_ACCESS_TOKEN)
    #     SendEmail(MAIL[0], PWD, MAIL[0], "Daily CableSnap/Banzai Report - " + str(CSPort[0]), body)
    #     body = Report("DailyReport", CSPort[1], CSTokens[1])
    #     SendEmail(MAIL[0], PWD, NREPORT[0], "Daily Report - " + str(CSPort[1]), body)
    #     SendEmail(MAIL[0], PWD, NREPORT[1], "Daily Report - " + str(CSPort[1]), body)
    #     dt_report += timedelta(hours=24)
    #     dt_report = dt_report.replace(minute=0, second=1, microsecond=1)
    time.sleep(1)