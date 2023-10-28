from datetime import datetime
import time

past = datetime.now()
time.sleep(2)
now = datetime.now()
diff = now-past
print(diff)
