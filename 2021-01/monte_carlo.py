from random import shuffle
from time import time

def run_once(num_figurines = 12):
	figurines = []
	for i in range(1,num_figurines+1):
		for a in range(i):
			figurines.append(i)
	shuffle(figurines)
	alex = dict()
	current = None
	while current != 1: # alex should never get the partridge and this is when it stops
	    if current:
	        if current in alex:
	            alex[current] += 1
	        else:
	            alex[current] = 1
	    current = figurines.pop()
	figurines.append(1)
	maxx = 0
	for i in range(1,num_figurines+1):
	    if i in alex and maxx < alex[i]:
	        maxx = alex[i]
	return maxx
	
def simulate(n = 100, num_figurines = 12):
    total = 0
    for i in range(n):
        total += run_once(num_figurines)
    return total/n
    
st = time()
print(simulate(10000000,12)) # print the expected number of figurines
print(time()-st) # print how long it took to run the simulation (in seconds)