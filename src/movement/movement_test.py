'''
CECS:491A
NAO Sorter Team
This program is used to test the NAO Robot's movements throughout the room.
To familiarize yourself with how the NAO Robot moves, adjust the values of X,Y, and Theta.
The NAO Robot's coordinates are relative to itself and they don't keep track of a world frame.
'''
import math
import almath
import argparse
from naoqi import ALProxy

def main(robotIP, PORT=9559):
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    #Wake up robot
    motionProxy.wakeUp()

    #Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
    
    #Simplified Robot Position
    useSensorValues = False
    result = motionProxy.getRobotPosition(useSensorValues)
    print "Robot Position", result

    #Robot's Displacement
    useSensorValues = False
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))
    print "Init Position: ", initRobotPosition

    x=0.5
    y=0.5
    theta = math.pi/2
    motionProxy.moveTo(x,y,theta)

    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))

    #Displacement after moving.
    robotMove = almath.pose2DInverse(initRobotPosition) * endRobotPosition
    print "Robot Move: ", robotMove
    
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot Ip Address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)

