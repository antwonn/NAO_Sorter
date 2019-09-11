from naoqi import ALProxy
import vision_definitions
from PIL import Image
import numpy as np
import os.path
import sys


'''
This function saves an image with the given file name.
Since this is supposed to take various screentshots from the NAO,
it checks if the filename exists and adds a number until it finds
a unique file name to save as.
'''
def saveImage(ip, port, proxy, client):
    name = raw_input('Input name of image: ')
    count = 0

    #Making sure file doesn't already exist.
    ordered_name = name + str(count) 
    path = '../../../images/' + ordered_name + '.png'
    while( os.path.exists(path) ):
        count += 1
        ordered_name = name + str(count)
        path = '../../../images/' + ordered_name + '.png'
    
    img = proxy.getImageRemote(client)
    width  = img[0]
    height = img[1]
    array  = img[6]

    img = Image.frombytes("RGB", (width, height), array)
    img.save(path)

#This function is if we want to show the image at the same time of screenshot.
#Need to thread this if we want to use it.
def showImage(ip, port):
    print "Creating ALVideoDevice proxy to ", IP
    camProxy = ALProxy('ALVideoDevice', ip, port)
    #CAMERA INFO: http://doc.aldebaran.com/2-1/family/robots/video_robot.html 
    resolution = 2  #VGA
    colorspace = 11 #RGB
    fps = 30

    client = camProxy.subscribe('python_GVM', resolution, colorspace, fps)
    camProxy.setResolution(client, resolution)

    while(true):
        img = camProxy.getImageRemote(client)
        width  = img[0]
        height = img[1]
        array  = img[6]

        img = Image.frombytes("RGB", (width, height), array)
        img.show()


if __name__ == '__main__':
    IP = "127.0.0.1"  # Replace here with your NaoQi's IP address.
    PORT = 9559

    # Read IP address from first argument if any.
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    camProxy = ALProxy('ALVideoDevice', IP, PORT)
    resolution = 2  #VGA
    colorspace = 11 #RGB
    fps = 30

    client = camProxy.subscribe('python_GVM', resolution, colorspace, fps)
    camProxy.setResolution(client, resolution)
     
    naoImage = saveImage(IP, PORT, camProxy, client)
    camProxy.unsubscribe(client)
