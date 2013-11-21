from load import *
def loadRareCandy():
    candy = load_model("Gold.egg")
    return candy

def loadLabyrinth():
    MAZE = load_model("3.egg")
    MAZE.reparentTo(render)
    MAZE.setPos(0,0,0)
    MAZE.setHpr(90,0,0)
    return MAZE

def loadRock():
    rock = load_model("rock.egg")
    rock.reparentTo(render)
    rock.setPos(0,0,1)
    return rock
