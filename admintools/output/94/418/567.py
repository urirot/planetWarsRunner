from random import randint
import math

handeled_planets = []

def order_planets(pw):
    dsts = [x for x in pw.neutral_planets() + pw.enemy_planets() if x not in handeled_planets]
    s = sorted(dsts, key=lambda c: c.num_ships())
    return s

def find_close(pw, planet) : 
    fx = planet.x()
    fy = planet.y()
    mindis = 1000000000000
    nearpla = pw.my_planets()[0]
    for pla in pw.my_planets():
        if math.hypot(fx - pla.x(), fy - pla.y()) < mindis : 
            mindis = math.hypot(fx - pla.x(), fy - pla.y())
            nearpla = pla
    return pla
    

def do_turn(pw):
    global handeled_planets

    if len(pw.my_planets()) == 0:
        return
    
    dst = (order_planets(pw) or [None])[0] #pw.neutral_planets()[randint(0, len(pw.neutral_planets()) - 1)]
    if not dst:
        return
    
    src = pw.my_planets()[randint(0, len(pw.my_planets()) - 1)]

    pw.issue_order(src, dst, min(dst.num_ships() + 1, src.num_ships()))
    handeled_planets.append(dst)

    handeled_planets = [x for x in handeled_planets if x not in pw.my_planets()]