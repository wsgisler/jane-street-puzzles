from random import shuffle
import itertools

NUM_CHILDREN = 5
NUM_CANDY_TYPES = 5 

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

success = 0
tries = 0
while success < 30000:
    tries += 1
    if tries%1000 == 0:
        print(tries)
    candies = list(itertools.chain(*[[i]*NUM_CHILDREN for i in range(1,NUM_CHILDREN+1)]))
    shuffle(candies)
    #print(candies)
    found = dominating(candies, NUM_CHILDREN, NUM_CANDY_TYPES)
    if found:
        success +=1
     
print()   
print(success)
print(tries)

print(success/tries)

# Testing
# print(dominating([1, 1, 2, 2, 3, 1, 2, 2, 2, 0, 1, 3, 3, 4, 0, 1, 3, 4, 4, 4, 3, 4, 0, 0, 0], 5, 5))
# 
# print(dominating([1, 1, 2, 4, 0, 1, 2, 2, 3, 4, 1, 2, 3, 3, 4, 2, 3, 4, 4, 0, 1, 3, 0, 0, 0], 5, 5))
# 
# print(dominating([1, 1, 1, 2, 3, 1, 2, 2, 3, 0, 1, 2, 3, 3, 0, 2, 4, 4, 4, 0, 3, 4, 4, 0, 0], 5, 5))
    