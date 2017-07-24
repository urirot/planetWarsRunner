turn = 0
def do_turn(pw):
    global turn
    turn = turn + 1
    if len(pw.my_planets()) == 0:
        return
    pw.debug(len(pw.enemy_planets()))
    if len(pw.enemy_planets())>1:
        #there is neutrul planets
        dest = pw.enemy_planets()[1]
        num = dest.num_ships()+1
        pw.debug(num)
        flag = False
        for x in pw.my_planets():
            pw.debug(x.num_ships())
            if x.num_ships() >= num:
                flag = True
                source = x
        pw.debug(flag)
        if flag:
            pw.issue_order(source, dest, num)
    #pw.debug(pw.distance(pw.my_planets()[0],minDis(pw.my_planets()[0],pw)))
    #elif turn == 999 - pw.distance(pw.my_planets()[0],minDis(pw.my_planets()[0],pw)):
    elif turn == 1000 - pw.distance(pw.my_planets()[0], minDis(pw.my_planets()[0],pw)):
        pw.issue_order(pw.my_planets()[0],minDis(pw.my_planets()[0],pw), minDis(pw.my_planets()[0],pw).num_ships() + 1)
		
def minDis(src,pw):
    min = pw.neutral_planets()[0]
    for planet in pw.neutral_planets():
        if pw.distance(planet, src) < pw.distance(min, src):
            pw.debug(pw.distance(min, src))
            min = planet
    return min