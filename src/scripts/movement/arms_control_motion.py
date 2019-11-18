import naoqi
import time
import almath
from naoqi import ALProxy
from math import pi, degrees, radians
from sys import argv
import sys

class RightHandControl:
	#Initialize the angle variable for armjoints
	def _init_(self, angleList, IP="127.0.0.1", port=9559):
		motion = ALProxy("ALMotion", IP, port)
		posture= ALProxy("ALRobotPosture", IP, port)
		self.RHandAngle = degree(motion.getAngles(angleList[0], True)[0])
		self.RWristYawAngle = degree(motion.getAngles(angleList[1], True)[0])
		self.RElbowRollAngle = degree(motion.getAngles(angleList[2], True)[0])
		self.RElbowYawAngle = degree(motion.getAngles(angleList[3], True)[0])
		self.RShoulderRollAngle = degree(motion.getAngles(angleList[4], True)[0])
		self.RShoulderPitchAngle = degree(motion.getAngles(angleList[5], True)[0])
		
		self.RHandTime = 0
		self.RWristYawTime = 0
		self.RElbowRollTime = 0
		self.RElbowYawTime = 0
		self.RShoulderRollTime = 0
		self.RShoulderPitchTime = 0
		
		nameList  = ['RHand', 'RWristYaw', 'RElbowRoll', 'RElbowYaw',\
					'RShoulderRoll','RShoulderPitch']		
		angleList = [self.RHandAngle, self.RWristYawAngle,self.RElbowRollAngle,\
					self.RElbowYawAngle,self.RShoulderRollAngle, self.RShoulderPitchAngle]
		timeList  = [self.RHandTime, self.RWristYawTime, self.RElbowRollTime,\
					self.RElbowYawTime, self.RShoulderRollTime, delf.RShoulderPitchTime]
		
		
	def moveRHand(nameList, angleList, timeList):
		#Right Arms joints
		RHand = self.RHandAngle	    					#open(1) or close(0) only
		RWristYaw = degrees(self.RWristYawAngle)    		#degree RWristYaw: -104.5 to 104.5
		RElbowRoll = degrees(self.RElbowRollAngle)  		#degree RElbowRoll: 2 to 88.5
		RElbowYaw = degree(self.RElbowYawAngle)     		#degree RElbowYaw: -119.5 to 119.5
		RShoulderRoll = degree(self.RShoulderRollAngle)	#degree RShoulderRoll = -76 to 18
		RShoulderPitch = degree(self.RShoulderPitchAngle)#degree RShoulderPitch = -119.5 to 119.5

		motion.angleInterpolation(nameList, angleList, timeList, True)
	
	def printRHandAngles(nameList):
		# Print the current right arms joint angles
		for name in nameList:
			print(name + ": " + str(degree(motion.getAngles(name, True)[0])))		
					
if __name__ == '__main__':
	IP = "127.0.0.1"
	port = 9559
	print("------------START--------------")
	motion = ALProxy("ALMotion", IP, port)
	posture = ALProxy("ALRobotPosture", IP, port)
	print("------------CALLING--------------")
	nameList  = ['RHand', 'RWristYaw', 'RElbowRoll', 'RElbowYaw', 'RShoulderRoll','RShoulderPitch']		
	#angleList = [RHandAngle, RWristYawAngle,RElbowRollAngle,RElbowYawAngle,RShoulderRollAngle, RShoulderPitchAngle]
	timeList = [1,3,3,3,3,3]
	
	angleList = []
	for name in nameList:
		angleList.append(degree(motion.getAngles(name, True)[0]))
	print("angleList: ", angleList)
	
	go = RightHandControl(IP, port)
	go.moveRHand(nameList, angleList, timeList)
	print("-------------DONE-------------")
