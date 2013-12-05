from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
ShowBase()
loader.loadModel("bulbasaur.egg").reparentTo(render)
loader.loadModel("pikachu.egg").reparentTo(render)
run()
