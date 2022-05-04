from docplex.cp.model import CpoModel

fields = list(range(1,29))

m = CpoModel()

x = {f: m.integer_var(1, 200) for f in fields}

m.add(m.all_diff(x.values()))

#square 1
sq = m.integer_var(6, 600)
rows = [[1,2,3],[4,5,6],[10,11,12]]
cols = [[1,4,10],[2,5,11],[3,6,12]]
digs = [[1,5,12],[10,5,3]]
triples = rows + cols + digs
for t in triples:
    m.add(x[t[0]] + x[t[1]] + x[t[2]] >= sq)
    m.add(x[t[0]] + x[t[1]] + x[t[2]] <= sq+1)
    
#square 2
sq = m.integer_var(6, 600)
rows = [[6,7,8],[12,13,14],[18,19,20]]
cols = [[6,12,18],[7,13,19],[8,14,20]]
digs = [[6,13,20],[18,13,8]]
triples = rows + cols + digs
for t in triples:
    m.add(x[t[0]] + x[t[1]] + x[t[2]] >= sq)
    m.add(x[t[0]] + x[t[1]] + x[t[2]] <= sq+1)
    
#square 3
sq = m.integer_var(6, 600)
rows = [[9,10,11],[15,16,17],[21,22,23]]
cols = [[9,15,21],[10,16,22],[11,17,23]]
digs = [[9,16,23],[21,16,11]]
triples = rows + cols + digs
for t in triples:
    m.add(x[t[0]] + x[t[1]] + x[t[2]] >= sq)
    m.add(x[t[0]] + x[t[1]] + x[t[2]] <= sq+1)
    
#square 4
sq = m.integer_var(6, 600)
rows = [[17,18,19],[23,24,25],[26,27,28]]
cols = [[17,23,26],[18,24,27],[19,25,28]]
digs = [[17,24,28],[26,24,19]]
triples = rows + cols + digs
for t in triples:
    m.add(x[t[0]] + x[t[1]] + x[t[2]] >= sq)
    m.add(x[t[0]] + x[t[1]] + x[t[2]] <= sq+1)
    
m.add(m.minimize_static_lex([m.sum(x.values()),0]))

m.set_search_phases([m.search_phase(list(x.values()))])

msol = m.solve(TimeLimit = 500)

for f in fields:
    print('%i: %i'%(f,msol[x[f]]))
   
for f in fields:
    print(msol[x[f]]) 