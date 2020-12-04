# Jane Street Puzzle - October 2020

Source: https://www.janestreet.com/puzzles/candy-collectors/

Five children went trick-or-treating together and decided to randomly split their candy haul at the end of the night.  As it turned out, they got a total of 25 pieces of candy, 5 copies each of 5 different types (they live in a small town).  They distribute the candies by choosing an ordering of the 25 uniformly at random from all shufflings, and then giving the first 5 to the first child, the second 5 to the second, and so on.

What is the probability that each child has one type of candy that they have strictly more of than every other trick-or-treater? Give your (exact!) answer in a lowest terms fraction.

## Solution Approach

Turns out, this is rather difficult to calculate... Much easier to solve it using a computer. 

In general, I am an advocate of teaching simulation techniques to solve questions about probability and combinatorics. A good understanding of Monte Carlo simulations etc. allows you to answer question like this one and much more complicated ones that are really hard to model in a very short time. Ok, the prolem statement is asking for an exact result, but in most business settings, that wouldn't be required. I started with an experimental approach (experimental.py) that just simulates the "draw" over and over again. First, this would allow me to verify whether an exact result is correct and secondly, I had hoped that I might see a pattern emerge. Unfortunately, the latter wasn't the case. However, I was able to observe the following:

With 2 children and 2 types of candy: 1/3 probability
With 3 children and 3 types of candy: approx. 0.29320927323194806 probability
With 4 children and 4 types of candy: approx. 0.16597143078438098 probability
With 5 children and 5 types of candy: approx. 0.04004570549854233 probability

After that, I turned to an exact approach. If every candy had a different color, we know that there are 25! different ways of sorting them. So, we need to figure out how many ways there are to sort them if we only consider the sequences that correspond to a solution where every child gets a dominating amount of candies. 25! is too hight to test every single permutation. However, we can limit this to the permutations where the candies "per child" are in a certain order. For example, if the candies are numbered 0-5, we can consider the two following solutions (for one child identical):

00111
10101

If we stick to the above "notation" (lower numbers before larger numbers), there are only 126 possible outcomes per child (ncr(5+5-1,5-1)) - see stars and bars problem. We can easily generate each of those outcomes using the itertools.combinations method. We can also quite easily calculate for each of these outcomes how many distinct permutations of the outcome exist:

00111
01110
01101
01011
10110
10101
10011
11010
11001
11100

In this particular case, there are ncr(5,2) distinct permutations. If we keep a list for all outcomes and for each of these outcomes we know the number of distinct permutations, we can calculate the total number of distinct permutations, we can calculate the total number of ways to get to this particular solution by calculating the product of the number of distinct permutations for the outcome of each child and then multiplying that by (5!)^5. The last step is only needed if you want to know the absolute number (which is useful, because we can later check it those numbers sum up to 25 factorial), but it isn't really needed since could just also leave it away when calculating the number of dominating outcomes.

Anyway, I do this for all possible outcomes and keep track of the sum. I get to 615847687168425984000000 dominating solutions and to a total of 15511210043330985984000000 possible solutions (which is equal to 25!, hence we did everything correctly). That means that the solution (in decimal) is 0.03970339421928004, which is very close to the experimental result.

There are two python scripts to calculate this: exact.py is more general. In can be used with any number of children and candies, but it is slower. exact2.py is for 5 children/ candies only, but a lot faster. It checks combinations before even finishing to make sure they have no more than 5 candies of one type, so it is possible to skip a lot of invalid solutions. Would be great to have an elegant way to do the same way with the more general solution. Could have done it with recursion, but that is only coming to my mind now.