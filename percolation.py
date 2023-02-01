from QuickUnion import WeightedQuickUnionWithPathComp
import random

# probability of the sites of being open

# extra two points for top and bottom virtual points


class Percolation:
    def __init__(self, nrows=4, ncols=5, prob=0.5, value=0):
        # initialize all the sites are closed
        self.open = [None]*nrows

        for row in range(nrows):
            self.open[row] = [value]*ncols
        # use the weighted quick union with path compression
        self.model = WeightedQuickUnionWithPathComp(nrows*ncols+2)
        self.prob = prob
        self.no_open = 0

    def is_top(self, i, j):
        return (i == 0)

    def is_bottom(self, i, j):
        nrows = len(self.open)
        return (i == nrows-1)

    # convert from 2d array to parent array
    def convert2Dto1D(self, i, j):
        nrows, ncols = len(self.open), len(self.open[0])
        return (i*ncols+j+1)

    def is_open(self):
        return random.random() < self.prob

    # check if the top(first) and bottom(last) is connected
    def percolates(self):
        nrows, ncols = len(self.open), len(self.open[0])
        return (self.model.connected(0, nrows*ncols+1))

    def check_connectivity(self, i, j):
        # check all the neighbours
        current = self.convert2Dto1D(i, j)
        nrows, ncols = len(self.open), len(self.open[0])
        if (i+1 <= nrows-1) and (self.open[i+1][j] == 1):
            self.model.union(
                current, self.convert2Dto1D(i+1, j))
        if (i-1 >= 0) and (self.open[i-1][j] == 1):
            self.model.union(
                current, self.convert2Dto1D(i-1, j))
        if (j+1 <= ncols-1) and (self.open[i][j+1] == 1):
            self.model.union(
                current, self.convert2Dto1D(i, j+1))
        if (j-1 >= 0) and (self.open[i][j-1] == 1):
            self.model.union(
                current, self.convert2Dto1D(i, j-1))

        # check if the site is top or bottom  to connect to the top or bottom virtual point
        if self.is_top(i, j):
            self.model.union(current, 0)
        if self.is_bottom(i, j):
            self.model.union(current, nrows*ncols+1)

    # loop over the grid by opening if the random probability is lower than the site vacancy probability  given
    def open_sites(self, *args):
        nrows, ncols = len(self.open), len(self.open[0])
        if args:
            i = args[0]
            j = args[1]
            self.open[i][j] = 1
            self.check_connectivity(i, j)

        else:

            for i in range(nrows):
                for j in range(ncols):
                    if self.is_open():
                        if self.open[i][j] == 0:
                            self.open[i][j] = 1
                            self.check_connectivity(i, j)
                            self.no_open += 1
