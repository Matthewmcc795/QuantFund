import sys
from datetime import datetime, timedelta

name = "Log file.txt"
file = open(name ,'a')
dt = datetime.now() + timedelta(hours=4)
dt = dt.replace(minute=0,second=1,microsecond=0)
file.write("Waiting until " + str(dt) + "\n")	
file.close()