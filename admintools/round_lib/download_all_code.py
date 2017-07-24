#! /usr/bin/python
from urllib import urlopen
import json
import os
import sys
import shutil
import requests
from config import *


if len(sys.argv) != 3:
    print "Usage: ./download_all_code.py <tournament id> <round id>"
    sys.exit(2)
tourn_id = sys.argv[1]
round_id = sys.argv[2]

dir = OUTPUT_DIR + tourn_id + "/" + round_id

if os.path.exists(dir):
    answer = raw_input("dir " + dir + " already exists, override? ")
    if answer.lower() != "y":
        print "Bye bye"
        sys.exit(1)
    else:
        shutil.rmtree(dir)

os.makedirs(dir)


rest_url = HOST + "tournaments/%s/get_all_programs.json" % tourn_id
all_progs = json.loads(urlopen(rest_url).read())

for (id, url) in all_progs.items():
    url += CODE_URL_SUFFIX
    try:
        content = requests.get(url, auth=CODE_URL_AUTH).text
    except IOError as e:
        print "PROBLEM WITH GROUP: %s with url %s" % (id, url)
        print str(e)
        content = ""

    f = open(dir + "/" + str(id) + ".py", "w").write(content)

