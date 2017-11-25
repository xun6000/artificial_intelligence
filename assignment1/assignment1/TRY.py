import util, submission
ucs = util.UniformCostSearch(verbose=1)
scenario = util.deliveryScenario1
ucs.solve(submission.DeliveryProblem(scenario))
scenario.simulate(ucs.actions, True)
print ucs.numStatesExplored,"NUMBER OS STATES, EXPLORED"