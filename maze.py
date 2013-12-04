# This class is a 2D representation of the board
import random
import AI
import copy
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
_ROWS, _COLS = 9, 15
_ROW_LABEL = (4, 3, 2, 1, 0.1, -0.8, -1.8, -2.8, -4)
_COL_LABEL = (-8.3, -7.2, -6.3, -4.5, -3.3, -2.4, -1.5,
               0, 1.3, 2.5, 3.5, 4.5, 6, 7.2, 8.3)
_LEFT_COL_LABEL = [i+0.25 for i in _COL_LABEL]
_RIGHT_COL_LABEL = [i-0.4 for i in _COL_LABEL]
_UP_ROW_LABEL = [i-0.3 for i in _ROW_LABEL]
_DOWN_ROW_LABEL = [i+0.3 for i in _ROW_LABEL]
_Z = 1.5
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
        self.ballRow, self.ballCol = 0, 8
        self.pokeRow, self.pokeCol = 4, 4
        self.candyOnMaze = False
        self.candyRow, self.candyCol = 0, 0
        self.rockOnMaze = False
        self.rockRow, self.rockCol = 0, 0
        self.onThunder = False
        self.playerCandyCount, self.pokeCandyCount = 0, 0
        self.distance = 0

    def two2Three(self, row, col):
        return ( _COL_LABEL[col],_ROW_LABEL[row], _Z)

    def nextState(self, dir1):
        # takes a current maze and a direction, returns the new state
        # move1 is pikachu's move
        move1 = _DIR[dir1]
        COPY = self.copy()
        COPY.pokeRow += move1[0]
        COPY.pokeCol += move1[1]
        return COPY

    def getDistance(self):
        row0, col0 = self.pokeRow, self.pokeCol
        row1, col1 = self.ballRow, self.ballCol
        drow, dcol  = abs(row0-row1), abs(col0-col1)
        return (drow**2+dcol**2)**.5
    
    def three2Two(self, x, y):
        return (findClosest(y,_ROW_LABEL), findClosest(x,_COL_LABEL))

    def canDropRock(self, rockX, rockY):
        row, col = self.three2Two(rockX, rockY)
        if self.board[row][col] == 1:
            return (row, col)
        else:
            return False
        
    def sendInformation(self, ballDirection, rockOnMaze, onThunder,
                        playerCandyCount, pokeCandyCount, distance):
        self.ballDirection = ballDirection
        self.rockOnMaze = rockOnMaze
        self.onThunder = onThunder
        self.playerCandyCount = playerCandyCount
        self.pokeCandyCount = pokeCandyCount
        self.distance = distance

    def useThunderDecision(self):
        decision = AI.useThunderAI(self.copy())
        return decision
        
    def dropRock(self,row, col):
        self.board[row][col] = 2
        self.rockRow, self.rockCol = row, col

    def clearRock(self):
        try:
            self.board[self.rockRow][self.rockCol] = 1
        except:
            pass
    
    def translateRockPosition(self, rockRefX, rockRefY, dX, dY):
        minXDist = min(1-rockRefX, rockRefX+1)
        minYDist = min(1-rockRefY, rockRefY+1)
        scaleX, scaleY = 8/minXDist, 4/minYDist
        return (dX*scaleX, dY*scaleY)
    
    def generateCandyPos(self):
        self.candyRow = random.randint(0, _ROWS-1)
        self.candyCol = random.randint(0, _COLS-1)
        while self.board[self.candyRow][self.candyCol] != 1: # cant place here
            self.candyRow = random.randint(0, _ROWS-1)
            self.candyCol = random.randint(0, _COLS-1)
        self.candyOnMaze = True
        return self.two2Three(self.candyRow, self.candyCol) # 1 is z position

    def __str__(self):
        return "(%d,%d)" %(self.pokeRow, self.pokeCol)

    def __repr__(self):
        return "(%d,%d)" %(self.pokeRow, self.pokeCol)
    
    def clearCandy(self):
        # clear candy on 2D representation
        self.candyOnMaze = False

    def __eq__(self, other):
        # this is for getting rid of duplicate search states

        return ((self.pokeRow == other.pokeRow) and
                (self.pokeCol == other.pokeCol))


    def __hash__(self):
        return 10*self.pokeRow + self.pokeCol
    
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
                if self.board[row+drow][col+dcol] == 1: # not wall nor rock
                    legals.append(dir)
        return legals

    def copy(self):
        COPY = Maze()
        COPY.board, COPY.ballDirection = (copy.deepcopy(self.board),
                                          self.ballDirection)
        COPY.ballRow, COPY.ballCol = self.ballRow, self.ballCol
        COPY.pokeRow, COPY.pokeCol = self.pokeRow, self.pokeCol
        """
        COPY.ballX, COPY.ballY = self.ballX, self.ballY
        COPY.pokeX, COPY.pokeY = self.pokeX, self.pokeY
        """
        if self.candyOnMaze:
            COPY.candyRow, COPY.candyCol = self.candyRow, self.candyCol
        COPY.candyOnMaze = self.candyOnMaze
        COPY.rockOnMaze = self.rockOnMaze
        COPY.rockRow, COPY.rockCol = self.rockRow, self.rockCol
        COPY.onThunder = self.onThunder
        COPY.distance = self.distance
        COPY.playerCandyCount, COPY.pokeCandyCount = (self.playerCandyCount,
                                                      self.pokeCandyCount)
        return COPY
    
    def getDecision(self):
        # get decision from AI
        # get all legal moves
        # legals = self.getLegalDirection()
        """
        decision = AI.AI0_OppositeDirection(self.ballY, self.ballX,
                                            self.pokeY, self.pokeX,
                                            self.ballRow, self.ballCol,
                                            self.pokeRow, self.pokeCol,
                                            legals)
        """
        """
        decision = AI.AI1_EuclideanDistance(self.ballRow, self.ballCol,
                                            self.pokeRow, self.pokeCol,
                                            legals)
        """
        decision = AI.AI3_EuclideanDistanceWithSearch(self.copy())
        return decision

