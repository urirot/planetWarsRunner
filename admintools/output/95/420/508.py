


def weak(source,dest):
	enemy = dest.num_ships()
	me = source.num_ships()
	return me - enemy
	
def setWorth(pw,source,enemyPlanets,neutralPlanets):
	lenE = len(enemyPlanets)
	lenN = len(neutralPlanets)
	ans = source
	currPower = 0
	power = 0
	for dest in neutralPlanets:
		if(weak(source,dest) - pw.distance(source,dest) > 0):
			power = weak(source,dest) - pw.distance(source,dest)
			if(power>currPower):
				currPower = power
				ans = dest
				
	for dest in enemyPlanets:
		if(weak(source,dest)-pw.distance(source,dest) > 0):
			power = weak(source,dest)  - pw.distance(source,dest)
			if(power>currPower):
				currPower = power
				ans = dest
	
	return [ans,currPower]

	

def do_turn(pw):
	
	if len(pw.my_planets()) == 0:
		return
		
	myPlanets = pw.my_planets()
	enemyPlanets = pw.enemy_planets()
	neutralPlanets = pw.neutral_planets()
	fleets = pw.fleets()
	
	for fleet in fleets:
		if fleet.owner() == 1:
			if (pw.get_planet(fleet.source_planet()) in myPlanets):
				myPlanets.remove(pw.get_planet(fleet.source_planet()))
	dest = 0
	currPower = 0
	currSource = 0
	for source in myPlanets:
		ans = setWorth(pw,source,enemyPlanets,neutralPlanets)
		if currPower < ans[1]:
			currPower = ans[1]
			dest = ans[0]
			currSource = source
		
	
	if  currPower and dest and currSource.num_ships() - currPower > 0:
		pw.issue_order(currSource, dest, currPower)
	return	
	
	
	



	
	
	
	





