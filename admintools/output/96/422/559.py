def do_turn(pw):
    if len(pw.my_fleets()) >= 1:
        return

    if len(pw.my_planets()) == 0:
        return

    if(pw.my_planets().__len__() < 3):

        my_main_planet = pw.my_planets()[0]

        best_score_n = 10000000
        best_ne_planet = 0

        for planet in pw.not_my_planets():
            if (pw.distance(planet, my_main_planet) < best_score_n):
                best_score_n = pw.distance(planet, my_main_planet)
                best_ne_planet = planet

        if (best_ne_planet != 0):
                all_planets_attack_this(pw, best_ne_planet)

        return

    enemy_fleets = pw.enemy_fleets()
    if(enemy_fleets.__len__() > 0):
        for en_fleet in enemy_fleets:
            pw.debug('Num Ships: ' + str(pw.get_planet(en_fleet.destination_planet()).owner()))
            if( pw.get_planet(en_fleet.destination_planet()).owner() == 1):
                #Relevant
                planet_to_protect = pw.get_planet(en_fleet.destination_planet())
                planet_to_attack = pw.get_planet(en_fleet.source_planet())
                best_planet = 0
                best_score_P = 0
                if(pw.my_planets().__len__() > 1):
                    for planet in pw.my_planets():
                        if(planet == planet_to_protect):
                            continue
                        score_P = pw.distance(planet, planet_to_protect)/float(planet.growth_rate()*planet.num_ships()+1)
                        if(score_P < best_score_P):
                            best_score_P = score_P
                            best_planet = planet

                    for planet in pw.my_planets()[::2]:
                        amount = planet_to_protect.num_ships() + 100
                        if (planet.num_ships() >= amount):
                            amount = planet_to_protect.num_ships() + 100
                        else:
                            amount = planet.num_ships()
                        pw.issue_order(planet, planet_to_protect, int(amount))

                    for planet in pw.my_planets()[1::2]:
                        amount = planet_to_attack.num_ships() + 100
                        if (planet.num_ships() >= amount):
                            amount = planet_to_attack.num_ships() + 100
                        else:
                            amount = planet.num_ships()
                        pw.issue_order(planet, planet_to_attack, int(amount))

                    return

    if(pw.my_planets().__len__() < pw.enemy_planets().__len__()):
        #Attack strongest point of enemy and then immediately start conquering more
        if(pw.my_planets().__len__() >= int(pw.enemy_planets().__len__()*0.4)  or pw.neutral_planets().__len__() == 0):
            best_planet = 0
            best_growth = 0
            for planet in pw.enemy_planets():
                if planet.growth_rate() > best_growth:
                    best_growth = planet.growth_rate()
                    best_planet = planet
            if(best_planet != 0):
                all_planets_attack_this(pw, best_planet)
                return
    best_score = 0
    best_my_planet = 0

    best_score_n = 10000000
    best_ne_planet = 0

    for planet in pw.not_my_planets():
        if(planet.num_ships() < best_score_n):
            best_score_n = planet.num_ships()
            best_ne_planet = planet

    if(best_ne_planet != 0):
        all_planets_attack_this(pw, best_ne_planet)
        return


def all_planets_attack_this(pw, target):
    for planet in pw.my_planets():
        amount = target.num_ships()+100
        if(planet.num_ships() >= amount):
            amount = target.num_ships()+100
        else:
            amount = planet.num_ships()
        pw.issue_order(planet, target, int(amount))