# This is the GUI menu of the game
#from pandac.PandaModules import loadPrcFileData 
#loadPrcFileData("", """ win-size 640 480""") 
from direct.showbase.ShowBase import ShowBase
# from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
# import direct.directbase.DirectStart # loader
from panda3d.core import loadPrcFileData 


# for CardMaker
from panda3d.core import *
# To enable transparency
from panda3d.core import TransparencyAttrib

import sys
from load import *
from pandac.PandaModules import *
# from ball import Labryn

def addOptions(text,font,pos):
    return OnscreenText(text=text,pos=pos,scale = .12,style=1,
                        font = font,fg=(1,0,0,255),
                        frame=(200,68,123,255))

# positions pokemon ball can be at
positions = ((-1.42,0,0.83),(-1.15,0,0.63),(-1.45,0,0.43),(-1,0,0.23))

class Menu(ShowBase):

    def __init__(self):
        # load font
        ShowBase.__init__(self)
        self.font = loader.loadFont('Ketchum.ttf')
        self.font.setPixelsPerUnit(50) # increase font quality
        # load background
        self.tex = load_tex("bg2.jpg")
        # load the ball icon
        self.ball = load_tex("ball.png")
        # load the sound
        self.pikaSound = load_sound("pikachu1.wav")
        self.isDialogOpen = 0

        # Set up a fullscreen card to set the image texture on
        self.cm = CardMaker("My Card")
        self.cm.setFrameFullscreenQuad()
        self.cm.setUvRange(self.tex)
        self.card = NodePath(self.cm.generate())
        self.card.reparentTo(render2d)
        self.card.setTexture(self.tex)
        self.pos = 0

        # add options
        self.op1 = addOptions("Adventure",self.font,(-1.1,0.8))
        self.op2 = addOptions("Multiplayer",self.font,(-0.8,0.6))
        self.op3 = addOptions("My Pokemon",self.font,(-1.1,0.4))
        self.op4 = addOptions("Quit",self.font,(-0.8,0.2))

        # respond to keyboard actions
        self.accept("arrow_up",self.moveArrow,["up"])
        self.accept("arrow_down",self.moveArrow,["down"])
        self.accept("arrow_left",self.moveArrow,["up"])
        self.accept("arrow_right",self.moveArrow,["down"])
        self.accept("enter", self.execute)
        self.accept("escape",sys.exit)
        # add ball
        self.myBall = OnscreenImage(self.ball,scale=0.05,
                                    pos=positions[self.pos])
        self.myBall.setTransparency(TransparencyAttrib.MAlpha)
        self.pikaSound.play()
    # moves the pokeball in reaction to arrow keys        
    def moveArrow(self,direction):
        self.myBall.destroy()
        if direction == "up":
            if self.pos != 0:
                self.pos -= 1
        elif direction == "down":
            if self.pos != 3:
                self.pos += 1
        self.myBall = OnscreenImage(self.ball,scale=0.05,
                                    pos=positions[self.pos])
        self.myBall.setTransparency(TransparencyAttrib.MAlpha)
    # these functions deals with dialogs that come after you hit enter
    def diaCom0(self,com):
        if com == 0:
            # single player
            sys.exit()
        else: self.dialog0.hide(); self.isDialogOpen = 0
    def diaCom1(self,com):
        if com == 0: sys.exit()
        else: self.dialog1.hide() ; self.isDialogOpen = 0
    def diaCom2(self,com):
        if com == 0: sys.exit()
        else: self.dialog2.hide() ; self.isDialogOpen = 0
    def diaCom3(self,com):
        if com == 0: sys.exit()
        else: self.dialog3.hide() ; self.isDialogOpen = 0
        
    def execute(self): # when you press enter
        if self.isDialogOpen == 0:
            position = self.pos
            if position == 0:
                self.dialog0 = YesNoDialog(text="Play single-player adventure?",
                                           command=self.diaCom0,
                                           buttonValueList=[0,1])
            elif position == 1:
                self.dialog1 = YesNoDialog(text="Play with your friends?",
                                           command=self.diaCom1,
                                           buttonValueList=[0,1])
            elif position == 2:
                self.dialog2 = YesNoDialog(text="Go to see your pokemon?",
                                           command=self.diaCom2,
                                           buttonValueList=[0,1])
            elif position == 3:
                self.dialog3 = YesNoDialog(text="Do you want to quit?",
                                           command=self.diaCom3,
                                           buttonValueList=[0,1])
            self.isDialogOpen = 1

m = Menu()            
m.run()
            
"""
if __name__ == "__main__":            
    m = Menu()
    run()
"""
