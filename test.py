from direct.fsm.FSM import FSM
 
class AvatarFSM(FSM):
    def __init__(self):#optional because FSM already defines __init__
        #if you do write your own, you *must* call the base __init__ :
        FSM.__init__(self, 'AvatarFSM')
        ##do your init code here
 
    def enterWalk(self):
        avatar.loop('walk')
        footstepsSound.play()
        enableDoorCollisions()
 
    def exitWalk(self):
        avatar.stop()
        footstepsSound.stop()
        disableDoorCollisions()
 
    def enterSwim(self):
        avatar.loop('swim')
        underwaterSound.play()
        render.setFog(underwaterFog)
        startAirTimer()
 
    def exitSwim(self):
        avatar.stop()
        underwaterSound.stop()
        render.clearFog()
        stopAirTimer()
 
myfsm = AvatarFSM()
