from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
_SCALE = (0.16,1,0.1)

def loadBackground(self, imagePath):
    self.background = OnscreenImage(parent=render2dp, image=imagePath)
    base.cam2dp.node().getDisplayRegion(0).setSort(-20)

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

def loadMyIcon(self, imagePath):
    pass

def loadPokeIcon(self, imagePath):
    pass
