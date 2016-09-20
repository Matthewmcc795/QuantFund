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

# Good example of a script that solves on optimizer type problem
# Similar to how indicator routines are ran seperate from the strategy

def IT_BreakEven(account_num, sec, trd_entry, curr_price, vol, vol_adj, file_nm, LIVE_ACCESS_TOKEN):
    if IT["BEV"][sec] == 0:
        IT["BEV"][sec] += vol + vol_adj
        IT["SL"][sec] = trd_entry*(vol/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
    else:
        prev_BEV = IT["BEV"][sec[i]]
        IT["BEV"][sec] += vol_adj
        IT["SL"][sec] = IT["SL"][sec]*(prev_BEV/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
    Open_IDs = GetOpenTradeIDs(account_num, sec)
    for j in range(len(Open_IDs)):
        UpdateStopLoss(account_num, Open_IDs[j], IT["SL"][sec], file_nm, LIVE_ACCESS_TOKEN)

# class PMAC:
#     def __init__(self,name):
#         self.data = json.loads(R)
#     def eat(self,food):
#         if food == "Apple": 
#             self.Health -= 100
#         elif food == "Ham":
#             self.Health += 20

# class PriceAction:
#     def __init__(self,name):
#         self.data = json.loads(R)
#     def eat(self,food):
#         if food == "Apple": 
#             self.Health -= 100
#         elif food == "Ham":
#             self.Health += 20

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
