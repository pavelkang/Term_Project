# This is a ball-in-maze program

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
# vector
from panda3d.core import Vec3,Vec4,BitMask32
# GUI
from direct.gui.OnscreenText import OnscreenText
# Direct Object
from direct.showbase.DirectObject import DirectObject
# Interval
from direct.interval.MetaInterval import Sequence,Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func,Wait
# Task
from direct.task.Task import Task
import sys

#self written module
from load import *

ACCELERATION = 70
MAX_SPEED = 5
MAX_SPEED_SQ = MAX_SPEED ** 2

# upward vector 
UP = Vec3(0,0,1)

class Labryn(DirectObject):
    def __init__(self):
        self.title = OnscreenText(text = "KAI KANG: BALL IN MAZE",
                                  style = 1, fg=(1,1,1,1),
                                  pos=(0.7,-0.95),scale= .07)
        self.instructions = OnscreenText(text="Mouse pointer tilts the board",
                                         pos = (-1.3, .95), fg=(1,1,1,1),
                                         align = TextNode.ALeft, scale=.05)
        self.accept("escape", sys.exit) # ESC to quit
        self.accept("arrow_up",self.moveBall,["up"])
        self.accept("arrow_down",self.moveBall,["down"])
        self.accept("arrow_left",self.moveBall,["left"])
        self.accept("arrow_right",self.moveBall,["right"])
        
        
        base.disableMouse() # Disable mouse-based camera control

        # place the camera
        camera.setPosHpr(0,-12,25,0,-65,0)

        self.jerk = (0,0,0)

        # load the maze model and reparent it to the topmost node
        #self.MAZE = load_model("groupegg.egg")
        self.MAZE = load_model("ground3.egg")
        self.MAZE.flattenLight()
        self.MAZE.reparentTo(render)
        self.MAZE.setPos(0,0,0)
        self.MAZE.setHpr(90,0,0)
        #self.MAZE.place()
        #self.pikachu = load_model("Groudon.egg")
        #self.pikachu = load_model("P2_Pikachu.egg")
        #self.pikachu.reparentTo(render)
        #self.pikachu.setScale(0.1)
    
        #self.pikachu.setTexture(self.pika_tex,1)
        #self.pikachu.setPos(endPos)
        # check the egg file <Collide>
        #self.walls = self.maze.find("**/wall_collide")
        self.WALLS = self.MAZE.find("**/Wall.003")

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

        # collision with wall
        #self.walls.node().setIntoCollideMask(BitMask32.bit(0))
        self.WALLS.node().setIntoCollideMask(BitMask32.bit(0))
        #self.WALLS.show()
        # holes. the triggers that cause you to lose the game
        self.loseTriggers = []

        # collision with the ground. different bit mask
        #self.mazeGround = self.maze.find("**/ground_collide")
        #self.mazeGround.node().setIntoCollideMask(BitMask32.bit(1))
        self.MAZEGROUND = self.MAZE.find("**/Cube.003")
        self.MAZEGROUND.node().setIntoCollideMask(BitMask32.bit(1))
                                         
        # load the ball and attach it to the scene.
        # it is on a dummy node so that we can rotate the ball
        # without rotating the ray that will be attached to it
        self.ballRoot = render.attachNewNode("ballRoot")
        self.ball = load_model("ball")
        self.ball.reparentTo(self.ballRoot)
        self.ball_tex = load_tex("pokeball.png")
        self.ball.setTexture(self.ball_tex,1)
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

        # CollisionTraversers calculate collisions
        self.cTrav = CollisionTraverser()
        #self.cTrav.showCollisions(render)
        # self.cTrav.showCollisions(render)
        # A list collision handler queue
        self.cHandler = CollisionHandlerQueue()

        # add collision nodes to the traverse.
        # maximum nodes per traverser: 32
        self.cTrav.addCollider(self.ballSphere,self.cHandler)
        self.cTrav.addCollider(self.ballGroundColNp,self.cHandler)
        
        # collision traversers have a built-in tool to visualize collisons
        # self.cTrav.showCollisions(render)

        # Lighting for the ball
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.55, .55, .55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(0,0,-1))
        directionalLight.setColor(Vec4(0.375,0.375,0.375,1))
        directionalLight.setSpecularColor(Vec4(1,1,1,1))
        self.ballRoot.setLight(render.attachNewNode(ambientLight))
        self.ballRoot.setLight(render.attachNewNode(directionalLight))
        #self.ballGroundColNp.show()
        # adding a specular highlight to the ball to make it shiny
        m = Material()
        m.setSpecular(Vec4(1,1,1,1))
        m.setShininess(96)
        self.ball.setMaterial(m,1)

        self.start()

    def start(self):
        # maze model has a locator in it
        self.ballRoot.show()
        startPos = self.MAZE.find("**/start").getPos()
        self.ballRoot.setPos(startPos) # set the ball in the pos
        self.ballV = Vec3(0,0,0) # initial velocity
        self.accelV = Vec3(0,0,0) # initial acceleration

        # for a traverser to work, need to call traverser.traverse()
        # base has a task that does this once a frame
        base.cTrav = self.cTrav

        # create the movement task, make sure its not already running
        taskMgr.remove("rollTask")
        self.mainLoop = taskMgr.add(self.rollTask, "rollTask")
        self.mainLoop.last = 0

    def moveBall(self,direction):
        jerk = 0.05
        if direction == "up":
            self.jerk = Vec3(0,jerk,0)
        elif direction == "down":
            self.jerk = Vec3(0,-jerk,0)
        elif direction == "left":
            self.jerk = Vec3(-jerk,0,0)
        elif direction == "right":
            self.jerk = Vec3(jerk,0,0)
        
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
            """
            if   name == "wall_collide":   self.wallCollideHandler(entry)
            elif name == "ground_collide": self.groundCollideHandler(entry)
            elif name == "loseTrigger":    self.lostGame(entry)
            elif name == "Wall.003":
                print entry.getSurfaceNormal(render)
                self.wallCollideHandler(entry)
            elif name=="Cube.003":
                self.wallCollideHandler(entry)
            #elif name == "Wall": self.wallCollideHandler(entry)
            """
            if name == "Wall.003":
                self.wallCollideHandler(entry)
            elif name=="Cube.003":
                self.groundCollideHandler(entry)

        # read the mouse position and tilt the maze accordingly
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

    def lostGame(self, entry):
        # the center of the ball should move to the collision point
        # to be in the hole
        toPos = entry.getInteriorPoint(render)
        taskMgr.remove('rollTask') # stop the maze task
        Sequence(
            Parallel(
                LerpFunc(self.ballRoot.setX, fromData = self.ballRoot.getX(),
                         toData = toPos.getX(), duration = .1),
                LerpFunc(self.ballRoot.setY, fromData = self.ballRoot.getY(),
                         toData = toPos.getY(), duration = .1),
                LerpFunc(self.ballRoot.setZ, fromData = self.ballRoot.getZ(),
                         toData = self.ballRoot.getZ() - .9, duration = .2)),
            Wait(1),
            Func(self.start)).start()
w = Labryn()
run()
