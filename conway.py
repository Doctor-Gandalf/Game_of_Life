#!/usr/bin/python3
__author__ = 'Kellan Childers'

from random import randint
from graph import Graph


class Conway(Graph):
    """Module for representing Conway's Game of Life in a simple graph format."""

    def __init__(self, width=10, height=10):
        """Construct a given Conway graph of given width and height.

        :param width: the width (x-axis) for the new graph (default 0)
        :param height: the height (y-axis) for the new graph (default 0)
        :return: null
        """
        super(Conway, self).__init__(width, height, 0)

    def conway(self):
        """Execute the rules of Conway's Game of Life on the Conway graph.

        :return: a reference to the Conway graph
        """
        self._graph = [[1 if sum(self.surrounding(x, y)) in (2, 3) else 0
                       for x in range(self.get_width())] for y in range(self.get_height())]
        return self

    def randomize(self):
        """Randomly fill the Conway graph with 0s and 1s.

        :return: a reference to the Conway graph
        """
        self._graph = [[randint(0, 1) for j in range(self.get_width())] for i in range(self.get_height())]
        return self

    def set_elem(self, val, x=0, y=0):
        """Change the value of an element and return the original value.

        :param val: the new value for the element at point (x, y)
        :param x: the x component of the point (default 0)
        :param y: the y component of the point (default 0)
        :return: the original value of the element at point (x, y)
        """
        if val is 0 or val is 1:
            return super(Conway, self).set_elem(val, x, y)
        else:
            raise TypeError("Value is not a boolean")

    def resize(self, x=0, y=0, default=0):
        """Change the dimensions of the graph.

        :param x: the new width of the Conway graph (default 0)
        :param y: the new height of the Conway graph (default 0)
        :param default: the default value for any elements not in the original scope (default None)
        :return: a reference to the Conway graph
        """
        if default is 0 or default is 1:
            return super(Conway, self).resize(x, y, default)
        else:
            raise TypeError("Default is not a bolean")

    def clear(self, default=0):
        """Remove all data from the current graph and restore it to default.

        :param default: the default value for each element in the graph (default None)
        :return: a reference to the graph
        """
        if default is 0 or default is 1:
            return super(Conway, self).clear(default)
        else:
            raise TypeError("Default is not a bolean")


if __name__ == "__main__":
    # Short program for showing capability of module.
    print("Demonstrating Conway's Game of Life on 5 x 5 Conway Graph\n")
    test = Conway(5, 5)
    test.randomize()
    print("Randomized graph:")
    test.print_all()
    print("\nGraph after executing one turn of Conway's Game of Life:")
    test.conway()
    test.print_all()
