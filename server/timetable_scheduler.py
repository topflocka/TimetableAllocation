import constraint 
from flask import Flask, request, jsonify, abort
from flask_cors import CORS 
import json
import constraint
from itertools import permutations

app = Flask(__name__)
CORS(app)

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
    for course in course_names:
        for i in range(max_course_hours):
            courses.append(course + "_" + str(i))
            # problem.addVariable(course + "_" + str(i), time_slots)
    
    # ensures an even distribution of courses in a week by using round robin
    # nd is the number of courses that should each day
    # ND = len(courses) // num_days + 1
    # for i in range(num_days):
    #     print(courses[i*ND:i*ND+ND])
    #     problem.addVariables(courses[i*ND:i*ND+ND], 
    #                          range(i*num_time_periods + num_time_periods - 1, i*num_time_periods - 1, -1))
    # print(courses[num_days*ND:])
    # Ensure even distribution of courses across the week using round-robin scheduling
    # courses_per_day = len(courseNames) // num_days + 1
    # for i in range(num_days):
    #     day_courses = courseNames[i * courses_per_day : (i + 1) * courses_per_day]
    #     for course in day_courses:
    #         for j in range(max_course_hours):
    #             course_variable = f"{course}_{j}"
    #             # Assign time slots for each course in a round-robin manner
    #             problem.addConstraint(constraint.NotInSetConstraint([i * num_time_periods + j for i in range(num_days)]), [course_variable])
    # courses_per_day = (len(course_names) * max_course_hours) // num_days + 1
    # for i in range(num_days):
    #     day_courses = course_names[i * courses_per_day : (i + 1) * courses_per_day]
    #     for course in day_courses:
    #         for j in range(max_course_hours):
    #             course_variable = f"{course}_{j}"
    #             problem.addVariable(course_variable, 
    #                          range(i*num_time_periods + num_time_periods - 1, i*num_time_periods - 1, -1))
                # Assign time slots for each course in a round-robin manner
                # problem.addConstraint(constraint.NotInSetConstraint([i * num_time_periods + j for i in range(num_days)]), [course_variable])

    ND = len(courses) // num_days + 1
    for i in range(num_days):
        print(courses[i*ND:i*ND+ND])
        problem.addVariables(courses[i*ND:i*ND+ND], 
                             range(i*num_time_periods + num_time_periods - 1, i*num_time_periods - 1, -1))

    # problem.addVariables([*courses], range(num_days * num_time_periods))
    
    # breaks = []
    # for i in range(len(time_slots) - len(courses)):  # One less break than the number of courses
    #     breaks.append("break" + "_" + str(i))
    #     # problem.addVariable('break' + "_" + str(i), time_slots)

    #no two courses can clash constraint
    # problem.addConstraint(constraint.AllDifferentConstraint(), [*courses, *breaks])
    problem.addConstraint(constraint.AllDifferentConstraint(), [*courses])

    #no course can occur during break time 
    problem.addConstraint(constraint.NotInSetConstraint([break_period + num_time_periods * i for i in range(num_days)]), [*courses])

    # a course can only hold at most twice consecutively
    # max_consecutive_courses = lambda *args: args[0] + 2 != args[2]
    # for course in courseNames:
    #     same_course = []
    #     for i in range(max_course_hours):
    #         same_course.append(course + "_" + str(i))

    #     for perm in permutations(same_course):
    #         problem.addConstraint(max_consecutive_courses, [*perm])
    
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
    # problem.addConstraint(constraint.MaxSumConstraint(300), [*courses])

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
    print('yes')
    return jsonify(timetable)

app.run(debug=True)