# COP4521 HW2 - Merging 2 Sorted Lists

## Authors
Brian Poblete & 
Jayen Lare

## Write Up

One algorithm to merge two sorted lists (a and b) would be to simply have a 
pointer at the start of each list. Then, you would add the smallest value being
pointed to between the two pointers to a new list. You then increment the 
pointer whose value was added to the new list. This process is repeated until
the new list is of the size (a.size + b.size).

The time complexity of this algorithm would be O(n). This process cannot be 
parallelized.

Another algorithm would utilize binary search to merge the two sorted lists.
For this algorithm, you would first select an element from one of the lists and
determine its index inside the list. You would then use binary search to find
the index that the element would take up if it were to be inserted into the 
other list. Those two indices would then be added to get the index of the 
element inside the newly created merged list. This process would be repeated 
for each of the elements inside both lists.

The time complexity of the binary search would be O(log(n)). You would perform
binary search for each element inside both lists. This would leave the time
complexity of the whole algorithm as O(n * log(n)).

However, this can be parallelized. The binary search for each element can 
be split between multiple tasks. This removes the n from the time complexity by
executing every binary search simultaneously.

Thus, we have an ultimate time complexity of **O(log(n)).**

## References

https://www.mcs.anl.gov/~itf/dbpp/text/node127.html#:~:text=A%20parallel%20merge%20algorithm%20performs,using%20the%20hypercube%20communication%20template.

https://stanford.edu/~rezab/classes/cme323/S16/notes/Lecture04/cme323_lec4.pdf

https://www.youtube.com/watch?v=_XOZ2IiP2nw&t=3s&ab_channel=Udacity

https://www.youtube.com/watch?v=GvtgV2NkdVg&ab_channel=Udacity


