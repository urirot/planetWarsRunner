def do_turn(pw):
	if len(pw.my_planets()) == 0:
		return

if len(pw.neutral_planets()) >= 1:
		dest = pw.neutral_planets()[0]

	else:
if len(pw.enemy_planets()) >= 1:
dest = pw.enemy_planets()[0]

	source = pw.my_planets()[0]
	
	num_ships = source.num_ships() / 2

	pw.issue_order(source, dest, num_ships)
