import time

from datetime import datetime

date = datetime.today()
d = '{:%d-%m %H:%M:%S}'.format(date)
a = str(d)
print(a)
