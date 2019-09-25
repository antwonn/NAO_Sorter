import naoqi
from naoqi import ALProxy
#netstat to find port number in normal command line (not python)

externalIP = "127.0.0.1"
port = 54823
'''
#Real robot
externalIP = "192.168.0.102"
port = 9559
'''


motion = ALProxy("ALMotion", externalIP, port)
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
lHip = [-1.5, 0]
lKnee = [0.4, 0]
rShoulder = [0, 1.57]
lAnkle = [-0.05, 0]

lHipTime = 	[2, 15]
lKneeTime = [1, 15]
lAnkleTime = [1, 15]
rShoulderTime = [4, 10]


degree = [lHip, lHip, lKnee, lKnee, rShoulder, lAnkle, lAnkle]
times = [lHipTime, lHipTime, lKneeTime, lKneeTime, rShoulderTime, lAnkleTime, lAnkleTime]
isAbsolute = True

motion.angleInterpolation(name, degree, times, isAbsolute)
