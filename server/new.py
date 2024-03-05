import constraint 
from flask import Flask, request, jsonify, abort
from flask_cors import CORS 
import json
import constraint
from itertools import permutations, cycle, repeat
import random 

app = Flask(__name__)
CORS(app)

def break_or_next_course_constraint(course1, course2, break_period):
    # Ensure that a break or next course is inserted after at most 2 consecutive times for a course
    return (course1 + 2 == break_period) or (course1 + 1 == course2)

def breakk(course, *breaks):
    print(course, breaks)
    return course + 1 in breaks

def evenly_distribute_courses(num_day, num_courses):
    problem = constraint.Problem()
    variables = range(num_day)
    problem.addVariables(variables, range(0, num_courses))

    problem.addConstraint(constraint.ExactSumConstraint(num_courses), variables)

    def evenly_distribute_courses(*args):
        tolerance = 1  # You may adjust this tolerance value as needed
        min_count = min(args)
        max_count = max(args)
        return max_count - min_count <= tolerance
    problem.addConstraint(evenly_distribute_courses, variables)
    
    return problem.getSolution().values()

@app.route("/get-timetable")
def get_timetable():
    courses_data = request.args.get("data") 
    
    if courses_data:
        course_names = json.loads(courses_data)
    else: 
        abort(400, "Bad request") 
    
    num_days = 5
    num_time_periods = 9
    max_consecutive_hours = 2
    max_course_hours = 3
    break_period = 6
    time_slots = range(num_days * num_time_periods) # 5 is the days of the week while 9 is the number of time slots in a day 
    problem = constraint.Problem()

    courses = []
    
    reverse_array = lambda x, cond: x[::-1] if cond else x    
    
    # this code inserts courses in a way that allows the same course to occur multiple times in the same day limited by their max consecutive hours
    for i, c in enumerate(repeat(course_names, max_course_hours // max_consecutive_hours + 1)):
        offset = i * max_consecutive_hours
        for j, course in enumerate(reverse_array(c, i % 2)):
            for k in range(min(max_consecutive_hours, max_course_hours - offset)):
                courses.insert(j * 2, course + "_" + str(k + offset))

    # ensures an even distribution of courses in a week using round robin scheduling 
    ND = len(courses) // num_days + 1
    CD = evenly_distribute_courses(num_days, len(courses)) #CD is the how the courses should distribute across the week
    CD = list(CD)
    j = 0
    for i in range(num_days):
        problem.addVariables(courses[j:j+CD[i]], 
                             range(i*num_time_periods + num_time_periods - 1, i*num_time_periods - 1, -1))
        j += CD[i]

    # problem.addVariables([*courses], range(num_days * num_time_periods))

    #no two courses can clash constraint
    # problem.addConstraint(constraint.AllDifferentConstraint(), [*courses, *breaks])
    problem.addConstraint(constraint.AllDifferentConstraint(), [*courses])

    #no course can occur during break time 
    problem.addConstraint(constraint.NotInSetConstraint([break_period + num_time_periods * i for i in range(num_days)]), [*courses])

    # problem.addConstraint(constraint.MinSumConstraint(400), [*courses])
    # for course in courses:
    #     # problem.addConstraint(lambda course, *breaks: course+1 in breaks, [course, *breaks])
    #     problem.addConstraint(breakk, [course, *breaks])
    
    solution_iter = problem.getSolutionIter()

    timetable = {}
    solution = next(solution_iter)
    for course in solution: 
        courseName = course[:course.find("_")]

        if courseName not in timetable:
            timetable[courseName] = []
        timetable[courseName].append([solution[course] // num_time_periods, solution[course] % num_time_periods])
    print(solution)
    return jsonify({"status": "success", "message": "timetable successfully generated", "data": timetable})

@app.errorhandler(Exception)
def handle_exception(error):
    # Log the exception
    app.logger.error(f'An error occurred: {str(error)}')

    # Return a JSON response with error message
    return jsonify({"status": "error", 'message': 'Internal Server Error'}), 500


app.run(debug=True)