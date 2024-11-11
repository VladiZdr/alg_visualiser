class State:
    def __init__(self, pr=None, n=None, i=-1,x = 0, y = 0):
        self.previous = pr
        self.next = n
        self.index = i
        self.pos_x = x
        self.pos_y = y