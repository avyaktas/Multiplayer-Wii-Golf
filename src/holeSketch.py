from cmu_graphics import *

import cv2
import numpy as np

imagePath = 'google earth.jpg'

def getHoleOutlines(imagePath):
    # Read the image
    img = cv2.imread(imagePath)
    if img is None:
        raise Exception("Image not found!")
    
    # Convert to HSV color space for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define color ranges in HSV
    pinkLower = np.array([145, 30, 180])
    pinkUpper = np.array([170, 255, 255])
    
    orangeLower = np.array([5, 100, 100]) 
    orangeUpper = np.array([15, 255, 255])
    
    redLower = np.array([0, 100, 100])
    redUpper = np.array([5, 255, 255])
    
    purpleLower = np.array([130, 50, 50])
    purpleUpper = np.array([145, 255, 255])
    
    blueLower = np.array([100, 100, 100])
    blueUpper = np.array([120, 255, 255])
    
    # Create masks for each color
    holeMask = cv2.inRange(hsv, pinkLower, pinkUpper)
    fairwayMask = cv2.inRange(hsv, orangeLower, orangeUpper)
    teeboxMask = cv2.inRange(hsv, redLower, redUpper)
    sandtrapMask = cv2.inRange(hsv, purpleLower, purpleUpper)
    greenMask = cv2.inRange(hsv, blueLower, blueUpper)
    
    # Find contours for each feature
    def getContourPoints(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []
        # Get the largest contour
        largestContour = max(contours, key=cv2.contourArea)
        # Convert contour to list of points
        return [(point[0][0], point[0][1]) for point in largestContour]
    
    holeOutline = getContourPoints(holeMask)
    fairwayOutline = getContourPoints(fairwayMask)
    teeboxOutline = getContourPoints(teeboxMask)
    sandtrapOutline = getContourPoints(sandtrapMask)
    greenOutline = getContourPoints(greenMask)
    
    return {
        'hole': holeOutline,
        'fairway': fairwayOutline,
        'teebox': teeboxOutline,
        'sandtrap': sandtrapOutline,
        'green': greenOutline
    }

