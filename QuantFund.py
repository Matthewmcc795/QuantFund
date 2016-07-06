# This script handles what should run, when it should run and with what starting parameters
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
from QF_Strategy import *
from QF_Functions import *
from QF_Optimizer import *
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD", "USD_CHF", "NZD_CHF",
        "EUR_GBP", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", 
        "AUD_CAD", "NZD_CAD", "AUD_NZD", "EUR_CHF", "GBP_CHF", "CAD_CHF", "AUD_CHF"]

cs_sec = ["EUR_USD", "GBP_USD", "EUR_GBP", "EUR_CAD", "EUR_AUD", "EUR_NZD", "GBP_CAD", "GBP_AUD", "GBP_NZD", "EUR_CHF", "GBP_CHF"]

account_id = 229783
account_id2 = 406207
account_id3 = 836663
# account_id4 = 167051
# account_id5 = 306386
# account_id6 = 816622
cs_vol = 1500
qf_vol = 100
main_log = "QF.txt"
fl_strat1 = "Day_Trade_Log.txt" 
fl_strat2 = "Swing_Trade_Log.txt"
fl_strat3 = "CableSnap_Log.txt"
# fl_strat1 = "PPBreakout_Log2.txt" 
# fl_strat2 = "MAC_Log.txt"
# fl_strat3 = "BusRide_Log.txt"
# fl_strat4 = "IntraTrend_Log.txt"
# fl_strat5 = "CableSnap_Log.txt"
# fl_strat5 = "CableSnap_Log2.txt"

dt_Intraday_PPB = Get_dt("dt_Intraday_PPB")
dt_Intraday_MAC = Get_dt("dt_Intraday_MAC")
dt_Intraday_BusRide = Get_dt("dt_Intraday_BusRide")
dt_Intraday_IntraTrend = Get_dt("dt_Intraday_IntraTrend")
dt_Swing_PPB = Get_dt("dt_Swing_PPB")
dt_Swing_MAC = Get_dt("dt_Swing_MAC")
dt_Swing_BusRide = Get_dt("dt_Swing_BusRide")
dt_Swing_IntraTrendD = Get_dt("dt_Swing_IntraTrendD")
dt_Swing_IntraTrendW = Get_dt("dt_Swing_IntraTrendW")
dt_Intraday_CableSnap = Get_dt("dt_Intraday_CableSnap")
dt_Swing_CableSnap = Get_dt("dt_Swing_CableSnap")

while True:
    ###############################################################################
    #                                QF - Day Trade                               #
    ###############################################################################
    if datetime.now() > dt_Intraday_PPB:
        SaveToLog(main_log, "Running Intraday_PPB")
        PivotPointBreakout(account_id, Sec, qf_vol, ["M5", "M15", "D"], fl_strat1)
        SaveToLog(main_log, "Intraday_PPB complete")
        dt_Intraday_PPB += timedelta(minutes=5)
        dt_Intraday_PPB = dt_Intraday_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_MAC:
        SaveToLog(main_log, "Running Intraday_MAC")
        MovingAverageContrarian(account_id, Sec, "M15" ,qf_vol, fl_strat1)
        SaveToLog(main_log, "Intraday_MAC complete")
        dt_Intraday_MAC += timedelta(minutes=15)
        dt_Intraday_MAC = dt_Intraday_MAC.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_BusRide:
        SaveToLog(main_log, "Running Intraday_BusRide")
        BusRide(account_id, Sec, qf_vol, "M15", fl_strat1)
        SaveToLog(main_log, "Intraday_BusRide complete")
        dt_Intraday_BusRide += timedelta(hours=24)
        dt_Intraday_BusRide = dt_BusRide.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Intraday_IntraTrend:
        SaveToLog(main_log, "Running Intraday_IntraTrend")
        IntraTrend(account_id, Sec, qf_vol, "M15", fl_strat1)
        SaveToLog(main_log, "Intraday_IntraTrend complete")
        dt_Intraday_IntraTrend += timedelta(minutes=15)
        dt_Intraday_IntraTrend = dt_Intraday_IntraTrend.replace(second=1, microsecond=1)
    ###############################################################################
    #                               QF - Swing Trade                              #
    ###############################################################################
    if datetime.now() > dt_Swing_PPB:
        SaveToLog(main_log, "Running Swing_PPB")
        PivotPointBreakout(account_id2, Sec, qf_vol, ["D", "D", "W"], fl_strat2)
        SaveToLog(main_log, "Swing_PPB complete")
        dt_Swing_PPB += timedelta(minutes=5)
        dt_Swing_PPB = dt_Swing_PPB.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Swing_MAC:
        SaveToLog(main_log, "Running Swing_MAC")
        MovingAverageContrarian(account_id2, Sec, qf_vol, "H4", fl_strat2)
        SaveToLog(main_log, "Swing_MAC complete")
        dt_Swing_MAC += timedelta(hours=4)
        dt_Swing_MAC = dt_Swing_MAC.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Swing_BusRide:
        SaveToLog(main_log, "Running Swing_BusRide")
        BusRide(account_id2, Sec, qf_vol, "D", fl_strat2)
        SaveToLog(main_log, "Swing_BusRide complete")
        dt_Swing_BusRide += timedelta(hours=24)
        dt_Swing_BusRide = dt_Swing_BusRide.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Swing_IntraTrendD:
        SaveToLog(main_log, "Running Swing_IntraTrendD")
        IntraTrend(account_id2, Sec, qf_vol, "D", fl_strat2)
        SaveToLog(main_log, "Swing_IntraTrendD complete")
        dt_Swing_IntraTrendD += timedelta(hours=24)
        dt_Swing_IntraTrendD = dt_Swing_IntraTrendD.replace(minute=0, second=1, microsecond=1)
    elif datetime.now() > dt_Swing_IntraTrendW:
        SaveToLog(main_log, "Running Swing_IntraTrendW")
        IntraTrend(account_id2, Sec, qf_vol, "W", fl_strat2)
        SaveToLog(main_log, "Swing_IntraTrendW complete")
        dt_Swing_IntraTrendW += timedelta(hours=168)
        dt_Swing_IntraTrendW = dt_Swing_IntraTrendW.replace(minute=0, second=1, microsecond=1)
    ###############################################################################
    #                            Ultra Short GBP EUR                              #
    ###############################################################################
    if datetime.now() > dt_Intraday_CableSnap:
        SaveToLog(main_log, "Running Intraday_CableSnap")
        CableSnap(account_id3, cs_sec, cs_vol, "M15", fl_strat3)
        SaveToLog(main_log, "Intraday_CableSnap complete")
        dt_Intraday_CableSnap += timedelta(minutes=15)
        dt_Intraday_CableSnap = dt_Intraday_CableSnap.replace(second=1, microsecond=1)
    elif datetime.now() > dt_Swing_CableSnap:
        SaveToLog(main_log, "Running Swing_CableSnap")
        CableSnap(account_id3, cs_sec, cs_vol/6, "D", fl_strat3)
        SaveToLog(main_log, "Swing_CableSnap complete")
        dt_Swing_CableSnap += timedelta(hours=24)
        dt_Swing_CableSnap = dt_Swing_CableSnap.replace(minute=0, second=1, microsecond=1)
    time.sleep(1)