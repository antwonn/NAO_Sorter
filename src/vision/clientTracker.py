import cv2
import socket
import pickle
import threading
import numpy as np
from Queue import Queue

class ClientTracker:
    port = 9001
    buffsize = 4096

    def __init__(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.track = False
        self.box   = Queue(maxsize=1)
        #assert self.socket.recv( self.buffsize) == b'INITIALIZED' )

    def start(self, camera, bounding_box ):
        if self.box.empty():
            self.box.put( bounding_box )
            self.box.task_done()
        else:
            rmv = self.box.get()
            self.box.put( bounding_box )
            self.box.task_done()
            
        self.camera = camera
        self.track = True

        resolution = 2
        colorspace = 13
        fps = 30
        client = self.camera.subscribe('python_GVM', resolution, colorspace, fps)

        img = self.camera.getImageRemote( client )
        img_width  = img[0]
        img_height = img[1]
        array      = img[6]
        img_data  = np.fromstring( array, np.uint8 ).reshape( img_height, img_width, 3)

        msg = pickle.dumps( ('start', img_data, bounding_box ) )
        self.socket.send( msg )
        #recv = self.socket.recv( self.buffsize )

        thread = threading.Thread( target=self.update )
        thread.start()

    def update(self):
        resolution = 2
        colorspace = 13
        fps = 30
        client = self.camera.subscribe('python_GVM', resolution, colorspace, fps)
        #camera.setResolution(client, resolution)

        while True:
            img = self.camera.getImageRemote(client)
            img_width  = img[0]
            img_height = img[1]
            array      = img[6]

            img_data  = np.fromstring( array, np.uint8 ).reshape( img_height, img_width, 3)
            data = pickle.dumps( ("update",img_data) )
            self.socket.send( data )

            recv = self.socket.recv( self.buffsize )
            print pickle.loads( recv )


            
            #send to server
            #save bounding box to Queue

    def stop(self):
        self.track = False

    def getBox(self):
        if this.box.empty():
            return None
        else:
            item = this.box.get() #grab from queue
            return_this = item    #set box to item in queue
            this.box.put(item)    #return box to queue
            box.task_done()
            return return_this
             

