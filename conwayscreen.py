__author__ = 'Kellan Childers'

import curses
import util


class ConwayScreen:
    def __init__(self, console_height, console_width, game_height, game_width, conway):
        self.conway = conway
        self.game_pad = curses.newpad(game_height+2, game_width+2)

        # Start and stop points for the graph [start, stop).
        self.start_y, self.start_x = util.center_start(console_height, console_width, game_height+2, game_width+2)
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
        self.fill_conway().refresh()
        self.conway.conway()

