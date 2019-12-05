import naoqi
import time
import almath, math
import argparse
from naoqi import ALProxy
from math import pi, degrees, radians
from sys import argv
import sys
from pick_up_position import bend_down

class RightHandControl:
	
	#Initialize the angle variable for armjoints
	def __init__(self, IP="127.0.0.1", port=9559):
		motion = ALProxy("ALMotion", IP, port)
		posture= ALProxy("ALRobotPosture", IP, port)
		self.nameList  = ["RHand", "RWristYaw", "RElbowRoll", "RElbowYaw",\
					"RShoulderRoll","RShoulderPitch"]
	
		self.RHandAngle = degrees(motion.getAngles(self.nameList[0], True)[0] )
		self.RWristYawAngle = degrees(motion.getAngles(self.nameList[1], True)[0] )
		self.RElbowRollAngle = degrees(motion.getAngles(self.nameList[2], True)[0] )
		self.RElbowYawAngle = degrees(motion.getAngles(self.nameList[3], True)[0] )
		self.RShoulderRollAngle = degrees(motion.getAngles(self.nameList[4], True)[0] )
		self.RShoulderPitchAngle = degrees(motion.getAngles(self.nameList[5], True)[0] )
		
		self.RHandTime = 0
		self.RWristYawTime = 1
		self.RElbowRollTime = 2
		self.RElbowYawTime = 3
		self.RShoulderRollTime = 3
		self.RShoulderPitchTime = 5
		
			
		self.angleList = [self.RHandAngle, self.RWristYawAngle,self.RElbowRollAngle,\
			self.RElbowYawAngle,self.RShoulderRollAngle, self.RShoulderPitchAngle]
		self.timeList  = [self.RHandTime, self.RWristYawTime, self.RElbowRollTime,\
			self.RElbowYawTime, self.RShoulderRollTime, self.RShoulderPitchTime]
		

	def setAngleList(self):
		self.angleList = [self.RHandAngle, self.RWristYawAngle,self.RElbowRollAngle,\
			self.RElbowYawAngle,self.RShoulderRollAngle, self.RShoulderPitchAngle]
		
		return self.angleList

	def moveRHand(self, setAngleList, timeList):
		# Convert Angle from degrees to radians
		angles = []
		for i in setAngleList:
			angles.append(math.radians(i))
		
		# Move the Right hand
		motion.angleInterpolation(self.nameList, angles, timeList, True)
		time.sleep(1.0)

	def printRHandAngles(self):
		# Print the current right arms joint angles
		for name in self.nameList:
			print(name + ": " + str(degrees(motion.getAngles(name, True)[0])))	
	
	def printAngleList(self):
		print("Angles :     " , self.angleList)

	def printNameAndAngle(self):
		for i in range(len(self.nameList)):
			print(self.nameList[i] + ": " + str(self.angleList[i]))	
		
	 
					
if __name__ == '__main__':
	IP = "127.0.0.1"
	port = 9559

	print("------------START--------------\n\n")
	motion = ALProxy("ALMotion", IP, port)
	posture = ALProxy("ALRobotPosture", IP, port)
	motion.wakeUp() 			# Wakes up the robot
	#posture.goToPosture("Stand", .7)	# Make it stand up
	bend_down(motion) 			# go to pick up position
	time.sleep(3.0)
	print("------------CALLING--------------\n\n")
	
	print("Current position-----------")
	go = RightHandControl(IP, port)
	go.printAngleList()    			#print out all Angle
	
	print("After changing Angle--------")
	go.RElbowRoll = 88.5
	go.RElbowYaw = 48.0960816068
	timeList = [1,2,3,4,5,6]
	setAngleList = go.setAngleList()
	print("setAngleList: ------" , setAngleList)

	go.moveRHand(setAngleList, timeList)
	go.printAngleList()    #print out all Angle
	








	'''
	# DO NOT DELETE ( hand control)
	setAngleList = [1, 104.5, 88.5, 119.5, 18, 119]	   #in degrees
	'''
	
	
	print("------------DONE--------------/n")







