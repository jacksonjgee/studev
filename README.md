# studev

Offline coding practice for students. No setup, no account, no internet.

> 🚧 Early development. Not ready to use yet.

studev is a LeetCode-style practice tool that runs entirely in the terminal. A single `pip install` gives you a set of coding problems to solve, with no account, no Docker and no internet needed. When a test fails, studev doesn't just say "Wrong Answer". It shows the input, the expected output and your output side by side, so every failed test teaches you something. You can also write your own problems and add them to your problem set.

## Usage

```
studev list                          # see all problems
studev list --difficulty easy        # filter by difficulty
studev show two-sum                  # read a problem
studev show --random                 # read a random problem
studev test two-sum solution.py      # test your solution
studev submit two-sum solution.py    # Submit your solution
```

### Write your own problems

```
studev new reverse-words             # create a problem template
studev add reverse-words             # add it to your problem set
studev remove reverse-words          # remove one of your problems
```

## Installation

Coming soon.

## License

MIT