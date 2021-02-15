from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from pandac.PandaModules import WindowProperties
pro = WindowProperties()
pro.setTitle('By Rizwan AR')

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.win.requestProperties(pro)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)

        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.pandaActor = Actor("models/panda-model", {"walk" : "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        self.accept('escape', self.quit)
        self.accept("arrow_up", self.Move)
        self.accept("arrow_up-repeat", self.Move)
        self.accept("arrow_up-up", self.stopMove)
        self.accept("arrow_right", self.Move2)
        self.accept("arrow_left", self.Move1)

        self.jump_speed = 0
        self.gravity_force = 9.8
        self.jump_status = False
        self.accept("space", self.set_jump)
        self.taskMgr.add(self.gravity, "gravity")

    def Move(self):
        self.pandaActor.setY(self.pandaActor, -30)
        self.pandaActor.setPlayRate(2, "walk")
        walk = self.pandaActor.getAnimControl("walk")
        if not walk.isPlaying():
            self.pandaActor.loop("walk")

    def stopMove(self):
        self.pandaActor.stop("walk")

    def Move2(self):
        self.pandaActor.setH(self.pandaActor, -45)

    def Move1(self):
        self.pandaActor.setH(self.pandaActor, 45)

    def set_jump(self):
        if self.jump_status == False:
            self.jump_speed = 4
            self.jump_status = True
            self.pandaActor.setY(self.pandaActor, -300)

    def gravity(self, task):
        self.pandaActor.setZ(self.pandaActor.getZ() + self.jump_speed * globalClock.getDt())
        if self.pandaActor.getZ() > 0:
            self.jump_speed = self.jump_speed - self.gravity_force * globalClock.getDt()
        if self.pandaActor.getZ() < 0:
            self.pandaActor.setZ(0)
            self.jump_speed = 0
            self.jump_status = False
        return Task.cont

    def spinCameraTask(self, task):
        angleDegrees = task.time * 8.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def quit(self):
        sys.exit()

app = MyApp()
app.run()
