def do_turn(pw):
    for p in pw.my_planets():
        destination = dis(pw, p)
        if p and destination:
            n_ships = get_num_ships(p, destination)
            pw.issue_order(p, destination, n_ships)


def dis(pw, my_planet):
    lst = sorted(pw.not_my_planets(), key=lambda x: pw.distance(x, my_planet))
    pw.debug(str([pw.distance(i, my_planet) for i in lst]))
    if lst:
        return lst[0]
    else:
        return


def get_num_ships(src, dst):
    if src.num_ships() > dst.num_ships():
        return dst.num_ships() + 1
    else:
        return src.num_ships()