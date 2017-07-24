#! /usr/bin/python

import sys
import os
import json
import requests
from config import *

if len(sys.argv) != 3:
    print "Usage: ./upload_round_results.py <tournament id> <round id>"
    sys.exit(2)

tournament_id = sys.argv[1]
round_id = sys.argv[2]
dir = OUTPUT_DIR + tournament_id + "/" + round_id

url = HOST + "tournaments/%s/round_code.json" % tournament_id
def post(data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print "post status code: " + str(r.status_code) + " : " + str(data["group"])

if not os.path.exists(dir):
    print "Directory " + dir + " doesn't exist"
    sys.exit(3)


groups = [g for g in os.listdir(dir) if g.endswith(".py")]
for g in groups:
    data = {}
    data["code"] = file(dir + "/" + g).read()
    data["round"] = int(round_id)
    data["group"] = g[:-3] # Remove the ".py"
    post(data)
