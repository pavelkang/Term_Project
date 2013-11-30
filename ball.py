# This is the single-player mode program
# Author: Kai Kang
# Functions groudCollideHandler, wallCollideHandler, and rollTask come from
# Panda3D sample code with slight modification.

import direct.directbase.DirectStart
# collision
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
# material
from panda3d.core import Material,LRotationf,NodePath
# light
from panda3d.core import AmbientLight,DirectionalLight
# node
from panda3d.core import TextNode
# enable particle effects
from direct.particles.ParticleEffect import ParticleEffect
# vector
from panda3d.core import Vec3,Vec4,BitMask32
# GUI
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib # enable transparency
# Direct Object
from direct.showbase.DirectObject import DirectObject
# Interval
from direct.interval.MetaInterval import Sequence,Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func,Wait
# Task
from direct.task.Task import Task
import sys

from math import pi, sin, cos

#self written module
from load import *
import TwoDInterface as Two_D
import maze
import Key_Control as Control
import Model_Load
from util import *

MAZE = maze.Maze()
ACCELERATION = 70
MAX_SPEED = 4
MAX_SPEED_SQ = MAX_SPEED ** 2
_JERK = 0.08
_SPEED = 0.05
UP = Vec3(0,0,1) # upward vector
_FLOOR = 1
_FOCUS = [0,0,0]
_FLAME = ParticleEffect()
_FLAME.loadConfig("fireish.ptf")
_EPSILON = 0.001

