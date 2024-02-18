from constraint import Problem
from constraint import *

# Define courses and their respective hours per week
courses = {
    'CSC421': 3,
    'CSC422': 2,
    'CSC427': 4,
    "CSC426": 0,
    "CSC424": 0,
    "CSC428": 0,
    # Add more courses as needed
}

# Define available time slots (e.g., hours in a week)
time_slots = range(45)  # Assuming 24 hours/day, 7 days/week

# Create a problem instance
problem = Problem()
courses_full = []

# Add variables (courses) and their domains (time slots)
for course, hours in courses.items():
    for i in range(1, 4):
        courses_full.append(course + str(i))
        problem.addVariable(course + str(i), time_slots)
print(courses_full)

# Define constraints
def no_overlap_constraint(*args):
    # Ensure no overlap by checking if any two courses have the same time slot
    return len(set(args)) == len(args)

def max_hours_per_week_constraint(*args):
    # Ensure that the sum of hours for each course does not exceed 3
    return sum(args) <= 3

# Add constraints
problem.addConstraint(AllDifferentConstraint(), courses_full)
# problem.addConstraint(max_hours_per_week_constraint, list(courses.keys()))

# Solve the problem
# solutions = problem.getSolutions()
a = problem.getSolutionIter()
print(next(a))
# Print solutions
# for solution in solutions:
#     print(solution)
# print(a)