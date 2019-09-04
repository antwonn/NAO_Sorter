from naoqi import ALProxy
import vision_definitions
from PIL import Image
import numpy as np
import cv2

IP = "127.0.0.1"
PORT = 9559

print "Creating ALVideoDevice proxy to ", IP

camProxy = ALProxy("ALVideoDevice", IP, PORT)

resolution = 2 #VGA
colorspace = 11 #RGB

fps = 30

client = camProxy.subscribe("python_GVM", resolution, colorspace, fps)

camProxy.setResolution(client, resolution)


print 'getting imaes in remote'
img = camProxy.getImageRemote(client)
width  = img[0]
height = img[1]
array  = img[6]

im = Image.frombytes("RGB", (width, height), array)
im.show()
im.save("../../../images/screenshot.png")

camProxy.unsubscribe(client)
print 'end'
