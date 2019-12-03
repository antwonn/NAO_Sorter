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
        recv = self.socket.recv( self.buffsize )

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
            while len(recv) % self.buffsize == 0:
                recv += self.client.recv(self.buffsize)
            

            #updated_box = pickle.loads( recv )
            #print updated_box
            success, bounding_box =  pickle.loads( recv )
            print success, bounding_box

            if success:
                old_box = self.box.get()
                self.box.put( bounding_box )
                self.box.task_done()

            #TODO: else return null for not found



            
            #send to server
            #save bounding box to Queue

    def stop(self):
        self.track = False

    def getBox(self):
        if self.box.empty():
            return None
        else:
            item = self.box.get() #grab from queue
            ret = item    #set box to item in queue
            self.box.put(item)    #return box to queue
            self.box.task_done()
            return ret
             

