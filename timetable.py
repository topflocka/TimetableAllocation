from constraint import Problem

# Define courses and their respective hours per week
courses = {
    'Math': 3,
    'Physics': 2,
    'Chemistry': 4,
    # Add more courses as needed
}

# Define available time slots (e.g., hours in a week)
time_slots = range(1, 5)  # Assuming 24 hours/day, 7 days/week

# Create a problem instance
problem = Problem()

# Add variables (courses) and their domains (time slots)
for course, hours in courses.items():
    for i in range(3):
        problem.addVariable(course, time_slots)

# Define constraints
def no_overlap_constraint(*args):
    # Ensure no overlap by checking if any two courses have the same time slot
    return len(set(args)) == len(args)

def max_hours_per_week_constraint(*args):
    # Ensure that the sum of hours for each course does not exceed 3
    return sum(args) <= 3

# Add constraints
problem.addConstraint(no_overlap_constraint, list(courses.keys()))
problem.addConstraint(max_hours_per_week_constraint, list(courses.keys()))

# Solve the problem
solutions = problem.getSolutions()

# Print solutions
for solution in solutions:
    print(solution)