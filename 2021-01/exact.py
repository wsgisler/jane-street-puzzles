from time import time
import operator as op
from itertools import product
from functools import reduce
from math import factorial

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom 

def calculate_number_permutations(num_figurines):
    stats = {i:0 for i in range(num_figurines+1)}
    possibilities = [[(f,i) for i in range(f+1)] for f in range(2,num_figurines+1)]
    for q in product(*possibilities):
        maxx = 0
        num_ways = 1
        num_f_used = 0
        num_f_unused = 0
        for f in q:
            maxx = maxx if f[1] < maxx else f[1]
            num_ways *= ncr(f[0],f[1])
            num_f_used += f[1]
            num_f_unused += f[0]-f[1]
        num_ways = num_ways*factorial(num_f_used)*factorial(num_f_unused)
        stats[maxx] += num_ways
    return stats
    
def calc(num_figurines):
    s = calculate_number_permutations(num_figurines)
    total = factorial((num_figurines+1)/2*num_figurines)
    e = 0
    for f in range(num_figurines+1):
        e += f*s[f]/total
    return e

st = time()
e = calc(6)
print('Expected value: '+str(e))
print('Time spent: '+str(time()-st))
            