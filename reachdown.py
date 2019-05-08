from naoqi import ALProxy
from math import pi, degrees, radians
from sys import argv
import time

ip_addr = argv[1]

port = int(argv[2])

hipPitchAngle       = radians(-84)
kneePitchAngle      = radians(45)
RShoulderPitchAngle = radians(20)
anklePitchAngle     = radians(3.6)
RElbowRollAngle     = radians(-2)
LShoulderRollAngle  = radians(40)

hipTime             = 2
kneeTime            = 2
shoulderPitchTime   = 2
ankleTime           = 5
elbowTime           = 4
shoulderRollTime    = 2

angleList =  [hipPitchAngle, hipPitchAngle, kneePitchAngle, kneePitchAngle,\
              RShoulderPitchAngle, anklePitchAngle, anklePitchAngle,\
              RElbowRollAngle, LShoulderRollAngle]

timeList  = [hipTime, hipTime, kneeTime, kneeTime, shoulderPitchTime,\
             ankleTime, ankleTime, elbowTime, shoulderRollTime]

nameList  = ['LHipPitch', 'RHipPitch', 'LKneePitch', 'RKneePitch', 'RShoulderPitch', 'RAnklePitch', 'LAnklePitch', 'RElbowRoll', 'LShoulderRoll']


if __name__ == '__main__':
    
    motion = ALProxy("ALMotion", ip_addr, port)
    posture= ALProxy("ALRobotPosture", ip_addr, port)
    motion.wakeUp() # Wakes up the robot
    posture.goToPosture("Stand", .7) # Commands the robot to stand up
    # Print the default joint angle values of the robot
    print "Hip Angle: " + str(deg(motion.getAngles("RHipPitch", True)[0]))
    print "Knee Angle: " + str(deg(motion.getAngles("LKneePitch", True)[0]))
    print "Shoulder Angle: " + str(deg(motion.getAngles("RShoulderPitch", True)[0]))
    print "Ankle Angle: " + str(deg(motion.getAngles("RAnklePitch", True)[0]))
    print "Elbow Angle: " + str(deg(motion.getAngles("RElbowRoll", True)[0]))
    time.sleep(3)
    motion.openHand("RHand")
    motion.angleInterpolation(nameList, angleList, timeList, True)
    print "Closing Hand!!"
    motion.closeHand("RHand")

