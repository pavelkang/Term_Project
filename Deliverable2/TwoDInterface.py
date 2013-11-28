from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
import direct.directbase.DirectStart # loader

_SCALE = (0.16,1,0.1)

def loadBackground(imagePath="../google_drive/ball/data/img/ground.jpg"):
    background = OnscreenImage(parent=render2dp, image=imagePath)

    return background

def loadMyPokemon_Dark(pokes=['caterpie', 'charmander', 'geodude']):
    path = r"../google_drive/ball/data/img/myPoke"
    pokePath = path + r"/%s" %(pokes[0]) + r"_dark.png"
    poke1 = OnscreenImage(parent=aspect2d, image=pokePath,
                         pos=(1.2,0,-0.8), scale=_SCALE)
    poke2Path = path + r"/%s" %(pokes[1]) + r"_dark.png"
    poke2 = OnscreenImage(parent=aspect2d, image=poke2Path,
                          pos=(0.9,0,-0.8), scale=_SCALE)
    poke3Path = path + r"/%s" %(pokes[2]) + r"_dark.png"
    poke3 = OnscreenImage(parent=aspect2d, image=poke3Path,
                          pos=(0.6,0,-0.8), scale=_SCALE)
    poke1.setTransparency(TransparencyAttrib.MAlpha)
    poke2.setTransparency(TransparencyAttrib.MAlpha)
    poke3.setTransparency(TransparencyAttrib.MAlpha)    
    return [poke1, poke2, poke3]

def loadMyPokemon_Bright(pokes=['caterpie', 'charmander', 'geodude']):
    # load bright pokemon pictures
    path = r"../google_drive/ball/data/img/myPoke"
    pokePath = path + r"/%s" %(pokes[0]) + r".png"
    poke1 = OnscreenImage(parent=aspect2d, image=pokePath,
                         pos=(1.2,0,-0.8), scale=_SCALE)
    poke2Path = path + r"/%s" %(pokes[1]) + r".png"
    poke2 = OnscreenImage(parent=aspect2d, image=poke2Path,
                          pos=(0.9,0,-0.8), scale=_SCALE)
    poke3Path = path + r"/%s" %(pokes[2]) + r".png"
    poke3 = OnscreenImage(parent=aspect2d, image=poke3Path,
                          pos=(0.6,0,-0.8), scale=_SCALE)
    poke1.setTransparency(TransparencyAttrib.MAlpha)
    poke2.setTransparency(TransparencyAttrib.MAlpha)
    poke3.setTransparency(TransparencyAttrib.MAlpha)    
    return [poke1, poke2, poke3]

def loadMyIcon():
    path = r"../google_drive/ball/data/img/my.png"
    my = OnscreenImage(parent=aspect2d, image = path, pos=(-1.3,0,-0.8),
                                                            scale=_SCALE)
    my.setTransparency(TransparencyAttrib.MAlpha)
    return my

def loadPokeIcon():
    path = r"../google_drive/ball/data/img/pika.png"
    pika = OnscreenImage(parent=aspect2d, image = path, pos=(-0.8,0,-0.8),
                                                            scale=_SCALE)
    pika.setTransparency(TransparencyAttrib.MAlpha)
    return pika

font = loader.loadFont('Ketchum.ttf')
font.setPixelsPerUnit(50) # increase font quality

def writePokeName(number):
    # 1 is charmander, 2 is geodude, 3 is caterpien
    MSG = {1:"Geodude", 2:"Charmander", 3:"Caterpie"}
    POS = {1:(.5, -.95, -0.8), 2:(.75,-.95,-.8),3:(1.1,-.95,-.8)}
    return OnscreenText(text=MSG[number], style=1, fg=(1,1,1,1), font = font,
                        pos=POS[number], align=TextNode.ALeft, scale = .05)



