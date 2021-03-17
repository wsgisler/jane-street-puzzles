from docplex.mp.model import Model

def detect_connected(g):
    encountered = set()
    current = list(g)[0] # randomly chose an element we want to explore
    to_explore = [current]
    while to_explore:
        current = to_explore.pop()
        r = current[0]
        c = current[1]
        encountered.add(current)
        if ((r+1,c) in g) and ((r+1,c) not in encountered):
            to_explore.append((r+1,c))
        if ((r-1,c) in g) and ((r-1,c) not in encountered):
            to_explore.append((r-1,c))
        if ((r,c+1) in g) and ((r,c+1) not in encountered):
            to_explore.append((r,c+1))
        if ((r,c-1) in g) and ((r,c-1) not in encountered):
            to_explore.append((r,c-1))
    return len(encountered) == len(g)

# define key parameters
side = [0,1,2,3,4,5,6,7,8]
lsizes = [1,2,3,4,5,6,7,8,9]
positions = [0,1,2,3] # 0: |^    1: ^|    2: _|    3: |_    (possible positions of L "knee")

# data
colors = {(0,0):'p1',(0,1):'p1',(0,2):'p1',(0,3):'p1',(0,4):'g1',(0,5):'o1',(0,6):'o1',(0,7):'p3',(0,8):'p3',(1,0):'p1',(1,1):'p1',(1,2):'g2',(1,3):'p1',(1,4):'g1',(1,5):'o1',(1,6):'p3',(1,7):'p3',(1,8):'b5',(2,0):'p1',(2,1):'p1',(2,2):'g2',(2,3):'p1',(2,4):'p1',(2,5):'b5',(2,6):'b5',(2,7):'b5',(2,8):'b5',(3,0):'b1',(3,1):'b1',(3,2):'g2',(3,3):'g2',(3,4):'p1',(3,5):'b5',(3,6):'p4',(3,7):'o4',(3,8):'o4',(4,0):'p2',(4,1):'p2',(4,2):'g2',(4,3):'o2',(4,4):'p1',(4,5):'b5',(4,6):'p4',(4,7):'o4',(4,8):'b6',(5,0):'g3',(5,1):'p2',(5,2):'o2',(5,3):'o2',(5,4):'g4',(5,5):'p4',(5,6):'p4',(5,7):'b6',(5,8):'b6',(6,0):'g3',(6,1):'g3',(6,2):'o2',(6,3):'g4',(6,4):'g4',(6,5):'g4',(6,6):'p4',(6,7):'g5',(6,8):'g5',(7,0):'b2',(7,1):'b2',(7,2):'o2',(7,3):'g4',(7,4):'b3',(7,5):'o3',(7,6):'o3',(7,7):'b4',(7,8):'b4',(8,0):'b2',(8,1):'b2',(8,2):'o2',(8,3):'g4',(8,4):'b3',(8,5):'o3',(8,6):'o3',(8,7):'b4',(8,8):'b4'}
prefilled = {(2,4): 4, (6,4): 5}

# declare models and variables
m = Model()
x = {(l,r,c,p): m.binary_var() for l in lsizes for r in side for c in side for p in positions} # defines the position and orientation of each "L"
y = {(l,r,c): m.binary_var() for l in lsizes for r in side for c in side} # is (r,c) part of an L with side-length l?
z = {(l,r,c): m.binary_var() for l in lsizes for r in side for c in side} # does the square in the end solution contain a given number l?

# Constraints
# every L appears exactly once
for l in lsizes:
    m.add(m.sum(x[(l,r,c,p)] for r in side for c in side for p in positions) == 1)
# each cell contains exactly one number
for r in side:
    for c in side:
        m.add(m.sum(y[(l,r,c)] for l in lsizes) == 1)
