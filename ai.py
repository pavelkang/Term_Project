<<<<<<< HEAD
from Tkinter import *

def run():
    root = Tk()
    canvas = Canvas(root, width = 300, height = 300)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    init(canvas)
    root.mainloop()

def init(canvas):
    d = canvas.data
    d.board = [ [ 0, 0, 0, 0],
                [ 0, 0, 0, 2],
                [ 0, 0, 0, 0],
                [ 0, 0, 1, 0]]
    d.mePos = (3,2) # 1
    d.enPos = (1,3) # 2
    
=======
# This is a 2d version of the AI
import random
direction = {'d':(1,0), 'u':(-1,0), 'l':(0,-1), 'r':(0,1)}
playerPos = [3,3]
computerPos = [4,4]

def makeBoard(rows, cols):
    return [[0]*cols for row in xrange(rows)]

def getMove(player, board):
    move = raw_input("Enter a Move ->") # format: 34
    if move == "c": # computer move
        return getComputerMove(board)
    elif move in direction:
        return direction[move]
    else:
        print "Not Legal"
        return (0,0)    

def getComputerMove(board):
    return aiComputerMove1(board)
    #return randomComputerMove(board)

def isLegal(board, move):
    rows, cols = len(board), len(board[0])
    x = computerPos[0] + move[0]
    y = computerPos[1] + move[1]
    if x<0 or x>=rows or y<0 or y>=cols: # out of board
        return False
    if x == playerPos and y == playerPos:
        return False
    return True

def randomComputerMove(board):
    move = direction[random.choice(['l','r','u','d'])]
    while isLegal(board,computerPos, playerPos, move) == False:
        move = direction[random.choice(['l','r','u','d'])]
    return move

def aiComputerMove1(board):
    # move by only considering the distance
    bestUtil = 0; bestMove = direction['d']
    for choice in direction:
        move = direction[choice]
        if isLegal(board, move):
            newComputerPos = [move[0]+computerPos[0], move[1]+computerPos[1]]
            util = utility1(playerPos, newComputerPos)
            if util > bestUtil:
                bestUtil = util
                bestMove = move
    return bestMove

def getLabel(n):
    d = {0:"-", 1:"x",2:"o"}
    return d[n]

def utility1(posP, posC):
    # utility by distance
    deltaX = abs(posP[0]-posC[0])
    deltaY = abs(posP[1]-posC[1])
    return (deltaX**2 + deltaY**2)**0.5

def printBoard(board):
    rows, cols = len(board), len(board[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if row == playerPos[0] and col == playerPos[1]:
                print getLabel(1)+" ",
            elif row == computerPos[0] and col == computerPos[1]:
                print getLabel(2)+" ",
            else:
                print getLabel(board[row][col])+" ",
        print

def makeMove(player, move,board):
    rows, cols = len(board), len(board[0])
    if player == 1: # human
        playerPos[0] += move[0]
        playerPos[1] += move[1]
    else: # computer
        computerPos[0] += move[0]
        computerPos[1] += move[1]
        
def play(rows, cols):
    board = makeBoard(rows,cols)
    current = 1; other = 2
    while 1:
        printBoard(board)
        move = getMove(current,board)
        makeMove(current, move,board)
        current = 1 if current == 2 else 2
        
play(8,8)    
>>>>>>> b8c4c576179f63b31df10b466dca071106b89c79
