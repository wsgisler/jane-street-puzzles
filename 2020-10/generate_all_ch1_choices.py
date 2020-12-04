from itertools import combinations, permutations

NUM_ITEMS = 3
NUM_TYPES = 3

combs = []
combs_num = []

for comb in combinations(list(range(NUM_ITEMS+NUM_TYPES-1)), NUM_TYPES-1):
    cc = []
    for type in range(NUM_TYPES-1):
        for rr in range(comb[type]-(comb[type-1]+1 if type > 0 else 0)):
            cc.append(type)
    for rr in range(comb[-1],NUM_ITEMS+NUM_TYPES-2):
        cc.append(type+1)
    combs.append(cc)
    myset = set()
    for perm in permutations(cc):
        myset.add(perm)
    combs_num.append(len(myset))
    
print(combs)
print(combs_num)
print(len(combs))