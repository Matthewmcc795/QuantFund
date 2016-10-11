import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STROA, STRHA, STRLA, STRCA, STROB, STRHB, STRLB, STRCB, STRV, STRCO
import httplib
import urllib
from QF_Strategy import *
from QF_Functions import *
from datetime import datetime, timedelta
import time
import sys
main_log = "QF.txt"

# Fundamental equation to optimize is Z = p(Re) + (1-p)(Ri)
# What factors can we correlate to the probability of success, reward or risk
# At the point of decision, calculate Z and compare to your target Z
# Or, compare the factors, p, Re and Ri to your target p*, Re* and Ri*

# For version 2.0, allow your targets to be dynamic to the market. 

# This file will operate as a "researcher" going over historical trades and price data
# Goal is to find adjustments within reasonable limits to improve profitability or reduce risk
# Output will be some sort of array of data points or an designated text file that is wiped and rebuilt on every run
# The Strategy objects will then request that file or array to make the adjustments
# Output might be doubles ex: 2.35 which would be a multiplier for the volume, so do 2.35x the base line
# Output might be upper/lower bounds for parameters ex: 10 < SL < 15. 
# #### "In this environment keep the stops tight".
# Output might be pairwise ex: if situation 1 then vol = 2.5, if situation 2 then vol = 0.5 
# #### "situation 1 is favourable so go heavy, situation 2 is unfavourable so trade lighter"

# TBD:
# Should the Optimizer decide on the current state or should the Strategy? I think Optimizer for now
# Should the Optimizer return anything within the code or should it just update all the backend stuff?
# Maybe use dictionaries to handle the output for each strategy
# #### Ex: PPB["State 1"]["Volume"][sec[i]]
# #### Handling different states for a given strategy easier to handle
# #### Variability of different parameters for each strategy easier to handle
# #### Easier to search for data points than looping through a file or using setting up panda dataframes
# Should there be a different script to manage the overall fund? I think yes, for now
# #### Ex. Historically we lose at most 3 times in a day. We just lost 4 times, what should we do?
# #### Ex2. Money management
# #### Ex3. Trade management

# To figure out:
# What is the best way to extract past trades and trade results from Oanda?

# from QF_Functions import *
# from QF_Strategy import *

# 14/7/2016
# Explore the idea of having multiple methodologies that meet periodically to make decisions
# Idea came about as a result of thinking of HR planning for the rest of the fund
#     You could design jobs and then design scripts to accomplish the tasks/asmuchaspossible
#     Think of a fund with various roles than have morning meetings, sector and PM meetings
# My theory is that by looking through different lenses we can establish competing points of view
#     Then when we compile our findings we can gain better perspective
#     Example, 
#         Have a macro analyst have periodic M --> W --> D analysis of macro patterns
#         Have a day trader who can give daily feedback of how the market is responding
#         By comparing the findings we can better estimate probabilities, R:R
# This could create the structure that motivates various Optimizer functions
#     Similar to how QF_Strategy has the strategies that motivate the indicator order functions
# The ideas of an Eric and a compliance officer or a risk manager would be functions w/ names
#     This script is sort of our "Optimizer Department" 
#     In addition to our "Strategy Department" which handles all signals
#     We could then create a "Trader Department" that optimizes entries
#     As well as a "Manager Department" that gives oversight to risk, compliance, reporting etc. 
# Some departments could be consolidators.
#     Traders and Managers would sync up to the analysis of the Optimizer

##########################################################################################################
#                                                                                                        #
#                                              Optimizer                                                 #
#                                                                                                        #
##########################################################################################################

