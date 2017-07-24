
def do_turn(all):
	# if len( all.my_fleets() ) > 0:
	# 	raise "foo"

	planets = all.my_planets()
	others = all.not_my_planets()

	if len(planets) == 0 or len(others) == 0:
		return

	for i in xrange(0, len(planets) ):
		this_planet = planets[i]
		other_planets = sorted(others, key=lambda other_planet: all.distance(this_planet, other_planet) )

		# all.debug(str([a.num_ships() for a in other_planets]) )
		if len( filter(lambda fleet: fleet.source_planet() == this_planet.planet_id(), all.my_fleets()) ) == 0:
			all.issue_order( this_planet, other_planets[0], this_planet.num_ships() / 1.45 )
