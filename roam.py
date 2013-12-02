# go fullscreen
# from panda3d.core import loadPrcFileData
#loadPrcFileData('', 'fullscreen 1')
import panda3d
import direct.directbase.DirectStart
from panda3d.core import *
from panda3d.core import TransparencyAttrib # enable transparency
from util import *  # useful helper functions
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.ShowBase import ShowBase

import random, sys, os, math
from load import *
_FLAME = ParticleEffect()
_FLAME.loadConfig("fireish.ptf")
_ROT_VEC = (0,90,0)
SPEED = 0.5

_PIKACHU_POS = (-109, 10, -0.5)
_PIKACHU_HPR = (180, 0, 0)
_BULBASAUR_POS = (-109.57, -36.61, 0)
_BULBASAUR_HPR = ( 120, 90, 0 )
_PICHU_POS = (-104.57, 11.61, -0.5)
_PICHU_HPR = (180, 90, 0)
_CHARMANDER_POS = (-103.57, -28.39, 0.19)
_CHARMANDER_HPR = (0, 0, 0)
_GROUDON_POS = (19.57, 9.39, 3.89)
_GROUDON_HPR = ( 320, 0, 0)
_SQUIRTLE_POS = (-99.57, -33.39, 0)
_SQUIRTLE_HPR = (230, 0, 0)
_CHARIZARD_POS = (-67.57, -44.39, 0.49)
_CHARIZARD_HPR = (110, 0, 0)
_BLASTOISE_POS = (-54.57, -44.39, -.49)
_BLASTOISE_HPR = (80, 0, 0)
_FLAME_POS = (-103.57, -24.69, 1.69)
_VENUSAUR_POS = (-44, -20, 0)
_VENUSAUR_HPR = (0,0,0)
_DRAGONITE_POS  = (-44.57, 33.39, .51)
_DRAGONITE_HPR = (0, 0, 0)

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

_BGMUSIC = ("palette.mp3", "route1.mp3", "themeSong.mp3", "cerulean.mp3",\
                "catchEmAll.ogg")

