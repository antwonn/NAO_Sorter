'''
CECS:491A
NAO Sorter Team
This program is used to test the face tracking feature of the NAO Robot.
'''
#TODO See how to implement own detection algorithms into the NAO's built in tracking.
import time
from naoqi import ALProxy

motion = ALProxy('ALMotion', '192.168.0.105', 9559)
posture = ALProxy('ALRobotPosture', '192.168.0.105', 9559)
tracker = ALProxy('ALTracker', '192.168.0.105', 9559)

motion.wakeUp()

speed = 0.8
posture.goToPosture('StandInit', speed)

target = 'Face'
size = .2
tracker.registerTarget(target, size)

mode = 'Move'
tracker.setMode(mode)

tracker.track(target)

print 'ALTracker started.'
print 'Use Ctrl-C to stop script.'

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print
    print 'Stopping.'

tracker.stopTracker()
tracker.unregisterAllTargets()
posture.goToPosture('Sit', speed)
motion.rest()

print 'ALTracker Stopped'
