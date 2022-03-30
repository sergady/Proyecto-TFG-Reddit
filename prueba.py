
from datetime import datetime
datenow = datetime.now()
timestamp = datenow.__str__().replace(" ", "_")[:-7]
print(timestamp)