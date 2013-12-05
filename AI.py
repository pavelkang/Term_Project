# All Aritifcial Intelligence algorithms
# AI 0
# find direction to move opposite to ball's position
from math import sqrt
import random

_DIR = {'l':(0,-1), 'r':(0,1), 'u':(-1,0), 'd':(1,0), 's':(0,0)}

_HEURSTIC_BOARD = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                   [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                   [1, 0, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 0, 1],
                   [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                   [2, 1, 3, 1, 1, 2, 0, 0.1, 0, 2, 1, 1, 3, 1, 1],
                   [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 1, 2, 1, 3, 1, 1, 1, 3, 1, 2, 1, 0, 1],
                   [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                   [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]]

def AI0_OppositeDirection(ballY,ballX,pokeY,pokeX,ballRow,ballCol,
                          pokeRow, pokeCol,legals):
    # legals are all legal directions pokemon can go
    dirs = set()
    if pokeY < ballY: dirs.add('d')
    if pokeY > ballY: dirs.add('u')
    if pokeX > ballX: dirs.add('r')
    if pokeX < ballX: dirs.add('l')
    exclude = set()
    if ballRow == pokeRow:
        if ballX < pokeX:
            exclude.add('l') # don't go left
        else:
            exclude.add('r')
    if ballCol == pokeCol:
        if ballY < pokeY:
            exclude.add('u')
        else:
            exclude.add('d')
    dirs = dirs.difference(exclude) # exclude
    dirs = dirs.intersection(set(legals)) # intersect with legals
    if len(dirs) == 0:
        return 's'
    else:
        return dirs.pop() # return the first element 
    return decision

# distance
def euclideanDistance(x, y):
    return sqrt(pow((x[0]-y[0]),2)+pow((x[1]-y[1]), 2))

def euclidHelp(x, y):
    dx = abs(x[0]- y[0])
    dy = abs(x[1]-y[1])
    return (dx, dy)

def euclidIn(x, y, oneDict):
    dx, dy = euclidHelp(x, y)
    for key in oneDict:
        if key == (dx, dy) or key == (dx, dy):
            return True
    return False
        
def memoized(f):
    cachedResults = dict()
    def wrapper(*args, **kwargs):
        arg = euclidHelp(args[0], args[1])
        if euclidIn(args[0], args[1], cachedResults) == False:
            cachedResults[arg] = f(*args, **kwargs)
        return cachedResults[arg]
    return wrapper

euclideanDistance = memoized(euclideanDistance)

def manhattanDistance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])

def evaluationFunc1(ballRow, ballCol, pokeRow, pokeCol, dir):
    # based on Euclidean distance
    newPokeRow, newPokeCol = pokeRow + dir[0], pokeCol + dir[1]
    return euclideanDistance( (ballRow,ballCol), (newPokeRow, newPokeCol))

def evaluationFunc2(ballRow, ballCol, pokeRow, pokeCol, dir):
    # based on Mahattan Distance
    newPokeRow, newPokeCol = pokeRow + dir[0], pokeCol + dir[1]
    return manhattanDistance( (ballRow,ballCol), (newPokeRow, newPokeCol))

def AI1_EuclideanDistance(ballRow, ballCol, pokeRow, pokeCol, legals):
    bestHeuristic = 0
    bestMove = None
    for move in legals:
        heuristic = evaluationFunc1(ballRow, ballCol, pokeRow, pokeCol,
                                    _DIR[move])
        if heuristic > bestHeuristic:
            bestHeuristic = heuristic
            bestMove = move
    return bestMove

def AI2_ManhattanDistance(ballRow, ballCol, pokeRow, pokeCol, legals):
    bestHeuristic = 0
    bestMove = None

    for move in legals:
        heuristic = evaluationFunc2(ballRow, ballCol, pokeRow, pokeCol,
                                  _DIR[move])

        if heuristic > bestHeuristic:
            bestHeuristic = heuristic
            bestMove = move

    return bestMove

_DEPTH = 2

def aheadToCandy(pokeRow, pokeCol, candyRow, candyCol, ballRow, ballCol):
    if euclideanDistance((pokeRow, pokeCol), (candyRow,candyCol)) < \
            euclideanDistance((ballRow, ballCol), (candyRow, candyCol)):
        return True
    return False