# class World(DirectObject):
class World(ShowBase):
    def skyBoxLoad(self):
        self.spaceSkyBox = load_model('skybox1.egg')
        self.spaceSkyBox.setScale(150)
        self.spaceSkyBox.setLightOff()
        self.spaceSkyBox.reparentTo(render)
        self.spaceSkyBox.setPos(0,0,-200)
        self.spaceSkyBox.setHpr(0,0,0)        

    def loadEnviron(self):
        self.environ = load_model("secondWorld.egg")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)

    def Hooh(self):
        """ hooh """
        self.hoohActor = Actor("anim2hooh.egg",
                           {"wing":"anim-Anim0.egg"})
        self.hoohActor.reparentTo(render)
        self.hoohActor.loop("wing")
        self.hoohActor.setPos(self.ralphStartPos[0],
                              self.ralphStartPos[1]+100,
                              self.ralphStartPos[2]+100)
        self.hoohActor.setPlayRate(4.0,"wing")
        self.hoohActor.setHpr(180,90,0)

        start = Point3(self.ralphStartPos[0], self.ralphStartPos[1]+95,
                       self.ralphStartPos[2]+100)
        end = Point3(self.ralphStartPos[0], self.ralphStartPos[1]-100,
                     self.ralphStartPos[2]+100)
        turnHpr1 = Point3(180,90,0)
        turnHpr2 = Point3(0,90,0) 
        hoohPosInt1 = self.hoohActor.posInterval(5.0, start, startPos = end)
        hoohPosInt2 = self.hoohActor.posInterval(5.0, end, startPos = start)
        hoohHprInt1 = self.hoohActor.hprInterval(1.0, turnHpr2,
                                                 startHpr=turnHpr1)
        hoohHprInt2 = self.hoohActor.hprInterval(1.0, turnHpr1,
                                                 startHpr=turnHpr2)        
        self.hoohFly = Sequence(hoohPosInt1,
                                hoohHprInt1,
                                hoohPosInt2,
                                hoohHprInt2,
                                name="hoohFly")
        self.hoohFly.loop()        

    def loadPokemon(self):
        """ Pikachu """
        self.pikachu = load_model("pikachu.egg")
        self.pikachu.reparentTo(render)
        self.pikachu.setPos(_PIKACHU_POS)
        self.pikachu.setHpr(_PIKACHU_HPR)

        """ Groudon """
        self.Groudon = load_model("Groudon.egg")
        self.Groudon.reparentTo(render)
        self.Groudon.setPos(_GROUDON_POS)
        self.Groudon.setHpr(_GROUDON_HPR)

        """ Bulbasaur """
        self.bulbasaur = load_model("bulbasaur.egg")
        self.bulbasaur.reparentTo(render)
        self.bulbasaur.setPos(_BULBASAUR_POS)
        self.bulbasaur.setHpr(_BULBASAUR_HPR)

        """ hooh """
        self.Hooh()

        """ Pichu """
        self.pichu = load_model("pichu.egg")
        self.pichu.reparentTo(render)
        self.pichu.setPos(_PICHU_POS)
        self.pichu.setHpr(_PICHU_HPR)

        """ Charmander """
        self.charmander = load_model("char.egg")
        self.charmander.reparentTo(render)
        self.charmander.setPos(_CHARMANDER_POS)
        self.charmander.setHpr(_CHARMANDER_HPR)

        """ charizard """
        self.charizard = load_model("charizard.egg")
        self.charizard.reparentTo(render)
        self.charizard.setPos(_CHARIZARD_POS)
        self.charizard.setHpr(_CHARIZARD_HPR)

        """ blastoise """
        self.blastoise = load_model("blastoise.egg")
        self.blastoise.reparentTo(render)
        self.blastoise.setPos(_BLASTOISE_POS)
        self.blastoise.setHpr(_BLASTOISE_HPR)

        """ Squirtle """
        self.squirtle = load_model("squirtle.egg")
        self.squirtle.reparentTo(render)
        self.squirtle.setPos(_SQUIRTLE_POS)
        self.squirtle.setHpr(_SQUIRTLE_HPR)

        """ Dragonite """
        self.dragonite = load_model("dragonite.egg")
        self.dragonite.reparentTo(render)
        self.dragonite.setPos(_DRAGONITE_POS)
        self.dragonite.setHpr(_DRAGONITE_HPR)
        
        _FLAME.setPos(_FLAME_POS)
        _FLAME.setScale(0.1)
        _FLAME.start(parent=render, renderParent=render)
        
        """ venusaur """
        self.venusaur = load_model("venusaur.egg")
        self.venusaur.reparentTo(render)
        self.venusaur.setPos(_VENUSAUR_POS)
        self.venusaur.setHpr(_VENUSAUR_HPR)
        
    def loadRalph(self):
        # Create the main character, Ralph
        basePath = r"../google_drive/ball/data/models/"
        self.ralphStartPos = self.environ.find("**/start_point").getPos()
        self.ralph = Actor(basePath+"ralph",{"run":basePath+"ralph-run",
                                  "walk":basePath+"ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(self.ralphStartPos)
        self.ralph.hide()                    

    def loadNextMusic(self, task):
        # random load background music
        if (self.music.status()!=self.music.PLAYING):
            # not playing
            self.musicCounter += 1
            index = self.musicCounter % len(_BGMUSIC)
            self.music = load_bgmusic(_BGMUSIC[index])
            self.music.play()
        return task.cont
        
    def keyControl(self):
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["forward",1])
        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["forward",0])
        self.accept("w",self.setKey,["upward",1])
        self.accept("w-up",self.setKey,["upward",0])
        self.accept("s",self.setKey,["downward",1])
        self.accept("s-up",self.setKey,["downward",0])
        self.accept("t", self.toggleMusic)
        self.accept("u", self.changeVolume, ['u'])
        self.accept("d", self.changeVolume, ['d'])
        self.accept("h", self.hideInstructions)

    def changeVolume(self, direction):
        if direction == 'u' and self.volume < 1:
            self.volume += 0.1
        else: # direction == 'd'
            if self.volume > 0:
                self.volume -= 0.1
        self.music.setVolume(self.volume)
            
    def toggleMusic(self):
        self.music.stop()
        self.musicCounter += 1 # increment the counter by 
        index = self.musicCounter % len(_BGMUSIC)
        self.music = load_bgmusic(_BGMUSIC[index])
        self.music.play()
        
    def displayInformation(self):
        self.title = addTitle("My Pokemon - Roam Mode")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[Arrow Keys]: Move")
        self.inst3 = addInstructions(0.85, "[w]: look up")
        self.inst4 = addInstructions(0.80, "[s]: look down")
        self.inst5 = addInstructions(0.75, "[t]: toggle next song")
        self.inst6 = addInstructions(0.70, "[u]: volume up")
        self.inst7 = addInstructions(0.65, "[d]: volume down")
        self.inst8 = addInstructions(0.60, "[h]: hide/show instructions")
        self.insts = [self.title, self.inst1, self.inst2, self.inst3,
                      self.inst4, self.inst5, self.inst6, self.inst7,
                      self.inst8]

    def hideInstructions(self):
        if self.instStatus == "show":
            self.instStatus = "hide"
            groupHide(self.insts)
        else: # instructions are hidden
            self.instStatus = "show"
            groupShow(self.insts)
        
    def __init__(self):
        base.enableParticles()
        self.keyMap = {"left":0, "right":0, "forward":0,"backward":0,
                       "upward":0, "downward":0, "leftward":0,"rightward":0,
                       "cam-left":0, "cam-right":0}
        self.instStatus = "show"
        self.musicCounter = 0
        self.music = load_bgmusic(_BGMUSIC[self.musicCounter])
        self.volume = 0
        self.music.setVolume(self.volume)
        base.win.setClearColor(Vec4(0,0,0,1))
        self.above = 3.0
        # load environment
        self.loadEnviron()
        # load ralph
        self.loadRalph()
        # load sky box
        self.skyBoxLoad()
        # load pokemon
        self.loadPokemon()

        self.displayInformation()
        self.keyControl()
        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        taskMgr.add(self.move,"moveTask")
        taskMgr.add(self.setAbove,"setAbove")
        taskMgr.add(self.loadNextMusic, "loadRandomMusic")
        # Game state variables
        self.isMoving = False
        # Set up the camera
        base.disableMouse()
        base.camera.setPos(self.ralph.getX(),self.ralph.getY(),2)
        self.cTrav = CollisionTraverser()
        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,1000)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

        # Uncomment this line to see the collision rays
        #self.ralphGroundColNp.show()
        #self.camGroundColNp.show()
       
        # Uncomment this line to show a visual representation of the 
        # collisions occuring
        #self.cTrav.showCollisions(render)
        
        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    def setAbove(self,task):
        if self.keyMap["upward"] == 1:
            self.above += 0.1
        if self.keyMap["downward"] == 1:
            self.above -= 0.1
        return task.cont
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

        if (self.keyMap["left"]!=0):
            self.ralph.setH(self.ralph.getH() + 113 * globalClock.getDt())
            base.camera.setX(base.camera, +20 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            self.ralph.setH(self.ralph.getH() - 113 * globalClock.getDt())
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["forward"]!=0):
            self.ralph.setY(self.ralph, -75 * globalClock.getDt())
        if (self.keyMap["backward"] != 0):
            pass
            #self.ralph.setY(self.ralph, 75 * globalClock.getDt())
        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):# or (self.keyMap["backward"]!=0):
            if self.isMoving is False:
                #self.ralph.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                #self.ralph.stop()
                #self.ralph.pose("walk",5)
                self.isMoving = False

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.ralph.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

        # Now check for collisions.

        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.
        
        entries = []
        for i in range(self.camGroundHandler.getNumEntries()):
            entry = self.camGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
        if (base.camera.getZ() < self.ralph.getZ() + 2.0):
            base.camera.setZ(self.ralph.getZ() + 2.0)
            
        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        
        self.floater.setPos(self.ralph.getPos())
        self.floater.setZ(self.ralph.getZ() + self.above)#self.above)
        
        base.camera.lookAt(self.floater)
        return task.cont


w = World()
run()

