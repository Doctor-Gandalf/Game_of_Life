__author__ = 'Kellan Childers'

import curses
from math import floor


def center_start(console_height, console_width, window_height, window_width):
    """Find point to start window on center.

    :param console_height: the height of the console
    :param console_width: the width of the console
    :param window_height: the height of the window
    :param window_width: the width of the window
    :return: a tuple representing the coordinates of the start window
    """
    start_y = floor((console_height-window_height)/2)
    start_x = floor((console_width-window_width)/2)
    return start_y, start_x


def custom_border(window, start_y, start_x, stop_y, stop_x, color):
    """Create a border around a window in a certain color."""
    try:
        for i in range(start_y, stop_y):
            window.addstr(i, start_x, ' ', curses.color_pair(color))
            window.addstr(i, stop_x, ' ', curses.color_pair(color))
        for i in range(start_x, stop_x):
            window.addstr(start_y, i, ' ', curses.color_pair(color))
            window.addstr(stop_y, i, ' ', curses.color_pair(color))
        # for loops fail to add last element.
        window.addstr(stop_y, stop_x, ' ', curses.color_pair(color))
    except curses.error:
        # curses.error is raised at end of line and can safely be ignored.
        pass


def fill_conway(conway_graph, curses_pad):
    """Fill the pad with elements from the Conway graph."""
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