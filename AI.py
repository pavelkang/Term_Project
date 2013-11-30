# All Aritifcial Intelligence algorithms
# AI 0
# find direction to move opposite to ball's position
_DIR = {'l':(0,-1), 'r':(0,1), 'u':(-1,0), 'd':(1,0), 's':(0,0)}

_HEURSTIC_BOARD = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                   [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                   [1, 0, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 0, 1],
                   [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                   [2, 1, 3, 1, 1, 2, 0, 1, 0, 2, 1, 1, 3, 1, 1],
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
    return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5

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
   return bestMove

def stateHeuristic1(maze, depth):
    if depth == _DEPTH: # reaches maximum depth
        # d is distance, cross is more toward crosswalk
        d = euclideanDistance((maze.ballRow,maze.ballCol), (maze.pokeRow,
                                                            maze.pokeCol))
        cross = _HEURSTIC_BOARD[maze.pokeRow][maze.pokeCol] * 0
        return d+cross

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
    return bestHeuristic + stateHeuristic1(maze,depth=_DEPTH)*0.1

