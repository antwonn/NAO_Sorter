from naoqi import ALProxy
from Queue import Queue
from enum import Enum
from movement.movement import Movement
from movement.pick_up_position import bend_down
from vision.clientTracker import ClientTracker
import argparse

GLOBAL_STATES = Enum('GlobalStates', 'INIT SEARCH TRACK PICKUP RETURN COMPLETED INCOMPLETE')
SEARCH_STATES = Enum('SearchStates', 'INIT MOVE HEAD_SCAN')
TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST MOVE_TOWARD')
PICKUP_STATES = Enum('PickUpStates', 'INIT ADJUST BEND_DOWN PID GRAB STAND_UP') 
RETURN_STATES = Enum('ReturnStates', 'INIT GO_HOME SCAN SEARCH_HOME DROP')

globalState = GLOBAL_STATES.TRACK
localState  = TRACK_STATES.INIT
motion      = None
posture     = None
camera      = None
tracker     = None


def main(ip, port = 9559):
    global globalState
    global localState
    global motion
    global posture
    global camera

    try:
        motion = ALProxy("ALMotion", ip, port)
    except Exception, e:
        print "Error connecting to ALMotion"
        print "Error: ", e

    try:
        posture = ALProxy("ALRobotPosture", ip, port)
    except Exception, e:
        print "Error connecting to ALRobotPosture"
        print "Error: ", e

    try:
        camera  = ALProxy("ALVideoDevice", ip, port)
    except Exception, e:
        print "Error connecting to ALVideoDevice"
        print "Error: ", e

    movement = Movement(ip, port)
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
        #TODO: SEARCH STATE
        searchEnd()
        print globalState
    elif globalState == GLOBAL_STATES.TRACK:
        #TODO: TRACH STATE
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
    global localState
    if localState == SEARCH_STATES.INIT:
        localState = SEARCH_STATES.MOVE
        print localState
    elif localState == SEARCH_STATES.MOVE:
        #MOVE TO OBJECT
        print localState
    elif localState == SEARCH_STATES.HEAD_SCAN:
        #MOVE HEAD
        print localState
    else:
        print 'SEARCH STATE START'

def searchEnd():
    global localState
    if localState == SEARCH_STATES.INIT:
        #START THREAD LOOKING FOR OBJECTS
        print localState
    elif localState == SEARCH_STATES.MOVE:
        #CHECK IF DETECTED
        #IF YES: CHANGE STATE TO TRACK
        print localState
    elif localState == SEARCH_STATES.HEAD_SCAN:
        print localState
    else:
        print 'SEARCH STATE END'


####################### TRACK #########################
#TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST MOVE_TOWARD')
def trackStart():
    global localState
    global tracker
    global camera

    if localState == TRACK_STATES.INIT:
        #initiate thread that is updating the box continuously
        #if bounding box is null then go back to search
        print localState
    elif localState == TRACK_STATES.ADJUST:
        print localState
    elif localState == TRACK_STATES.TOWARD:
        print localState
    else:
        print 'TRACK STATE START'

def trackEnd():
    global localState
    global tracker
    global camera

    if localState == TRACK_STATES.INIT:
        bounding_box = (50, 50, 50, 50) #initiate bounding box
        tracker = ClientTracker( '127.0.0.1' )
        print camera
        tracker.start( camera, bounding_box )
        #TODO: get initial adjustent
        print 'TRACK_STATES.INIT'
        localState = TRACK_STATES.ADJUST
        print localState
    elif localState == TRACK_STATES.ADJUST:
        print localState
    elif localState == TRACK_STATES.TOWARD:
        print localState
    else:
        print 'TRACK STATE END'



####################### PICK UP #######################
def pickUpStart():
    global motion
    global localState

    if localState == PICKUP_STATES.INIT:
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


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help = 'Robot IP Address')
    parser.add_argument('--port', type=int, default = 9559,
                        help = 'Robot Port Number')

    args = parser.parse_args()
    main(args.ip, args.port)
