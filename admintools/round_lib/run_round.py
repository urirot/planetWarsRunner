#! /usr/bin/python
import sys
import os
import shutil
import random
from config import *
from multiprocessing import Pool

# Example for command:
# java -jar tools/PlayGame.jar map.txt 1000 1000 log.txt "python tools/run_bot.py Iftach1.py" "python tools/run_bot.py Iftach1.py"
RUN_GAME_COMMAND = "java -jar " + GAME_JAR + " " + MAP_FILE + " 1000 1000 {logfile}" + \
                   ' "python ' + RUN_BOT_FILE + ' {prog1}" "python ' + RUN_BOT_FILE + ' {prog2}" > {output} 2> /dev/null'

if len(sys.argv) != 3:
    print "Usage: ./run_round.py <tournament id> <round id>"
    sys.exit(2)

tourn_id = sys.argv[1]
round_id = sys.argv[2]
dir = OUTPUT_DIR + tourn_id + "/" + round_id

if not os.path.exists(dir):
    print "Directory " + dir + " doesn't exist"
    sys.exit(3)

results_dir = dir + "/results"
if os.path.exists(results_dir):
    answer = raw_input("dir " + results_dir + " already exists, override? ")
    if answer.lower() == "y":
        shutil.rmtree(results_dir)
    else:
        print "Bye bye"
        sys.exit(1)

os.makedirs(results_dir)

groups = [g[:-3] for g in os.listdir(dir) if g.endswith(".py")]
rounds = []
for i in range(len(groups)):
    for j in range(i + 1, len(groups)):
        rounds.append((groups[i], groups[j]))

def run_game(params):
    print "Running: " + params["g1"] + " VS " + params["g2"]
    print params["command"]
    os.system(params["command"])
    os.system(params["tail_command"])

params_list = []
for (g1, g2) in rounds:
    # We do that in order to make sure players don't take advantage of their place in a match
    # We had a case when one player was always on one side and he used the planet ids in his source.
    # Although this is fair game, they need to check where they are first and don't assume it
    if random.getrandbits(1):
        g1, g2 = g2, g1

    output_file = results_dir + "/" + g1 + "_" + g2 + ".result"
    logfile = results_dir + "/" + g1 + "_" + g2 + ".log"
    command = RUN_GAME_COMMAND\
        .replace("{prog1}", dir + "/" + g1 + ".py")\
        .replace("{prog2}", dir + "/" + g2 + ".py")\
        .replace("{logfile}", logfile)\
        .replace("{output}", output_file)
    params_list.append({
        "g1": g1,
        "g2": g2,
        "command": command,
        "tail_command": "tail -2 " + logfile + " > " + output_file + ".meta"
    })

#p = Pool(2)
#p.map(run_game, params_list)
for p in params_list:
    run_game(p)
print "Round is done!"
