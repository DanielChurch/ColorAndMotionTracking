'''
Daniel Church
Assignment 2 Part 1
'''

#Imports
import numpy as np
import cv2 as cv
from tkinter import Tk
from tkinter import filedialog

#Window delcarations
default_window = 'Default';
cv.namedWindow(default_window);

hsv_window = 'hsv';
cv.namedWindow(hsv_window);

track_window = 'Track';

#Functions
def setThreshold(f):
    lower_track = [cv.getTrackbarPos('Lower R', track_window), cv.getTrackbarPos('Lower G', track_window), cv.getTrackbarPos('Lower B', track_window)];
    upper_track = [cv.getTrackbarPos('Upper R', track_window), cv.getTrackbarPos('Upper G', track_window), cv.getTrackbarPos('Upper B', track_window)];
    global lower, upper;
    for i in range(0,3):
        lower[i] = color[i]-lower_track[i];
        upper[i] = color[i]+upper_track[i];

def getPixelColor (event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        global color;
        color = hsv[y][x];
        if(cv.getWindowProperty(track_window, 0) == -1): #track_window isn't open
            cv.namedWindow(track_window);
            cv.createTrackbar('Lower R', track_window, abs(color[0]-10),255, setThreshold);
            cv.createTrackbar('Lower G', track_window, abs(color[1]-10),255, setThreshold);
            cv.createTrackbar('Lower B', track_window, abs(color[2]-10),255, setThreshold);
            cv.createTrackbar('Upper R', track_window, abs(color[0]+10),255, setThreshold);
            cv.createTrackbar('Upper G', track_window, abs(color[1]+10),255, setThreshold);
            cv.createTrackbar('Upper B', track_window, abs(color[2]+10),255, setThreshold);
            lower_track = [cv.getTrackbarPos('Lower R', track_window), cv.getTrackbarPos('Lower G', track_window), cv.getTrackbarPos('Lower B', track_window)];
            upper_track = [cv.getTrackbarPos('Upper R', track_window), cv.getTrackbarPos('Upper G', track_window), cv.getTrackbarPos('Upper B', track_window)];
            global lower, upper;
            for i in range(0,3):
                lower[i] = color[i]-lower_track[i];
                upper[i] = color[i]+upper_track[i];
            
#No TK Window
Tk().withdraw();

filename = filedialog.askopenfilename();

color = [];
lower = [0,0,0];
upper = [0,0,0];
lower_track = [];
upper_track = [];

cap = cv.VideoCapture(filename);

cv.setMouseCallback(hsv_window, getPixelColor);

while True :
    ret, img = cap.read();
    
    if(type(img) == type(None)): #Loop video if it ends (Not applicable for live video)
        cap.set(cv.CAP_PROP_POS_FRAMES, 0);
        continue;
    
    cv.imshow(default_window, img);
    
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV);
    cv.imshow(hsv_window, hsv);

    kernel = np.ones((5,5),np.uint8);
    erosion = cv.erode(hsv,kernel,iterations = 1);
    dilation = cv.dilate(erosion,kernel,iterations = 1);
    if(upper != [0,0,0]):
        mask = cv.inRange(dilation, np.array(lower), np.array(upper));
        color_mask = cv.bitwise_and(img, img, mask=mask);
        cv.imshow('mask', mask);
        cv.imshow(track_window, color_mask);
    k = cv.waitKey(30) & 0xff;
    if(k == 27):
        break;
cap.release();
cv.destroyAllWindows();
