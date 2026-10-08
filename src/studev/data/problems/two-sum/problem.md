Given a list of integers and a target, find the **two different positions**
whose numbers add up to the target.

## Input

- **Line 1:** the numbers, separated by spaces
- **Line 2:** the target

## Output

The two positions (counting from 0), **smallest first**, separated by a space.

## Example 1

Input:

```
2 7 11 15
9
```

Output:

```
0 1
```

`2 + 7 = 9`, and they are at positions 0 and 1.

## Example 2

Input:

```
3 2 4
6
```

Output:

```
1 2
```

## Constraints

- There are between 2 and 10,000 numbers.
- Each number and the target fit in a normal integer (positive or negative).
- There is **always exactly one** answer.
- You may not use the same position twice.

## Hint

Checking every pair works, but takes O(n²) time.
Can you do it in one pass using a dictionary?