# class PriceAction:
#     def __init__(self, sec):
#         self.sec = sec 
#     def UpdatePrices(self, symbol):
#         self.DO, self.DH, self.DL, self.DC = Get_Price(symbol, "D", 2, "ohlc", "midpoint")
#         self.M15O, self.M15H, self.M15L, self.M15C = Get_Price(symbol, "M15", 101, "ohlc", "midpoint")
#     def RunAnalysis(self):
#         for i in range(len(self.sec)):
#             self.UpdatePrices(self.sec[i])
#             self.PivotPointAnalysis()
#             self.ZScoreAnalysis()
#             self.LoadIndicators()
#     def UpdatePivotPoints(self):
#         for i in range(len(self.sec)):
#             self.UpdatePrices(self.sec[i])
#             self.PP = [0,0,0,0,0]
#             self.PP[2] = round((self.DH[1] + self.DL[1] + self.DC[1])/3 +0.00001,5)
#             self.PP[0] = round(self.PP[2] - self.DH[1] + self.DL[1],5)
#             self.PP[1] = round(2*self.PP[2] - self.DH[1],5)
#             self.PP[3] = round(2*self.PP[2] - self.DL[1],5)
#             self.PP[4] = round(self.PP[2] + self.DH[1] - self.DL[1],5)
#             PP["R2"][self.symbol] = self.PP[4]
#             PP["R1"][self.symbol] = self.PP[3]
#             PP["PP"][self.symbol] = self.PP[2]
#             PP["S1"][self.symbol] = self.PP[1]
#             PP["S2"][self.symbol] = self.PP[0]
#     def PivotPointAnalysis(self):
#         for j in range(len(self.sec)):
#             self.PP[4] = PP["R2"][self.sec[j]]
#             self.PP[3] = PP["R1"][self.sec[j]]
#             self.PP[2] = PP["PP"][self.sec[j]]
#             self.PP[1] = PP["S1"][self.sec[j]]
#             self.PP[0] = PP["S2"][self.sec[j]]
#             self.Pos = [0]*100
#             for i in range(100): 
#                 if self.M15C[i] >= self.PP[4]:
#                     self.Pos[i] = 5
#                 elif self.M15C[i] >= self.PP[3] and self.M15C[i] < self.PP[4]:
#                     self.Pos[i] = 4
#                 elif self.M15C[i] >= self.PP[2] and self.M15C[i] < self.PP[3]
#                     self.Pos[i] = 3
#                 elif self.M15C[i] >= self.PP[1] and self.M15C[i] < self.PP[2]:
#                     self.Pos[i] = 2
#                 elif self.M15C[i] >= self.PP[0] and self.M15C[i] < self.PP[1]:
#                     self.Pos[i] = 1
#                 elif self.M15C[i] < self.PP[0]:
#                     self.Pos[i] = 0
#                 if self.Pos[offset] == 5:
#                     Indicators[self.sec[j]]["s"] =  PP["R2"][self.sec[j]]
#                     Indicators[self.sec[j]]["r"] = 2*self.M15C[0]
#                 elif self.Pos[offset] == 0:
#                     Indicators[self.sec[j]]["s"] =  0
#                     Indicators[self.sec[j]]["r"] = PP["S2"][self.sec[j]]
#                 else:
#                     Indicators[self.sec[j]]["s"] = self.PP[self.Pos[offset-1]]
#                     Indicators[self.sec[j]]["r"] = self.PP[self.Pos[offset]]
#     def ZScoreAnalysis(self):
#         self.SMA50 = [0]*100
#         self.SMA21 = [0]*100
#         self.SMA10 = [0]*100
#         self.SD50 = [0]*100
#         self.SD21 = [0]*100
#         self.SD10 = [0]*100
#         for i in range(100-50):
#             SMA50[100-50 - i] = SMA(self.M15C, 50, i)
#             SD50[100-50-i] = STDEV(self.M15C, 50, i)
#         for i in range(100-21):
#             SMA21[100-21 - i] = SMA(self.M15C, 21, i)
#             SD21[100-21-i] = STDEV(self.M15C, 21, i)
#         for i in range(100-10):
#             SMA10[100 -10 - i] = SMA(self.M15C, 10, i)
#             SD10[100-10-i] = STDEV(self.M15C, 10, i)
#         self.Z50 = [0]*100
#         self.Z21 = [0]*100
#         self.Z10 = [0]*100
#         for i in range(100-50):
#             Z50[100-50 - i] = (self.M15C[i] - self.SMA50[i])/self.SD50[i]
#         for i in range(100-21):
#             Z21[100-21-i] = (self.M15C[i] - self.SMA21[i])/self.SD21[i]
#         for i in range(100-10):
#             Z10[100-10-i] = (self.M15C[i] - self.SMA10[i])/self.SD10[i]   
#     def LoadIndicators(self):
#         Indicators[self.sec[i]]["ATR"] = Get_ATR(self.M15H, self.M15L, self.M15C, self.sec[i])

