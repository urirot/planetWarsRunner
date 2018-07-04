# The host to run against
HOST = "http://http://34.212.203.64"
#HOST = "http://fgpoint.dev:3000/"

# The output directory to use, sometimes this is useful to have a look in if something goes wrong
OUTPUT_DIR = "output/"

# The directory of the simulator (the java and python) to use
GAME_DIR = "../simulator"
GAME_JAR = GAME_DIR + "/tools/PlayGame.jar"
RUN_BOT_FILE = GAME_DIR + "/tools/run_bot.py"

# The map file to use - in the future it's best that we get the map from the server
MAP_FILE = GAME_DIR + "/maps/default_map.txt"

# When downloading the code, is there something needed to be added (for example when using gist, we need to add /raw"
CODE_URL_SUFFIX = "/raw"

# When downloading the code, sometimes basic HTTP auth is needed, supply it as ("user", "pass"), or None if irrelevant
CODE_URL_AUTH = None
