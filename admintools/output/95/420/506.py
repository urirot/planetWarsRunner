
def do_turn(pw):
	if len(pw.my_fleets()) >= 1:
		return
	if len(pw.my_planets()) == 0:
		return
	else:
		p1 = pw.my_planets()[0]
	if len(pw.neutral_planets()) >= 1:
		n_planets = pw.neutral_planets()
		a_planets = pw.not_my_planets()
		p1 = max(pw.my_planets())
		a_planets = sorted(a_planets, key=lambda x: pw.distance(p1, x))
		if p1.num_ships() > a_planets[0].num_ships() + 30:
			pw.issue_order(p1, a_planets[0],a_planets[0].num_ships() + 30)

	else:
		if len(pw.enemy_planets()) >= 1:
			dest = pw.enemy_planets()[0]

			source = pw.my_planets()[0]
	    	num_ships = source.num_ships() / 2
	    	pw.debug('Num Ships: ' + str(num_ships))
	    	pw.issue_order(source, dest, num_ships)
