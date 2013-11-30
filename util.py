from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

def checkEat(x, y, candyX, candyY):
    epsilon = 0.3
    if abs(x-candyX) <= epsilon:
        if abs(y-candyY) <= epsilon:
            return True
    return False

def groupHide(group):
    for i in group:
        i.hide()

def groupShow(group):
    for i in group:
        i.show()

def candyStatus(player, number): # 0 is left, 1 is right
    msg = str(number)
    if player == 0: # this is player
        pos1 = (0.26, -0.78, -0.8)
    else:
        pos1 = (-0.21, -0.78, -0.8)
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=pos1, align=TextNode.ALeft, scale = .08)
    
