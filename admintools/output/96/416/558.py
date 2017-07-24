from math import ceil
from PlanetWars import Planet

distances = []
nearestNeighbors = []

def distance(p1id, p2id):
  if isinstance(p1id, Planet) and isinstance(p2id, Planet):
    return distances[p1id.planet_id()][p2id.planet_id()][1]
  return distances[p1id][p2id][1]

def ComputePlanetdistances(pw):
  Planets = sorted(pw.planets(), key=lambda x: x.planet_id())
  for p in Planets:
    dists = []
    for q in Planets:
      dists.append((q.planet_id(), pw.distance(p,q)))
    nearestNeighbors.append(sorted(dists, key=lambda x: x[1]))
    distances.append(dists)

class Planetsim:
  """Useful for predicting the future state of a Planet based on
  incoming fleets
  Always uses the convention that my ships and Planets are positive
  Enemy and neutral are negative.
  """
  def __init__(self, startingShips, rate, isNeutral):
    if isNeutral:        
      self.startingShips = 0
      self.neutralShips = startingShips
    else:
      self.startingShips = startingShips
      self.neutralShips = 0        
    self.rate = rate
    self.fleets = []
  def addFleet(self, turn, num_ships):
    self.fleets.append((turn, num_ships))
  def delFleet(self, turn, num_ships):
    self.fleets.remove((turn, num_ships))
  def findMinFleetOwn(self, turn):
    # what if we do nothing
    left = self.simulate()
    if left > 0: # Already have it
      return 0
    currFleetSize = 0
    while left < 0:
      # May have to adjust increment to prevent timeout
      currFleetSize += 4
      self.addFleet(turn, currFleetSize)
      left = self.simulate()        
      #debug("currfleet: " + str(currFleetSize) + " left: " + str(left))
      self.delFleet(turn, currFleetSize)
    if left == 0:
        currFleetSize += 1
    return currFleetSize
  def findMaxExpenditureWhileKeeping(self):
    """ Assumes we own the Planet in question """
    # May have to adjust increment to prevent timeout
    increment = 4
    # what if we do nothing?  
    left = self.simulate()
    # we're gonna lose it, can't spend a dime
    if left <= 0:
      return 0
    else:
      startingShips = self.startingShips  
      maxSpend = 0
      while left > 0:
        # can't spend more than you have
        if maxSpend + increment >= startingShips:
          break
        maxSpend += increment
        if startingShips <= increment:
          break
        self.startingShips -= maxSpend
        left = self.simulate()
        # restore startingShips state
        self.startingShips = startingShips
      # check if we failed on last simulation
      # if so, take 2 back
      if left <= 0:
        return maxSpend - increment
      return maxSpend    
  def simulate(self):
    """After all fleets have come in, how many ships does the
    Planet have?"""
    def reducedFleets():
      """Reduce the fleets so that if multiple fleets happen on
      the same turn, there combined effect is reduced to one
      event"""
      reduced = []
      fleets = sorted(self.fleets, key=lambda x: x[0])
      currTurn = 0
      reducedValue = 0
      for e in fleets:
        if e[0] == currTurn:
          reducedValue += e[1]
        else:
          reduced.append((currTurn,reducedValue))
          reducedValue = e[1]
          currTurn = e[0]
      if reducedValue:
        reduced.append((currTurn, reducedValue))
      return reduced
    currTurn = 0
    ships = self.startingShips
    neuShips = self.neutralShips
    for e in reducedFleets():
      remain = e[1]
      #debug("fleetSize: " + str(remain))
      # Remove Neutrals if any
      if neuShips < 0:
        if abs(remain) >= abs(neuShips):
          if remain > 0:
            remain += neuShips
          else:
            remain -= neuShips
          neuShips = 0
          currTurn = e[0]
        else:
          neuShips += abs(remain)
          remain = 0
      # If there are no neutrals, update Planet
      # and apply remaining fleet
      if neuShips == 0 and remain != 0:
        turns = e[0] - currTurn
        #debug("turns:" + str(turns) + " remain: " + str(remain))
        if ships >= 0:
          ships = ships + self.rate*turns + remain            
        else:
          ships = ships - self.rate*turns + remain
      # Update turn
      #debug("ships: " + str(ships))
      currTurn = e[0]      
    if neuShips:
      return neuShips
    else:
      return ships

def BreakEvenTurns(pw, Planet, fleetdistance):
  """Returns number of turns it will take to break even on
  taking this Planet.
  """
  if Planet.growth_rate() == 0:
#    debug("wtf, ZERO GROWTH on " + str(Planet.planet_id()))
    return 100000
  cost = FleetRequiredToTake(pw, Planet, fleetdistance)
  # if it is already being taken, then we won't break even
  if cost <= 0:
#    debug(str(Planet.planet_id()) + " already being taken")
    return 100000
  if Planet.owner() == 2:
    # enemy Planets pay back in half the time
    # because there is the growth that the enemy didn't get
    # plus the growth that I did get
    returnRate = 2*float(Planet.growth_rate())
  else:
    returnRate = float(Planet.growth_rate())
  return int(ceil(cost / returnRate))

