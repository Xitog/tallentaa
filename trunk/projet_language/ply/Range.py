import random   # for range
import datetime # for date

class PLP_DATE(object):
    
    def __init__(self):
        self.core = datetime.datetime.today()
    
    def year(self):
        return self.core.year
    
    def __str__(self):
        return "Date(Y=%d/M=%d/D=%d)" % (self.core.year, self.core.month, self.core.day)

class PLP_TIME(object):
    
    def __init__(self):
        self.core = datetime.datetime.now()

class PLP_RANGE(object):
    
    def __init__(self, x, y):
        self.core = xrange(x, y)
    
    def random(self):
        return random.randint(self.core[0], self.core[len(self.core)-1]+1)

    def __repr__(self):
        return "Range(%d,%d)" % (self.core[0], self.core[len(self.core)-1]+1)
