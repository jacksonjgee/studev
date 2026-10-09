## Idea
The list is sorted, so compare the target with the middle number.
If they match, you're done. If the target is bigger, it can only be in the right half; if smaller, only in the left half.
Throw away the other half and repeat until you find it or nothing is left.

## Steps
1. Keep two positions: `low` (start) and `high` (end).
2. While `low <= high`, look at the middle position.
3. Equal: print the middle position.
4. Middle is smaller than the target: move `low` to just after the middle.
5. Middle is bigger: move `high` to just before the middle.
6. If the loop ends, the target isn't there: print `-1`.

## Complexity
- Time: O(log n), the search space halves each step.
- Space: O(1).
- Checking every number works too, but is O(n).
