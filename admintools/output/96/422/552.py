from PlanetWars import *
import math


FLEET_PERCENTAGE = 0.3
FLEET_THRESHOLD = 10.0

DISTANCE_MULTIPLIER = 2 * math.e  # 4.0
NUM_SHIPS_MULTIPLIER = 1.0


def weight(pw, source, destination):
    # type: (PlanetWars, Planet, Planet) -> float
    distance = pw.distance(source, destination)
    num_ships = destination.num_ships()
    return -(math.log(distance * DISTANCE_MULTIPLIER, math.e)) * (num_ships * NUM_SHIPS_MULTIPLIER)


def assist(pw, planet, assistance):
    # type: (PlanetWars, Planet, int) -> None
    my_planets = pw.my_planets()  # type: list[Planet]
    assisting = my_planets[0]
    for my_planet in my_planets:
        if my_planet.planet_id() == planet.planet_id():
            continue
        if my_planet.num_ships() > assisting.num_ships():
            assisting = my_planet
    num_ships = int(min(ceil(assisting.num_ships() / 2), assistance))
    pw.issue_order(assisting, planet, num_ships)


def can_send(pw, planet):
    # type: (PlanetWars, Planet) -> (bool, int, int)
    enemy_fleets = pw.enemy_fleets()  # type: list[Fleet]
    enemy_ships_arrive = {}
    for enemy_fleet in enemy_fleets:
        if enemy_fleet.destination_planet() == planet.planet_id():
            if not enemy_ships_arrive.has_key(enemy_fleet.turns_remaining()):
                enemy_ships_arrive[enemy_fleet.turns_remaining()] = 0
            enemy_ships_arrive[enemy_fleet.turns_remaining()] += enemy_fleet.num_ships()
    my_fleets = pw.my_fleets()  # type: list[Fleet]
    my_ships_arrive = {}
    for my_fleet in my_fleets:
        if my_fleet.destination_planet() == planet.planet_id():
            if not my_ships_arrive.has_key(my_fleet.turns_remaining()):
                my_ships_arrive[my_fleet.turns_remaining()] = 0
            my_ships_arrive[my_fleet.turns_remaining()] += my_fleet.num_ships()
    cur_ships = planet.num_ships()
    min_max_send = cur_ships / 2
    for turns in enemy_ships_arrive.keys():
        turn = turns - 1
        enemy_ships_arriving = enemy_ships_arrive[turns]
        my_ships_arriving = 0
        try:
            my_ships_arriving = my_ships_arrive[turns]
        except:
            pass
        growth = turn * planet.growth_rate()
        future_ships = cur_ships + growth

        min_max_send = min(min_max_send, future_ships - enemy_ships_arriving)
        if cur_ships + growth < enemy_ships_arriving:
            return False, 0, enemy_ships_arriving - (cur_ships + growth + my_ships_arriving)
    return True, min_max_send, 0


def do_turn(pw):
    # type: (PlanetWars) -> None
    my_planets = pw.my_planets()            # type: list[Planet]
    neutral_planets = pw.neutral_planets()  # type: list[Planet]
    enemy_planets = pw.enemy_planets()      # type: list[Planet]

    my_fleets = pw.my_fleets()              # type: list[Fleet]
    enemy_fleets = pw.enemy_fleets()        # type: list[Fleet]

    my_fleets_ships = 0                     # type: int
    enemy_fleets_ships = 0                  # type: int

    my_plants_ships = 0                     # type: int
    enemy_plants_ships = 0                  # type: int

    my_ships = 0                            # type: int
    enemy_ships = 0                         # type: int

    for my_fleet in my_fleets:
        my_fleets_ships += my_fleet.num_ships()
    for enemy_fleet in enemy_fleets:
        enemy_fleets_ships += enemy_fleet.num_ships()

    for my_planet in my_planets:
        my_plants_ships += my_planet.num_ships()
    for enemy_planet in enemy_planets:
        enemy_plants_ships += enemy_planet.num_ships()

    my_ships = my_fleets_ships + my_plants_ships
    enemy_ships = enemy_fleets_ships + enemy_plants_ships

    if len(my_planets) == 0:
        return
    if float(my_fleets_ships) > my_ships * FLEET_PERCENTAGE:
        return
    if len(neutral_planets) > 0:
        for source in my_planets:
            should_send, amount, assistance = can_send(pw, source)
            if not should_send:
                if assistance > 0:
                    assist(pw, source, assistance)
                continue
            dest = neutral_planets[0]
            for neutral_planet in neutral_planets:
                if weight(pw, source, neutral_planet) > weight(pw, source, dest):
                    dest = neutral_planet

            num_ships = amount

            pw.issue_order(source, dest, num_ships)
    elif len(enemy_planets) > 0:
        for source in my_planets:
            should_send, amount, assistance = can_send(pw, source)
            if not should_send:
                if assistance > 0:
                    assist(pw, source, assistance)
                continue
            dest = enemy_planets[0]
            for enemy_planet in enemy_planets:
                if weight(pw, source, enemy_planet) > weight(pw, source, dest):
                    dest = enemy_planet

            num_ships = amount

            pw.issue_order(source, dest, num_ships)

