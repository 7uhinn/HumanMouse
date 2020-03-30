#importing libraries
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx 

#instance of pynput (for mouse)
mouse = Controller()

#instance of wxpython 
app = wx.App(False)

(camx,camy) = (320,240) #image resolution of the captured image
(sx,sy) = wx.GetDisplaySize() #Screen resolution

lB = np.array([86,80,40])
uB = np.array([148,255,255]) #lower and upper bound of HSV values for blue (object color)

#instance of OpenCV VideoCapture through default camera
cam = cv2.VideoCapture(0)

#Filters initiated for Morphological Operations Later
kO = np.ones((5,5)) #for Opening
kC = np.ones((20,20)) #for Closing

FingersClosed = 0 #to signify if the fingers were closed or not

while True:
    ret, img = cam.read() #frames of the video stored in 'img' (real-time)
    img = cv2.resize(img,(camx,camy)) #image size set to the image resolution

    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert RGB to HSV format
    
    mask = cv2.inRange(imgHSV,lB,uB) #creating the mask
 
    maskO = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kO) #Morphological Opening Operation
    maskC = cv2.morphologyEx(maskO,cv2.MORPH_CLOSE,kC) #Morphological Closing Operation

    maskF = maskC
    conts,h = cv2.findContours(maskF.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #Areas of interests
    
    if(len(conts)==2): #if there are 2 fingers apart
        if(FingersClosed==1): 
            FingersClosed=0
            mouse.release(Button.left) #release left click (traversal mode)
        x1,y1,w1,h1 = cv2.boundingRect(conts[0]) 
        x2,y2,w2,h2 = cv2.boundingRect(conts[1]) #returns outscribed rectangle of the AOIs
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2) #draws the rectangle
        
        cx1=x1+w1//2 #x coordinate of centre of 1st AOI
        cy1=y1+h1//2 #y coordinate of centre of 1st AOI
        cx2=x2+w2//2 #x coordinate of centre of 2nd AOI
        cy2=y2+h2//2 #y coordinate of centre of 2nd AOI
        
        cx=(cx1+cx2)//2 #x coordinate of centre of both AOIs
        cy=(cy1+cy2)//2 #y coordinate of centre of both AOIs
        
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2) #line joining the 2 AOIs
        cv2.circle(img, (cx,cy),2,(0,0,255),2) #circle in the middle
        
        pos = (sx-(cx*sx//camx), cy*sy//camy) #mouse positioning in screen relative to movement in image
        mouse.position = pos 
        while mouse.position != pos:
            pass
        
    elif(len(conts)==1): #if the fingers join to make one large AOI (fingers closed)
        x,y,w,h = cv2.boundingRect(conts[0]) #returns outscribed rectangle of the AOI
        
        if(FingersClosed==0):
            FingersClosed=1
            mouse.press(Button.left) #perform left click (traversal mode)

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draws the rectangle
        
        cx=x+w//2 #x coordinate of centre of AOI
        cy=y+h//2 #y coordinate of centre of AOI
        
        cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2) #larger circle
        
        pos = (sx-(cx*sx//camx), cy*sy//camy) #mouse positioning in screen relative to movement in image
        mouse.position = pos 
        while mouse.position!=pos:
            pass
        
    elif(len(conts)==3): #if there are 3 fingers apart
        x,y,w,h = cv2.boundingRect(conts[0]) #returns outscribed rectangle of the AOI
        
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draws the rectangle
        
        mouse.press(Button.right) 
        
    cv2.imshow("cam",img) #finally show image on the 'cam' window
    cv2.waitKey(5)