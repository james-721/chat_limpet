#!/home/robotnik/opt/python-3.8.1/bin/python3

import requests
from statics import redsquid_url

message = 'FNORD'
myobj = {'content': message }
x = requests.post(redsquid_url, data = myobj)
print(x)