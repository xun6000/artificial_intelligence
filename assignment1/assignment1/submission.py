import re, util

############################################################
# Problem 1a: UCS test case

# Return an instance of util.SearchProblem.
# You might find it convenient to use
# util.createSearchProblemFromString.
def createUCSTestCase(n):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    newgraphstr = ""
    for i in range(n):
        newgraphstr += ("a " + "n" + str(i) + " " + str(i) + "\n")
    # print newgraphstr
    return util.createSearchProblemFromString("a", "n" + str(n - 1), newgraphstr)

    #raise Exception("Not implemented yet")
    # END_YOUR_CODE
import util
ucs = util.UniformCostSearch(verbose=3)
ucs.solve(util.trivialProblem)





############################################################
# Problem 1b: A-star search

# Takes the SearchProblem |problem| you're trying to solve and a |heuristic|
# (which is a function that maps a state to an estimate of the cost to the
# goal).  Returns another search problem |newProblem| such that running uniform
# cost search on |newProblem| is equivalent to running A* on |problem| with
# |heuristic|.
def astarReduction(problem, heuristic):
    class NewSearchProblem(util.SearchProblem):
        # Please refer to util.SearchProblem to see the functions you need to
        # overried.
        # BEGIN_YOUR_CODE (around 9 lines of code expected)
        def __init__(self):
            self.new = problem
            # self.old_heuristic = heuristic
        def startState(self):
            return self.new.startState()
        def isGoal(self, state):
            return self.new.isGoal(state)
        def succAndCost(self, state):
            ans = []
            for action, newstate, cost in self.new.succAndCost(state):
                newcost = cost + heuristic(newstate) - heuristic(state)
                ans.append((action, newstate, newcost))
            return ans
        #raise Exception("Not implemented yet")
        # END_YOUR_CODE
    newProblem = NewSearchProblem()
    return newProblem

# Implements A-star search by doing a reduction.
class AStarSearch(util.SearchAlgorithm):
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, problem):
        # Reduce the |problem| to |newProblem|, which is solved by UCS.
        newProblem = astarReduction(problem, self.heuristic)
        algorithm = util.UniformCostSearch()
        algorithm.solve(newProblem)

        # Copy solution back
        self.actions = algorithm.actions
        if algorithm.totalCost != None:
            self.totalCost = algorithm.totalCost + self.heuristic(problem.startState())
        else:
            self.totalCost = None
        self.numStatesExplored = algorithm.numStatesExplored

############################################################
# Problem 2b: Delivery

class DeliveryProblem(util.SearchProblem):
    # |scenario|: delivery specification.
    def __init__(self, scenario):
        self.scenario = scenario

    # Return the start state.
    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        self.startLocation = self.scenario.truckLocation
        self.statuses = ['ready' for i in range(self.scenario.numPackages)]
        return (self.startLocation, tuple(self.statuses))
        # END_YOUR_CODE

    # Return whether |state| is a goal state or not.
    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        if state[0] == self.startState()[0] :
            if state[1] == tuple(['done'] * self.scenario.numPackages):
                return True
            else:
                return False
        else:
            return False

        # END_YOUR_CODE

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state):
        # Hint: Call self.scenario.getNeighbors((x,y)) to get the valid neighbors
        # at that location. In order for the simulation code to work, please use
        # the exact strings 'Pickup' and 'Dropoff' for those two actions.
        # BEGIN_YOUR_CODE (around 18 lines of code expected)

        packagestatus = list(state[1])
        noftranspack = packagestatus.count('transit')
        ans = []
        cost = noftranspack + 1
        for action, newposition in self.scenario.getNeighbors((state[0])):
            ans.append((action, (newposition, state[1]), cost))
        x, y = state[0]
        pickup = packagestatus[:]
        dropoff = packagestatus[:]
        nofdroppack = 0
        nofpickpack = 0
        for package, loc in enumerate(self.scenario.dropoffLocations):
            if loc == (x, y) and dropoff[package] == 'transit':
                nofdroppack = nofdroppack + 1
                dropoff[package] = 'done'

        for package, loc in enumerate(self.scenario.pickupLocations):
            if loc == (x, y) and pickup[package] == 'ready':
                nofpickpack = nofpickpack + 1
                pickup[package] = 'transit'
        for i in range(nofpickpack):
            ans.append(('Pickup', (state[0], tuple(pickup)), 0))
        for i in range(nofdroppack):
            ans.append(('Dropoff', (state[0], tuple(dropoff)), 0))

        # print "succAndCost old state: ", state, "---->", result
        return ans
        # END_YOUR_CODE





