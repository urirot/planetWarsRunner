def do_turn(pw):
    defend(pw)
    anti_capture(pw)
    capture(pw)
    attack(pw)





# check if we can prevent from enemy to conquer a planet
def anti_capture(pw):
    #planet = get_best_src_planet(pw)
    #neutral = get_enemy_neutral_fleets(pw)
    pass


# return best attack src for specific planet
def get_best_src_planet(pw):
    planets = pw.my_planets()
    if len(planets)  == 0:
        return
    planet = planets[0]
    for p in planets:
        if p.num_ships() > planet.num_ships():
            planet = p
    return planet

def get_enemy_neutral_fleets(pw):
    enemy_fleets = pw.enemy_fleets()
    neutrals = []
    for ff in enemy_fleets:
        if ff.destination_planet().owner() == 0:
            neutrals.append(ff)
    return neutrals

# Defend -
# 1) Check if enemy fleets exist
# 2) Check if enemy fleets dest is MY planet
# 3) Check if my planet is defendable, if it is, send fleets
def defend(pw):
    pass

# Capture -
# 1) Check if neutral planets exist
# 2) Check by distance, growth rate, number of troops the best planet
# 3) Attack selected planet
def capture(pw):
    planets = pw.neutral_planets()
    my_planets = pw.my_planets()
    if len(my_planets) > 0:
        for myp in my_planets:
            if len(planets) > 0:
                planet = planets[0]
                for p in planets:
                    if pw.distance(myp, p) < pw.distance(myp, planet):
                        planet = p
                numships = myp.num_ships()
                if numships > planet.num_ships() + 3:
                    toMove = planet.num_ships() + 2
                    if pw.turn_number() < 75:
                        move_fleet(pw, myp, planet, toMove)
# Attack -
# 1) Check if enemy planets exist
# 2) Check by distance, growth rate, number of troops the best planet
# 3) Attack selected planet
def attack(pw):
    if pw.turn_number() > 80:
        my_planets = pw.my_planets()
        enemy_planets = pw.enemy_planets()

        for myp in my_planets:
            enemy_planet = get_closest_planet_to_src(pw, myp, enemy_planets)
            if enemy_planet is not None:
                move_fleet(pw, myp, enemy_planet, myp.num_ships()/2)

# getting src island and list of island to check
def get_closest_planet_to_src(pw, myp, enemy_planets):
    if len(enemy_planets) == 0: return None
    close = enemy_planets[0]
    for pln in enemy_planets:
        if(pw.distance(myp, close) > pw.distance(myp, pln)):
            close = pln
    return close

# move fleet
def move_fleet(pw, source, dest, num_ships):
    pw.issue_order(source, dest, num_ships)

# get list of enemy's fleets
def get_enemy_fleets(pw):
    myFleets = []
    for f in pw.fleets():
        if(f.owner() == 2):
            myFleets.append(f)

