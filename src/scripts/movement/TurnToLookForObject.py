import math
#turn 90 degree box
#turn 90 degree box connect with redballDectected box 
#so that if nao turn around to look for red ball

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        x = self.getParameter("x")
        y = self.getParameter("y")
        amountOfStepToTurn = math.atan2(y,x)
        amountOfStepToWalk = math.sqrt(x*x+y*y)

        motionProxy = ALProxy("ALMotion")
        motionProxy.walkTo(0,0,amountOfStepToTurn)
        #motionProxy.walkTo(amountOfStepToWalk,0,0)

        #self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        #self.onStopped() #activate the output of the box
        pass
