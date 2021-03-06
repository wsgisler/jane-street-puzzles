from itertools import product, combinations, permutations
from math import factorial

def dominating(candies, num_children, num_candy_types):
    child_candies = [[candies[child*int(len(candies)/num_children)+ca] for ca in range(int(len(candies)/num_children))] for child in range(num_children)]
    #print(child_candies)
    child_candies_count = {(child, candy): child_candies[child].count(candy) for child in range(num_children) for candy in range(num_candy_types+1)}
    #print(child_candies_count)
    dominating = True
    for child in range(num_children):
        child_dominates = False
        for candy in range(num_candy_types+1):
            if child_candies_count[(child, candy)] > max([child_candies_count[(ch, candy)] for ch in range(num_children) if ch != child]):
                child_dominates = True
                #print('Child '+str(child)+' has a dominating amount of candy '+str(candy))
                break
        if not child_dominates:
            dominating = False
            break
    return dominating
    
def get_patts(N, output = True):
    combs = []
    combs_num = []

    for comb in combinations(list(range(N+N-1)), N-1):
        cc = []
        for type in range(N-1):
            for rr in range(comb[type]-(comb[type-1]+1 if type > 0 else 0)):
                cc.append(type)
        for rr in range(comb[-1],N+N-2):
            cc.append(type+1)
        combs.append(cc)
        myset = set()
        for perm in permutations(cc):
            myset.add(perm)
        combs_num.append(len(myset))
    
    if output: print(combs)
    if output: print(combs_num)
    if output: print(len(combs))
    return combs, combs_num

def main(N = 5):
    F = factorial(N)

    patts, patts_num_combs = get_patts(N, output = False)

    combinations = []
    comb_count = 0
    dom_combinations = []
    dom_comb_count = 0
    counter = 0

    for i in range(len(patts)):
        for j in range(len(patts)):
            temp = patts[i] + patts[j]
            if temp.count(0) <= N and temp.count(1) <= N and temp.count(2) <= N and temp.count(3) <= N and temp.count(4) <= N: 
                for k in range(len(patts)):
                    print('%d-%d-%d'%(i,j,k))
                    temp = patts[i] + patts[j] + patts[k]
                    if temp.count(0) <= N and temp.count(1) <= N and temp.count(2) <= N and temp.count(3) <= N and temp.count(4) <= N:
                        for l in range(len(patts)):
                            temp = patts[i] + patts[j] + patts[k] + patts[l]
                            if temp.count(0) <= N and temp.count(1) <= N and temp.count(2) <= N and temp.count(3) <= N and temp.count(4) <= N:
                                for m in range(len(patts)):
                                    c = F**N
                                    patt = []
                                    for p in [i,j,k,l,m]:
                                        c = c*patts_num_combs[p]
                                        patt += patts[p]
                                    good = True
                                    for item in range(N):
                                        if patt.count(item) != N:
                                            good = False
                                            break
                                    if good:
                                        combinations.append(patt)
                                        comb_count += c
                                        if dominating(patt, N, N):
                                            dom_combinations.append(patt)
                                            dom_comb_count += c                

    print()
    print('Result: ')
    print(dom_comb_count)
    print(comb_count)
    print(dom_comb_count/comb_count)
    
if __name__ == "__main__":
    main()