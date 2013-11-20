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
_LEFT_COL_LABEL = [i+0.3 for i in _COL_LABEL]
_RIGHT_COL_LABEL = [i-0.4 for i in _COL_LABEL]
_UP_ROW_LABEL = [i-0.3 for i in _ROW_LABEL]
_DOWN_ROW_LABEL = [i+0.3 for i in _ROW_LABEL]

_DIR = {'l':(0,-1), 'r':(0,1), 'u':(-1,0), 'd':(1,0), 's':(0,0)}

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
        self.ballRow = findClosest(y, _ROW_LABEL)
        self.ballCol = findClosest(x, _COL_LABEL)
        
    def setPokeCoord(self, x, y,direction):
        self.pokeX = x
        self.pokeY = y
        self.pokeRow = findClosest(y, _ROW_LABEL)
        if direction == 'r':
            self.pokeCol = findClosest(x, _LEFT_COL_LABEL)
            self.pokeRow = findClosest(y, _ROW_LABEL)
        elif direction == 'l':
            self.pokeCol = findClosest(x, _RIGHT_COL_LABEL)
            self.pokeRow = findClosest(y, _ROW_LABEL)
        elif direction == 'u':
            self.pokeCol = findClosest(x, _COL_LABEL)
            self.pokeRow = findClosest(y, _DOWN_ROW_LABEL)
        elif direction == 'd':
            self.pokeCol = findClosest(x, _COL_LABEL)
            self.pokeRow = findClosest(y, _UP_ROW_LABEL)
            
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
                if self.board[row+drow][col+dcol] == 1: # not wall
                    legals.append(dir)
        #print legals
        return legals

    def getDecision(self):
        # get decision from AI
        # get all legal moves
        legals = self.getLegalDirection()
        decision = AI.AI0_OppositeDirection(self.ballY, self.ballX,
                                            self.pokeY, self.pokeX,
                                            self.ballRow, self.ballCol,
                                            self.pokeRow, self.pokeCol,
                                            legals)
        #print "decision", decision
        return decision
