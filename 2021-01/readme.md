# Problem statement

Source: https://www.janestreet.com/puzzles/figurine-figuring/ 

Jane received 78 figurines as gifts this holiday season:  12 drummers drumming, 11 pipers piping, 10 lords a-leaping, etc., down to 1 partridge in a pear tree.   They are all mixed together in a big bag.  She agrees with her friend Alex that this seems like too many figurines for one person to have, so she decides to give some of her figurines to Alex.   Jane will uniformly randomly pull figurines out of the bag one at a time until she pulls out the partridge in a pear tree, and will give Alex all of the figurines she pulled out of the bag (except the partridge, that’s Jane’s favorite). 

# Solution
  
To get a feeling for the expected number, I chose to use a Monte Carlo simulation first. It is rather easy to simulate the outcome of this game. Unfortunately, even with a high number of simulations it is not possible to determine the expected number with a sufficient accuracy.

For a lower number of figurines (e.g. 4) it is possible to enumerate every single possible outcome so it is perfectly possible to calculate the number of figurines that Alex will get.

However, it is not necessary to enumerate every single combination. It is relatively easy to calculate the number of ways that a certain combination (e.g. 3 pipers and 2 lords) can be chosen. In this case: $ncr(11,3) * ncr(10,2) * 5! * (78-5-1)!$. Explanation: $ncr(11,3)$ is the number of ways 3 pipers can be chosen from all 11 pipers. 5! is the number of ways the 3 pipers and 2 lords can be ordered. (78-5-1)! is the number of ways the remaining figurines (after the partridge) could be in the order. It is important not to forget about this part.

Having this formula, we can enumerate all possible draws (independent of order, before drawing the partridge). With this, we know how many draws (out of all possible draws) will have max 1 figure, 2 figurines etc. Let's call this $d_f$ (d for draws, f for figurine)

The total number of outcomes is $78! = ((n+1)/2*n)$.

The expected value is now as follows $sum(f*d_f/(78!))$

# Validation and conclusion

I compared the simulated result and the calculated result, and they are typically very close (<0.0001).

The method still requires a significant amount of time but it is obviously a lot more efficient than enumerating all outcomes (which is impossible with more than 4 figurines). For 12 figurines, it takes about half a day, 13 figurines would take close to a week on a single score. I assume there is a more direct way of doing it, without enumerating all possible draws (independent of order)

# Result:

For 12 figurines, the expected value is: 6.8597874
