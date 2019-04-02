import bisect


class TreeSet:
    def __init__(self):
        self._hashset = set()
        self._treeset = []

    def add(self, element):
        if element not in self:
            bisect.insort(self._treeset, element)
            self._hashset.add(element)

    def __getitem__(self, i):
        return self._treeset[i]

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

    def __str__(self):
        return str(self._hashset)

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
