def do_turn(pw):

	COUNT = 1.25
	MAX_S = 0.9
	
	if len(pw.my_fleets()) >= 1:
		return
		
	if len(pw.my_planets()) == 0:
		return

	source = sorted(pw.my_planets(), key=lambda planet: planet.num_ships())[-1]
	
	if len(pw.not_my_planets()) >= 1:
        # dst = pw.neutral_planets()[0]
		sorted_planets = sorted(pw.not_my_planets(), key=lambda planet: pw.distance(planet, source))
		dst = sorted_planets[0]
	else:
		return

	if dst.owner() == 0:  # neutral
		#global COUNT
		#COUNT = 1.25
		pass
	elif dst.owner() == 2:  # enemy
		pw.debug('Distance: ' + str(pw.distance(dst, source)))
		#global COUNT
		COUNT = (1.25 * dst.growth_rate() * pw.distance(dst, source))

	if COUNT == 0:
		COUNT = 1.25
		
	num_ships = int(dst.num_ships() * COUNT)
	
	if num_ships > source.num_ships() * MAX_S:
		num_ships = int(source.num_ships() * MAX_S)

	pw.debug('Num Ships: ' + str(num_ships))
	
	pw.issue_order(source, dst, num_ships)