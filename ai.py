# This is a 2d version of the AI
direction = {'d':(1,0), 'u':(-1,0), 'l':(0,-1), 'r':(0,1)}

def makeBoard(rows, cols):
    return [[0]*cols for row in xrange(rows)]

def getMove(player, board):
    printBoard(board)
    move = raw_input("Enter a Move ->") # format: 34
    if move == "c": # computer move
        return getComputerMove(board)
    elif move in direction:
        return direction[move]
    else:
        print "Not Legal"
        return (0,0)
    return (int(row), int(col))

def getComputerMove(board):
    pass

def randomComputerMove(board):
    



def getLabel(n):
    d = {0:"-", 1:"x",2:"o"}
    return d[n]

def printBoard(board):
    rows, cols = len(board), len(board[0])
    for row in xrange(rows):
        for col in xrange(cols):
            print getLabel(board[row][col])+" ",
        print

def makeMove(player, move,board):
    rows, cols = len(board), len(board[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if board[row][col] == player:
                board[row][col] = 0
    board[move[0]][move[1]] = player
        
def play(rows, cols):
    board = makeBoard(rows,cols)
    current = 1; other = 2
    board[3][3] = current
    board[4][4] = other
    playerPosition = (3,3)
    computerPosition = (4,4)
    while 1:
        move = getMove(current,board)
        makeMove(current, move,board)
        current = 1 if current == 2 else 2
        
play(8,8)    
