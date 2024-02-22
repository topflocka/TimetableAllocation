from constraint import *

def nqueens(n):
    problem = Problem()
    
    # Define variables for each row, representing the column position of the queen in that row
    for i in range(n):
        problem.addVariable(i, range(n))
    
    # Add constraints to ensure that no two queens share the same column or diagonal
    for i in range(n):
        for j in range(i+1, n):
            problem.addConstraint(lambda xi, xj, i=i, j=j: xi != xj and abs(xi - xj) != j - i, (i, j))
    
    # Find solution
    solutions = problem.getSolutions()
    
    return solutions

# Example usage:
n = 20
solutions = nqueens(n)

print(f"Number of solutions for {n}-queens problem: {len(solutions)}")
for i, solution in enumerate(solutions[:3]):
    print(f"Solution {i+1}: {solution}")