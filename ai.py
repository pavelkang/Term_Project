from Tkinter import *

def run():
    root = Tk()
    canvas = Canvas(root, width = 300, height = 300)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    init(canvas)
    root.mainloop()

def init(canvas):
    d = canvas.data
    d.board = [ [ 0, 0, 0, 0],
                [ 0, 0, 0, 2],
                [ 0, 0, 0, 0],
                [ 0, 0, 1, 0]]
    d.mePos = (3,2) # 1
    d.enPos = (1,3) # 2
    