class Labryn(DirectObject): # game class

    def setCamera(self, spin):
        # set camera spin state
        self.spin = spin
    
    def spinCamera(self, task):
        # deal with spinning the camera
        # _FOCUS: focus point, changed by panning the camera
        # CAM_R: radius, changed by zooming
        # cameraSpinCount: amount of spinning, changed by spinning
        if self.spin == 1: # spin counter-clockwise
            self.cameraSpinCount += 1
            angleDegrees = self.cameraSpinCount
            angleRadians =  angleDegrees * (pi/ 180)
            self.CAM_RAD = angleRadians
            camera.setPos(_FOCUS[0]+self.CAM_R*cos(-pi/2+self.CAM_RAD),
                          _FOCUS[1]+self.CAM_R*sin(-pi/2+self.CAM_RAD),
                          (25.0/12)*self.CAM_R) 
            camera.setHpr(angleDegrees,-65,0)
        elif self.spin == 2: # spin clockwise
            self.cameraSpinCount  -= 1
            angleDegrees = self.cameraSpinCount
            angleRadians =  angleDegrees * (pi/ 180)
            self.CAM_RAD = angleRadians
            camera.setPos(_FOCUS[0]+self.CAM_R*cos(-pi/2+self.CAM_RAD),
                          _FOCUS[1]+self.CAM_R*sin(-pi/2+self.CAM_RAD),
                          (25.0/12)*self.CAM_R)
            camera.setHpr(angleDegrees,-65,0)
        elif self.spin == 3: # ZOOM IN not spin
            self.cameraZoomCount += 1
            deltaR = self.cameraZoomCount * 0.1
            new_R = 12-deltaR
            self.CAM_R = new_R
            camera.setPos(_FOCUS[0] + self.CAM_R*cos(-pi/2+self.CAM_RAD),
                          _FOCUS[1] + self.CAM_R*sin(-pi/2+self.CAM_RAD),
                          (25.0/12)*new_R)
        elif self.spin == 4: # ZOOM OUT
            self.cameraZoomCount -= 1
            deltaR = self.cameraZoomCount * 0.1
            new_R = 12-deltaR
            self.CAM_R = new_R
            camera.setPos(_FOCUS[0] + self.CAM_R*cos(-pi/2+self.CAM_RAD),
                          _FOCUS[1] + self.CAM_R*sin(-pi/2+self.CAM_RAD),
                          (25.0/12)*self.CAM_R)
        return Task.cont

    def checkMouse(self, task):
        # get mouse position 
        if base.mouseWatcherNode.hasMouse():
            self.mouseX=base.mouseWatcherNode.getMouseX()
            self.mouseY=base.mouseWatcherNode.getMouseY()
        return Task.cont

    def dropRock(self):
        # when the user clicks, rock is dropped
        if self.pokeMoveChoice == 1: # selected Geodude
            result = MAZE.canDropRock(self.rockX, self.rockY)
            if result != False: # can place rock here
                MAZE.dropRock(result[0],result[1])
                self.rock.setPos(self.rockX, self.rockY, 1)
                self.rockOnMaze = True
                self.pokeMoveChoice = None
                self.myPokeName.hide()
                self.myPokeName = None
                self.updateTwoD()
                self.playerCandyCount -= 1

    def useFlame(self):
        # use flame to Pikachu -> cannot move
        self.onFire = True # on fire
        self.playerCandyCount -= 1
        self.pokeStatus = 1
        self.flame = ParticleEffect()
        self.flame.loadConfig("fireish.ptf")
        self.flame.setPos(self.pikachu.getPos())
        self.flame.start(parent=render, renderParent=render)
        self.updateTwoD()

    def useStringShot(self):
        # use string shot -> speed goes down
        self.pokeStatus = 2
        self.updateTwoD()

    def placeRock(self, task):
        # rock moves with mouse cursor
        if self.pokeMoveChoice == 1: # selected Geodude
            dX,dY = ((self.mouseX-self.rockRefX),
                     (self.mouseY-self.rockRefY))
            self.rockX, self.rockY = MAZE.translateRockPosition(self.rockRefX,
                                                      self.rockRefY,
                                                      dX, dY)
            self.rock.show()
            self.rock.setPos(self.rockX, self.rockY, 1)
        self.updateTwoD()
        return Task.cont
    
    def placeRareCandy(self, task):
        # place rare candy with interval
        # needs to be improved
        if int(task.time) % 4 == 9 and self.candyOnBoard:
            self.candy.hide()
            self.candyOnBoard = False
        if int(task.time) % 10 ==  0 and (self.candyOnBoard == False):
            # every 10 seconds
            self.candy.setPos(MAZE.generateCandyPos())
            self.candy.show()
            self.candyOnBoard = True
        return Task.cont

    def updateTwoD(self):
        # update player candy count
        self.playerCandyStatus.destroy()
        self.playerCandyStatus = candyStatus(0, self.playerCandyCount)
        self.pokeCandyStatus.destroy()
        self.pokeCandyStatus = candyStatus(1, self.pokeCandyCount)
        # update my pokes color     
        if self.playerCandyCount == 0 :
            groupHide(self.myPokesBright)
            groupShow(self.myPokesDark)
            # update name
            if self.myPokeName != None:
                self.myPokeName.destroy()

    def clearRock(self):
        # clear rock 
        self.rock.hide()
        self.rockOnMaze = False
        MAZE.clearRock() # clear it in 2D

    def clearFlame(self):
        # clear flame
        self.onFire = False
        self.flame.cleanup()
        self.pokeStatus = 0
        self.pokeMoveChoice = None
        try:
            self.myPokeName.destroy()
        except:
            pass
        self.myPokeName = None

    def clearString(self):
        # clear string shot
        self.pokeStatus = 0
        self.pokeMoveChoice = None
        try:
            self.myPokeName.destroy()
        except:
            pass
        self.myPokeName = None

        
    def timer(self, task): # deals with moves' lasting effects
        ##############################################################
        if self.rockOnMaze: # rock on maze
            self.rockCounter += 1
        elif self.rockCounter != 1: # rock not on maze, counter not cleared
            self.rockCounter = 0

        if self.onFire:
            self.fireCounter += 1
        elif self.fireCounter != 1:
            self.fireCounter = 0

        if self.pokeStatus == 2: # string shot
            self.stringCounter += 1
        elif self.stringCounter != 1:
            self.stringCounter = 0

        ##################################################################
        if self.rockCounter == 500:
            self.clearRock()

        if self.fireCounter == 80:
            self.clearFlame()

        if self.stringCounter == 120:
            self.clearString()
            
        return Task.cont
    
    def usePokeMove(self, number):
        # use pokemon move
        if self.playerCandyCount > 0: # have more than one candy
            if number == 1 and self.rockOnMaze == False:
                if self.pokeMoveChoice != 1: # NONE or other
                    # set to center position
                    centerx =  base.win.getProperties().getXSize()/2
                    centery =  base.win.getProperties().getYSize()/2
                    base.win.movePointer(0,centerx,centery)
                    self.pokeMoveChoice = 1 # placeRock called here
                    self.rockRefX, self.rockRefY = 0,0
                    self.rock.show()
                    self.rock.setPos(0,0,1)
                else: # already 1
                    self.pokeMoveChoice = None
                    self.clearRock() # clear rock
            elif number == 2:
                if self.pokeMoveChoice != 2:
                    self.pokeMoveChoice = 2
                    self.useFlame()
                else:
                    self.pokeMoveChoice = None
            elif number == 3:
                if self.pokeMoveChoice != 3:
                    self.pokeMoveChoice = 3
                    self.useStringShot()
                else:
                    self.pokeMoveChoice = None
            if self.pokeMoveChoice == None: # no choice
                if self.myPokeName != None: # there is a name on board
                    self.myPokeName.destroy() # kill it
                else: # no name
                    pass
            else: # there is a choice
                if self.myPokeName != None:
                    self.myPokeName.destroy()
                self.myPokeName = Two_D.writePokeName(self.pokeMoveChoice)
  
    def loadRareCandy(self):
        # load rare candy (a box)
        # needs to be improved
        self.candy = Model_Load.loadRareCandy()
        self.candy.reparentTo(render)
        self.candy.setScale(0.1)
        self.candy.hide()
        
    def eatRareCandy(self, task):
        # check who eats candy
        if self.candyOnBoard: # candy on board
            if checkEat(self.ballRoot.getX(), self.ballRoot.getY(),
                        self.candy.getX(), self.candy.getY()): # ball eats
                self.candy.hide() # eaten
                self.candyOnBoard = False
                self.playerCandyCount += 1
                groupShow(self.myPokesBright)

            elif checkEat(self.pikachu.getX(), self.pikachu.getY(),
                          self.candy.getX(), self.candy.getY()):
                self.candy.hide()
                self.candyOnBoard = False
                self.pokeCandyCount += 1
        return Task.cont

    def setFocus(self, changing):
        # set focus of the camera while panning
        self.changingFocus = changing
        if changing == True: # Just Pressed
            self.referenceX, self.referenceY = self.mouseX, self.mouseY
        else: # cursor moves up
            self.referenceX, self.referenceY = None, None

    def resetView(self):
        # reset the view to default
        self.CAM_R, self.CAM_RAD = 12, 0
        self.cameraSpinCount, self.cameraZoomCount = 0, 0
        # _FOCUS = [0,0,0] does not work WHY???
        _FOCUS[0], _FOCUS[1], _FOCUS[2] = 0,0,0
        self.changingFocus = False
        self.referenceX, self.referenceY = None, None
        camera.setPos(_FOCUS[0], _FOCUS[1]-self.CAM_R, 25)
        camera.setHpr(0, -65, 0)
        
    def changeFocus(self, task):
        # change focus with displacement of mouse cursor
        if (self.changingFocus == True and self.mouseX != None and
            self.mouseY != None ):
            dX, dY = ((self.mouseX - self.referenceX)*0.1,
                      (self.mouseY - self.referenceY)*0.1)
            _FOCUS[0] += dX
            _FOCUS[1] += dY
            camera.setPos(_FOCUS[0] + self.CAM_R*cos(-pi/2+self.CAM_RAD),
                          _FOCUS[1] + self.CAM_R*sin(-pi/2+self.CAM_RAD),
                          (25.0/12)*self.CAM_R)
        return Task.cont

    def initialize(self):
        #bgmusic = load_bgmusic("palette.mp3")
        #bgmusic.play()

        self.background = Two_D.loadBackground()
        base.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.candyOnBoard = False
        self.playerCandyCount, self.pokeCandyCount = 0, 0
        ######################Rare Candy###############################
        pokes=['caterpie', 'charmander', 'geodude']
        self.myPokesDark = Two_D.loadMyPokemon_Dark(pokes) # my pokemons
        self.myPokesBright = Two_D.loadMyPokemon_Bright()
        groupHide(self.myPokesBright)
        self.loadRareCandy() # load rare candy
        ######################Camera Initialization####################
        self.CAM_R, self.CAM_RAD = 12, 0
        camera.setPos(_FOCUS[0],_FOCUS[1]-12,_FOCUS[2]+25)
        camera.setHpr(0, -65, 0)
        self.cameraSpinCount, self.cameraZoomCount = 0, 0
        self.changingFocus = False
        self.spin = 0
        #######################ICONS###################################
        self.myIcon = Two_D.loadMyIcon()
        self.pokeIcon = Two_D.loadPokeIcon()
        self.playerCandyStatus = candyStatus(0, self.playerCandyCount)
        self.pokeCandyStatus = candyStatus(1, self.pokeCandyCount)
        self.rareCandyImage = Two_D.loadRareCandyImage()
        self.pokeRareCandyImage = Two_D.loadRareCandyImage(pos=(-.3,0,-.75))
        #######################FLAMES##################################
        base.enableParticles()
        self.fireCounter = 0
        self.onFire = False
        #######################STRINGSHOT#############################
        self.stringCounter = 0
        #######################"GLOBALS"#################################
        self.speedCounter = 0
        self.direction = 's'
        self.myDirection = ['zx', 'zy']
        self.rockCounter  = 0
        self.rockX, self.rockY = None, None
        self.rockOnMaze = False
        self.pokeMoveChoice = None
        self.myPokeName = None
        self.arrowKeyPressed = False
        self.pokemonDirection = 'd'
        self.mouseX, self.mouseY = None, None
        # direction the ball is going
        self.jerkDirection = None
        base.disableMouse()
        self.jerk = (0,0,0)
        self.MAZE = Model_Load.loadLabyrinth()
        Control.keyControl(self)
        self.loadPokemonLevel1()
        self.light()
        self.loadBall()
        self.pokeStatus = 0 # 0 is normal, 1 is burned, 2 is slow-speed
        ########################################ROCK###################
        self.rock = Model_Load.loadRock()
        self.rock.reparentTo(render)
        self.rock.hide() # Do not show, but load beforehand for performance
        
    def loadPokemonLevel1(self):
        self.pikachu = load_model("pikachu.egg")
        self.pikachu.reparentTo(render)
        self.pikachu.setScale(0.3)
        endPos = self.MAZE.find("**/end").getPos()
        self.pikachu.setPos(endPos)
        self.pichu = load_model("pichu.egg")
        self.pichu.reparentTo(render)
        self.pichu.setScale(0.3)
        self.pichu.setPos(0,1,1)
        self.pichu.setHpr(0,70,0)
        
    def light(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    def loadBall(self):
        self.ballRoot = render.attachNewNode("ballRoot")
        self.ball = load_model("ball")
        self.ball.reparentTo(self.ballRoot)
        self.ball_tex = load_tex("pokeball.png")
        self.ball.setTexture(self.ball_tex,1)
        self.ball.setScale(0.8)
        # Find the collision sphere for the ball in egg.
        self.ballSphere = self.ball.find("**/ball")
        self.ballSphere.node().setFromCollideMask(BitMask32.bit(0))
        self.ballSphere.node().setIntoCollideMask(BitMask32.allOff())
        #self.ballSphere.show()
        # Now we create a ray to cast down at the ball.
        self.ballGroundRay = CollisionRay()
        self.ballGroundRay.setOrigin(0,0,10)
        self.ballGroundRay.setDirection(0,0,-1)

        # Collision solids go in CollisionNode
        self.ballGroundCol =  CollisionNode('groundRay')
        self.ballGroundCol.addSolid(self.ballGroundRay)
        self.ballGroundCol.setFromCollideMask(BitMask32.bit(1))
        self.ballGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ballGroundColNp = self.ballRoot.attachNewNode(self.ballGroundCol)
        
        # light
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.55, .55, .55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(0,0,-1))
        directionalLight.setColor(Vec4(0.375,0.375,0.375,1))
        directionalLight.setSpecularColor(Vec4(1,1,1,1))
        self.ballRoot.setLight(render.attachNewNode(ambientLight))
        self.ballRoot.setLight(render.attachNewNode(directionalLight))
        # material to the ball
        m = Material()
        m.setSpecular(Vec4(1,1,1,1))
        m.setShininess(96)
        self.ball.setMaterial(m,1)

    def __init__(self):
        self.initialize()
        self.WALLS = self.MAZE.find("**/Wall.004")
        self.WALLS.node().setIntoCollideMask(BitMask32.bit(0))
        # collision with the ground. different bit mask
        #self.mazeGround = self.maze.find("**/ground_collide")
        #self.mazeGround.node().setIntoCollideMask(BitMask32.bit(1))
        self.MAZEGROUND = self.MAZE.find("**/Cube.004")
        self.MAZEGROUND.node().setIntoCollideMask(BitMask32.bit(1))
        # add collision to the rock
        cs = CollisionSphere(0, 0, 0, 0.5)
        self.cnodePath = self.rock.attachNewNode(CollisionNode('cnode'))
        self.cnodePath.node().addSolid(cs)
        self.cnodePath.show()
        self.cnodePath.node().setIntoCollideMask(BitMask32.bit(0))
        # load the ball and attach it to the scene.
        # it is on a dummy node so that we can rotate the ball
        # without rotating the ray that will be attached to it

        # CollisionTraversers calculate collisions
        self.cTrav = CollisionTraverser()
        #self.cTrav.showCollisions(render)
        #self.cTrav.showCollisions(render)
        # A list collision handler queue
        self.cHandler = CollisionHandlerQueue()
        # add collision nodes to the traverse.
        # maximum nodes per traverser: 32
        self.cTrav.addCollider(self.ballSphere,self.cHandler)
        self.cTrav.addCollider(self.ballGroundColNp,self.cHandler)
        self.cTrav.addCollider(self.cnodePath, self.cHandler)
        # collision traversers have a built-in tool to visualize collisons
        #self.cTrav.showCollisions(render)
        self.start()

    def pokemonTurn(self, pokemon, direction):
        if direction  == 'l' and self.pokemonDirection != 'l':
            self.pokemonDirection = 'l'
            pokemon.setH(-90)
        if direction  == 'r' and self.pokemonDirection != 'r':
            self.pokemonDirection = 'r'
            pokemon.setH(90)
        if direction  == 'd' and self.pokemonDirection != 'd':
            self.pokemonDirection = 'd'
            pokemon.setH(0)
        if direction  == 'u' and self.pokemonDirection != 'u':
            self.pokemonDirection = 'u'
            pokemon.setH(180)
                        
    def pokemonMove(self, pokemon, direction):
        self.pokemonTurn(pokemon, direction)
        if self.pokeStatus == 0: speed = _SPEED
        elif self.pokeStatus == 1: speed = 0
        else: # self.pokeStatus == 2
            speed = _SPEED/2.0
        if direction == 'l':
            newX = pokemon.getX() - speed
            pokemon.setX(newX)
        elif direction == 'r':
            newX = pokemon.getX() + speed
            pokemon.setX(newX)
        elif direction == 'u':
            newY = pokemon.getY() + speed
            pokemon.setY(newY)
        elif direction == 'd':
            newY = pokemon.getY() - speed
            pokemon.setY(newY)
        elif direction == "s": # stop
            pass
        
    def whereToGo(self, task):
        # this returns the direction pokemon should go
        # tell MAZE pokemon and ball's board position
        #print self.myDirection
        self.pokemonMove(self.pikachu, self.direction)
        MAZE.setPokeCoord(self.pikachu.getX(), self.pikachu.getY(),
                          self.pokemonDirection)
        MAZE.setBallCoord(self.ballRoot.getX(), self.ballRoot.getY())
        MAZE.sendInformation(self.myDirection)
        # find out which direction to go
        self.direction = MAZE.getDecision()
        self.pokemonMove(self.pikachu,self.direction)
        return Task.cont

    def getInformation(self, task):
        # get information on the board
        self.speedCounter += 1 # sample every other call to avoid 
        if self.speedCounter % 2 == 0:
            dX = self.ballRoot.getX() - self.oldPos[0]
            dY = self.ballRoot.getY() - self.oldPos[1]
            if dX < 0 :
                # print "going left"
                self.myDirection[0] = 'l'
            elif abs(dX) < _EPSILON:
                # print "not moving horiz"
                self.myDirection[0] = 'zx'
            else:
                # print "going right"
                self.myDirection[0] = 'r'

            if dY < 0 :
                # print "going down"
                self.myDirection[1] = 'd'
            elif abs(dY) < _EPSILON:
                # print "not moving verti"
                self.myDirection[1] = 'zy'
            else:
                # print "going up"
                self.myDirection[1] = 'u'
            self.oldPos = self.ballRoot.getPos()
        return Task.cont
    
    def start(self):
        # maze model has a locator in it
        # self.ballRoot.show()
        self.startPos = self.MAZE.find("**/start").getPos()
        self.oldPos = self.MAZE.find("**/start").getPos()
        self.ballRoot.setPos(self.startPos) # set the ball in the pos
        self.ballV = Vec3(0,0,0) # initial velocity
        self.accelV = Vec3(0,0,0) # initial acceleration

        # for a traverser to work, need to call traverser.traverse()
        # base has a task that does this once a frame
        base.cTrav = self.cTrav

        # create the movement task, make sure its not already running
        taskMgr.remove("rollTask")
        taskMgr.add(self.placeRock, "placeRock")
        taskMgr.add(self.timer, "timer")
        taskMgr.add(self.getInformation, "getInformation")
        taskMgr.add(self.eatRareCandy, "eatRareCandy")
        taskMgr.add(self.placeRareCandy, "placeRareCandy")
        taskMgr.add(self.checkMouse, "checkMouse")
        taskMgr.add(self.spinCamera, "spinCamera")
        taskMgr.add(self.changeFocus, "changeFocus")
        taskMgr.add(self.whereToGo, "whereToGo")
        # taskMgr.add(lambda task: self.moveBall(task, self.jerkDirection),
                    # "moveBall")
        taskMgr.add(self.moveBall, "moveBall")
        self.mainLoop = taskMgr.add(self.rollTask, "rollTask")
        self.mainLoop.last = 0

    def moveBallWrapper(self, direction):
        # wrapper for moving the ball
        # needs to be improved
        if direction == False:
            self.arrowKeyPressed = False
        else:
            self.arrowKeyPressed = True
            self.jerkDirection = direction
    
    def moveBall(self, task):
        # move the ball
        # a key press changes the jerk
        direction = self.jerkDirection
        if self.arrowKeyPressed == True:
            if direction == "u":
                self.jerk = Vec3(0,_JERK,0)
            elif direction == "d":
                self.jerk = Vec3(0,-_JERK,0)
            elif direction == "l":
                self.jerk = Vec3(-_JERK,0,0)
            elif direction == "r":
                self.jerk = Vec3(_JERK,0,0)
        return Task.cont        

    # collision between ray and ground
    # info about the interaction is passed in colEntry
    
    def groundCollideHandler(self,colEntry):
        # set the ball to the appropriate Z for it to be on the ground
        newZ = colEntry.getSurfacePoint(render).getZ()
        self.ballRoot.setZ(newZ+.4)

        # up vector X normal vector
        norm = colEntry.getSurfaceNormal(render)
        accelSide = norm.cross(UP)
        self.accelV = norm.cross(accelSide)

    # collision between the ball and a wall
    def wallCollideHandler(self,colEntry):
        # some vectors needed to do the calculation
        norm = colEntry.getSurfaceNormal(render) * -1
        norm.normalize()
        curSpeed = self.ballV.length()
        inVec = self.ballV/curSpeed
        velAngle = norm.dot(inVec) # angle of incidance
        hitDir = colEntry.getSurfacePoint(render) - self.ballRoot.getPos()
        hitDir.normalize()
        hitAngle = norm.dot(hitDir)
    # deal with collision cases
        if velAngle > 0 and hitAngle >.995:
            # standard reflection equation
            reflectVec = (norm * norm.dot(inVec*-1)*2) + inVec
            # makes velocity half of hitting dead-on
            self.ballV = reflectVec * (curSpeed * (((1-velAngle)*.5)+.5))
            # a collision means the ball is already a little bit buried in
            # move it so exactly touching the wall
            disp = (colEntry.getSurfacePoint(render) -
                    colEntry.getInteriorPoint(render))
            newPos = self.ballRoot.getPos() + disp
            self.ballRoot.setPos(newPos)
            
    def rollTask(self,task):
        # standard technique for finding the amount of time
        # since the last frame
        dt = task.time - task.last
        task.last = task.time
        # If dt is large, then there is a HICCUP
        # ignore the frame
        if dt > .2: return Task.cont
        # dispatch which function to handle the collision based on name
        for i in range(self.cHandler.getNumEntries()):
            entry = self.cHandler.getEntry(i)
            name = entry.getIntoNode().getName()
       
            if name == "Wall.004":
                self.wallCollideHandler(entry)
            elif name=="Cube.004":
                self.groundCollideHandler(entry)
            else: 
                if self.rockOnMaze == True:
                    self.wallCollideHandler(entry)
        self.accelV += self.jerk
        # move the ball, update the velocity based on accel
        self.ballV += self.accelV * dt * ACCELERATION
        # clamp the velocity to the max speed
        if self.ballV.lengthSquared() > MAX_SPEED_SQ:
            self.ballV.normalize()
            self.ballV *= MAX_SPEED
        # update the position
        self.ballRoot.setPos(self.ballRoot.getPos() + (self.ballV*dt))

        # uses quaternion to rotate the ball
        prevRot = LRotationf(self.ball.getQuat())
        axis = UP.cross(self.ballV)
        newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
        self.ball.setQuat(prevRot * newRot)
        return Task.cont # continue the task

w = Labryn()
run()
