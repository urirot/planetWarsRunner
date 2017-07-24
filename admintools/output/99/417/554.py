def do_turn(pw):
    if not len(pw.my_planets()):
        return
    
    #For each friendly planet:
    for my_planet in pw.my_planets():
        threatning_ships = sum([x.num_ships() for x in pw.enemy_fleets() if x.destination_planet() == my_planet])
        dedicated_ships = my_planet.num_ships()-threatning_ships
        dedicated_ships = int(dedicated_ships/2)
        
        #Check for neutrals:
        neutrals = pw.neutral_planets()
        if len(pw.my_planets()) < 3:
            neutrals.sort(key=lambda planet:planet.growth_rate()-0.5*pw.distance(planet,my_planet),reverse=True)
        else:
            neutrals.sort(key=lambda planet:planet.growth_rate(),reverse=True)
        sent_to_neutral = False
        for planet in neutrals:
            my_fleets_sum = sum([x.num_ships() for x in pw.my_fleets() if x.destination_planet() == planet])
            enemy_fleets_sum = sum([x.num_ships() for x in pw.enemy_fleets() if x.destination_planet() == planet])
            needed_ships = max((enemy_fleets_sum + planet.num_ships()- my_fleets_sum),0)
            if dedicated_ships >= needed_ships + 1:
                pw.issue_order(my_planet,planet,needed_ships+1)#Just barely to conquer
                sent_to_neutral = True
                break

        if sent_to_neutral:
            return

        enemies = pw.enemy_planets()
        enemies.sort(key=lambda planet:planet.growth_rate(),reverse=True)
        for planet in enemies:
            my_fleets_sum = sum([x.num_ships() for x in pw.my_fleets() if x.destination_planet() == planet])
            enemy_fleets_sum = sum([x.num_ships() for x in pw.enemy_fleets() if x.destination_planet() == planet])
            needed_ships = max((enemy_fleets_sum + planet.num_ships() + planet.growth_rate()*max([0]+[x.turns_remaining() for x in pw.my_fleets() if x.destination_planet() == planet]) - my_fleets_sum),0)
            
            if dedicated_ships >= needed_ships + 1:
                pw.issue_order(my_planet,planet,needed_ships+1)#Just barely to conquer
                break