def stateHeuristic1(maze, depth):
    def evalFunc_dist_cross_candy(ballRow, ballCol, pokeRow, pokeCol,
                                  candyRow, candyCol, candyOnMaze):
        d = euclideanDistance((maze.ballRow,maze.ballCol), (maze.pokeRow,
                                                            maze.pokeCol))
        
        cross = _HEURSTIC_BOARD[maze.pokeRow][maze.pokeCol] * 0.1
        candy = 0
        if candyOnMaze == True: # there is candy
            candy = 1.0/(0.001+euclideanDistance((maze.pokeRow, maze.pokeCol),
                                          (maze.candyRow, maze.candyCol)))
        return d + cross + candy * .1

    def evalFunc_dist_cross_candy_rock(ballRow, ballCol, pokeRow, pokeCol,
                                       candyRow, candyCol, candyOnMaze,
                                       rockOnMaze, rockRow, rockCol,
                                       onThunder):
        d = euclideanDistance((pokeRow, pokeCol), (ballRow, ballCol))
        cross = _HEURSTIC_BOARD[maze.pokeRow][maze.pokeCol] * 0.1
        candy = 0
        if candyOnMaze == True: # there is candy
            candy = 1.0/(0.001+euclideanDistance((maze.pokeRow,
                                                  maze.pokeCol),
                                                 (maze.candyRow,
                                                  maze.candyCol)))
        if d < 3:
            # too close
            return d
        if d > 8:
            # very safe
            return candy
        if onThunder == True: # go to candy if on Thunder
            rock = 0
            if rockOnMaze == True: # there is rock
                rock =  euclideanDistance((maze.pokeRow, maze.pokeCol),
                                          (maze.rockRow, maze.rockCol))
            return cross + candy*10 + rock*.2 + d
        else: # not on thunder
            if candyOnMaze == True and aheadToCandy(maze.pokeRow,
                            maze.pokeCol, maze.candyRow,
                            maze.candyCol, maze.ballRow, maze.ballCol):
                # pikachu has the advantage of getting candy
                candy= 1.0/(0.001+euclideanDistance((maze.pokeRow,
                                                      maze.pokeCol),
                                                     (maze.candyRow,
                                                      maze.candyCol)))
                return d + candy*1.5 + cross*3
            rock = 0
            if rockOnMaze == True: # there is rock
                rock =  euclideanDistance((maze.pokeRow, maze.pokeCol),
                                          (maze.rockRow, maze.rockCol))

            return d + cross + candy * .1 + rock * 2
    
    if depth == _DEPTH: # reaches maximum depth
        # d is distance, cross is more toward crosswalk
        return evalFunc_dist_cross_candy_rock(maze.ballRow, maze.ballCol,
                                         maze.pokeRow, maze.pokeCol,
                                         maze.candyRow, maze.candyCol,
                                         maze.candyOnMaze, maze.rockOnMaze,
                                         maze.rockRow, maze.rockCol,
                                              maze.onThunder)
    else:
        legals = maze.getLegalDirection()
        bestHeuristic = 0
        for move in legals:
            next_state = maze.nextState(move)
            heuristic = stateHeuristic1(next_state, depth+1)
            if heuristic > bestHeuristic:
                bestHeuristic = heuristic
    # the reason to add stateHeuristic1(maze, depth=_DEPTH) is to
    # break ties by the heurisic of the CURRENT move
    # a = random.randint(0,10) / 1000.0
    return bestHeuristic + stateHeuristic1(maze,depth=_DEPTH)*0.1 #+ a


def AI3_EuclideanDistanceWithSearch(maze):
    bestHeuristic = 0
    bestMove = None
    legals = maze.getLegalDirection()
    for move in legals:
        next_state = maze.nextState(move)
        heuristic = stateHeuristic1(next_state, 0)
        if heuristic > bestHeuristic:
            bestMove = move
            bestHeuristic = heuristic
   # print bestMove
    return bestMove

def useThunderAI(maze):
    if maze.onThunder == True:
        return False
    if maze.pokeCandyCount == 3:
        # has three rare candies
        pokeCandy = euclideanDistance((maze.pokeRow, maze.pokeCol),
                                      (maze.candyRow, maze.candyCol))
        if pokeCandy < 3:
            # very close to candy
            return True
    
    # when player and pikachu are competing for a candy, player is not too
    # close to the candy, use thunderbolt and get that candy.
    if maze.candyOnMaze:
        playerCandy = euclideanDistance((maze.ballRow, maze.ballCol),
                                        (maze.candyRow, maze.candyCol))
        pokeCandy = euclideanDistance((maze.pokeRow, maze.pokeCol),
                                      (maze.candyRow, maze.candyCol))
        diff = playerCandy - pokeCandy
        if -4<diff<2: # if player too close or pokemon too close, no need
            return True

    if maze.playerCandyCount == 0: # player has no candy
        return False
    else: # player has candy
        if maze.distance < 4:
            return True
        else:
            return False
"""
when player and pikachu are competing for a candy, player is not too
close to the candy, use thunderbolt and get that candy.

if maze.candyOnBoard:
    playerCandy = euclideanDistance((maze.ballRow, maze.ballCol),
                                    (maze.candyRow, maze.candyCol))
    pokeCandy = euclideanDistance((maze.pokeRow, maze.pokeCol),
                                    (maze.candyRow, maze.candyCol))
    if pokeCandy + 4 > playerCandy: # player not too close to candy
        return True
"""
