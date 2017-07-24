import sys
import os
import importlib

from PlanetWars import PlanetWars

def main():
    pw = PlanetWars('')
    do_turn(pw)

def do_turn(pw):

    if len(pw.enemy_planets()) != 0:

        if len(pw.my_fleets()) >= 1:
            return

        if len(pw.my_planets()) == 0:
            return

        source = pw.my_planets()[0]
        dest = pw.enemy_planets()[0]

        nPlanetList = pw.neutral_planets()
        pw.debug(len(nPlanetList))

        if len(nPlanetList) >= 1:
            SortedNPList = sorted(nPlanetList, key=lambda planet: planet.growth_rate(), reverse=False)
            SortedMYPList = sorted(pw.my_planets(), key=lambda planet: planet.num_ships(), reverse=True)
            for planet in SortedNPList:
                if(planet.num_ships() * 2) < SortedMYPList[0].num_ships():
                    dest = planet
                    source = SortedMYPList[0]
                    pass
        else:
            if len(pw.enemy_planets()) >= 1:
                SortedEPList = sorted(pw.enemy_planets(), key=lambda planet: planet.growth_rate(), reverse=False)
                SortedMYPList = sorted(pw.my_planets(), key=lambda planet: planet.num_ships(), reverse=True)
                for planet in SortedEPList:
                    if(planet.num_ships() * 2) < SortedMYPList[0].num_ships():
                        dest = planet
                        source = SortedMYPList[0]
                        pass

        num_ships = source.num_ships() / 2

        pw.issue_order(source, dest, num_ships)

if __name__ == '__main__':
	main()