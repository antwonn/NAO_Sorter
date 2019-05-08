import time


# Detectting a red bal then report by say "I found it" 

class MyClass(GeneratedClass):

def __init__(self):

GeneratedClass.__init__(self)

self.tracker = ALProxy( "ALTracker" )

self.memory = ALProxy("ALMemory")

self.posture = ALProxy("ALRobotPosture")

self.motion = ALProxy("ALMotion")

self.tts = ALProxy("ALTextToSpeech")

self.targetName = "RedBall"

self.fractionMaxSpeed = 0.8



def onLoad(self):

self.logger.debug("Loaded box %s", self.getName())



def onUnload(self):

self.logger.debug("onUnload %s", self.getName())

self.tracker.stopTracker()

self.tracker.unregisterAllTargets()



def onInput_onStart(self):

self.logger.debug("onInput_onStart %s", self.getName())

self.memory.subscribeToEvent("redBallDetected", self.getName(), "onBallDetected")

# First, wake up.

self.motion.wakeUp()

# Go to posture stand

self.posture.goToPosture("StandInit", self.fractionMaxSpeed)

# Add target to track.

self.tracker.registerTarget(self.targetName, 0.0381)

# set mode

self.tracker.setMode("Move")

# Then, start tracker.

self.tracker.track(self.targetName)

self.tts.say(self.tracker.getActiveTarget())



def onInput_onStop(self):

self.logger.debug("onInput_onStop %s", self.getName())

self.onStopped()

self.onUnload()

def onBallDetected(self, key, value, message):

self.tts.say("I found it")    