def UpdatePivotPoints(sec):
    for i in range(len(sec)):
        DH, DL, DC = Get_Price(sec[i], "D", 2, "hlc", "midpoint")
        Piv = [0,0,0,0,0]
        Piv[2] = round((DH[1] + DL[1] + DC[1])/3 +0.00001,5)
        Piv[0] = round(Piv[2] - DH[1] + DL[1],5)
        Piv[1] = round(2*Piv[2] - DH[1],5)
        Piv[3] = round(2*Piv[2] - DL[1],5)
        Piv[4] = round(Piv[2] + DH[1] - DL[1],5)
        PP["R2"][sec[i]] = Piv[4]
        PP["R1"][sec[i]] = Piv[3]
        PP["PP"][sec[i]] = Piv[2]
        PP["S1"][sec[i]] = Piv[1]
        PP["S2"][sec[i]] = Piv[0]

def LoadIndicators(sec, tf):
    for i in range(len(sec)):
        if tf == "M5":
            M5C = Get_Price(sec[i], "M5", 1, "c", "midpoint")
            Piv = [0,0,0,0,0]
            Piv[4] = PP["R2"][sec[i]]
            Piv[3] = PP["R1"][sec[i]]
            Piv[2] = PP["PP"][sec[i]]
            Piv[1] = PP["S1"][sec[i]]
            Piv[0] = PP["S2"][sec[i]]
            Pos = 0
            if M5C[0] >= Piv[4]:
                Pos = 5
            elif M5C[0] >= Piv[3] and M5C[0] < Piv[4]:
                Pos = 4
            elif M5C[0] >= Piv[2] and M5C[0] < Piv[3]:
                Pos = 3
            elif M5C[0] >= Piv[1] and M5C[0] < Piv[2]:
                Pos = 2
            elif M5C[0] >= Piv[0] and M5C[0] < Piv[1]:
                Pos = 1
            elif M5C[0] < Piv[0]:
                Pos = 0
            if Pos == 5:
                Indicators[sec[i]]["s"] =  PP["R2"][sec[i]]
                Indicators[sec[i]]["r"] = 2*M5C[0]
            elif Pos == 0:
                Indicators[sec[i]]["s"] =  0
                Indicators[sec[i]]["r"] = PP["S2"][sec[i]]
            else:
                Indicators[sec[i]]["s"] = Piv[Pos-1]
                Indicators[sec[i]]["r"] = Piv[Pos]
        elif tf == "M15":
            M15H, M15L, M15C = Get_Price(sec[i], "M15", 101, "hlc", "midpoint")
            Indicators[sec[i]]["SMA100"] = round(SMA(M15C, 10, 0),5)
            Indicators[sec[i]]["SMA101"] = round(SMA(M15C, 10, 1),5)
            Indicators[sec[i]]["SMA102"] = round(SMA(M15C, 10, 2),5)
            Indicators[sec[i]]["SMA210"] = round(SMA(M15C, 21, 0),5)
            Indicators[sec[i]]["SMA211"] = round(SMA(M15C, 21, 1),5)
            Indicators[sec[i]]["SMA212"] = round(SMA(M15C, 21, 2),5)
            Indicators[sec[i]]["SMA500"] = round(SMA(M15C, 50, 0),5)
            Indicators[sec[i]]["ATR"] = round(Get_ATR(M15H, M15L, M15C, sec[i]),6)

# class MoneyManagement():
#     def __init__(self, sec):
#         self.sec = sec
#     def UpdateOpenUnits(self, account_id, strat):
#         if strat == "PPB"
#             for i in range(len(self.sec))
#                 PPB["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)
#         elif strat == "IT"
#             for i in range(len(self.sec))
#                 IT["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)
#         elif strat == "MAC"
#             for i in range(len(self.sec))
#                 MAC["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)

