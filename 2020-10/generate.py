from docplex.mp.model import Model

m = Model()

children = [1,2,3,4,5]
candies = [1,2,3,4,5]
quants = [0,1,2,3,4,5]

x = {(ch,ca): m.integer_var(lb = 0, ub = 5, name = 'x_%i_%i'%(ch,ca)) for ch in children for ca in candies}
xx = {(ch,ca,qu): m.binary_var() for ch in children for ca in candies for qu in quants}
d = {(ch,ca): m.binary_var() for ch in children for ca in candies}

for ch in children:
    m.add(m.sum(x[(ch,ca)] for ca in candies) == len(candies)*max(quants)/len(children))

for ca in candies:
    m.add(m.sum(x[(ch,ca)] for ch in children) == max(quants))
    
for ch in children:
    m.add(m.sum(d[(ch,ca)] for ca in candies) >= 1)
    
for ca in candies:
    m.add(m.sum(d[(ch,ca)] for ch in children) <= 1)
    
for ch in children:
    for ca in candies:
        for ch2 in set(children)-{ch}:
            m.add(d[(ch,ca)] <= 0.9+(x[(ch,ca)]-x[(ch2,ca)])/(max(quants)+1))
            
for ch in children:
    for ca in candies:
        m.add(m.sum(xx[(ch,ca,qu)]*qu for qu in quants) == x[(ch,ca)])
        m.add(m.sum(xx[(ch,ca,qu)] for qu in quants) == 1)
        
# Add that for child 1, candy 1 is dominating
m.add(d[(1,1)] == 1)
# Add that for child 2, candy 2 is dominating
m.add(d[(2,2)] == 1)
# Add that for child 3, candy 3 is dominating
m.add(d[(3,3)] == 1)
# Add that for child 4, candy 4 is dominating
m.add(d[(4,4)] == 1)
# Add that for child 5, candy 5 is dominating
m.add(d[(5,5)] == 1)

m.parameters.threads = 4

solutions = []           
while True:
    solves = m.solve(log_output = False)

    if not solves:
        break
    
    sol = []    
    for ch in children:
        for ca in candies:
            for i in range(int(x[(ch,ca)].solution_value)):
                sol.append(ca)
    
    m.add(m.sum(xx[(ch,ca,qu)] for ch in children for ca in candies for qu in quants if xx[(ch,ca,qu)].solution_value > 0.5) <= len(children)*len(candies)-1)
            
    print(sol)
    solutions.append(sol)

print(len(solutions))