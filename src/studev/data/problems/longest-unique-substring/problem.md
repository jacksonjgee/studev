# Longest Unique Substring

Given a string, find the length of the **longest substring** in which
**no character appears more than once**.

A substring is a run of characters that sit next to each other in the string.
`"bca"` is a substring of `"abcabc"`, but `"acb"` is not.

## Input

- **Line 1:** the string (it may be empty)

## Output

A single integer: the length of the longest substring with no repeated characters.

## Example 1

Input:

```
abcabcbb
```

Output:

```
3
```

`"abc"` is the longest run with no repeats.

## Example 2

Input:

```
pwwkew
```

Output:

```
3
```

`"wke"` works. `"pwke"` is not a substring, because its letters are not next to each other.

## Constraints

- The string has between 0 and 50,000 characters.
- It contains letters, digits, symbols and spaces.

## Hint

Checking every substring is far too slow.
Try keeping a "window" between two positions, and remember where you last saw each character.
