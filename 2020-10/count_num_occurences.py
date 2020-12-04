from itertools import permutations

find_string = '111222333'

counter = 0
for permut in permutations([1,1,1,2,2,2,3,3,3]):
    if ''.join([str(p) for p in permut]) == find_string:
        counter += 1
        
print(counter)