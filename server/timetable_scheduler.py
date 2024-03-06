import constraint 
from flask import Flask, request, jsonify, abort
from flask_cors import CORS 
import json
import constraint
from itertools import permutations

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return json({"status": "success", "message": "Server is up and running"}), 200

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
    problem = constraint.Problem(constraint.MinConflictsSolver())

    courses = []
    for course in courseNames:
        for i in range(max_course_hours):
            courses.append(course + "_" + str(i))
            problem.addVariable(course + "_" + str(i), time_slots)

    #no two courses can clash constraint
    problem.addConstraint(constraint.AllDifferentConstraint(), [*courses])

    #no course cannot occur during break time 
    problem.addConstraint(constraint.NotInSetConstraint([break_period + num_time_periods * i for i in range(num_days)]), [*courses])

    # a course can only hold at most twice consecutively
    max_consecutive_courses = lambda *args: args[0] + 2 != args[2]
    for course in courseNames:
        same_course = []
        for i in range(max_course_hours):
            same_course.append(course + "_" + str(i))

        for i in permutations(same_course):
            problem.addConstraint(max_consecutive_courses, [*i])
    
    #even distribution of courses across the week
    def evenly_distribute_courses(*args):
        bins = {i: 0 for i in range(num_days)}

        for course_slot in args:
            bins[course_slot // num_time_periods] += 1

        # Check if the difference in counts between days is within a tolerance
        tolerance = 1  # You may adjust this tolerance value as needed
        min_count = min(bins.values())
        max_count = max(bins.values())
        return max_count - min_count <= tolerance
    
    problem.addConstraint(evenly_distribute_courses, [*courses])

    timetable = {}
    solution = problem.getSolution()
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