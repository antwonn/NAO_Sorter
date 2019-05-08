'''
CECS 491A
NAO Sorter Team
This program is used to detect and show any circles of a certain color on images provided by the NAO Robot. 
In order to change the color detected change the value of the H in the HSV image.
Might have to calibrate the sensitivity to adjust to the lighting of the room in HoughCircles.
This would allow for more accurate detection.
'''

#TODO Add sliders on the HSV values to be able to adjust to rooms more quickly.

import time
import argparse
import cv2
import numpy as np
from naoqi import ALProxy

def main(robotIP, PORT=9559):
    resolution = 2  #640x480
    colorSpace = 13 #RGB

    ### Subscribe to video from NAO Robot
    camProxy = ALProxy('ALVideoDevice', robotIP , PORT)
    videoClient = camProxy.subscribe('ball_detection', resolution, colorSpace, 5)

    try:
        while True:
            #Get image and relevant information
            img = camProxy.getImageRemote(videoClient)
            img_width  = img[0]
            img_height = img[1]
            array      = img[6]
            #Convert image to numpy array
            data = np.fromstring(array, np.uint8).reshape(img_height, img_width, 3)

            #Give it a small blur for contours
            blur = cv2.GaussianBlur(data, (11,11), 0)
            hsv = cv2.cvtColor(data, cv2.COLOR_RGB2HSV) #HSY Color Space (Hue, Saturation, Brightness)

            #These are the colors which are detected in the vision detection.
            #Only one is available at a time for now, choose which with color.
            green  = 60
            blue   = 120
            sensitivity = 15
            color = blue
            lower_bound = np.array([color - sensitivity, 100, 30])
            upper_bound = np.array([color + sensitivity, 255, 255])

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            #mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            #SINCE RED IS 0 and HSV GOES FROM 0 to 180 WE NEED TO TAKE TWO RANGES AND BITWISE OR THEM TOGETHER
            '''  RED BALL MASK
            red_0 = 0
            red_180 = 180
            lower_bound_red_0 = np.array([red_0,100,100])
            upper_bound_red_0 = np.array([red_0+sensitivity,100,100])

            lower_bound_red_180 = np.array([red180-sensitivity,100,100])
            upper_bound_red_180 = np.array([red180,100,100])

            mask_red_1 = cv2.inRange(hsv, lower_bound_red_0, upper_bound_red_0)
            mask_red_2 = cv2.inRange(hsv, lower_bound_red_180, upper_bound_red_180)
            mask = cv2.bitwise_or(mask1, mask2)
            '''

            circles = cv2.HoughCircles(mask, cv2.cv.CV_HOUGH_GRADIENT, 1, 40,
            param1=30, 
            param2=10, 
            minRadius=0, 
            maxRadius=0)
            print circles

            #Color circles if they exist
            if circles is not None:
                for circle in circles[0,:]:
                    cv2.circle(data, (circle[0], circle[1]), 
                            circle[2], (255,0,0), 2)
                    cv2.circle(data, (circle[0], circle[1]),
                                2, (0,0,255), 3)
                

            cv2.imshow('mask', mask)
            cv2.imshow('test', data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0)
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
