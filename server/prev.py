import constraint 
from flask import Flask, request, jsonify, abort
from flask_cors import CORS 
import json
import constraint
import time
from itertools import permutations

app = Flask(__name__)
CORS(app)
def break_or_next_course_constraint(course1, course2, break_period):
    # Ensure that a break or next course is inserted after at most 2 consecutive times for a course
    return (course1 + 2 == break_period) or (course1 + 1 == course2)


@app.route("/get-timetable")
def get_timetable():
    courses_data = request.args.get("data") 
    if courses_data:
        courseNames = json.loads(courses_data)
    else: 
        abort(400, "Bad request") 
        
    num_days = 5
    num_time_periods = 9
    max_course_hours = 3
    break_period = 6
    time_slots = range(num_days * num_time_periods) # 5 is the days of the week while 9 is the number of time slots in a day 
    problem = constraint.Problem()

    courses = []
    for course in courseNames:
        for i in range(max_course_hours):
            courses.append(course + "_" + str(i))
            problem.addVariable(course + "_" + str(i), time_slots)

    breaks = []
    for i in range(len(time_slots) - len(courses)):  # One less break than the number of courses
        breaks.append("break" + "_" + str(i))
        # problem.addVariable('break' + "_" + str(i), time_slots)

    #no two courses can clash constraint
    # problem.addConstraint(constraint.AllDifferentConstraint(), [*courses, *breaks])
    problem.addConstraint(constraint.AllDifferentConstraint(), [*courses])

    #no course can occur during break time 
    problem.addConstraint(constraint.NotInSetConstraint([break_period + num_time_periods * i for i in range(num_days)]), [*courses])

    # a course can only hold at most twice consecutively
    max_consecutive_courses = lambda *args: args[0] + 2 != args[2]
    for course in courseNames:
        same_course = []
        for i in range(max_course_hours):
            same_course.append(course + "_" + str(i))

        for i in permutations(same_course):
            problem.addConstraint(max_consecutive_courses, [*i])
    
    #even distribution of courses
    def evenly_distribute_courses(*args):
        bins = {i: 0 for i in range(num_days)}

        for course_slot in args:
            bins[course_slot // num_time_periods] += 1

        # print(bins)
            # Check if the difference in counts between days is within a tolerance
        tolerance = 1  # You may adjust this tolerance value as needed
        min_count = min(bins.values())
        max_count = max(bins.values())
        print(max_count)
        print(min_count)
        return max_count - min_count <= tolerance
    
    # problem.addConstraint(evenly_distribute_courses, [*courses])
    # problem.addConstraint(constraint.MaxSumConstraint(180), [*courses])

    # def test(*args):
    #     print(sum(args))
    #     return True
    # problem.addConstraint(test, [*courses])

    # courses_per_day = len(courses) // num_time_periods

    # problem.addConstraint(constraint.MinSumConstraint(450), [*courses])
    # problem.addConstraint(constraint.MaxSumConstraint(470), [*courses])

    solution_iter = problem.getSolutionIter()

    timetable = {}
    solution = next(solution_iter)
    print("solution")
    # print(solution)
    for course in solution: 
        courseName = course[:course.find("_")]

        # if courseName == "break":
        #     continue 

        if courseName not in timetable:
            timetable[courseName] = []
        timetable[courseName].append([solution[course] // num_time_periods, solution[course] % num_time_periods])
    print(solution)
    return jsonify(timetable)


app.run(debug=True)