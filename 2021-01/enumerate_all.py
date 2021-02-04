from itertools import permutations

num_figurines = 4

figurines = []
for i in range(1,num_figurines+1):
	for a in range(i):
		figurines.append(i)

c = 0
stats = {i:0 for i in range(num_figurines+1)}
statss = {(f,count):0 for f in list(range(num_figurines+1)) for count in list(range(num_figurines+1))}
for permutation in permutations(figurines):
    c += 1
    tracker = {i:0 for i in range(1,num_figurines+1)}
    permutation = list(permutation)
    while permutation[0] != 1:
        current = permutation.pop(0)
        tracker[current] += 1
    maxx = 0
    maxxi = 0
    for i in tracker:
        if maxx < tracker[i]:
            maxx = tracker[i]
            maxxi = i
    stats[maxx] += 1
    statss[(maxxi, maxx)] += 1

print(c)
print(stats)
print(statss)
print(sum([i*stats[i]/c for i in stats]))