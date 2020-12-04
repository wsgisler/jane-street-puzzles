from docplex.mp.model import Model

m = Model()

children = [1,2,3,4,5]
candies = [1,2,3,4,5]
quants = [0,1,2,3,4,5]


children = [1,2,3]
candies = [1,2,3]
quants = [0,1,2,3]

children = [1,2]
candies = [1,2]
quants = [0,1,2]

x = {(ch,ca): m.integer_var(lb = 0, ub = 5, name = 'x_%i_%i'%(ch,ca)) for ch in children for ca in candies}
xx = {(ch,ca,qu): m.binary_var() for ch in children for ca in candies for qu in quants}

for ch in children:
    m.add(m.sum(x[(ch,ca)] for ca in candies) == len(candies)*max(quants)/len(children))

for ca in candies:
    m.add(m.sum(x[(ch,ca)] for ch in children) == max(quants))
            
for ch in children:
    for ca in candies:
        m.add(m.sum(xx[(ch,ca,qu)]*qu for qu in quants) == x[(ch,ca)])
        m.add(m.sum(xx[(ch,ca,qu)] for qu in quants) == 1)

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