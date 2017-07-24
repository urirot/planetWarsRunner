#! /usr/bin/python
from urllib import urlopen
import json
import sys
from config import *

if len(sys.argv) != 3:
    print "Usage: ./get_round_id.py <tournament id> <round number>"
    sys.exit(2)
tourn_id = sys.argv[1]
round_number = sys.argv[2]

url = HOST + "tournaments/%s/round_by_name?name=%s" % (tourn_id, round_number)
result = urlopen(url).read()

if not result:
    sys.stderr.write("Can't find this round (round number = %s). Are you sure you created it?\n" % round_number)
    sys.exit(1)

round_id = str(json.loads(result)["id"])

print round_id
