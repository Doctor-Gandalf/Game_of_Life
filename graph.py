#!/usr/bin/python3
__author__ = 'Kellan Childers'


class Graph:
    """Simple module for representing data as a two-dimensional cartesian graph."""
    def __init__(self, width=10, height=10, default=None):
        """Construct a graph of given width and height.

        :param width: the width (x-axis) for the new graph (default 0)
        :param height: the height (y-axis) for the new graph (default 0)
        :param default: the default value for each element in the graph (default None)
        :return: null
        """
        if width < 0 or height < 0:
            raise IndexError("Cannot initialize graph with less than zero dimension")
        self._graph = [[default]*width for i in range(height)]

    def contains_point(self, x=0, y=0):
        """Test if the point (x, y) can be found in graph.

        :param x: the x component of the point (default 0)
        :param y: the y component of the point (default 0)
        :return: a boolean value representing the point's presence in the graph
        """
        return 0 <= x < self.get_width() and 0 <= y < self.get_height()

    def get_elem(self, x=0, y=0):
        """Access the element at a given point (x, y).

        :param x: the x component of the point (default 0)
        :param y: the y component of the point (default 0)
        :return: the element at (x, y)
        """
        if not self.contains_point():
            raise IndexError("Element not present in graph")
        return self._graph[y][x]

    def set_elem(self, val, x=0, y=0):
        """Change the value of an element and return the original value.

        :param val: the new value for the element at point (x, y)
        :param x: the x component of the point (default 0)
        :param y: the y component of the point (default 0)
        :return: the original value of the element at point (x, y)
        """
        if not self.contains_point():
            raise IndexError("Element not present in graph")
        old = self.get_elem(x, y)
        self._graph[y][x] = val
        return old

    def surrounding(self, x=0, y=0):
        """Generate a list of elements surrounding (x, y).

        :param x: the x component of the point (default 0)
        :param y: the y component of the point (default 0)
        :return: a list of elements around (x, y)
        """
        if not self.contains_point(x, y):
            raise IndexError("Element not present in graph")
        # Iterates around (x, y) and adds all points
        tmp = [self.get_elem(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2)
               if self.contains_point(x+i, y+j)]
        # Removes (x, y) from tmp.
        tmp.remove(self.get_elem(x, y))
        return tmp

    def get_height(self):
        """Get the height of the graph.

        :return: the height of the graph
        """
        return len(self._graph)

    def get_width(self):
        """Get the width of the graph.

        :return: the width of the graph
        """
        return len(self._graph[0])

    def resize(self, x=0, y=0, default=None):
        """Change the dimensions of the graph.

        :param x: the new width of the graph (default 0)
        :param y: the new height of the graph (default 0)
        :param default: the default value for any elements not in the original scope (default None)
        :return: a reference to the graph
        """
        if x == self.get_width() and y == self.get_height():
            return self
        elif x < 0 or y < 0:
            raise IndexError("Unable to resize to negative size")
        self._graph = [[self.get_elem(i, j) if self.contains_point(i, j) else default
                        for i in range(x)] for j in range(y)]
        return self

    def copy(self):
        """Copy the graph to a new location.

        :return: a copy of the graph
        """
        new_graph = Graph()
        new_graph._graph = [[self.get_elem(i, j) for i in range(self.get_width())]
                            for j in range(self.get_height())]
        return new_graph

    def clear(self, default=None):
        """Remove all data from the current graph and restore it to default.

        :param default: the default value for each element in the graph (default None)
        :return: a reference to the graph
        """
        for i in range(self.get_height()):
            self._graph[i] = [default] * self.get_width()
        return self

    def print_all(self):
        """Print every row to the command line, starting from row zero.

        :return: null
        """
        for element in self._graph:
            print(element)

if __name__ == "__main__":
    # Short program for showing off capability of module.
    print("Demonstrating graph.py\n")
    print("Creating standard graph")
    print("Printing unmodified graph")
    test = Graph()
    test.print_all()

    print("\nDemonstrating resize\nResizing to three by three")
    test.resize(3, 3)
    test.print_all()

    print("\nDemonstrating get_width and get_height\n")
    print("The width of the graph is {0} and the height of the graph is {1}".format(
        test.get_width(), test.get_height()))

    print("Demonstrating get_elem, set_elem, and surrounding\n")
    print("Adding the numbers 1-9 around point (1, 1) and setting point (1, 1) to 5\n")

    count = 1
    for i in range(3):
        for j in range(3):
            test.set_elem(count, j, i)
            count += 1
    test.print_all()

    print("\nElements surrounding (1, 1):", end=" ")
    for i in test.surrounding(1, 1):
        print(i, end=" ")
    print("\nElement (1, 1) is:", test.get_elem(1, 1))

    print("Demonstrating copy and clear\n")
    print("Copying graph to new graph, then clearing original graph")
    test1 = test.copy()
    test.clear()

    print("\nOriginal graph is:")
    test.print_all()
    print("\nNew graph is:")
    test1.print_all()
