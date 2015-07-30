#!/usr/bin/python3
__author__ = 'Kellan Childers'

import curses
import util


class ConwayScreen:
    def __init__(self, console_height, console_width, game_height, game_width, conway):
        """Initialize ConwayScreen.

        :param console_height: the height of the console
        :param console_width: the width of the console
        :param game_height: the height of the game
        :param game_width: the width of the game
        :param conway: a Conway graph
        :return: null
        """
        self.conway = conway
        self.game_pad = curses.newpad(game_height, game_width)

        # Start and stop points for the graph [start, stop).
        self.start_y, self.start_x = util.center_start(console_height, console_width, game_height, game_width)
        # Stop points are a function based on the start.
        self.stop_y, self.stop_x = self.start_y + game_height, self.start_x + game_width

        # Surround Conway graph with a box
        util.color_box(self.game_pad, 0, 0, game_height, game_width, 0)

    def fill_conway(self):
        """Fill the pad with elements from the Conway graph."""
        # Even when Conway class implements an iterator, this needs
        # to stay this way to avoid printing in wrong location.
        for i in range(self.conway.get_height()):
            for j in range(self.conway.get_width()):
                try:
                    # Color the space either type 1 (currently blue) or type 2 (currently white).
                    if self.conway.get_elem(j, i):
                        self.game_pad.addstr(i+1, j+1, ' ', curses.color_pair(1))
                    else:
                        self.game_pad.addstr(i+1, j+1, ' ', curses.color_pair(2))
                except curses.error:
                    # curses.error is raised at end of line and can safely be ignored.
                    pass
        return self

    def refresh(self):
        """Fully refresh the ConwayScreen.

        :return: a reference to the ConwayScreen
        """
        self.game_pad.refresh(0, 0, self.start_y, self.start_x, self.stop_y, self.stop_x)
        return self

    def take_turn(self):
        """Take a turn of Conway's Game of life."""
        self.fill_conway().refresh()
        self.conway.conway()
        self.game_pad.nodelay(True)

        # Since there is no delay on picking up characters on stdscr,
        # not inputting a character skips over break.
        try:
            key = self.game_pad.getkey()
            if key == 'q':
                exit()
            elif key == 'p':
                self.pause()
        except curses.error:
            # curses.error is raised if there was no keypress, so loop should continue.
            pass

    def pause(self):
        """Pause the game and take commands until unpaused."""
        self.game_pad.nodelay(False)
        key = self.game_pad.getkey()
        if key == 'p':
            # At this point, clean up and quit.
            self.game_pad.nodelay(True)
            return
        elif key == 'q':
            # Explicitly quit game.
            exit()
        elif key == '\n':
            # Take a step if user hit enter.
            self.take_turn()
        self.pause()

if __name__ == "__main__":
    print("This file creates a curses Conway screen for Game_of_life. Please run Game_of_Life for a demonstration.")
