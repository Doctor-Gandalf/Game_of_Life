#!/usr/bin/python3
__author__ = 'Kellan Childers'

import curses
from conway import Conway


def game(stdscr):
    stdscr.clear()
    curses.curs_set(False)
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)

    stdscr.noutrefresh()

    console_height, console_width = stdscr.getmaxyx()
    game_height, game_width = 250, 100

    game_pad = curses.newpad(game_height, game_width)
    conway = Conway(game_height, game_width)

    conway.randomize()
    fill_conway(conway, game_pad)
    game_pad.refresh(0, 0, 0, 0, console_height-1, console_width-1)

    while True:
        conway.conway()
        fill_conway(conway, game_pad)
        game_pad.refresh(0, 0, 0, 0, console_height-1, console_width-1)

        try:
            stdscr.getkey()
            break
        except curses.error:
            # curses.error is raised if there was no keypress, so loop should continue.
            pass


def fill_conway(conway_graph, curses_pad):
    for i in range(conway_graph.get_height()):
        for j in range(conway_graph.get_width()):
            try:
                if conway_graph.get_elem(j, i):
                    curses_pad.addstr(i, j, '\u2588', curses.color_pair(1))
                else:
                    curses_pad.addstr(i, j, '\u2588', curses.color_pair(2))
            except curses.error:
                # curses.error is raised at end of line and can safely be ignored.
                pass

if __name__ == "__main__":
    curses.wrapper(game)
