class Problem {
    constructor() {
        this.variables = {};
        this.constraints = [];
    }

    addVariable(name, domain) {
        this.variables[name] = domain;
    }

    addConstraint(constraintFunction, variableNames) {
        this.constraints.push({constraintFunction, variableNames});
    }

    solve() {
        const assignment = {};
        const isSolved = this.backtrack(assignment);

        if (isSolved) {
            console.log("Solution found:", assignment);
        } else {
            console.log("No solution found.");
        }
    }

    // Recursive backtracking search algorithm
    backtrack(assignment) {
        if (
            Object.keys(assignment).length ===
            Object.keys(this.variables).length
        ) {
            return true; // All variables are assigned, solution found
        }

        const variable = this.selectUnassignedVariable(assignment);
        const domain = this.variables[variable];

        console.log(variable);
        console.log(domain);

        for (const value of domain) {
            if (this.isValueConsistent(variable, value, assignment)) {
                assignment[variable] = value;
                if (this.backtrack(assignment)) {
                    return true;
                }
                delete assignment[variable];
            }
        }

        return false; // No consistent value found for the variable
    }

    // Method to select an unassigned variable
    selectUnassignedVariable(assignment) {
        for (const variable in this.variables) {
            if (!(variable in assignment)) {
                return variable;
            }
        }
        return null; // All variables are assigned
    }

    // Method to check if a value is consistent with the current assignment
    isValueConsistent(variable, value, assignment) {
        for (const constraint of this.constraints) {
            if (constraint.variableNames.includes(variable)) {
                const args = constraint.variableNames.map(
                    (varName) => assignment[varName] || varName
                );
                console.log(assignment);
                console.log(args.conat(value));
                if (
                    !constraint.constraintFunction.apply(
                        null,
                        args.concat(value)
                    )
                ) {
                    return false; // Value is not consistent with the constraint
                }
            }
        }
        return true; // Value is consistent with all constraints
    }
}

// import Problem from "./csp-solver";

// Example usage:
const cspSolver = new Problem();

// Define variables and their domains
cspSolver.addVariable("x", [1, 2, 3]);
cspSolver.addVariable("y", [4, 5, 6]);

// Define a constraint function
function constraintFunction(x, y) {
  return x + y <= 8;
}

// Add the constraint to the CSP
cspSolver.addConstraint(constraintFunction, ["x", "y"]);
console.log(cspSolver.variables)
// Solve the CSP
console.log(cspSolver.solve());

export default Problem;