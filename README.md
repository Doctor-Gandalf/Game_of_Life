# Game_of_Life
Simple implementation of Conway's Game of Life using Python and Curses

Built and tested on OSX 10.10.4 using Python 3.4.3.
Will probably run on Linux as long as Python 3 is installed, but due to using Curses will probably not run on Windows.

Interpreter located at /usr/bin/python3, if otherwise either modify Game_of_Life appropriately
or run using python3 instead of open.
To run, open Game_of_Life (either by running python3 or opening).
To close, press 'q'.

To come:
- More commands via keyboard
- Better visuals (to the extent Curses allows)
- Ability to resize terminal while running program
- Ability to recolor true and false

Known issues:
- Program crashes when switching from full screen to windowed view or when shrinking windowed view
- When in windowed, increasing size leaves graph in top left corner and not surrounded by border