def do_turn(pw):

    if len(pw.my_planets()) == 0:
        return

    source = pw.my_planets()[0]
    for i in pw.my_planets():
        if i.num_ships() > source.num_ships():
            source = i
    num_ships = pw.my_planets()[0].num_ships() / 2
    if num_ships < 40:
        return
    if len(pw.not_my_planets())>0:
        max = 1
        z= pw.planets()[0]
        for x in (pw.not_my_planets()):
            if x.num_ships() < num_ships:
               if x.growth_rate()>max:
                   max = x.growth_rate()
                   z=x
        dest = z
    pw.issue_order(source,dest,num_ships)