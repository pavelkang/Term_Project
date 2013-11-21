
def checkEat(x, y, candyX, candyY):
    epsilon = 0.1
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
