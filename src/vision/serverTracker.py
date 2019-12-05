import cv2
import socket
import pickle
import numpy as np

class ServerTracker:
    port     = 9001
    buffsize = 4096
    encoding = 'utf-8'


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
            'start'  : self.start,
            'update' : self.update
        }

        self.handleRequests()

    def handleRequests(self):
        while True:
            recv = self.client.recv( self.buffsize )
            while len(recv) % self.buffsize == 0:
                recv += self.client.recv(self.buffsize)
            msg  = pickle.loads( recv, encoding='bytes')
            s = str(msg[0], self.encoding)
            ret = pickle.dumps(self.DISPATCHER[s]( msg ), protocol=2)
            self.client.send(ret)


    def start(self, msg):
        self.tracker = cv2.TrackerCSRT_create()
        self.frame = msg[1]
        self.tracker.init( self.frame, msg[2] ) 
        return 'started tracker'


    def update(self, msg):
        self.frame = msg[1]
        msg = self.tracker.update( self.frame )
        if msg[0]:
            (x, y, w, h) = [int(v) for v in msg[1]]
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("frame", self.frame)
        key = cv2.waitkey(1) & 0xFF
        return msg


ip = '127.0.0.1'
print ('Starting ServerTracker at: ' + ip)
server = ServerTracker( ip )
