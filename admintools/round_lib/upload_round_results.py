#! /usr/bin/python
import sys
import os
from glob import glob
import json
import requests
import zlib
import base64
from config import *

if len(sys.argv) != 3:
    print "Usage: ./upload_round_results.py <tournament id> <round id>"
    sys.exit(2)

tourn_id = sys.argv[1]
round_id = sys.argv[2]
dir = OUTPUT_DIR + tourn_id + "/" + round_id
results_dir = dir + "/results"

url = HOST + "tournaments/%s/upload_game_results.json" % tourn_id
def post(results):
    print "About to upload " + str(len(results)) + " results"
    for i in range(0, len(results), 5):
        part = results[i:i+5]
        data = {"results": base64.b64encode(zlib.compress(json.dumps(part)))}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print "post status code: %d with %d-%d results" % (r.status_code, i, i+5)

if not os.path.exists(dir):
    print "Directory " + dir + " doesn't exist"
    sys.exit(3)
if not os.path.exists(results_dir):
    print "Directory " + results_dir + " doesn't exist"
    sys.exit(4)

all_reuslts = [tuple(x.split("/")[-1].split(".")[0].split("_")) for x in glob(results_dir + "/*.meta")]

results = []
for (g1, g2) in all_reuslts:
    filename = results_dir + "/" + g1 + "_" + g2 + ".result"
    game = file(filename).read()
    meta = file(filename + ".meta").read()

    winner = None
    if meta.split("\n")[1] != "Draw":
        print filename 
        winner = int(meta.split("\n")[1].split(": ")[1])

    data = {}
    data["round"] = dir.split("/")[-1]
    data["group1"] = int(g1)
    data["group2"] = int(g2)
    data["winner"] = winner
    data["turns"] = int(meta.split("\n")[0].split(": ")[1])
    data["game"] = game
    results.append(data)

post(results)
