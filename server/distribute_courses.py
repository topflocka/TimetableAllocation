from constraint import Problem, ExactSumConstraint

num_day = 5
num_courses = 10

problem = Problem()
variables = range(num_day)
problem.addVariables(variables, range(0, num_courses))

problem.addConstraint(ExactSumConstraint(num_courses), variables)

def evenly_distribute_courses(*args):
    tolerance = 1  # You may adjust this tolerance value as needed
    min_count = min(args)
    max_count = max(args)
    return max_count - min_count <= tolerance
problem.addConstraint(evenly_distribute_courses, variables)

print(problem.getSolutions())