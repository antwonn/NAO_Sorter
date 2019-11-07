from pydarknet import Detector, Image
import cv2
import socket
import pickle
import numpy as np

class Server:

    host = None 
    port = 9000
    buffsize = 4096

    def __init__(self, host):
        self.host = host
        self.net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.backup", encoding="utf-8"), 0,
                   bytes("data/pong.data", encoding="utf-8"))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.client, _ = self.socket.accept()
        self.client.send(b'INITIALIZED')
        self.handleRequests()

    def handleRequests(self):
        client = self.client
        net = self.net
        while True:
            recv = client.recv(self.buffsize)
            while len(recv) % self.buffsize == 0:
                recv += client.recv(self.buffsize)
            frame = pickle.loads(recv, protocol=2)
            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame
            
            data = []
            for cat, score, bounds in results:
                obj = []
                x, y, w, h = bounds
                obj.append(cat.decode('utf-8'))
                obj.append(score)
                obj.append(x)
                obj.append(y)
                obj.append(w)
                obj.append(h)
                data.append(obj) 
            
            ret = pickle.dumps(data, protocol=2)
            print('sending data')
            client.send(ret)

        
