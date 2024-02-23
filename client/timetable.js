// // const CSP = require("./csp");

// // const CSP = require("./csp");

// const params = new URLSearchParams(window.location.search);
// const encodedData = params.get("data");
// const courseNames = JSON.parse(decodeURIComponent(encodedData));
// console.log(courseNames);
// const maxCourseHours = 3;
// const variables = {};
// // const timeSlots = 9 * 5; // 9 is the time period for each day, 5 is the number of days in the week

// const courses = []

// require.config({
//     baseUrl: "../src/",
// });

// require(["csp", "Hash", "Set"], function (csp, Hash, Set) {
//     function noOverlapConstraint(...args) {
//         // Ensure no overlap by checking if any two courses have the same time slot
//         return new Set(args).size === args.length;
//     }

//     const timeSlots = [...Array(9*5)].map(
//         (item, index) => index
//     );

//     const p = csp.DiscreteProblem();

//     for (const courseName of courseNames) {
//         for (let i = 0; i < maxCourseHours; i++) {
//             variables[courseName + i] = timeSlots;
//             p.addVariable(courseName+i, timeSlots)
//         }
//     }
//     p.addConstraint(Object.keys(variables), noOverlapConstraint)
//     // console.log(p.getSolution())
//     const solutionIterator = p.solver.getSolutionIter(p).next();

//     console.log(solutionIterator.value)
// });

// import Problem from "./csp-solver";

// // Example usage:
// const cspSolver = new Problem();

// // Define variables and their domains
// cspSolver.addVariable("x", [1, 2, 3]);
// cspSolver.addVariable("y", [4, 5, 6]);

// // Define a constraint function
// function constraintFunction(x, y) {
//   return x + y <= 8;
// }

// // Add the constraint to the CSP
// cspSolver.addConstraint(constraintFunction, ["x", "y"]);

// // Solve the CSP
// console.log(cspSolver.solve());

const params = new URLSearchParams(window.location.search);
const encodedData = params.get("data");
const breakPeriod = 6;

fetch(`http://127.0.0.1:5000/get-timetable?data=${encodedData}`)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
		console.log(data)
        for (const [courseName, schedules] of Object.entries(data)) {
            for (const schedule of schedules) {
                const dayRow =
                    document.getElementsByTagName("tbody")[0].children[
                        4 + schedule[0]
                    ];
                const day = dayRow.children[1 + ((schedule[1] >= breakPeriod && schedule[0] != 0) ? schedule[1] - 1 : schedule[1])];
                console.log(dayRow);
                console.log(1 + schedule[1]);
                day.textContent = courseName;

            }
        }
    }).catch((error) => {

		console.log(error)
	});
