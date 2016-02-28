from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import numpy as np
import matplotlib.pyplot as plt
from Backtest_Objects import *
import pandas as pd
import time

start_time = time.time()
Sec = []
# Sec.append("EUR_USD")
# Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
# Sec.append("EUR_GBP")
# Sec.append("EUR_CAD")
# Sec.append("EUR_AUD")
# Sec.append("EUR_NZD")
# Sec.append("GBP_AUD")
# Sec.append("GBP_NZD")
# Sec.append("GBP_CAD")
# Sec.append("AUD_CAD")
# Sec.append("AUD_NZD")
# Sec.append("NZD_CAD")

st = "2015-01-01"
en = "2016-02-24"
end_dt = FindDateRange(st, 24*12)
print end_dt
while np.busday_count(end_dt, en) > 10:

    end_dt = FindDateRange(end_dt, 24*12)
    print end_dt


# tf1 = "H4"
# p = 0
# md = pDate(Sec[p], tf1, st, en)
# mc = pClose(Sec[p], tf1, st, en)
# mc1 = pClose(Sec[p+1], tf1, st, en)
# ZScoreSpreads(mc, mc1, 20)
# Events = Calendar(Sec[0], "1 month")
# Act = Calendar_Actual(Sec[0], "1 month")
# Curr = Calendar_Currency(Sec[0], "1 month")

# for i in range(0, len(Events)):
#     if Curr[i] == "CAD":
#         print Events[i]
#         print Act[i]
# lots = 5000
# portfolio_plot = np.zeros((len(Sec), len(mc)))
# hr = pHour(md)
# lvl = LevelizedPrice(mc, hr, 2, 5)
# plt.plot(lvl)
# plt.ylim(0.9,1.1)
# plt.show()
# for p in range(0,len(Sec)):
#     mo = pOpen(Sec[p], tf1, st, en)
#     mh = pHigh(Sec[p], tf1, st, en)
#     ml = pLow(Sec[p], tf1, st, en)
#     mc = pClose(Sec[p], tf1, st, en)
#     Bearish = BearishReversal(mo,mh,ml,mc,2)
#     Bullish = BullishReversal(mo,mh,ml,mc,2)
#     ATR = pATR(mc, mh, ml, 14)
#     MA = pMa(mc,20)
#     SD = pStd(mc,20)
#     UpperBand = UpperMovingAverageBand(mc, MA, SD, 2, "U")
#     CloseUpperBand = UpperMovingAverageBand(mc, MA, SD, 2, "D")
#     LowerBand = LowerMovingAverageBand(mc, MA, SD, 2, "D")
#     CloseLowerBand = LowerMovingAverageBand(mc, MA, SD, 2,"U")
#     Buy_Signals = np.where(LowerBand + Bullish > 1, 1, 0)
#     Buy_SL = mc - 3*ATR
#     Buy_TP = mc + 3*ATR
#     BuyWin = np.where(mh > Buy_TP, 1, 0)
#     BuyLoss = np.where(ml < Buy_SL, 1, 0)
#     CloseBuy = BuyWin + BuyLoss
#     Sell_Signals = np.where(UpperBand + Bearish > 1, 1, 0)
#     SellWin = np.where(ml < Buy_SL, 1, 0)
#     SellLoss = np.where(mh > Buy_TP, 1, 0)
#     CloseSell = SellWin + SellLoss

#     portfolio = MarketOnClosePortfolio(Sec[p], mc, lots, Buy_Signals, CloseBuy, initial_capital = 1000)
#     buy_returns = portfolio.backtest_portfolio()
#     portfolio = MarketOnClosePortfolio(Sec[p], mc, -1*lots, Sell_Signals, CloseSell, initial_capital = 1000)
#     sell_returns = portfolio.backtest_portfolio()
#     returns = buy_returns*0.5 + sell_returns*0.5
#     portfolio_plot = SaveToPlot(portfolio_plot, returns, p)

# # a = backtest_stats(portfolio_plot)
# plot_Data = np.mean(portfolio_plot, axis = 0)
# plt.plot(plot_Data)
# plt.ylim(min(plot_Data)*0.9,max(plot_Data)*1.1)
# print("--- %s seconds ---" % (time.time() - start_time))
# plt.show()