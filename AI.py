# All Aritifcial Intelligence algorithms
# AI 0
# find direction to move opposite to ball's position
def AI0_OppositeDirection(ballY,ballX,pokeY,pokeX):
    dirs = []
    if pokeY < ballY :
        dirs.append('d')
    if pokeY > ballY :
        dirs.append('u')
    if pokeX > ballX:
        dirs.append('r')
    if pokeX < ballX:
        dirs.append('l')
    return dirs
