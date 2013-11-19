# All Aritifcial Intelligence algorithms
# AI 0
# find direction to move opposite to ball's position
def AI0_OppositeDirection(ballY,ballX,pokeY,pokeX,ballRow,ballCol,
                          pokeRow, pokeCol,legals):
    # legals are all legal directions pokemon can go
    dirs = set()
    print "dirs", dirs
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
    # when ball has blocked one direction
    if row == ballRow: # in the same row
        if dcol * (ballCol-col) > 0: # same direction
            pass
        if col == ballCol:
            if drow * (ballRow-row) > 0:
                pass

