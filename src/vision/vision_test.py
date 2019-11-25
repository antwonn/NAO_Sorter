import time
import argparse
import cv2
import numpy as np
from naoqi import ALProxy
import vision_definitions

def main(robotIP, PORT=9559):
    resolution = 2  #640x480
    colorSpace = 13 #RGB

    ### Subscribe to video from NAO Robot
    camProxy = ALProxy('ALVideoDevice', robotIP , PORT)
    print(camProxy)
    videoClient = camProxy.subscribe('python_GVM', resolution, colorSpace, 5)
    import client

    try:
        c = client.Client('192.168.0.109')
        while True:
            #Get image and relevant information
            start = time.time()
            img = camProxy.getImageRemote(videoClient)
            img_width  = img[0]
            img_height = img[1]
            array      = img[6]
            data = np.fromstring(array, np.uint8).reshape(img_height, img_width, 3)
            image = c.detect(data)
            for res in image:
                cat,score,x,y,w,h = res
                cv2.rectangle(data, (int(x-w/2),int(y-h/2)), (int(x+w/2), int(y+h/2)), (255,0,0))
            cv2.imshow('window', data)
            print 'time lapse: ' + str(time.time()-start)
            k = cv2.waitKey(1)
            
    except KeyboardInterrupt:
        print
        print 'Stopping'

    print 'Unsubscribing'
    camProxy.unsubscribe()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='Robot IP Address')
    parser.add_argument('--port', type=int, default=9559,
                        help='Robot Port Number')
    args = parser.parse_args()
    main(args.ip, args.port)
