import cv2
import socket
import pickle
import threading
import numpy as np

class ClientTracker:
    port = 9001
    buffsize = 4096

    def __init__(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.track = False
        assert self.socket.recv( self.buffsize) == b'INITIALIZED' )

    def start( camera, bounding_box ):
        self.box    = bounding_box
        self.camera = camera
        self.track = True

        thread = threading.Thread( target=ClientTracker.update )
        thread.start()

    def update():
        resolution = 1
        colorspace = 11
        fps = 30
        client = self.camera.subscribe('python_GVM', resolution, colorspace, fps)
        camera.setResolution(client, resolution)

        while True:
            img = camera.getImageRemote(client, resolution)
            #convert to np image
            #send to server
            #save bounding box to Queue

    def getBox():
        #grab from queue
        #set box to item in queue
        #return box to queue
        return
