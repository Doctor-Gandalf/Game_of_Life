#!/usr/bin/python3
__author__ = 'Kellan Childers'

import curses
import util
from conway import Conway


class IntroScreen:
    def __init__(self, console_height, console_width):
        """Initialize IntroScreen

        :param console_height: the height of the console
        :param console_width: the width of the console
        :return: null
        """
        # If the console window is less wide than the text, it needs to adjust appropriately.
        self.console_height, self.console_width = console_height, console_width
        self.win_height, self.win_width = 8, 49 if console_width >= 49 else console_width
        begin_y, begin_x = util.center_start(console_height, console_width, self.win_height, self.win_width)
        self.intro_win = curses.newwin(self.win_height, self.win_width, begin_y, begin_x)

    def add_intro_text(self):
        """Add text to IntroScreen, centered.

        :return: a reference to the IntroScreen
        """
        self.intro_win.addstr(1, 0, " Welcome to the Conway’s Game of Life simulator!")
        self.intro_win.addstr(3, 0, " To start with a randomized screen, press enter.")
        self.intro_win.addstr(4, 1, " If you would prefer to load a save, press ‘l’.")
        self.intro_win.addstr(6, 14, "To quit, press ‘q’.")

        self.refresh()
        return self

    def add_text_easy(self, y, x, text):
        """Add text that could hit a line break (easier than repeating try catch loop).

        :return: a reference to the IntroScreen
        """
        try:
            self.intro_win.addstr(y, x, text)
        except curses.error:
            pass

        self.refresh()

        return self

    def refresh(self):
        """Refresh contents of IntroScreen.

        :return: a reference to the IntroScreen
        """
        self.intro_win.refresh()
        return self

    def start_conway(self, game_height, game_width):
        """Load or generate a Conway graph from input.

        Quits if 'q' is hit.
        :param game_height: the height of the Conway graph
        :param game_width: the width of the Conway graph
        :return: a Conway graph fitting input
        """
        # Start a new Conway graph to be returned.
        conway = Conway(game_width, game_height)

        # Either randomize the Conway graph (enter), load ('l'), or quit ('q').
        key = self.intro_win.getkey()
        if key is '\n':
            # If enter is hit, start conway as a randomized graph.
            return conway.randomize()
        elif key is 'l':
            # If 'l' is hit, load from file.

            # Clear line 7 in case user input a key other than enter or 'l'.
            self.add_text_easy(7, 0, ' '*49).add_text_easy(7, 0, "Enter filename: ")

            curses.echo()
            filename = self.intro_win.getstr(7, 16)
            curses.noecho()

            try:
                return conway.read_from_file(filename)
            except FileNotFoundError:
                self.add_text_easy(7, 0, ' '*self.win_width)
                self.add_text_easy(7, 7, "File not found. Please try again.")
                return self.start_conway(game_height, game_width)
        elif key is 'q':
            # Exit the program safely.
            exit()
        else:
            # If another key is hit, tell the user it was invalid and retry.
            self.add_text_easy(7, 0, ' '*49).add_text_easy(7, 16, "Invalid command.")
            return self.start_conway(game_height, game_width)

if __name__ == "__main__":
    print("This file creates a curses intro screen for Game_of_life. Please run Game_of_Life for a demonstration.")
