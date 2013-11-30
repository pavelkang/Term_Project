from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        self.environ.setScale(.25,.25,.25)
        self.environ.setPos(-8,42,0)
        self.actor = Actor("anim2hooh.egg",
                           {"wing":"anim-Anim0.egg"})
        self.actor.reparentTo(render)
        self.actor.loop("wing")

app = MyApp()
app.run()
