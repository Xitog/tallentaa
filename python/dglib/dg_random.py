#-------------------------------------------------------------------------------
# Random utilities
#-------------------------------------------------------------------------------

# This module provides some classes to handle randomness.
# First of all, Interval which act as a Dice.
# The Dice class is just an alias of it with the alias 'roll' for 'random'.
# The Table class stores intervals, results and a dice in order to provide matching:
#      Dice = D20 (1 to 20)
#      If result is Interval(1-5) : Critical Failure
#      If result is Interval(6-10) : Failure
#      If result is Interval(11-15) : Sucess
#      If result is Interval(16-20) : Critical Success

# Damien Gouteux, 2017
#-------------------------------------------------------------------------------

import random
random.seed()

# An interval between two values included
class Interval:

    def __init__(self, start, end):
        if end < start:
            raise Exception("End must be superior to start.")
        self.start = start
        self.end = end

    def __contains__(self, elem):
        return self.start <= elem <= self.end

    def intersect(self, inter):
        return (self.start >= inter.start  and self.end <= inter.end) or (inter.start >= self.start  and inter.end <= self.end)

    def random(self, mod = 0):
        return random.randint(self.start, self.end) + mod

# Just an alias for interval
class Dice(Interval):

    def __init__(self, start=1, end=6):
        Interval.__init__(self, start, end)

    def roll(self, mod = 0):
        return self.random(mod)

# A table matching an interval for a result
class Table:

    def __init__(self, dice):
        self.dice = dice
        self.intervals = []
        self.results = {}
    
    def register(self, interval, result):
        self.intervals.append(interval)
        index = len(self.intervals) - 1
        self.results[index] = result

    def roll(self, mod = 0):
        result = self.dice.roll(mod)
        for i in range(0, len(self.intervals)):
            if result in self.intervals[i]:
                return self.results[i], result
        raise Exception('Result out of all intervals')

def test_random():
    inter1 = Interval(0, 10)
    inter2 = Interval(1, 5)
    inter3 = Interval(20, 100)
    dice = Dice()
    tab_dice = Dice(1, 20)
    tab = Table(tab_dice)
    tab.register(Interval(1, 5), 'Easy')
    tab.register(Interval(6, 10), 'Medium')
    tab.register(Interval(11, 15), 'Hard')
    tab.register(Interval(16, 20), 'Very hard')
    print(1, True, 6 in inter1)
    print(2, False, 6 in inter2)
    print(3, True, inter2.intersect(inter1))
    print(4, True, inter1.intersect(inter2))
    print(5, False, inter1.intersect(inter3))
    print(6, False, inter3.intersect(inter1))
    print(7, '0 <= x <= 10 : ', inter1.random())
    print(8, '1 <= x <= 5 : ', inter2.random())
    print(9, '1 <= x <= 6 : ', dice.roll())
    i = 10
    for i in range(10, 16):
        res, nb = tab.roll()
        print(i, '1-5 : Easy, 6-10 : Medium, 11-15 : Hard, 16-20 : Very hard => ', res, nb)

if __name__ == '__main__':
    test_random()
