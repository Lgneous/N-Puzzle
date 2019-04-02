import bisect


class TreeSet:
    def __init__(self):
        self._hashset = set()
        self._treeset = []

    def add(self, element):
        if element not in self:
            bisect.insort(self._treeset, element)
            self._hashset.add(element)

    def ceiling(self, e):
        index = bisect.bisect_right(self._treeset, e)
        if self[index - 1] == e:
            return e
        return self._treeset[bisect.bisect_right(self._treeset, e)]

    def floor(self, e):
        index = bisect.bisect_left(self._treeset, e)
        if self[index] == e:
            return e
        return self._treeset[bisect.bisect_left(self._treeset, e) - 1]

    def __getitem__(self, i):
        return self._treeset[i]

    def __len__(self):
        return len(self._treeset)

    def remove(self, element):
        """
        Remove element if element in TreeSet.
        """
        self._hashset.remove(element)
        try:
            self._treeset.remove(element)
        except ValueError:
            return False
        return True

    def __iter__(self):
        """
        Do ascending iteration for TreeSet
        """
        for element in self._treeset:
            yield element

    def pop(self, index):
        self._hashset.pop(index)
        return self._treeset.pop(index)

    def __str__(self):
        return str(self._hashset)

    def __eq__(self, target):
        if isinstance(target, TreeSet):
            return self._treeset == target._treeset
        if isinstance(target, list):
            return self._treeset == target
        return False

    def __contains__(self, e):
        """
        Fast attribution judgment by bisect
        """
        return e in self._hashset

    def find_lt(self, x):
        "Find rightmost value less than x"
        i = bisect.bisect_left(self._treeset, x)
        if i and self[i - 1] == x:
            to_del = self._treeset.pop(i - 1)
            self._hashset.remove(to_del)
            return True
        return False
