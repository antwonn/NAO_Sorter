import cv2
import socket
import pickle
import numpy as np

class serverTracker:
    port     = 9001
    buffsize = 4096


    def __init__(self, host):
        self.host        = host
        self.tracker     = None
        self.boundingBox = None
        self.frame       = None

        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )  
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.client, _ = self.socket.accept()

        self.DISPATCHER = {
            "start"  : serverTracker.start,
            "update" : serverTracker.update
        }

        #self.client.send(b'INITIALIZED')
        self.handleRequests()

    def handleRequests(self):
        while True:
            recv = self.client.recv( self.buffsize )
            while len(recv) % self.buffsize == 0:
                recv += self.client.recv(self.buffsize)
            msg  = pickle.loads( recv, encoding='bytes')
            print (msg[2])
            # if start then update bounding box and frame
            # if update then update frame and return bounding box


    def start(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init( frame, boundingBox ) 
        print ('started tracker')


    def update(self):
        (success, box) = self.tracker.update( self.frame ) 
        if success:
            msg = pickle.dumps( box )
        print ('update')

server = serverTracker('127.0.0.1')
