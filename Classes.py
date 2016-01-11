# classes
import requests
import json
from array import *
from Settings import API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID

class Execution:
	def __init__(self,domain,access_token,account_id):
		self.domain = domain
		self.access_token = access_token 
		self.account_id = account_id
		self.conn = self.obtain_connection()

	def obtain_connection(self):
		return httplib.HTTPSConnection(self.domain)

	def execute_order(self,event):
		headers = {'Authorization' : self.access_token}
		params = urllib.urlencode() # this line is asking the events class what the current side, size, pair and type the trade is
		self.conn.request("Post", "/v1/accounts/%s/orders" % str(self.account_id), params, headers)
		response = self.conn.getresponse().read()
		print response

class Hero:
	def __init__(self,name):
		self.data = json.loads(R)
	def eat(self,food):
		if food == "Apple": 
			self.Health -= 100
		elif food == "Ham":
			self.Health += 20

Bob = Hero("Bob")
print Bob.Name
print Bob.Health
Bob.eat("Ham")
print Bob.Health

Order = Enter_Order("EUR_USD",1,"Limit","Buy",Close(i),SL,TP)
Account = Portfolio()
Order = Exit()

class Enter_Order:
    def __init__(self, instrument, units, order_type, side, price, SL, TP):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side
        self.price = price
        self.SL = price + SL
        self.TP = price + TP

class Portfolio:
    def __init__(self, instrument, units, order_type, side, price):
        self.Balance = 1000
        self.side = side
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025
        self.Lots = 1000
        self.Entry_Price = price
        self.Open = 1

    def Check_Close(self, entry, Lots, side):
        if side == "B" and :    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025

	def Market_Close(self, price):
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025

    def Close_Order(self, price):
        self.Balance = 1000
        self.side = side
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025
        self.Lots = 1000
        self.Entry_Price = price
        self.Open = 0

class Open_Order:
    def __init__(self, instrument, units, order_type, side, price):
        self.Balance = 1000
        self.side = side
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025
        self.Lots = 1000
        self.Entry_Price = price
        self.Open = 1

    def Check_Close(self, entry, Lots, side):
        if side == "B" and :    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025

	def Market_Close(self, price):
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025

    def Close_Order(self, price):
        self.Balance = 1000
        self.side = side
        if side == "B":    	
	        self.SL = price - 0.02
	        self.TP = price + 0.025
	    elif side == "S":
	        self.SL = price + 0.02
	        self.TP = price - 0.025
        self.Lots = 1000
        self.Entry_Price = price
        self.Open = 0

Open_Order = 0
Carry_Price = 0.0
TP = 0.025
SL = -0.02
Account = 1000
Lots = 1000
n = 50
last_entry = 0 
spacer = 5
Starting_Balance = Account

for i in range(0,10):
    if Open_Order == 0:
        Carry_Price = Close(i-1)
    aavg = 0.0
    SMA = 0.0
    ssd = 0.0
    sd = 0.0
    tail = 0.0
    wick = 0.0
    
    for j in range(0,n):
        aavg = Close(i-j) + aavg
    SMA = aavg/n
    
    for j in range(0,n):
        ssd = (Close(i-j) - SMA)**2 +ssd
    sd = (ssd/(n-1))**(0.5)
    Upper_Band = SMA + 2*sd
    Lower_Band = SMA - 2*sd
    
    if Close(i-1) > Open(i-1):
        wick = High(i-1) - Close(i-1)
        tail = Open(i-1) - Low(i-1)
    else:
        wick = High(i-1) - Open(i-1)
        tail = Close(i-1) - Low(i-1)

    if Close(i-1) < Lower_Band and Open_Order == 0 and i - last_entry > spacer:
        Open_Order = 1
        Open_Price = Close(i-1)
        Stop_Loss = Open(i) + SL
        Take_Profit = Open(i) + TP
        Carry_Price = Close(i-1)
        last_entry = i
        print("Buy" + str(i))
    
    if Close(i-1) > Upper_Band and Open_Order == 0 and i - last_entry > spacer:
        Open_Order = -1
        Open_Price = Close(i-1)
        Stop_Loss = Open(i) - SL
        Take_Profit = Open(i) - TP
        Carry_Price = Close(i-1)
        last_entry = i
        print("Sell" + str(i))

    if Open_Order == 1:
        if High(i-1) > Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0
            Starting_Balance = Account
        if Low(i-1) < Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if High(i-1) < Take_Profit and Low(i-1) > Stop_Loss:
            Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

    if Open_Order == -1:
        if High(i-1) > Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i-1) < Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i-1) > Take_Profit and High(i-1) < Stop_Loss:
            Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
    Account_Chart.append(Account)