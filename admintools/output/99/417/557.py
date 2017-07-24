import math

def do_turn(pw):
	
	if len(pw.enemy_planets()) == 0 or len(pw.my_planets()) == 0:
		return
		
	myPs = len(pw.my_planets())
	source = pw.my_planets() 

	for myP in xrange(0,myPs) :
		destid = findTheSmall(source[myP], pw)

		if len(pw.my_planets()) > len(pw.enemy_planets()) or len(pw.my_planets()) > 3:
			destid = findThesmallEnemy(source[myP], pw)

		if(destid[1] > source[myP].num_ships()):
			return
		
		else:
			pw.issue_order(source[myP], destid[0], destid[1])

def minShips (source,dest):
	num_of_turn = math.ceil(math.sqrt(math.pow(dest.x() - source.x(),2) + math.pow(dest.y()-source.y(),2)))  
	minShips = ((dest.growth_rate()) * num_of_turn)+ dest.num_ships() + 1
	return minShips;
	
def minShips2 (dest): 
	minShips = dest.num_ships() + 1
	return minShips;

def findTheSmall(source, pw):
	if len(pw.neutral_planets()) == 0:
		dest1 = pw.enemy_planets()[0]
		smallest = minShips2(pw.enemy_planets()[0])
	else:
		dest1 = pw.neutral_planets()[0]
		smallest = minShips2(pw.neutral_planets()[0])
	for i in xrange(1 , len(pw.neutral_planets())):
		if minShips2(pw.neutral_planets()[i]) < smallest:
			smallest = minShips2(pw.neutral_planets()[i])
			dest1 = pw.neutral_planets()[i]
	for i in xrange(0 , len(pw.enemy_planets())):
		if ((minShips(source,pw.enemy_planets()[i]))) < smallest:
			smallest = minShips(source,pw.enemy_planets()[i])
			dest1 = pw.enemy_planets()[i]
	return dest1,smallest
	
def findThesmallEnemy(source, pw):
	dest1 = pw.enemy_planets()[0]
	smallest = minShips2(pw.enemy_planets()[0])
	for i in xrange(0 , len(pw.enemy_planets())):
		if ((minShips(source,pw.enemy_planets()[i]))) < smallest:
			smallest = minShips(source,pw.enemy_planets()[i])
			dest1 = pw.enemy_planets()[i]
	return dest1,smallest
	
if __name__ == "__main__":
	do_turn(pw)