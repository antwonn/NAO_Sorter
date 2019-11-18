from naoqi import ALProxy
import almath

class Movement:
    def __init__(self, IP, PORT): 
        self.motionProxy = ALProxy("ALMotion", IP, PORT)
        self.pose = almath.Pose2D( self.motionProxy.getRobotPosition(True) )

    def position():
        return self.pose

    def rotate( degrees, direction = 'LEFT' ):
        #motionProxy.moveTo( 0.0, 0.0,  
        print 'rotato'