# force where numbers will be based on position of L
for l in lsizes:
    for r in side:
        for c in side:
            for p in positions:
                if p == 0:
                    if r+l > side[-1]+1 or c+l > side[-1]+1:
                        m.add(x[(l,r,c,p)] == 0)
                    else:
                        for of in range(l):
                            m.add(x[(l,r,c,p)] <= y[(l,r+of,c)])
                            m.add(x[(l,r,c,p)] <= y[(l,r,c+of)])
                if p == 1:
                    if r+l > side[-1]+1 or c-l < -1:
                        m.add(x[(l,r,c,p)] == 0)
                    else:
                        for of in range(l):
                            m.add(x[(l,r,c,p)] <= y[(l,r+of,c)])
                            m.add(x[(l,r,c,p)] <= y[(l,r,c-of)])
                if p == 2:
                    if r-l < -1 or c-l < -1:
                        m.add(x[(l,r,c,p)] == 0)
                    else:
                        for of in range(l):
                            m.add(x[(l,r,c,p)] <= y[(l,r-of,c)])
                            m.add(x[(l,r,c,p)] <= y[(l,r,c-of)])
                if p == 3:
                    if r-l < -1 or c+l > side[-1]+1:
                        m.add(x[(l,r,c,p)] == 0)
                    else:
                        for of in range(l):
                            m.add(x[(l,r,c,p)] <= y[(l,r-of,c)])
                            m.add(x[(l,r,c,p)] <= y[(l,r,c+of)])
# Conditions for z variable
for l in lsizes:
    m.add(m.sum(z[(l,r,c)] for r in side for c in side) == l)
for r in side:
    for c in side:
        m.add(m.sum(z[(l,r,c)] for l in lsizes) <= 1)
for r in side:
    for c in side:
        if (r,c) in prefilled:
            m.add(z[(prefilled[(r,c)],r,c)] == 1)
            m.add(y[(prefilled[(r,c)],r,c)] == 1)
        for l in lsizes:
            m.add(z[(l,r,c)] <= y[(l,r,c)])
# z-Variable region has to be connected (can't be done completely, but we can limit it a bit)
for r in side:
    for c in side:
        around = 0
        around += m.sum(z[(l,r+1,c)] for l in lsizes) if (l,r+1,c) in z else 0
        around += m.sum(z[(l,r,c+1)] for l in lsizes) if (l,r,c+1) in z else 0
        around += m.sum(z[(l,r-1,c)] for l in lsizes) if (l,r-1,c) in z else 0
        around += m.sum(z[(l,r,c-1)] for l in lsizes) if (l,r,c-1) in z else 0
        m.add(m.sum(z[(l,r,c)] for l in lsizes) <= around) # This avoids single cells (but doesn't avoid "islands" of connected cells)
# Every connected region with the same color needs to have the same sum
conregions = set()
special_sum = m.continuous_var()
for r,c in colors:
    conregions.add(colors[(c,r)])
for region in conregions:
    m.add(m.sum(z[(l,r,c)]*l for r in side for c in side for l in lsizes if colors[(r,c)] == region) == special_sum)
# Every 2x2 region must contain an empty square
for r in side[:-1]:
    for c in side[:-1]:
        m.add(m.sum(z[(l,rr,cc)] for l in lsizes for rr in [r,r+1] for cc in [c,c+1]) <= 3)

solution = m.solve(log_output = False)

while solution:
    output = ''
    for r in side:
        line = ''
        for c in side:
            for l in lsizes:
                if y[(l,r,c)].solution_value > 0.5:
                    line += str(l)+','
        output += line+'\n'
    output += '\n'

    g = set()
    for r in side:
        line = ''
        for c in side:
            count = 0
            for l in lsizes:
                if z[(l,r,c)].solution_value > 0.5:
                    line += str(l)+','
                    g.add((r,c))
                    count += 1
            if not count:
                line += ' ,'
        output += line+'\n'
    if detect_connected(g):
        print('The region is connected')
        print(output)
        print()
    else:
        print('Not connected!!!')
    m.add(m.sum(z[(l,r,c)] for l in lsizes for r in side for c in side if z[(l,r,c)].solution_value > 0.5) <= sum(z[(l,r,c)].solution_value for l in lsizes for r in side for c in side)-0.9)
    solution = m.solve(log_output = False)