############################################################
# Problem 2c: heuristic 1


# Return a heuristic corresponding to solving a relaxed problem
# where you can ignore all barriers and not do any deliveries,
# you just need to go home
def createHeuristic1(scenario):
    def heuristic(state):
        #print state,((1, 6), ('ready',))
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        noftranspack = list(state[1]).count('transit')
        start_location = scenario.truckLocation
        return (abs(start_location[0] - state[0][0]) + abs(start_location[1] - state[0][1])) * (noftranspack + 1)
        # END_YOUR_CODE
    return heuristic

############################################################
# Problem 2d: heuristic 2

# Return a heuristic corresponding to solving a relaxed problem
# where you can ignore all barriers, but
# you'll need to deliver the given |package|, and then go home
def createHeuristic2(scenario, package):

    def heuristic(state):
        #print state #here we have two pacakage
        # BEGIN_YOUR_CODE (around 11 lines of code expected)
        # the package will gothrough all the numbers
        #print state #(pisition) and status of packages((1, 4), ('done', 'done'))
        oldStatuses = list(state[1]) #('done', 'done')
        # print state
        # print "pack",package
        start_location = scenario.truckLocation
        current_location = state[0]
        pickup_cost = 0
        dropoff_cost = 0
        back_to_start_cost = 0
        #print scenario.dropoffLocations,"loc"
        dropoff_location = scenario.dropoffLocations[package]
        pickup_location = scenario.pickupLocations[package]

        if oldStatuses[package] == 'ready':
            ntp = 0
            pickup_cost = (abs(current_location[0] - pickup_location[0]) + abs(current_location[1] - pickup_location[1])) * (
            ntp + 1)
            dropoff_cost = (abs(pickup_location[0] - dropoff_location[0]) + abs(pickup_location[1] - dropoff_location[1])) * (
            ntp + 1 + 1)
            back_to_start_cost = (abs(start_location[0] - dropoff_location[0]) + abs(start_location[1] - dropoff_location[1])) * (
            ntp + 1)
        elif oldStatuses[package] == 'done':
            ntp = 0
            back_to_start_cost = (abs(start_location[0] - current_location[0]) + abs(
                start_location[1] - current_location[1])) * (ntp + 1)
        elif oldStatuses[package] == 'transit':
            ntp = 1
            dropoff_cost = (abs(current_location[0] - dropoff_location[0]) + abs(current_location[1] - dropoff_location[1])) * (
            ntp + 1)
            back_to_start_cost = (abs(start_location[0] - dropoff_location[0]) + abs(start_location[1] - dropoff_location[1])) * (
            ntp)
        totalcost = pickup_cost + dropoff_cost + back_to_start_cost
        return totalcost
        # END_YOUR_CODE
    return heuristic

############################################################
# Problem 2e: heuristic 3

# Return a heuristic corresponding to solving a relaxed problem
# where you will delivery the worst(i.e. most costly) |package|,
# you can ignore all barriers.
# Hint: you might find it useful to call
# createHeuristic2.
def createHeuristic3(scenario):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    def heuristic(state):
        # print "checking heuristic of state:",state
        maxx = 0
        #print state
        for i in range(scenario.numPackages):
            cur_package_heuristic = createHeuristic2(scenario, i)
            package_cost = cur_package_heuristic(state)
            maxx = max(package_cost,maxx)

        return maxx
    return heuristic
    # END_YOUR_CODE
