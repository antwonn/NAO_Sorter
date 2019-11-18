from naoqi import ALProxy
from math import pi, degrees, radians
from sys import argv
import time

'''
IP = argv[1]
port = int(argv[2])
'''

#Initialize the angle variable for armjoints
RHandAngle = 1
RWristYawAngle= 
RElbowRollAngle = 
RElbowYawAngle = 
RShoulderRollAngle =
RShoulderPitchAngle = 

#Right Arms joints
RHand = RHandAngle	    					#open(1) or close(0) only
RWristYaw = degrees(RWristYawAngle)    		#degree RWristYaw: -104.5 to 104.5
RElbowRoll = degrees(RElbowRollAngle)  		#degree RElbowRoll: 2 to 88.5
RElbowYaw = degree(RElbowYawAngle)     		#degree RElbowYaw: -119.5 to 119.5
RShoulderRoll = degree(RShoulderRollAngle)	#degree RShoulderRoll = -76 to 18
RShoulderPitch = degree(RShoulderPitchAngle)#degree RShoulderPitch = -119.5 to 119.5

nameList  = ['RHand', 'RWristYaw', 'RElbowRoll', \
			'RElbowYaw', 'RShoulderRoll','RShoulderPitch']		
angleList =  [RHandAngle, RWristYawAngle,RElbowRollAngle,\
			RElbowYawAngle,RShoulderRollAngle, RShoulderPitchAngle]

if __name__ == '__main__':
	try:
		IP = "127.0.0.1"
		port = 9559
		motion = ALProxy("ALMotion", IP, port)
		posture= ALProxy("ALRobotPosture", IP, port)
		# Print the current right arms joint angles
		for name in nameList:
			print (name + ": " + str(degree(motion.getAngles(name, True)[0]))
