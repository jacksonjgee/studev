# Development Markdown
A list of features to add, notes, bugs, improvements, etc.

## Commands

`studev list`

Shows a full list of all available problems by default. The user can filter the list by difficulty, topic, favourites, user-created, etc.

`studev show <problem name>`

Displays the specified problem's statement as Markdown in the terminal, using the rich library. Instead of a name, the user can pass `--random` to show a random problem, optionally filtered by difficulty, topic, favourites, user-created, etc.

`studev test <problem name> <your solution>`

Unofficially tests your solution's code against sample data of a specified problem to check its correctness.

`studev submit <problem name> <your solution>`
Official attempt at a question that gets tested against all secret test cases for correctness.

`studev new <problem name>`

Generates a problem template with the given name for the user to fill out, in the current working directory by default. The user can specify a different folder to generate the template in.

`studev add <problem folder>`

Adds a problem to the user's problem set. The problem is only added if it is valid, meaning all necessary fields are filled out and in the correct format. Running `add` again on the same problem updates it.

`studev remove <problem name>`

Removes a problem from the user's problem set. Only user-added problems can be removed.

`studev solution <problem name>`

Gives solution statement for a given problem. However the solution is just a description, not in any specific coding language, therefore inplementation of your own solution is still required to solve the problem.

## Problem Template
Each problem will have the following format:
```
problem_name/
├── problem.md     ← problem statement
├── solution.md    ← problem's solution explanation
├── meta.json      ← meta data
└── data/
    ├── 1.in       ← inputs
    └── 1.out      ← outputs
```

### Meta Data
```
meta.json
├── title          ← display name of the problem
├── difficulty     ← "easy", "medium" or "hard"
├── topics         ← list of topic tags
├── user_created   ← true if the user added it
├── starred        ← true if the user starred it
├── attempts       ← number of times it was tested
└── solves         ← number of times all tests passed
```

## Useful Libraries
- `argparse`: commands and flags
- `pathlib`: walking folders and working with file paths
- `subprocess`: running the user's solution and capturing its output
- `json`: reading and writing problem metadata (`meta.json`)
- `shutil`: copying and removing problem folders for `add` and `remove`

- `pytest`: for testing your code
- `blessed`, `textual`, `rich`: Python TUI package

## Future Ideas

- **Playlists:** group problems into named lists, e.g. `studev list --difficulty easy --save ps`, then `studev show --random --playlist ps`.
- **Review mode:** `studev review` brings back previously solved problems after a few days or weeks (spaced repetition).
- **Exam mode:** `studev exam --playlist ps --count 3 --time 60` gives a timed set of problems with a score at the end.
- **Problem packs:** share problem sets as a zip or folder, e.g. `studev import pack.zip`.
- **Speed check:** run a solution on growing input sizes to estimate its time complexity.
- **Custom input:** `studev test two-sum sol.py --input my_case.txt` runs your solution on your own input.
- **Attempt history:** keep every submitted version of a solution to compare progress.
- **Problem notes:** `studev note two-sum` opens a notes file attached to the problem.