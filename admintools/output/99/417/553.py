def do_turn(pw):
	#if(len(pw.my_fleets()) >= 1):
		#return
	div = 0.5
	#check_enemy_fleet(pw)
	for my_planet in pw.my_planets():
		if(my_planet.growth_rate() <= 2):
			div = 0.9
		dest = get_shortest(pw, my_planet)
		if dest == None:
			continue
		if (my_planet.num_ships() * div > dest.num_ships() + 5) and (dest.growth_rate() > 2):
			pw.issue_order(my_planet, dest, int(my_planet.num_ships() * div))
		elif (my_planet.num_ships() * div > dest.num_ships() + 5):
			pw.issue_order(my_planet, dest, int(my_planet.num_ships() * div))
		else:
			pw.issue_order(my_planet, dest, int(my_planet.num_ships() * 0.1))
		div = 0.5
		
def get_shortest(pw, src):
	if(len(pw.not_my_planets()) < 1):
		return None
	shortest_planet = pw.not_my_planets()[0]
	min = pw.distance(src, shortest_planet)
	for planet in pw.not_my_planets():
		if(pw.distance(src, planet) < min):
			min = pw.distance(src, planet)
			shortest_planet = planet
	return shortest_planet