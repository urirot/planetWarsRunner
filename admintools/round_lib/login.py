#! /usr/bin/python
from urllib import urlopen
import json
import sys
import requests
from config import *

url = HOST + "tournaments/login.json"
def login(username, password):
    data = {"username" : username, "password": password}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        return json.loads(r.text)["id"]
    raise Exception("Wrong username/password")

if len(sys.argv) != 3:
    print "Usage: ./login.py <username> <password>"
    sys.exit(2)

username = sys.argv[1]
password = sys.argv[2]

print login(username, password)
