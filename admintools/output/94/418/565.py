def do_turn(pw):
    """"""
    N_COUNT = 1.25
    E_COUNT = 1.25
    MAX_S = 0.9

    targeted_planets = list(pw.not_my_planets())
    # pw.debug(str(type(targeted_planets)))
    """
    if len(pw.my_fleets()) >= 1:
        return
    """

    if len(pw.my_planets()) == 0:
        return

    my_planets = sorted(pw.my_planets(), key=lambda planet: planet.num_ships(), reverse=True)

    there_is_more = True

    if len(my_planets) < 5:
        max_len = len(my_planets)
    else:
        max_len = 5

    max_len = len(my_planets)

    for source in my_planets[:max_len]:
        if source.num_ships() < 10:
            return
        for fleet in pw.my_fleets():
            # pw.debug(str(type(targeted_planets)))
            # pw.debug(str(targeted_planets[0]) + ", " + str(fleet.destination_planet()))
            if remove_planet_by_id(targeted_planets, fleet.destination_planet()):
                pw.debug("removed: " + str(fleet.destination_planet()))

        count = source.num_ships()
        there_is_more = True
        while there_is_more:
            dst = None
            if len(targeted_planets) >= 1:
                # dst = pw.neutral_planets()[0]
                sorted_planets = sorted(targeted_planets, key=lambda planet: pw.distance(planet, source))  # type: list

                sorted_planets = filter(lambda plan: plan.num_ships() < source.num_ships(), sorted_planets)
                if len(sorted_planets) == 0:
                    break
                dst = sorted_planets[0]
            else:
                return

            if dst.owner() == 0:  # neutral
                num_ships = int(dst.num_ships() * N_COUNT)
            elif dst.owner() == 2:  # enemy
                num_ships = cal_steps(pw, source, dst) * E_COUNT
                # num_ships = int(dst.num_ships() * E_COUNT)
                """if num_ships < int(0.3 * source.num_ships()):
                    num_ships = int(0.3 * source.num_ships())"""
            else:
                num_ships = int(dst.num_ships() * N_COUNT)

            if num_ships > count * MAX_S:
                # num_ships = int(source.num_ships() * MAX_S)
                break
            pw.debug('Num Ships: ' + str(num_ships))

            pw.issue_order(source, dst, num_ships)
            targeted_planets.remove(dst)
            count -= num_ships


def remove_planet_by_id(l, pid):
    """
    :param l:
    :type l: list
    :param pid:
    :type pid: int
    :return:
    """
    for p in l:
        if p.planet_id() == pid:
            l.remove(p)
            return True
    return False


def cal_steps(pw, src, dst):
    """
    :param pw:
    :param src:
    :param dst:
    :return:
    """
    return pw.distance(src, dst) * dst.growth_rate() + dst.num_ships()
