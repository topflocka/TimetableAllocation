from constraint import Problem
from constraint import *

# Define courses and their respective hours per week
course_details = {
    'CSC421': 3,
    'CSC422': 2,
    'CSC427': 4,
    "CSC426": 0,
    "CSC424": 0,
    "CSC428": 0,
    # Add more courses as needed
}

# Define available time slots (e.g., hours in a week)
time_slots = range(9*5)  # Assuming 24 hours/day, 7 days/week

# Define break duration (in hours)
break_duration = 1

# Create a problem instance
problem = Problem()
courses = []

# Add variables (courses) and their domains (time slots)
for course, hours in course_details.items():
    for i in range(3):
        courses.append(course + str(i))
        problem.addVariable(course + str(i), time_slots)

breaks = []
# Add variables (break periods)
for i in range(len(time_slots) - len(courses)):  # One less break than the number of courses
    breaks.append("break" + str(i))
    problem.addVariable('break' + str(i), time_slots)
print([*breaks, *courses])

# Define constraints
def no_overlap_constraint(*args):
    # Ensure no overlap by checking if any two courses have the same time slot
    return len(set(args)) == len(args)

# def break_or_next_course_constraint(course1, course2, break_period):
#     # Ensure that a break or next course is inserted after at most 2 consecutive times for a course
#     return (course1 + 1 == course2) or (course1 + 2 == break_period)

def break_or_next_course_constraint(course1, course2, break_period):
    # Ensure that a break or next course is inserted after at most 2 consecutive times for a course
    return (course1 + 2 == break_period) or (course1 + 1 == course2)

# Add constraints
# problem.addConstraint(no_overlap_constraint, list(courses.keys()))

# for i, (course1, course2) in enumerate(zip(courses, courses[1:])):
#     problem.addConstraint(break_or_next_course_constraint, [course1 + str(courses[course1] - 1), course2 + '0', 'break' + str(i)])

def evenly_distribute_courses(*args):
        bins = {i: 0 for i in range(5)}

        for course_slot in args:
            bins[course_slot // 9] += 1

        # print(bins)
            # Check if the difference in counts between days is within a tolerance
        tolerance = 1  # You may adjust this tolerance value as needed
        min_count = min(bins.values())
        max_count = max(bins.values())
        # print(max_count)
        # print(min_count)
        return max_count - min_count <= tolerance

problem.addConstraint(evenly_distribute_courses, [*courses])

for course in course_details.keys():
    # for i in range(courses[course] - 1): # number of hours
    for i in range(2): # number of hours
        problem.addConstraint(break_or_next_course_constraint, [course + str(i), course + str(i + 1), 'break' + str(i)])

problem.addConstraint(AllDifferentConstraint(), [*courses, *breaks])

# Solve the problem
# solutions = problem.getSolutions()
a = problem.getSolutionIter()
print(next(a))
# Print solutions
# for solution in solutions:
#     print(solution)
# print(len(solutions))