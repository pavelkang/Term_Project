# This module helps load source

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import TransparencyAttrib
import direct.directbase.DirectStart # loader

# for CardMaker
from panda3d.core import *
import os

def load_model(name):
    filePath = os.path.join('..','google_drive','ball','data','models',name)
    try:
        file = loader.loadModel(filePath)
    except:
        raise SystemExit, "Failed to import model %s" %name
    return file

def load_tmodel(name):
    filePath = os.path.join('..','Downloads','bulbasaur',name)
    try:
        file = loader.loadModel(filePath)
    except:
        raise SystemExit, "Failed to import model %s" %name
    return file


def load_tex(name):
    filePath = os.path.join('..','google_drive','ball','data','img',name)
    try:
        file = loader.loadTexture(filePath)
    except:
        raise SystemExit, "Failed to import texture %s" %name
    return file

def load_sound(name):
    filePath = os.path.join('..','google_drive','ball','data','sound',name)
    try:
        file = loader.loadSfx(filePath)
    except:
        raise SystemExit, "Failed to import texture %s" %name
    return file

def load_bgmusic(name):
    filePath = os.path.join('..','google_drive','ball','data','bgmusic',name)
    try:
        file = loader.loadSfx(filePath)
    except:
        raise SystemExit, "Failed to import texture %s" %name
    return file


