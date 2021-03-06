import cv2
import socket
import pickle
import numpy as np

'''
Client running on the robot.
Create a function that sends numpy image through a socket.
'''

class Client:
    host = None
    port = 9000
    buffsize = 4096

    def __init__(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        assert self.socket.recv(self.buffsize) == b'INITIALIZED'

    def detect(self, np_image):
        data = pickle.dumps(np_image, protocol=2) # Binary data
        self.socket.send(data) # Send Binary Data
        print('sent: ' + str(len(data)) + ' bytes')
        recv = self.socket.recv(self.buffsize) # Receive Detected Object
        while len(recv) % self.buffsize == 0:
            recv += self.socket.recv(self.buffsize)
        return pickle.loads(recv) # Return Detected Object



            
