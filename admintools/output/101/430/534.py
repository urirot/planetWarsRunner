def do_turn(pw):
    if len(pw.my_planets()) == 0:
        return

    our_src = pw.my_planets()[0]
    if(len(pw.enemy_planets()) == 0):
        return
    enemy_src = pw.enemy_planets()[0]
    pw.debug("first")
    dst = find_closest_island(pw, our_src, pw.not_my_planets(), [])
    pw.debug("first - end")
    pw.issue_order(our_src, dst, our_src.num_ships() / 2)
    if pw.turn_number() > 2: #Attack:
        dst = findWeakestIsland(pw)
        attackers = []
        attacker = planetToSendFrom(pw, dst.planet_id(), [])
        attackers.append(attacker)
        secondAttacker = planetToSendFrom(pw, dst.planet_id(), attackers)
        attackers.append(secondAttacker)
        thirdAttacker = planetToSendFrom(pw, dst.planet_id(), attackers)
        if secondAttacker != None:
            pw.issue_order(secondAttacker, dst, (secondAttacker.num_ships()) / 2)
        if thirdAttacker != None:
            pw.issue_order(thirdAttacker, dst, (thirdAttacker.num_ships()) / 4)
        if attacker:
            pw.issue_order(attacker, dst, (attacker.num_ships()) / 2)
        #else:

    else:#Create defence base
        dst = pw.planets()[15]
        pw.issue_order(our_src, findWeakestIsland(pw), our_src.num_ships() / 4)
        dst = pw.planets()[4]
        pw.issue_order(our_src, findWeakestIsland(pw), our_src.num_ships() / 4)
    return

def find_closest_island(pw, planetId, groupToCheck, exceptions):
    closest_dst = pw.distance(planetId, groupToCheck[0])
    closest_planet = groupToCheck[0]
    for i in groupToCheck:
        if i.planet_id() not in exceptions:
            dst = pw.distance(planetId, i)
            if(dst < closest_dst):
                closest_dst = dst
                closest_planet = i
    return closest_planet
"""def findBestTarget(pw, growLength, shipsNeeded, avialableShips):

def planetToSendFrom(pw):
    f
"""
def findWeakestIsland(pw):
    enemyIslands = pw.not_my_planets()
    smallestNumOfShips = pw.enemy_planets()[0].num_ships()
    smallestNumOfShipsISLAND = pw.enemy_planets()[0]
    for i in enemyIslands:
        if i.num_ships() < smallestNumOfShips:
            smallestNumOfShipsISLAND  = i
            smallestNumOfShips = i.num_ships()
    return smallestNumOfShipsISLAND
def planetToSendFrom(pw, planetId, exceptions):
    selected = []
    for currIsland in pw.my_planets():
        attacker = find_closest_island(pw, planetId, pw.my_planets(), selected)
        selected.append(attacker.planet_id())
        if attacker not in exceptions:
            return attacker
    return None