def FleetRequiredToTake(pw, Planet, fleetdistance):
  """Returns the exact size of a fleet required to take the given
  Planet.
  """
  sim = Planetsim(-Planet.num_ships(), Planet.growth_rate(), Planet.owner()==0)
  for f in pw.fleets():
    if f.destination_planet() == Planet.planet_id():
      if f.owner() == 2:
        sim.addFleet(f.turns_remaining(), -f.num_ships())
      else:
        sim.addFleet(f.turns_remaining(), f.num_ships())
  minFleet = sim.findMinFleetOwn(fleetdistance)
  return minFleet

def GeneralDefenseRequired(pw, Planet):
  """How many reserves do I need if the nearest enemies send everything"""
  defense = 0
  rate = Planet.growth_rate()
  neighbors = nearestNeighbors[Planet.planet_id()]
  for n in neighbors:
    # If enemy and can hit me in 15 turns or less
    p = pw.get_planet(n[0])
    if n[1] < 15 and p.owner() == 2:
      defense += p.num_ships() - rate*distance(n[0], Planet.planet_id())
  defense = int(ceil(defense))
#  debug("GeneralDefenseRequired Planet " + str(Planet.planet_id()) + " " + str(defense))
  return defense

def DefenseRequiredForIncoming(pw, Planet):
  """How many reserves do I need to leave to protect me from the
  incoming waves?"""
  sim = Planetsim(Planet.num_ships(), Planet.growth_rate(), Planet.owner()==0)
  for f in pw.fleets():
    if f.destination_planet() == Planet.planet_id():
      if f.owner() == 2:
        sim.addFleet(f.turns_remaining(), -f.num_ships())
      else:
        sim.addFleet(f.turns_remaining(), f.num_ships())
  required = Planet.num_ships() - sim.findMaxExpenditureWhileKeeping()
#  debug(str(required) + " required to defend " + str(Planet.planet_id()) + " from incoming ")
  return required

def do_turn(pw):
  orders = []
  urgentPlanets = []
  my_Planets = []
  enemyTargets = []
  enemy_planets = pw.enemy_planets()
  neutral_planets = pw.neutral_planets()
  my_fleets = pw.my_fleets()
  enemy_fleets = pw.enemy_fleets()
  enemySize = 0
  mySize = 0

  # InterPlanetary distances will come in handy
  if not distances:
    ComputePlanetdistances(pw)
	
  for p in pw.my_planets():
    mySize = mySize + p.num_ships()
    defInc = DefenseRequiredForIncoming(pw, p)
    # Who needs help urgently, and how much?
    if p.num_ships() < defInc:
      urgentPlanets.append((p, defInc))
    else:
      my_Planets.append((p, int(ceil(.75*GeneralDefenseRequired(pw, p)))))

  # How is the enemy doing?
  for p in enemy_planets:
    enemySize = enemySize + p.num_ships()

  if ( enemySize <= 0 ):
    winRatio = 0
  else:
    winRatio = float(mySize)/enemySize

  # Defend myself first
  # some urgent Planets are more urgent
  urgentPlanets.sort(key=lambda x: x[0].growth_rate(), reverse=True)  
  for helpme in urgentPlanets:
    totalNeeded = helpme[1]
    helpsofar = 0
    plannedSend = []
    # Make a defense plan. Prefer close help
    for helper in sorted(my_Planets, key=lambda x: distance(x[0],helpme[0])):
      # Don't undefend yourself      
      tosend = helper[0].num_ships()
      defReq = helper[1]
      if defReq > 0:
        tosend -= defReq
      if tosend <= 0:
        continue        
      # Only send what is still needed
      stillNeeded = totalNeeded - helpsofar
      if tosend > stillNeeded:
        tosend = stillNeeded
      plannedSend.append((helper[0], helpme[0], tosend))
      helpsofar += tosend
      if helpsofar >= totalNeeded:
        break
    # issue actual orders
    if helpsofar >= totalNeeded:
      for p in plannedSend:
        pw.issue_order(p[0], p[1], p[2])
        remaining = p[0].num_ships()-p[2]
        orders.append(p)
        p[0].num_ships(remaining)
    # else, TODO: this Planet is BONED until I fix

  # Maximize investments, Minimize enemy
  if winRatio >= 1.5:
    targets = enemy_planets
  else:
    targets = enemy_planets+neutral_planets
  for taker in my_Planets:
    defenseReq = max(DefenseRequiredForIncoming(pw, taker[0]), \
                     int(ceil(.10*GeneralDefenseRequired(pw, taker[0]))))
    surplus = taker[0].num_ships()
    if defenseReq > 0:
      surplus -= defenseReq
    potTargets = []    
    # Calculate investement risks for this tak
    for p in targets:
      dist = distance(p.planet_id(), taker[0].planet_id())
      breakEvenTurns = BreakEvenTurns(pw, p, dist)
      potTargets.append((p, breakEvenTurns))
    # Prefer lower risk, take as many targets as possible
    potTargets.sort(key=lambda x: x[1])
    for potTarget in potTargets:
      needed = FleetRequiredToTake(pw, potTarget[0], \
                                    distance(potTarget[0].planet_id(), p.planet_id()))
      isenemy = False
      if potTarget[0].owner() == 2:
        isenemy = True
      
        
      # take if we can
      if needed > 0 and surplus > needed:
        pw.issue_order(taker[0], potTarget[0], needed)
        remaining = taker[0].num_ships() - needed
        taker[0].num_ships(remaining)
        surplus -= needed
        # remove this from the targets list
        for t in targets:
          if t.planet_id() == potTarget[0].planet_id():
            targets.remove(t)
            break
      elif surplus <= 0:
        break