def UpdateOpenUnits(sec, account_id, strat):
    if strat == "PPB":
        for i in range(len(sec)):
            PPB["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
    elif strat == "IT":
        for i in range(len(sec)):
            IT["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
    elif strat == "MAC":
        for i in range(len(sec)):
            MAC["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)

# def GetTradeSecurities(strat, sec):
#     sec_temp = []
#     if strat == "PPB":
#         for i in range(len(sec)):
#             c = Get_Price(sec[i], "M1", 1, "c", "midpoint")
#             if PPB["Units"][sec[i]] == 0:
#                 sec_temp.append(sec[i])
#             if PPB["Active"][sec[i]] == 1:
#                 sec_temp2.append(sec[i])
#         # if open units > 
#         # prices closer to PP get loaded earlier
#     elif strat == "IT":
#         # if open units > 0
#         # prices closer to SMAs get loaded earlier
#     elif start == "MAC":

# Good example of a script that solves on optimizer type problem
# Similar to how indicator routines are ran seperate from the strategy

# def IT_BreakEven(account_num, sec, trd_entry, curr_price, vol, vol_adj, file_nm, LIVE_ACCESS_TOKEN):
#     if IT["BEV"][sec] == 0:
#         IT["BEV"][sec] += vol + vol_adj
#         IT["SL"][sec] = trd_entry*(vol/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
#     else:
#         prev_BEV = IT["BEV"][sec[i]]
#         IT["BEV"][sec] += vol_adj
#         IT["SL"][sec] = IT["SL"][sec]*(prev_BEV/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
#     Open_IDs = GetOpenTradeIDs(account_num, sec)
#     for j in range(len(Open_IDs)):
#         UpdateStopLoss(account_num, Open_IDs[j], IT["SL"][sec], file_nm, LIVE_ACCESS_TOKEN)

# def AnalyzePricePatterns(sec):
#     for i in range(len(sec)):
#         DH, DL, DC = Get_Price(sec[i], "D", 2, "hlc", "midpoint")
#         M15C = Get_Price(sec[i], "M15", 10, "c", "midpoint")
#         M5C = Get_Price(sec[i], "M5", 1, "c", "midpoint")
#         lwr = True
#         SMA100 = Indicators[sec[i]]["SMA100"]
#         SMA101 = Indicators[sec[i]]["SMA101"]
#         SMA102 = Indicators[sec[i]]["SMA102"]
#         SMA103 = Indicators[sec[i]]["SMA103"]
#         SMA210 = Indicators[sec[i]]["SMA210"]
#         SMA211 = Indicators[sec[i]]["SMA211"]
#         SMA212 = Indicators[sec[i]]["SMA212"]
#         SMA213 = Indicators[sec[i]]["SMA213"]
#         SMA500 = Indicators[sec[i]]["SMA500"]
#         if min (SMA101 - M15C[1], SMA102 - M15C[2], SMA103 - M15C[3]) > 0:
#         if lwr == True and M15C[0] < SMA100 and M15C[1] < SMA101 and M15C[2] < SMA102 and SMA101 - M15C[1] < 0.0002 and SMA102 - M15C[2] < 0.0002 and M15C[0] < min (M15C[1], M15C[2]) and SMA100 < SMA210 and SMA210 < SMA500:
#             PriceAction[sec[i]]["SMA10Bounce"] = 1

##########################################################################################################
#                                                                                                        #
#                                                Manager                                                 #
#                                                                                                        #
##########################################################################################################

# def RiskvsReward():
    # If things are going well go hard and seek out more opportunities
    # If things are going badly do less and lower the volume
# def Compliance():
    # Job is to ensure that trade performance is compliant with investors expectations and backtests
# def Reporting():
    # Sending the weekly and the reminder to send the monthly reports
# def HeadTrader():
    # Consolidate the positions requested from Signals and it had been adjusted by optimizer and managers

##########################################################################################################
#                                                                                                        #
#                                                 Trader                                                 #
#                                                                                                        #
##########################################################################################################

# Routines to try and optimize best entry prices over a certain time window
# Next 4hr prices could break out of a pattern and fall another 0.5% to let's buy half now and half then
