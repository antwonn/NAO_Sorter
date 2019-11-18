from naoqi import ALProxy
from Queue import Queue
from enum import Enum
from movement.movement import Movement
from movement.pick_up_position import bend_down
import argparse

GLOBAL_STATES = Enum('GlobalStates', 'INIT SEARCH TRACK PICKUP RETURN COMPLETED INCOMPLETE')
SEARCH_STATES = Enum('SearchStates', 'INIT MOVE HEAD_SCAN')
TRACK_STATES  = Enum('TrackStates',  'INIT ADJUST MOVE_TOWARD')
PICKUP_STATES = Enum('PickUpStates', 'INIT ADJUST BEND_DOWN PID GRAB STAND_UP') 
RETURN_STATES = Enum('ReturnStates', 'INIT GO_HOME SCAN SEARCH_HOME DROP')

globalState = GLOBAL_STATES.PICKUP
localState  = PICKUP_STATES.BEND_DOWN
motion      = None
posture     = None


def main(ip, port = 9559):
    global globalState
    global localState
    global motion
    global posture

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
        print globalState
    elif globalState == GLOBAL_STATES.TRACK:
        #TODO: TRACK STATE
        print globalState
    elif globalState == GLOBAL_STATES.PICKUP:
        #TODO: PICKUP STATE
        print globalState
        pickUpStart()
    elif globalState == GLOBAL_STATES.RETURN:
        #TODO: RETURN STATE
        print globalState
    else:
        print('STATE NOT APPLICABLE')

    globalState = GLOBAL_STATES.SEARCH
    

def stateMachineEnd():
    global globalState
    global localState

    if globalState == GLOBAL_STATES.INIT:
        #TODO: INIT STATE 
        print globalState
    elif globalState == GLOBAL_STATES.SEARCH:
        #TODO: SEARCH STATE
        print globalState
    elif globalState == GLOBAL_STATES.TRACK:
        #TODO: TRACH STATE
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
    
#######################PICK UP#######################
def pickUpStart():
    global motion

    if localState == PICKUP_STATES.INIT:
        print localState
    elif localState == PICKUP_STATES.ADJUST:
        print localState
    elif localState == PICKUP_STATES.BEND_DOWN:
        print localState
        bend_down( motion )     
    elif localState == PICKUP_STATES.PID:
        print localState
    elif localState == PICKUP_STATES.GRAB:
        print localState
    elif localState == PICKUP_STATES.STAND_UP:
        print localState
    else:
        print 'IN PICKUP STATE BUT NO LOCAL STATE'
    
def pickUpEnd():
    if localState == PICKUP_STATES.INIT:
        print localState
    elif localState == PICKUP_STATES.ADJUST:
        print localState
    elif localState == PICKUP_STATES.BEND_DOWN:
        print localState
    elif localState == PICKUP_STATES.PID:
        print localState
    elif localState == PICKUP_STATES.GRAB:
        print localState
    elif localState == PICKUP_STATES.STAND_UP:
        print localState
    else:
        print 'IN PICKUP STATE BUT NO LOCAL STATE'
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help = 'Robot IP Address')
    parser.add_argument('--port', type=int, default = 9559,
                        help = 'Robot Port Number')

    args = parser.parse_args()
    main(args.ip, args.port)
