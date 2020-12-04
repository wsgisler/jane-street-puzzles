from random import shuffle
import itertools

NUM_CHILDREN = 3
NUM_CANDY_TYPES = 3

def dominating(candies, num_children, num_candy_types):
    child_candies = [[candies[child*int(len(candies)/num_children)+ca] for ca in range(int(len(candies)/num_children))] for child in range(num_children)]
    print(child_candies)
    child_candies_count = {(child, candy): child_candies[child].count(candy) for child in range(num_children) for candy in range(num_candy_types+1)}
    print(child_candies_count)
    dominating = True
    for child in range(num_children):
        child_dominates = False
        for candy in range(num_candy_types+1):
            if child_candies_count[(child, candy)] > max([child_candies_count[(ch, candy)] for ch in range(num_children) if ch != child]):
                child_dominates = True
                print('Child '+str(child)+' has a dominating amount of candy '+str(candy))
                break
        if not child_dominates:
            dominating = False
            break
    return dominating

success = 0
tries = 0
havent_found = True
while havent_found:
    tries += 1
    candies = list(itertools.chain(*[[i]*3 for i in range(1,4)]))
    shuffle(candies)
    print(candies)
    found = dominating(candies, NUM_CHILDREN, NUM_CANDY_TYPES)
    if found:
        havent_found = False
        print(tries)