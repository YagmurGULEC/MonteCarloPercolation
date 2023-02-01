
# eager approach
class QuickFind(object):
    def __init__(self, n=10):
        # store the parent of each node
        self.parent = [i for i in range(n)]
        # the number of components
        self.count = n

    # merge the components in the same root
    def union(self, i, j):
        p1 = self.parent[i]
        p2 = self.parent[j]
        if (p1 == p2):
            return
        else:
            for i in range(len(self.parent)):
                if self.parent[i] == p1:
                    self.parent[i] = p2
            self.count -= 1

    def connected(self, i, j):
        return (self.parent[i] == self.parent[j])


# lazy approach inherited from QuickFind
class QuickUnion(QuickFind):
    def __init__(self, n=10):
        super().__init__(n)
        # # store the parent of each node
        # self.parent = [i for i in range(n)]
        # # the number of components
        # self.count = n

    def root(self, i):
        while (i != self.parent[i]):
            i = self.parent[i]

        return i

    # assign the root of the first argument as the root of the second
    def union(self, i, j):
        p1 = self.root(i)
        p2 = self.root(j)
        self.parent[p1] = p2
        self.count -= 1


# Weighted QuickUnion
# try to maintain lower depth in binary tree
class WeightedQuickUnion(QuickUnion):
    def __init__(self, n=10):
        super().__init__(n)
        # keep track of the number of objects in the tree rooted at each nodes
        self.size = [1 for i in range(n)]

    # assign the root of the first argument as the root of the second

    def union(self, i, j):
        p1 = self.root(i)
        p2 = self.root(j)
        if (p1 == p2):
            return
        # link root of smaller tree to root of larger tree
        if (self.size[p1] < self.size[p2]):
            self.parent[p1] = p2
            self.size[p2] += self.size[p1]
        else:
            self.parent[p2] = p1
            self.size[p1] += self.size[p2]

        self.count -= 1


# Weighted QuickUnion With Path Compression
# fastest method since it contains the improvement of path compression and  weighted approach
class WeightedQuickUnionWithPathComp(WeightedQuickUnion):
    def __init__(self, n=10):
        super().__init__(n)

    def root(self, i):
        while (i != self.parent[i]):
            # extra line to flatten the tree
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]

        return i


if __name__ == "__main__":
    # test cases for QuickFind implementation
    d = QuickFind()
    d.union(4, 3)
    print(d.parent == [0, 1, 2, 3, 3, 5, 6, 7, 8, 9])
    d.union(3, 8)
    print(d.parent == [0, 1, 2, 8, 8, 5, 6, 7, 8, 9])
    d.union(6, 5)
    print(d.parent == [0, 1, 2, 8, 8, 5, 5, 7, 8, 9])
    d.union(9, 4)
    print(d.parent == [0, 1, 2, 8, 8, 5, 5, 7, 8, 8])
    d.union(2, 1)
    print(d.parent == [0, 1, 1, 8, 8, 5, 5, 7, 8, 8])
    print(d.connected(8, 9) == True)
    print(d.connected(5, 0) == False)
    d.union(5, 0)
    print(d.parent == [0, 1, 1, 8, 8, 0, 0, 7, 8, 8])
    d.union(7, 2)
    print(d.parent == [0, 1, 1, 8, 8, 0, 0, 1, 8, 8])
    d.union(6, 1)
    print(d.parent == [1, 1, 1, 8, 8, 1, 1, 1, 8, 8])
    print(d.count)
    e = QuickUnion()
    # test cases for QuickUnion implementation
    e.union(4, 3)
    print(e.parent == [0, 1, 2, 3, 3, 5, 6, 7, 8, 9])
    e.union(3, 8)
    print(e.parent == [0, 1, 2, 8, 3, 5, 6, 7, 8, 9])
    e.union(6, 5)
    print(e.parent == [0, 1, 2, 8, 3, 5, 5, 7, 8, 9])
    e.union(9, 4)
    print(e.parent == [0, 1, 2, 8, 3, 5, 5, 7, 8, 8])
    e.union(2, 1)
    print(e.parent == [0, 1, 1, 8, 3, 5, 5, 7, 8, 8])
    print(e.connected(8, 9) == True)
    print(e.connected(5, 4) == False)
    e.union(5, 0)
    print(e.parent == [0, 1, 1, 8, 3, 0, 5, 7, 8, 8])
    e.union(7, 2)
    print(e.parent == [0, 1, 1, 8, 3, 0, 5, 1, 8, 8])
    e.union(6, 1)
    print(e.parent == [1, 1, 1, 8, 3, 0, 5, 1, 8, 8])
    e.union(7, 3)
    print(e.parent == [1, 8, 1, 8, 3, 0, 5, 1, 8, 8])
    print(e.count)
    f = WeightedQuickUnion()
    f.union(4, 3)
    print(f.parent == [0, 1, 2, 4, 4, 5, 6, 7, 8, 9])
    f.union(3, 8)
    print(f.parent == [0, 1, 2, 4, 4, 5, 6, 7, 4, 9])
    f.union(6, 5)
    print(f.parent == [0, 1, 2, 4, 4, 6, 6, 7, 4, 9])
    f.union(9, 4)
    print(f.parent == [0, 1, 2, 4, 4, 6, 6, 7, 4, 4])
    f.union(2, 1)
    print(f.parent == [0, 2, 2, 4, 4, 6, 6, 7, 4, 4])
    f.union(5, 0)
    print(f.parent == [6, 2, 2, 4, 4, 6, 6, 7, 4, 4])
    f.union(7, 2)
    print(f.parent == [6, 2, 2, 4, 4, 6, 6, 2, 4, 4])
    f.union(6, 1)
    print(f.parent == [6, 2, 6, 4, 4, 6, 6, 2, 4, 4])
    f.union(7, 3)
    print(f.parent == [6, 2, 6, 4, 6, 6, 6, 2, 4, 4])
