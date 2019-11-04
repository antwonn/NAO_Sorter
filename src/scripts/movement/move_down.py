import naoqi
import sys
import time
import almath
from naoqi import ALProxy

#netstat to find port number in normal command line (not python)

def stiffness_on( proxy ):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main( IP ):
    try:
        motion = ALProxy("ALMotion", IP, port)
    except Exception, e:
        print "Error connecting to ALMotion"
        print "Error: ", e

    try:
        posture = ALProxy("ALRobotPosture", IP, port)
    except Exception, e:
        print "Error connecting to ALRobotPosture"
        print "Error: ", e

    stiffness_on( motion )
    motion.setIdlePostureEnabled( 'All', False)
    #motion.setStiffnesses('Arms', 1.0)
    posture.goToPosture("Crouch", .5)

    name = ["LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch",
                    "RShoulderPitch", "LAnklePitch", "RAnklePitch"]
    '''
#go down with balance, not too low
    lHip = [-0.3, 0]
    lKnee = [0.3, 0]
    rShoulder = [0, 1.57]
    lAnkle = [-0.05, 0]
    lHipTime = 	[1, 20]
    lKneeTime = [1, 20]
    lAnkleTime = [1, 20]
    rShoulderTime = [4, 10]
    '''

#go down with balance, low
    #lHip = [-1.5, 0]
    #lHipTime = 	[2, 15]
    #rHip = [-1.5, 0]
    #rHipTime = 	[2, 15]

    #lKnee = [0.4, 0]
    #lKneeTime = [1, 15]
    #rKnee = [0.4, 0]
    #rKneeTime = [1, 15]

    #lShoulder = [0, 1.57]
    #lShoulderTime = [4, 10]
    #rShoulder = [0, 1.57]
    #rShoulderTime = [4, 10]

    #lAnkle = [-0.05, 0]
    #lAnkleTime = [1, 15]
    #rAnkle = [-0.05, 0]
    #rAnkleTime = [1, 15]


    #degree = [lHip, rHip, lKnee, rKnee, rShoulder, lAnkle, rAnkle]
    #times = [lHipTime, rHipTime, lKneeTime, rKneeTime, rShoulderTime, lAnkleTime, rAnkleTime]
    #isAbsolute = True

    #motion.angleInterpolation(name, degree, times, isAbsolute)


    names      = "LShoulderPitch"
    #              2 angles
    angleLists = [30.0*almath.TO_RAD]
    #              2 times
    timeLists  = [1.0]
    isAbsolute = True
    #motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)



    #OPEN HIPS
    hips = ["LHipYawPitch", "RHipYawPitch"]

    angleLists = [-45.0*almath.TO_RAD, -45.0*almath.TO_RAD]
    #              2 times
    timeLists  = [1.0, 1.0]
    isAbsolute = True
    motion.angleInterpolation(hips, angleLists, timeLists, isAbsolute)


    #PREPARE FOR FALL
    arms = ["LShoulderPitch", "LElbowRoll", "LElbowYaw", "LWristYaw",
            "RShoulderPitch", "RElbowRoll", "RElbowYaw", "RWristYaw"]
    angleLists = [ 30.0 * almath.TO_RAD, -2.0 * almath.TO_RAD, 0, -104.5 * almath.TO_RAD, \
                   30.0 * almath.TO_RAD, -2.0 * almath.TO_RAD, 0, 104.5 * almath.TO_RAD ]
    timeLists  = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ] 
    isAbsolute = True
    motion.angleInterpolation(arms, angleLists, timeLists, isAbsolute)

    #TIP OVER
    tips       = ["LHipPitch", "RHipPitch", "LHipYawPitch", "RHipYawPitch"]
    angleLists = [ -60.0 * almath.TO_RAD, -60.0 * almath.TO_RAD, -55.0 * almath.TO_RAD, -55.0 *
    almath.TO_RAD ]
    timeLists  = [ 1.0, 1.0, 1.0, 1.0 ]
    isAbsolute = True
    motion.angleInterpolation(tips, angleLists, timeLists, isAbsolute)


    ankles     = [ "LKneePitch", "RKneePitch" ]
    angleLists = [ 140.0 * almath.TO_RAD, 140.0 * almath.TO_RAD  ]
    timeLists  = [ 1.0, 1.0 ]
    motion.angleInterpolation(ankles, angleLists, timeLists, isAbsolute)

    lHip = [-85.0 * almath.TO_RAD]
    lHipTime = 	[2]
    rHip = [-85.0 * almath.TO_RAD]
    rHipTime = 	[2]

    lKnee = [24 * almath.TO_RAD]
    lKneeTime = [1]
    rKnee = [24 * almath.TO_RAD]
    rKneeTime = [1]

    #lShoulder = [0, 1.57]
    #lShoulderTime = [4, 10]
    #rShoulder = [0, 1.57]
    #rShoulderTime = [4, 10]

    #lAnkle = [-0.05, 0]
    #lAnkleTime = [1, 15]
    #rAnkle = [-0.05, 0]
    #rAnkleTime = [1, 15]
    names = ["LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch" ]
                    #"RShoulderPitch", "LAnklePitch", "RAnklePitch"]

    degree = [lHip, rHip, lKnee, rKnee] #,lShoulder, rShoulder, lAnkle, rAnkle]
    times = [lHipTime, rHipTime, lKneeTime, rKneeTime]#, rShoulderTime, lAnkleTime, rAnkleTime]
    isAbsolute = True

    #motion.angleInterpolation(names, degree, times, isAbsolute)



if __name__ == "__main__":
    robotIp = "127.0.0.1"
    port = 9559

    if len(sys.argv) <= 1:
        print "Usage python motion_wbMultipleEffectors.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
