## Idea
For each number, the partner you need is `target - number`.
Instead of checking every pair, remember the numbers you've already seen.

## Steps
1. Keep a dictionary: number → its position.
2. For each number, check if `target - number` is in the dictionary.
3. If it is, print its position and the current position. Done.
4. If not, store the current number and move on.

## Complexity
- Time: O(n), one pass through the list.
- Space: O(n), for the dictionary.
- Checking every pair works too, but is O(n²).