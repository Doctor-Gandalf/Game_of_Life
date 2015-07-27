#!/usr/bin/python3
__author__ = 'Kellan Childers'

import curses
from conway import Conway


def game(stdscr):
    # Ensures a clean visual space.
    stdscr.clear()
    curses.curs_set(False)
    stdscr.nodelay(True)

    # Sets the two main colors for the Conway graph.
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)

    # Creates a pad and Conway graph based on the size of the console.
    console_height, console_width = stdscr.getmaxyx()
    game_pad = curses.newpad(console_height, console_width)
    conway = Conway(console_width, console_height)

    # Fills the Conway graph and displays first iteration.
    conway.randomize()
    fill_conway(conway, game_pad)
    game_pad.refresh(0, 0, 0, 0, console_height-1, console_width-1)

    # Executes Conway's Game of Life repeatedly until user inputs character.
    while True:
        conway.conway()
        fill_conway(conway, game_pad)
        game_pad.refresh(0, 0, 0, 0, console_height-1, console_width-1)

        # Since there is no delay on picking up characters, not inputting a character skips over break.
        try:
            stdscr.getkey()
            break
        except curses.error:
            # curses.error is raised if there was no keypress, so loop should continue.
            pass


def fill_conway(conway_graph, curses_pad):
    # Even when Conway class implements an iterator, this needs to stay this way to avoid printing in wrong location.
    for i in range(conway_graph.get_height()):
        for j in range(conway_graph.get_width()):
            try:
                # Color the space either type 1 (currently blue) or type 2 (currently white).
                if conway_graph.get_elem(j, i):
                    curses_pad.addstr(i, j, ' ', curses.color_pair(1))
                else:
                    curses_pad.addstr(i, j, ' ', curses.color_pair(2))
            except curses.error:
                # curses.error is raised at end of line and can safely be ignored.
                pass

if __name__ == "__main__":
    # curses.wrapper ensures that program will always fully exit from curses mode if an error occurs.
    curses.wrapper(game)
