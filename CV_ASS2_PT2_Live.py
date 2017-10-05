'''
Daniel Church
Assignment 2 Part 2
'''

#Imports
import numpy as np
import cv2 as cv

#Window delcarations
default_window = 'normal';
cv.namedWindow(default_window);

cap = cv.VideoCapture(0);

images = [];
count = 0;
max_count = 5;

while True :
    ret, img = cap.read();
    
    blur = cv.blur(img,(5,5));
    
    if(count >= max_count): #Remove first if full and always append to the end
        images.pop(0);
    images.append(blur);
    
    outputImage = np.zeros((int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), 3), np.float32);
    
    imageSum = np.zeros((int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), 3), np.float32);
    
    if(count > max_count):
        for i in range(0,max_count):
            imageSum += cv.accumulateWeighted(images[i], outputImage, 2/max_count/max_count); #Found 2/max_count/max_count works well from experimentation
    
    imageSum = cv.convertScaleAbs(imageSum);
    
    cv.imshow('Accumulation', imageSum);
    
    difference = cv.absdiff(img, imageSum);
    cv.imshow('Difference', difference);
    
    gray = cv.cvtColor(difference, cv.COLOR_RGB2GRAY);
    
    ret, lowThresh=cv.threshold(gray, 30, 255, cv.THRESH_BINARY);
    blur = cv.blur(lowThresh,(5,5));
    ret, highThresh=cv.threshold(blur, 200, 255, cv.THRESH_BINARY);
    
    im2, contours, hierarchy = cv.findContours(highThresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    
    cv.imshow("Final - Only Lower Threshold", lowThresh);
    
    #Calculate the largest contour
    maxArea = 0;
    maxAreaIndex = -1;
    for i in contours :
        if(cv.contourArea(i) > maxArea):
            maxArea = cv.contourArea(i);
            maxAreaIndex = i;
    
    if(type(maxAreaIndex) != int): #Only show bounding box if contours exist
        x,y,w,h = cv.boundingRect(maxAreaIndex)
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #cv.drawContours(highThresh, contours, -1, (0,255,0), 3)
        
    cv.imshow('Final - Upper & Lower Threshold', highThresh);
    cv.imshow(default_window, img);
    
    k = cv.waitKey(30) & 0xff;
    if(k == 27):
        break;
    
    count+=1;
cap.release();
cv.destroyAllWindows();
