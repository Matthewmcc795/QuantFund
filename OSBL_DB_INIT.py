import pypyodbc
from array import *

file_Name = "ODBC;DSN=QuickBooks Data;SERVER=QODBC"

pypyodbc.win_create_mdb(file_Name)

conn = pypyodbc.win_connect_mdb(file_Name) 
cur = conn.cursor()

cur.execute(u"sp_report ARAgingSummary show Current_Title, Amount_Title, Text, Label, Current, Amount parameters DateMacro = 'ThisWeek', AgingAsOf = 'ThisWeek';")
results = cur.fetchall()
print results

# cur.execute(u"CREATE TABLE User_Log (ID INTEGER PRIMARY KEY, Time_Stamp String, User String, Type String, Update String)")

# cur.execute(u"CREATE TABLE Customer (ID INTEGER PRIMARY KEY, TimeCreated Date, TimeModified Date, FullName String, IsActive String, Salutation String, FirstName String, LastName String, BillAddressAddr1 String, BillAddressAddr2 String, BillAddressAddr3 String, BillAddressAddr4 String, BillAddressCity String, BillAddressNote String, Phone String, AltPhone String, Fax String, Email String, Contact String, AltContact String, SalesRepRefFullName String, ResaleNumber Integer, CreditLimit Integer)") 

# cur.execute(u"CREATE TABLE Vendor (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Item (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Inventory (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE AR_Summary (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE AP_Summary (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Sales_Customer_Summary (ID INTEGER PRIMARY KEY, Day String, Ticker String, Open Double, High Double, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Sales_Item_Summary (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Purchase_Item_Summary (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Purchase_Vendor_Summary (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE AR_Input (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE AP_Input (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Account_Balance(ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# cur.execute(u"CREATE TABLE Bills_Due (ID INTEGER PRIMARY KEY, Low Double, Close Double)")

# #cur.execute('''INSERT INTO M5_Price(ID,Day,Ticker,Open,High,Low,Close) VALUES(?,?,?,?,?,?,?)''',(i+p,Date(i),str(Sec[j]),Open(i),High(i),Low(i),Close(i)))
# #cur.commit()

conn.commit()
conn.close()