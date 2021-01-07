"""
Original problem statement: https://www.janestreet.com/puzzles/twenty-four-seven-2-by-2-2/

I am using a MIP to solve this problem.
- most constraints are straightforward, but the constraint concerning the blue numbers are quite interesting and not so simple
- the constraint for the connectedness is not sufficient. It is in fact allowing solutions with multiple independent connected components.
- We therefore have to generate all feasible solutions and then check which ones is truly connected and which one isn't. 
- We could do this with some code, but there aren't many solutions, so I didn't implement this and checked it by hand instead
- To solve the examples, set example (line 14) to a value between 1 and 4 to solve grid 1 to 4
- I then entered the valid solution (which turns out to be unique) into an Excel sheet and calculated the sum of the grids and the sum of squares in this final grid.
- The solution to this challenge is 8520
"""

from docplex.mp.model import Model

example = 4

if example == 1:
    grid = [[0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 6, 0],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0]]
    top = [5, 4, 0, 0, 0, 7, 5]
    left = [5, 7, 0, 0, 0, 5, 7]
    right = [7, 4, 0, 0, 0, 7, 6]
    bottom = [5, 7, 0, 0, 0, 0, 0]
if example == 2:
    grid = [[0, 2, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1]]
    top = [0, 0, 5, 6, 0, 6, 7]
    left = [0, 0, 5, 6, 0, 7, 6]
    right = [6, 6, 4, 0, 0, 0, 0]
    bottom = [6, 7, 5, 0, 0, 0, 0]
if example == 3:
    grid = [[0, 0, 0, 0, 4, 0, 0],
            [0, 6, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 6, 0],
            [0, 0, 4, 0, 0, 0, 0]]
    top = [7, 0, 0, 5, 0, 7, 0]
    left = [0, 0, 0, 7, 0, 0, 0]
    right = [0, 0, 0, 5, 0, 0, 0]
    bottom = [0, 7, 0, 3, 0, 0, 5]
if example == 4:
    grid = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0]]
    top = [0, 0, 0, 0, 0, 0, 0]
    left = [1, 2, 3, 4, 5, 6, 7]
    right = [0, 6, 0, 4, 0, 2, 0]
    bottom = [0, 6, 0, 5, 0, 4, 0]


rows = range(len(grid))
cols = range(len(grid[0]))
numbers = [1,2,3,4,5,6,7]

model = Model()

x = {(r,c,i): model.binary_var() for r in rows for c in cols for i in numbers}

# 1 has to appear once, 2 has to appear twice, etc.
for i in numbers:
    model.add(model.sum(x[(r,c,i)] for r in rows for c in cols) == i)
    
# preset numbers
for r in rows:
    for c in cols:
        if grid[r][c]:
            model.add(x[(r,c,grid[r][c])] == 1)
            
# At most one number per cell
for r in rows:
    for c in cols:
        model.add(model.sum(x[(r,c,i)] for i in numbers) <= 1)
        
# every row and every column has to contain 4 numbers and they have to add up to 20
for r in rows:
    model.add(model.sum(x[(r,c,i)] for i in numbers for c in cols) == 4)
    model.add(model.sum(x[(r,c,i)]*i for i in numbers for c in cols) == 20)
for c in cols:
    model.add(model.sum(x[(r,c,i)] for i in numbers for r in rows) == 4)
    model.add(model.sum(x[(r,c,i)]*i for i in numbers for r in rows) == 20)
    
# every 2x2 subsquare should contain at least one empty cell
for r in rows[:-1]:
    for c in cols[:-1]:
        model.add(model.sum(x[(r,c,i)]+x[(r+1,c,i)]+x[(r+1,c+1,i)]+x[(r,c+1,i)] for i in numbers) <= 3)
        
# blue numbers indicate the first value seen in the corresponding row or column when looking into the grid from that location
# from the top
for c in cols:
    for r in rows:
        allempty = model.continuous_var(lb = 0, ub = 1)
        model.add(1-model.sum(x[(rr,c,i)] for rr in rows if rr <= r for i in numbers)/len(rows) >= allempty)
        if top[c]:
            model.add(model.sum(x[(rr,c,top[c])] for rr in rows if rr <= r) >= 1 - allempty)
# from the bottom
for c in cols:
    for r in rows:
        allempty = model.continuous_var(lb = 0, ub = 1)
        model.add(1-model.sum(x[(rr,c,i)] for rr in rows if rr >= r for i in numbers)/len(rows) >= allempty)
        if bottom[c]:
            model.add(model.sum(x[(rr,c,bottom[c])] for rr in rows if rr >= r) >= 1 - allempty)
# from the left
for c in cols:
    for r in rows:
        allempty = model.continuous_var(lb = 0, ub = 1)
        model.add(1-model.sum(x[(r,cc,i)] for cc in cols if cc <= c for i in numbers)/len(cols) >= allempty)
        if left[r]:
            model.add(model.sum(x[(r,cc,left[r])] for cc in cols if cc <= c) >= 1 - allempty)
# from the right
for c in cols:
    for r in rows:
        allempty = model.continuous_var(lb = 0, ub = 1)
        model.add(1-model.sum(x[(r,cc,i)] for cc in cols if cc >= c for i in numbers)/len(cols) >= allempty)
        if right[r]:
            model.add(model.sum(x[(r,cc,right[r])] for cc in cols if cc >= c) >= 1 - allempty)

# numbered cells must form a connected region (interpretation 1 - can also be over diagonals)
# --> too many feasible solution - only the second interpretation allows unique solutionss
# for r in rows:
#     for c in cols:
#         for i in numbers:
#             numbered_surrounding_cells = model.sum(x[(rr,cc,ii)] for ii in numbers for rr in range(max(0,r-1),min(r+2,len(rows))) for cc in range(max(0,c-1),min(c+2,len(cols))))
#             model.add(x[(r,c,i)]*2 <= numbered_surrounding_cells)
            
# numbered cells must form a connected region (interpretation 2 - diagonals don't form a connection)
# this is not sufficient, actually - but it is good enough to reduce the choice enough to find the solution manually amongst the remaining solutions
for r in rows:
    for c in cols:
        for i in numbers:
            numbered_surrounding_cells = model.sum(x[(r+1,c,ii)] for ii in numbers) if r+1 < len(rows) else 0
            numbered_surrounding_cells += model.sum(x[(r-1,c,ii)] for ii in numbers) if r-1 >= 0 else 0
            numbered_surrounding_cells += model.sum(x[(r,c+1,ii)] for ii in numbers) if c+1 < len(cols) else 0
            numbered_surrounding_cells += model.sum(x[(r,c-1,ii)] for ii in numbers) if c-1 >= 0 else 0
            model.add(x[(r,c,i)] <= numbered_surrounding_cells)
            
model.solve(log_output = True)

for r in rows:
    entries = ''
    for c in cols:
        entry = ''
        for i in numbers:
            entry = str(i) if x[(r,c,i)].solution_value > 0.5 else entry
        entries += entry if entry else ' '
    print(entries)
    
solution = True
while solution:
    model.add(model.sum(x[(r,c,i)] for r in rows for c in cols for i in numbers if x[(r,c,i)].solution_value > 0.5) <= model.sum(x[(r,c,i)].solution_value for r in rows for c in cols for i in numbers)-0.9)

    solution = model.solve()

    if solution:
        print('solution is not unique')
        for r in rows:
            entries = ''
            for c in cols:
                entry = ''
                for i in numbers:
                    entry = str(i) if x[(r,c,i)].solution_value > 0.5 else entry
                entries += entry if entry else ' '
            print(entries)