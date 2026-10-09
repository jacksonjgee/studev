Find the position of the target in a sorted list, or print `-1`.

## Input
- Line 1: distinct numbers, sorted smallest to largest
- Line 2: the target

## Output
The target's position (from 0), or `-1` if it isn't there.

## Example
```
in:  -1 0 3 5 9 12
     9
out: 4
```

## Notes
- 1 to 100,000 numbers.
- Hint: the list is sorted, so each check can rule out half of what's left.
