from datetime import datetime, timedelta
import time
import sys

dt = datetime.strptime('January 23 16 22:30', '%B %d %y %H:%M')
print dt
print str(datetime.now())
dt = datetime.now() + timedelta(minutes=5)
print dt
dt = dt.replace(second=0,microsecond=1)
print dt