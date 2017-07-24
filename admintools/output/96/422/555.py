def do_turn(pw):
    max_planets = 0
    temp1 = 0
    s = True
    global dest
    if len(pw.my_planets()) == 0:
        return

    if len(pw.neutral_planets()) >= 1:
        dest = pw.neutral_planets()[0]

    else:
        if len(pw.enemy_planets()) >= 1:
            dest = pw.enemy_planets()[0]

    for my_ship in pw.my_planets():

        temp1 = my_ship.num_ships()
        pw.debug('num ships :' + str(my_ship.num_ships()))

        temp = 200000000

        for dest_ship in pw.not_my_planets():
            if isPlanetInDanger(dest_ship , pw):
                if(my_ship.num_ships() > 10):
			        pw.issue_order(my_ship ,dest_ship , 10)
            elif pw.distance(my_ship, dest_ship) < temp and temp1/2 > dest_ship.num_ships():
                temp = pw.distance(my_ship, dest)
                dest = dest_ship
                if(my_ship.num_ships() > 1):
			        pw.issue_order(my_ship ,dest_ship , temp1)

        pw.debug('num ships :' + str(my_ship.num_ships()))

def listOfPossiblePlanetsToAttack(p,pw):
    num = p.num_ships()
    owner = p.owner()

    possiblePlanets = []

    if owner == 0:
        return
    elif owner == 1:
        planets = pw.not_my_planets()
        for i in planets:
            if num/2 > i.num_ships()+i.growth_rate()*pw.distance(p,i):
                possiblePlanets.append(i)
    elif owner == 2:
        planets = pw.my_planets()
        planets.extend(pw.neutral_planets())
        for i in planets:
            if num > i.num_ships()+i.growth_rate()*pw.distance(i,p):
                possiblePlanets.append(i)

    return possiblePlanets

def isPlanetInDanger(p, pw):
    fleets = pw.fleets()
    newFleets = []
    numOfShips = 0

    for i in fleets:
        if fleets.destination_planet() == p:
            enterSortedFleet(newFleets,i)

    balance = p.num_ships()
    for i in range(1,newFleets[len(newFleets)-1].turns_remaining()):
        if balance < 0:
            owner = 2
        else:
            owner = 1
        if 1 == pw.owner():
            balance += p.growth_rate()
        else:
            balance -= p.growth_rate()
        for j in newFleets:
            if j.turns_remaining() == i:
                if j.owner() == pw.owner():
                    balance += j.num_ships()
                else:
                    balance -= j.num_ships()
    if balance < 0:
        return True
    else:
        return False


def enterSortedFleet(list, f):
    list.insert(f)
    for i in range(len(list))-1:
        for j in range(0,i):
            if list[j].turns_remaining() > list[j+1].turns_remaining():
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp