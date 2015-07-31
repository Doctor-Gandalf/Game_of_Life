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

        # Initializes pause window for use in pause().
        pause_height, pause_width = 8, 50
        pause_y, pause_x = util.center_start(console_height, console_width, pause_height, pause_width)
        self.pause_window = curses.newwin(pause_height, pause_width, pause_y, pause_x)

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
        self.pause_window.clrtobot()
        self.pause_window.bkgd(' ', 0)

        self.pause_window.addstr(0, 19, "Game paused")
        self.pause_window.addstr(2, 11, "To take a step, press enter")
        self.pause_window.addstr(3, 11, "To save the game, press 's'")
        self.pause_window.addstr(4, 12, "To load a game, press 'l'")
        self.pause_window.addstr(5, 15, "To quit, press 'q'")
        self.pause_window.refresh()

        key = self.pause_window.getkey()
        self.pause_command(key)

    def pause_command(self, key):
        """Take a command in the pause menu."""
        if key == 'p':
            # At this point, clean up and quit.
            self.game_pad.nodelay(True)
            return
        elif key == '\n':
            # Take a step if user hit enter.
            self.take_turn()
            key = self.pause_window.getkey()
            self.pause_command(key)
        elif key == 's':
            # Save to a file.
            self.pause_window.addstr(7, 0, "Enter filename: ")
            self.pause_window.refresh()
            curses.echo()
            filename = self.pause_window.getstr(7, 16)
            curses.noecho()

            try:
                self.conway.save_to_file(filename)
            except FileNotFoundError:
                # Shouldn't ever happen, but just in case.
                self.pause_window.addstr(7, 0, ' '*50)
                self.pause_window.addstr(7, 8, "File not found. Please try again.")
                self.pause_window.refresh()
            finally:
                self.pause()
        elif key == 'l':
            # Load from a file.
            self.pause_window.addstr(7, 0, "Enter filename: ")
            self.pause_window.refresh()
            curses.echo()
            filename = self.pause_window.getstr(7, 16)
            curses.noecho()

            try:
                self.conway.read_from_file(filename)
            except FileNotFoundError:
                # Currently does not work--pause() immediately clears.
                self.pause_window.addstr(7, 0, ' '*50)
                self.pause_window.addstr(7, 8, "File not found. Please try again.")
                self.pause_window.refresh()
            finally:
                self.pause()
        elif key == 'q':
            # Explicitly quit game.
            exit()
        else:
            # If another key is hit, tell the user it was invalid and retry.
            self.pause_window.addstr(7, 0, ' '*50)
            self.pause_window.addstr(7, 16, "Invalid command.")
            self.pause_window.refresh()
            self.pause()

if __name__ == "__main__":
    print("This file creates a curses Conway screen for Game_of_life. Please run Game_of_Life for a demonstration.")
