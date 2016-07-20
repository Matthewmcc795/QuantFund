import requests
import json
from array import *
from Backtest_Objects import *
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

EUc = pClose("EUR_USD", "H4", "2014-01-01", "2016-07-01")
EGc = pClose("EUR_GBP", "H4", "2014-01-01", "2016-07-01")
GUc = pClose("GBP_USD", "H4", "2014-01-01", "2016-07-01")
EUma = pMa(EUc, 50)
EGma = pMa(EGc, 50)
GUma = pMa(GUc, 50)
EUsd = pStd(EUc, 50)
EGsd = pStd(EGc, 50)
GUsd = pStd(GUc, 50)
EUEGcorrel = pCorr(EUc, EGc, 50)
GUEGcorrel = pCorr(GUc, EGc, 50)
EUGUcorrel = pCorr(EUc, GUc, 50)

EUZ = []
EGZ = []
GUZ = []
for i in range(3501):
    EUZ.append((EUc[3501-i] - EUma[3501-i])/EUsd[3501-i])
    EGZ.append((EGc[3501-i] - EGma[3501-i])/EGsd[3501-i])
    GUZ.append((GUc[3501-i] - GUma[3501-i])/GUsd[3501-i])

EU_GU = []
EU_EG = []
GU_EU = []
GU_EG = []
EG_EU = []
EG_GU = []
for i in range(3500):
    EU_GU.append(GUZ[3500-i]*EUGUcorrel[3500-i])
    EU_EG.append(EGZ[3500-i]*EUEGcorrel[3500-i])
    GU_EU.append(EUZ[3500-i]*EUGUcorrel[3500-i])
    GU_EG.append(EGZ[3500-i]*GUEGcorrel[3500-i])
    EG_EU.append(EUZ[3500-i]*EUEGcorrel[3500-i])
    EG_GU.append(GUZ[3500-i]*GUEGcorrel[3500-i])

EUZ_adj = []
GUZ_adj = []
EGZ_adj = []
for i in range(3500):
    EUZ_adj.append((EU_GU[i]*abs(EUGUcorrel[i]))/(abs(EUGUcorrel[i])+abs(EUEGcorrel[i])) + (EU_EG[i]*abs(EUEGcorrel[i]))/(abs(EUGUcorrel[i])+abs(EUEGcorrel[i])))
    GUZ_adj.append((GU_EU[i]*abs(EUGUcorrel[i]))/(abs(EUGUcorrel[i])+abs(GUEGcorrel[i])) + (GU_EG[i]*abs(GUEGcorrel[i]))/(abs(EUGUcorrel[i])+abs(GUEGcorrel[i])))
    EGZ_adj.append((EG_EU[i]*abs(EUEGcorrel[i]))/(abs(EUEGcorrel[i])+abs(GUEGcorrel[i])) + (EG_GU[i]*abs(GUEGcorrel[i]))/(abs(EUEGcorrel[i])+abs(GUEGcorrel[i])))


plt.plot(EUZ)
plt.plot(EUZ_adj)
plt.ylim(-5,5)
plt.show()

plt.plot(GUZ)
plt.plot(GUZ_adj)
plt.ylim(-5,5)
plt.show()

plt.plot(EGZ)
plt.plot(EGZ_adj)
plt.ylim(-5,5)
plt.show()
