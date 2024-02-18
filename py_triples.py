from constraint import * 
problem = Problem()
problem.addVariable("a", range(16))
problem.addVariable("b", range(16))
problem.addVariable("c", range(16))
problem.addConstraint(lambda a, b, c: (a**2 + b**2) == (c**2), ["a", "b", "c"])
# problem.addConstraint(lambda a, b, c: (a != 0 and b != 0 and c != 0), ["a", "b", "c"] )
problem.addConstraint(AllDifferentConstraint())

print(problem.getSolutions())