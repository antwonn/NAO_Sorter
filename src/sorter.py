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
SEARCH_STATES = Enum('SearchStates', 'INIT MOVE HEAD_SCAN')
TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST CENTER MOVE_TOWARD')
PICKUP_STATES = Enum('PickUpStates', 'INIT ADJUST BEND_DOWN PID GRAB STAND_UP') 
RETURN_STATES = Enum('ReturnStates', 'INIT GO_HOME SCAN SEARCH_HOME DROP')

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
resolution  = RESOLUTIONS[2]
tts         = None
tracker     = None
client      = None
videoClient = None
objects     = None
bounding_box = None
pid         = PID(.001, 0.0001, 0, setpoint=0)
pid.output_limits = (-.35, .35)

def main(ip, port = 9559):
    global globalState
    global localState
    global motion
    global posture
    global tts
    global camera
    global videoClient
    global resolution

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
        videoClient = camera.subscribe('nao_sorter', 2, 13, 30)
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
        print globalState
    elif globalState == GLOBAL_STATES.SEARCH:
        searchEnd()
        print globalState
    elif globalState == GLOBAL_STATES.TRACK:
        if trackEnd() == GLOBAL_STATES.COMPLETED:
            globalState = GLOBAL_STATES.PICKUP
            localState  = PICKUP_STATES.INIT
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
#SEARCH_STATES = Enum('SearchStates', 'INIT MOVE HEAD_SCAN')
def searchStart():
    global globalState
    global localState
    global client
    global objects
    global tts

    if localState == SEARCH_STATES.INIT:
        if not client:
            #client = cl.Client(args.ip)
            client = cl.Client('127.0.0.1')
	tts.say("Searching")
        objects = findObjects()
        if objects:
            globalState = GLOBAL_STATES.TRACK
            localState = TRACK_STATES.INIT
        else:
            localState = SEARCH_STATES.HEAD_SCAN
            
    elif localState == SEARCH_STATES.MOVE:
        #MOVE TO OBJECT
        print localState

    elif localState == SEARCH_STATES.HEAD_SCAN:
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
    if localState == SEARCH_STATES.INIT:
        #START THREAD LOOKING FOR OBJECTS
        print localState
    elif localState == SEARCH_STATES.MOVE:
        #CHECK IF DETECTED
        #IF YES: CHANGE STATE TO TRACK
        print localState
    elif localState == SEARCH_STATES.HEAD_SCAN:
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

    if localState == TRACK_STATES.INIT:
        #initiate thread that is updating the box continuously
        #if bounding box is null then go back to search
        print localState
    elif localState == TRACK_STATES.ADJUST:
        #print localState
        return
    elif localState == TRACK_STATES.TOWARD:
        print localState
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
        #print objects
        sortedObjects = sortObjects( objects )
        #print '\n\n\n\n'
        #sortedObjects = reversed( sorted( lambda x: x[3], objects ) )
        print sortedObjects

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
        print localState
    elif localState == TRACK_STATES.ADJUST:
        #print localState
        state = adjust( bounding_box )

        if state == GLOBAL_STATES.COMPLETED:
            return state
        elif state == TRACK_STATES.CENTER:
            #tts.say("Centering Object")
            center( bounding_box )
	    globalState = GLOBAL_STATES.SEARCH
	    localState  = SEARCH_STATES.INIT

        return GLOBAL_STATES.INCOMPLETE
    elif localState == TRACK_STATES.TOWARD:
        print localState
    else:
        print 'TRACK STATE END'

def adjust( box ):
    global resolution
    global tts

    x, y, width, height = box 
    print (x)
    print (resolution[0]/2)

    if ( abs( (resolution[0]/2) - x ) > 10 ):
        #tts.say("Object is not center.")
        return TRACK_STATES.CENTER
    elif False:
        #TODO CHECK IF Y IS TOO FAR UP
        return TRACK_STATES.MOVE_TOWARD

    return GLOBAL_STATES.COMPLETED

def center( box ):
    global resolution
    global tts
    global motion
    global pid

    x, y, width, height = box

    offset = x - (resolution[0]/2)
    if offset > 0:
        #tts.say("Object is to my right")
	out = pid(offset)
	print out
        motion.moveTo(0,0, out)
    elif offset < 0:
        #tts.say("Object is to my left")
	out = pid(offset)
	print out
        motion.moveTo(0,0, out)
    return
    

####################### PICK UP #######################
def pickUpStart():
    global motion
    global localState

    if localState == PICKUP_STATES.INIT:
        while True:
            x = 1
        print localState
    elif localState == PICKUP_STATES.ADJUST:
        print localState
    elif localState == PICKUP_STATES.BEND_DOWN:
        print localState
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
