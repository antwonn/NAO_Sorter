import cv2
import socket
import pickle
import numpy as np

'''
Client running on the robot.
Create a function that sends numpy image through a socket.
'''

class Client:
    host = '127.0.0.1'
    port = 9000
    buffsize = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.recv(self.buffsize)
        assert self.socket.recv(self.buffsize) == b'INITIALIZED'

    def detect(np_image):
        data = pickle.dumps(np_image) # Binary data
        self.socket.send(data) # Send Binary Data
        recv = self.socket.recv(self.buffsize) # Receive Detected Object
        while len(recv) % self.buffsize == 0:
            recv += self.socket.recv(self.buffsize)
        return pickle.loads(recv) # Return Detected Object



            
