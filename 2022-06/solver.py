from docplex.mp.model import Model

rows = [0,1,2,3,4,5,6,7,8,9]
cols = [0,1,2,3,4,5,6,7,8,9]
nums = [1,2,3,4,5,6,7,8,9,10]

prefilled = {(0,1): 3,(0,5): 7,(1,3): 4,(2,8): 2,(3,3): 1,(4,0): 6,(4,2): 1,(5,7): 3,(5,9): 6,(6,6): 2,(7,1): 2,(8,6): 6,(9,4): 5,(9,8): 2}
areas = {(0,0): 1,(0,1): 3,(0,2): 3,(0,3): 3,(0,4): 11,(0,5): 11,(0,6): 11,(0,7): 11,(0,8): 11,(0,9): 11,(1,0): 1,(1,1): 1,(1,2): 3,(1,3): 3,(1,4): 3,(1,5): 11,(1,6): 18,(1,7): 18,(1,8): 11,(1,9): 11,(2,0): 1,(2,1): 1,(2,2): 6,(2,3): 6,(2,4): 12,(2,5): 12,(2,6): 14,(2,7): 18,(2,8): 23,(2,9): 23,(3,0): 1,(3,1): 1,(3,2): 4,(3,3): 6,(3,4): 8,(3,5): 14,(3,6): 14,(3,7): 14,(3,8): 23,(3,9): 23,(4,0): 1,(4,1): 4,(4,2): 4,(4,3): 8,(4,4): 8,(4,5): 15,(4,6): 19,(4,7): 14,(4,8): 14,(4,9): 23,(5,0): 1,(5,1): 5,(5,2): 4,(5,3): 9,(5,4): 13,(5,5): 15,(5,6): 20,(5,7): 20,(5,8): 23,(5,9): 23,(6,0): 1,(6,1): 2,(6,2): 7,(6,3): 9,(6,4): 9,(6,5): 9,(6,6): 20,(6,7): 21,(6,8): 21,(6,9): 21,(7,0): 2,(7,1): 2,(7,2): 7,(7,3): 10,(7,4): 9,(7,5): 16,(7,6): 17,(7,7): 22,(7,8): 22,(7,9): 17,(8,0): 2,(8,1): 2,(8,2): 2,(8,3): 10,(8,4): 10,(8,5): 17,(8,6): 17,(8,7): 22,(8,8): 22,(8,9): 17,(9,0): 2,(9,1): 2,(9,2): 2,(9,3): 2,(9,4): 10,(9,5): 10,(9,6): 17,(9,7): 17,(9,8): 17,(9,9): 17}

m = Model()

vars = {(r,c,n): m.binary_var('var'+str(r)+'_'+str(c)+'_'+str(n)) for r in rows for c in cols for n in nums}

# Every r/c has exactly one number
for r in rows:
    for c in cols:
        m.add(m.sum(vars[(r,c,n)] for n in nums) == 1)

# In every area, if the area has size x, the area needs to contain the numbers from 1-x
areasize = {a:sum(1 for v in areas.values() if v == a) for a in areas.values()}
for area in areasize.keys():
    for size in range(1,areasize[area]+1):
        m.add(m.sum(vars[(r,c,size)] for r in rows for c in cols if areas[(r,c)] == area) == 1)

# Prefilled values
for r,c in prefilled:
    m.add(vars[(r,c,prefilled[(r,c)])] == 1)
    
# If r,c contains n, then there has to be another n within a distance of n
for r,c in areas:
    for n in nums:
        m.add(vars[(r,c,n)] <= m.sum(vars[(r2,c2,n)] for r2 in rows for c2 in cols if abs(r-r2)+abs(c-c2) == n))
        for r2 in rows:
            for c2 in cols:
                if abs(r-r2)+abs(c-c2) < n and abs(r-r2)+abs(c-c2) != 0:
                    m.add(vars[(r,c,n)] + vars[(r2,c2,n)] <= 1) # But not any closer
        
m.solve(log_output = True)
m.export_as_lp('model.lp')

for r in rows:
    thisrow = ''
    for c in cols:
        for n in nums:
            if vars[(r,c,n)].solution_value > 0.5:
                thisrow += str(n)+'\t'
    print(thisrow)