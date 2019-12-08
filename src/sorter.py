from naoqi import ALProxy
from Queue import Queue
from enum import Enum
from movement.movement import Movement
from movement.pick_up_position import bend_down
from vision.clientTracker import ClientTracker
import argparse
import numpy as np
import almath
import time
from vision import client as cl
from simple_pid import PID

GLOBAL_STATES = Enum('GlobalStates', 'INIT SEARCH TRACK PICKUP RETURN COMPLETED INCOMPLETE')
SEARCH_STATES = Enum('SearchStates', 'INIT MOVE SCAN')
TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST CENTER MOVE_TOWARD SWITCH_CAMERA')
PICKUP_STATES = Enum('PickUpStates', 'INIT ADJUST BEND_DOWN PID GRAB STAND_UP') 
RETURN_STATES = Enum('ReturnStates', 'INIT GO_HOME SCAN SEARCH_HOME DROP')

resolutionIndex = 3
RESOLUTIONS = { 0:(160,120),
                1:(320,240),
                2:(640, 480),
                3:(1280,960) 
              }

globalState = GLOBAL_STATES.SEARCH
localState  = SEARCH_STATES.INIT
motion      = None
posture     = None
camera      = None
cameraID    = 'nao_sorter'
cameraIndex = 0
resolution  = RESOLUTIONS[resolutionIndex]
tts         = None
tracker     = None
client      = None
videoClient = None
objects     = None
bounding_box = None
error       = 100
#centerPid         = PID(.001, 0.0001, 0, setpoint=0)
centerPid         = PID(.0003, 0.00005, 0, setpoint=0)
centerPid.output_limits = (-.35, .35)
walkPid     = PID(.00002, 0.000004, 0, setpoint=resolution[1]-100)

def main(ip, port = 9559):
    global globalState
    global localState
    global motion
    global posture
    global tts
    global camera
    global cameraID
    global cameraIndex
    global videoClient
    global resolution
    global resolutionIndex

    try:
        motion = ALProxy("ALMotion", ip, port)
        motion.wakeUp()
    except Exception, e:
        print "Error connecting to ALMotion"
        print "Error: ", e

    try:
        posture = ALProxy("ALRobotPosture", ip, port)
        posture.goToPosture("StandInit", 0.5)

        motion.setStiffnesses("Head", 1.0)
        headpitch = "HeadPitch"
        targetAngle = [15.0*almath.TO_RAD]
        targetTime  = [1.0]
        isAbsolute  = True
        motion.angleInterpolation(headpitch, targetAngle, targetTime, isAbsolute)
        time.sleep(1)
    except Exception, e:
        print "Error connecting to ALRobotPosture"
        print "Error: ", e

    try:
        camera = ALProxy("ALVideoDevice", ip, port)
        if camera.getSubscribers() > 1:
            for x in camera.getSubscribers()[1:]:
                camera.unsubscribe(x)
        videoClient = camera.subscribeCamera(cameraID, cameraIndex, resolutionIndex, 13, 30)
    except Exception, e:
        print "Error connecting to ALVideoDevice"
        print "Error: ", e

    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
    except Exception, e:
        print "Error connecting to ALTextToSpeech"
        print "Error: ", e

    #movement = Movement(ip, port)
    print( globalState )
    tts.say("Hi! My name is Paquito.")
    tts.say("This is the nao sorter.")

    while True:
        stateMachineStart()
        stateMachineEnd()


def stateMachineStart():
    global globalState
    global localState

    if globalState == GLOBAL_STATES.INIT:
        #TODO: INIT STATE 
        print globalState
    elif globalState == GLOBAL_STATES.SEARCH:
        #TODO: SEARCH STATE
        searchStart()
        print globalState
    elif globalState == GLOBAL_STATES.TRACK:
        #TODO: TRACK STATE
        print globalState
        trackStart()
    elif globalState == GLOBAL_STATES.PICKUP:
        #TODO: PICKUP STATE
        print globalState
        pickUpStart()
    elif globalState == GLOBAL_STATES.RETURN:
        #TODO: RETURN STATE
        print globalState
    else:
        print('STATE NOT APPLICABLE')
    

def stateMachineEnd():
    global globalState
    global localState

    if globalState == GLOBAL_STATES.INIT:
        #TODO: INIT STATE
        #      MAKE AN ANIMATION WITH THE ROBOT
        print globalState
    elif globalState == GLOBAL_STATES.SEARCH:
        if searchEnd() == GLOBAL_STATES.COMPLETED:
            globalState = GLOBAL_STATES.TRACK
            localState  = TRACK_STATES.INIT
    elif globalState == GLOBAL_STATES.TRACK:
        if trackEnd() == GLOBAL_STATES.COMPLETED:
            globalState = GLOBAL_STATES.PICKUP
            localState  = PICKUP_STATES.BEND_DOWN
        print globalState
    elif globalState == GLOBAL_STATES.PICKUP:
        if pickUpEnd() == GLOBAL_STATES.COMPLETED: 
            globalState = GLOBAL_STATES.RETURN
            localState  = RETURN_STATES.INIT
    elif globalState == GLOBAL_STATES.RETURN:
        #TODO: RETURN STATE
        print globalState
    else:
        print 'STATE NOT APPLICABLE'
    
