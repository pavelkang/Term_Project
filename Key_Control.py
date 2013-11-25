import sys

def keyControl(self):
    # get user input
    self.accept("escape", sys.exit) # ESC to quit
    self.accept("w",self.moveBallWrapper,["u"])
    self.accept("s",self.moveBallWrapper,["d"])
    self.accept("a",self.moveBallWrapper,["l"])
    self.accept("d",self.moveBallWrapper,["r"])
    self.accept("w-up",self.moveBallWrapper,[False])
    self.accept("s-up",self.moveBallWrapper,[False])
    self.accept("a-up",self.moveBallWrapper,[False])
    self.accept("d-up",self.moveBallWrapper,[False])
    self.accept("mouse1-up", self.dropRock)
    self.accept("e", self.setCamera, [1])
    self.accept("e-up", self.setCamera, [0])
    self.accept("q", self.setCamera, [2])
    self.accept("q-up", self.setCamera, [0])
    self.accept("z", self.setCamera, [3])
    self.accept("z-up", self.setCamera, [0])
    self.accept("c", self.setCamera, [4])
    self.accept("c-up", self.setCamera, [0])
    self.accept("shift", self.setFocus, [True])
    self.accept("shift-up", self.setFocus, [False])
    self.accept("r", self.resetView)
    self.accept("1", self.usePokeMove, [1])
    self.accept("2", self.usePokeMove, [2])     
    self.accept("3", self.usePokeMove, [3])
