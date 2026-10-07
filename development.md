# Development Markdown
A List of features to add, notes, bugs, improvements, etc.

## Commands

### `studev ls`
This should all of the files in the working directory as well as subdirectories, displayed as a tree structure.
Optional parameters: 
- maximum depth of the tree
- to show all files or to condense it

Example:
```
studev
├── src/
│   └── studev/
│       ├── commands/
│       │   ├── explain.py
│       │   └── ls.py
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
├── LICENSE
├── pyproject.toml
└── README.md
```

### `studev explain`
This should explain the nuances of the native version of a command. By default it is previous command's native version.
Optional parameters:
- Should be able to specify which command to using `studev explain "example"`

### `studev help`
This should give a helpful list of studev commands.
Optional parameters:
- Could be nice to specify which area/package you want to filter the help list
- Could specify difficulty of commands

## New Features Ideas
### `studev quiz`
This should test the user with a random leetcode question
Optional parameters:
- filter between different types of questions
- specify which question the user would like to try

### `studev note`
This should be able to take a quick note from a specific file and store it in an organised way.

## Possible Useful Libraries
- `argparse`: commands and flags (you're already using it)
- `pathlib`: walking folders and working with file paths, for ls
- `shlex`: splitting a command string into parts, for explain
- `subprocess`: running real commands like git from Python
- `platform`: detecting Mac, Linux or Windows, for --teach
- `json`: storing your command explanations as data
- `random and webbrowser`: useful for the LeetCode idea
- `rich`: colours, bold text, tables and nice formatting in the terminal. It would make studev look polished with little effort. (It also has a ready-made tree display, so if you want the tree logic to be your own work, use rich for colours only.)
- `pytest`: for testing your code.
