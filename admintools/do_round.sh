# This script is used to run a full round of a specific tournament
#
# Usage: ./do_round.sh
#
set -e

username="$1"
password="$2"
round_number="$3"

tourn_id=$(python round_lib/login.py $username $password)


set -x
round_id=$(python round_lib/get_round_id.py $tourn_id $round_number)
python round_lib/download_all_code.py $tourn_id $round_id
python round_lib/run_round.py $tourn_id $round_id
python round_lib/upload_round_code.py $tourn_id $round_id
python round_lib/upload_round_results.py $tourn_id $round_id
