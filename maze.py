# This class is a 2D representation of the board
import random
import AI

# 0 is wall. 1 is path
_BOARD = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
          [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
          [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
          [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
          [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
          [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
          [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
          [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1] ]

_ROW_LABEL = (4, 3, 2, 1, 0.1, -0.8, -1.8, -2.8, -4)
_COL_LABEL = (-8.3, -7.2, -6.3, -4.5, -3.3, -2.4, -1.5,
               0, 1.3, 2.5, 3.5, 4.5, 6, 7.2, 8.3)
#_COL_LABEL2 = [i-0.5 for i in _COL_LABEL]
_COL_LABEL2 = (-8.3, -7.2, -6.3, -4.5, -3.3, -2.9, -1.5,
               0, 1.3, 2.3, 3.5, 4.1, 6, 7.2, 8.3)
_DIR = {'l':(0,-1), 'r':(0,1), 'u':(-1,0), 'd':(1,0)}

def coordToPos(number, sequence):
    pass


def findClosest(number, sequence):
    # find the closest entry in a sorted sequence with number
    min_difference = abs(number-sequence[0])
    min_index = 0
    for i in xrange(1, len(sequence)):
        diff = abs(sequence[i]-number)
        if diff < min_difference:
            min_difference = diff
            min_index = i
    return min_index

class Maze(object):
    def __init__(self):
        self.board = _BOARD
    
    def setBallCoord(self, x, y):
        self.ballX = x
        self.ballY = y
        # IMPORTANT TO SWAP X AND Y BELOW
        print "self.ballY", self.ballY
        self.ballRow = findClosest(y, _ROW_LABEL)
        self.ballCol = findClosest(x, _COL_LABEL2)
        
    def setPokeCoord(self, x, y):
        self.pokeX = x
        self.pokeY = y
        self.pokeRow = findClosest(y, _ROW_LABEL)
        self.pokeCol = findClosest(x, _COL_LABEL2)

    def getLegalDirection(self):
        # find out legal direction
        row, col = self.pokeRow, self.pokeCol
        ballRow, ballCol = self.ballRow, self.ballCol
        rows, cols = len(self.board), len(self.board[1])
        legals = []
        for dir in _DIR:
            drow, dcol = _DIR[dir][0], _DIR[dir][1]
            newRow, newCol = drow +row, dcol + col # new row, col for pokemon
            if (newRow < 0 or newRow>= rows or newCol < 0 or newCol>=cols):
                # out of board
                pass
            else:
                # when ball has blocked one direction
                if row == ballRow: # in the same row
                    if dcol * (ballCol-col) > 0: # same direction
                        pass
                if col == ballCol:
                    if drow * (ballRow-row) > 0:
                        pass
                if self.board[row+drow][col+dcol] == 1:
                    legals.append(dir)
        return legals
    
    def getDir(self):
        legals = self.getLegalDirection()
        dirs = AI.AI0_OppositeDirection(self.ballY, self.ballX, self.pokeY,
                                 self.pokeX)
        inter = set(legals).intersection(set(dirs))
        print "dirs", dirs
        print "pokeRow", self.pokeRow, self.pokeCol
        
        if len(inter) != 0:
            result = inter.pop()
        else:
            result = legals[0]
        return result
            