####################### SEARCH ########################
#SEARCH_STATES = Enum('SearchStates', 'INIT MOVE SCAN')
def searchStart():
    global globalState
    global localState
    global client
    global objects
    global tts

    if localState == SEARCH_STATES.INIT:
        return
    elif localState == SEARCH_STATES.SCAN:  
        return
    elif localState == SEARCH_STATES.MOVE:
        #MOVE TO OBJECT
        print localState
    elif localState == SEARCH_STATES.SCAN:
        #MOVE HEAD
        # IF STRAIGHT LOOK LEFT
        # IF LEFT LOOK RIGHT
        # IF RIGHT LOOK LEFT
        print localState

    else:
        print 'SEARCH STATE START'

def searchEnd():
    global globalState
    global localState
    global client
    global objects 

    if localState == SEARCH_STATES.INIT:
	#tts.say("Initializing Search")
        if not client:
            client = cl.Client('127.0.0.1')
        objects = findObjects()
        if objects:
            return GLOBAL_STATES.COMPLETED
        else:
            localState = SEARCH_STATES.SCAN
            return GLOBAL_STATES.INCOMPLETE
    elif localState == SEARCH_STATES.MOVE:
        #CHECK IF DETECTED
        #IF YES: CHANGE STATE TO TRACK
        print localState
    elif localState == SEARCH_STATES.SCAN:
        objects = findObjects()
        if objects:
            globalState = GLOBAL_STATES.TRACK
            localState = TRACK_STATES.INIT
        print localState
    else:
        print 'SEARCH STATE END'


####################### TRACK #########################
#TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST MOVE_TOWARD')
def trackStart():
    global localState
    global tracker
    global camera
    global objects
    global bounding_box

    if localState == TRACK_STATES.INIT:
        return
    elif localState == TRACK_STATES.ADJUST:
        return
    elif localState == TRACK_STATES.CENTER:
        center( bounding_box )
    elif localState == TRACK_STATES.MOVE_TOWARD:
        moveToward( bounding_box )
    else:
        print 'TRACK STATE START'

def trackEnd():
    global globalState
    global localState
    global tracker
    global camera
    global objects
    global tts
    global client
    global bounding_box

    if localState == TRACK_STATES.INIT:
        #SORT THE LIST OF OBJECTS AND PICK ONE
        #AFTER THAT PICK ONE AND INITIALIZE THE BOUNDING_BOX VARIABLE TO THE ONE PICKED
        #MAKE NAO SAY WHICH ONE IS PICKED
        if ( objects is None ):
            globalState = GLOBAL_STATES.SEARCH
            localState  = SEARCH_STATES.INIT
            return GLOBAL_STATES.INCOMPLETE

        #tts.say("Found " + str( len(objects) ) + " objects.")

        sortedObjects = sortObjects( objects )
        cubes = countObjects( sortedObjects, "cube" )
        balls = countObjects( sortedObjects, "ball" )

        #tts.say("There are " + str(cubes) + " cubes.")
        #tts.say("There are " + str(balls) + " balls.")
        #tts.say("Tracking the closest object. It is a " + str(sortedObjects[0,0]))

        box = sortedObjects[0,2:]
        box = box.astype(float)
        box[0] = int(box[0] - box[2]/2)
        box[1] = int(box[1] - box[3]/2)
        box[2] = int(box[2])
        box[3] = int(box[3])

        bounding_box = tuple(box) 
        print bounding_box
        
        #tracker = ClientTracker( '127.0.0.1', camera )
        #tracker.start( bounding_box )
        localState = TRACK_STATES.ADJUST
        return GLOBAL_STATES.INCOMPLETE
    elif localState == TRACK_STATES.ADJUST:
        #print localState
        state = adjust( bounding_box )

        if state == GLOBAL_STATES.COMPLETED:
            return state
        else:
            localState = state
            return GLOBAL_STATES.INCOMPLETE
    elif localState == TRACK_STATES.CENTER:
        globalState = GLOBAL_STATES.SEARCH
        localState  = SEARCH_STATES.SCAN
    elif localState == TRACK_STATES.MOVE_TOWARD:
        globalState = GLOBAL_STATES.SEARCH
        localState  = SEARCH_STATES.SCAN
    elif localState == TRACK_STATES.SWITCH_CAMERA:
    	switchCamera()
	globalState = GLOBAL_STATES.SEARCH
        localState  = SEARCH_STATES.SCAN

