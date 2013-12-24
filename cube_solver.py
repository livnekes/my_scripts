#!/usr/bin/python
import sys
import time
from pdb import set_trace
from random import randrange

EMPTY = '0'

class Board:
    def __init__(self):
        self.dim_x = 6
        self.dim_y = 4
        self.board = []
        for i in range(self.dim_x):
            self.board.append([EMPTY] * self.dim_y)

    def print_board(self):
        for i in range(self.dim_y):
            print self.get_row(i)
        print 

    def get_tile(self, x, y):
        return self.board[x][y]
    
    def get_row(self, y):
        return [self.board[x][y] for x in range(self.dim_x)]

    def get_column(self, x):
        return self.board[x]

    def set_tile(self, x, y, val):
        self.board[x][y] = val

    def is_complete(self):
        """ Calc if the board is complete """

        for i in self.board.dim_x:
            for j in self.board.dim_y:
                if self.board.get_tile(x,y) == EMPTY:
                    return False
        return True

def main():
    """ This is the Main function """

    b = Board()
    b.print_board()
    for i in range(8):    
        val = str(randrange(1,10))
        x = randrange(b.dim_x)
        y = randrange(b.dim_y)
        b.set_tile(x,y,val)
    b.print_board()

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    main()
    print "Time: ",time.time() - start," seconds"