def adjust( box ):
    global resolution
    global tts
    global error

    x, y, width, height = box 
    print (x)
    print (resolution[0]/2)

    if ( abs( (resolution[0]/2) - x ) > 50 ):
        #tts.say("Object is not center.")
        return TRACK_STATES.CENTER
    else:
        tts.say("Object is center.")

    if cameraIndex == 0:
        if ( ((resolution[1]-50) - y) > error ):
	    tts.say("Camera 1: moving closer to object.")
	    return TRACK_STATES.MOVE_TOWARD
        else:
	    return TRACK_STATES.SWITCH_CAMERA
    else:
        print 'Resolution, y, error'
        print resolution[1]/2
	print y
	print error
        if ( (resolution[1]/5*3) - y > error ):
	    tts.say("Camera 2: moving closer to object.")
	    return TRACK_STATES.MOVE_TOWARD
        else:
            tts.say("Object is in position for pickup.")	
	    return GLOBAL_STATES.COMPLETED
  

    tts.say("W.T.F")
    #TODO: CHECK ANGLE OF NAO HEAD TO SEE IF IT'S THE MOST IT CAN GO

    #return GLOBAL_STATES.COMPLETED

def center( box ):
    global resolution
    global tts
    global motion
    global centerPid

    x, y, width, height = box

    offset = x - (resolution[0]/2)
    if offset > 0:
        #tts.say("Object is to my right")
	out = centerPid(offset)
	print out
        motion.moveTo(0,0, out)
    elif offset < 0:
        #tts.say("Object is to my left")
	out = centerPid(offset)
	print out
        motion.moveTo(0,0, out)
    return

def moveToward( box ):
   _, y, _, _ = box
   out = walkPid(y)
   print "OutToward: " + str(out)
   motion.moveTo(out, 0, 0)

def switchCamera():
   global videoClient
   global cameraIndex
   global walkPid
   global error

   if camera.getSubscribers() > 1:
     for x in camera.getSubscribers()[1:]:
       camera.unsubscribe(x)

   if cameraIndex == 0:
     walkPid     = PID(.00002, 0.000004, 0, setpoint=(resolution[1]/5)*3)
     cameraIndex = 1
   else:
     walkPid     = PID(.00002, 0.000004, 0, setpoint=resolution[1]-100)
     cameraIndex = 0

   videoClient = camera.subscribeCamera(cameraID, cameraIndex, resolutionIndex, 13, 30)
    
    

####################### PICK UP #######################
def pickUpStart():
    global motion
    global localState
    global tts
    global posture

    if localState == PICKUP_STATES.INIT:
        print localState
    elif localState == PICKUP_STATES.ADJUST:
        print localState
    elif localState == PICKUP_STATES.BEND_DOWN:
        tts.say("Picking up object.")
        posture.goToPosture("StandInit", 0.5)
	time.sleep(0.5)
        bend_down( motion )     
    elif localState == PICKUP_STATES.PID:
        #Truc:Adjust right hand to decrease error.
        print localState
    elif localState == PICKUP_STATES.GRAB:
        print localState
    elif localState == PICKUP_STATES.STAND_UP:
        print localState
    else:
        print 'IN PICKUP STATE BUT NO LOCAL STATE'
    
def pickUpEnd():
    global localState

    if localState == PICKUP_STATES.INIT:
        print localState
    elif localState == PICKUP_STATES.ADJUST:
        print localState
    elif localState == PICKUP_STATES.BEND_DOWN:
        print localState
	while True:
	  x = 1
    elif localState == PICKUP_STATES.PID:
        #Truc:Check if error is zero.
        print localState
    elif localState == PICKUP_STATES.GRAB:
        print localState
    elif localState == PICKUP_STATES.STAND_UP:
        print localState
    else:
        print 'IN PICKUP STATE BUT NO LOCAL STATE'

################ RETURN ##############################
#RETURN_STATES = Enum('ReturnStates', 'INIT GO_HOME SCAN SEARCH_HOME DROP')
def returnStart():
    global localState

    if localState == RETURN_STATES.INIT:
        print localState
    elif localState == RETURN_STATES.GO_HOME:
        print localState
    elif localState == RETURN_STATES.SCAN:
        print localState
    elif localState == RETURN_STATES.SEARCH_HOME:
        print localState
    elif localState == RETURN_STATES.DROP:
        print localState
    else:
        print 'IN RETURN STATE START'

def returnEnd():
    global localState

    if localState == RETURN_STATES.INIT:
        print localState
    elif localState == RETURN_STATES.GO_HOME:
        print localState
    elif localState == RETURN_STATES.SCAN:
        print localState
    elif localState == RETURN_STATES.SEARCH_HOME:
        print localState
    elif localState == RETURN_STATES.DROP:
        print localState
    else:
        print 'IN RETURN STATE END'

############################## HELPER FUNCTIONS ##############################
def findObjects():
    image = camera.getImageRemote(videoClient)
    width, height, np_str = image[0], image[1], image[6]
    image = np.fromstring(np_str, np.uint8).reshape(height, width, 3)
    return client.detect(image)

def sortObjects( objects ):
    array = np.array( objects )
    array = array[ array[:,3].argsort() ]
    print array
    return array[::-1]

def countObjects( array, target ):
    return np.count_nonzero( array == target )

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help = 'Robot IP Address')
    parser.add_argument('--port', type=int, default = 9559,
                        help = 'Robot Port Number')

    args = parser.parse_args()
    main(args.ip, args.port)
