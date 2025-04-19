from cmu_graphics import *

import cv2
import numpy as np

imagePath = 'Hole.jpg'


def getHoleOutlines(imagePath):
    # Read the image
    img = cv2.imread(imagePath)
    if img is None:
        raise Exception("Image not found!")
    
    # Convert to HSV color space for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define color ranges in HSV
    pinkLower = np.array([160, 100, 100])
    pinkUpper = np.array([175, 255, 255])
    
    orangeLower = np.array([15, 100, 100]) 
    orangeUpper = np.array([25, 255, 255])
    
    redLower = np.array([0, 100, 100])
    redUpper = np.array([10, 255, 255])
    
    purpleLower = np.array([130, 30, 30])
    purpleUpper = np.array([160, 255, 255])
    
    blueLower = np.array([100, 100, 100])
    blueUpper = np.array([130, 255, 255])

    # Create masks for each color
    holeMask = cv2.inRange(hsv, pinkLower, pinkUpper)
    fairwayMask = cv2.inRange(hsv, orangeLower, orangeUpper)
    teeboxMask = cv2.inRange(hsv, redLower, redUpper)
    sandtrapMask = cv2.inRange(hsv, purpleLower, purpleUpper)
    greenMask = cv2.inRange(hsv, blueLower, blueUpper)
    
    def scaleAndCenterPoints(points, origW, origH, canvasW, canvasH):
    # Keep aspect ratio while scaling
        scale = min(canvasW / origW, canvasH / origH)

    # Find offset to center shapes
        offsetX = (canvasW - origW * scale) / 2
        offsetY = (canvasH - origH * scale) / 2

        scaled = []
        for (x, y) in points:
            newX = int(x * scale + offsetX)
            newY = int(y * scale + offsetY)
            scaled.append((newX, newY))
        return scaled
    
    # Find contours for each feature
    def getContourPoints(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []
        largest = max(contours, key=cv2.contourArea)
        return [(int(pt[0][0]), int(pt[0][1])) for pt in largest]

    
    def getAllContours(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        allContours = []
        for contour in contours:
            if len(contour) >= 3:  # skip too-small ones
                pts = [(int(x), int(y)) for [[x, y]] in contour]
                allContours.append(pts)
        return allContours
    
    origW, origH = img.shape[1], img.shape[0]
    canvasW, canvasH = 1000, 600
    
    holeContoursRaw = getAllContours(holeMask)
    holeContours = [scaleAndCenterPoints(c, origW, origH, canvasW, canvasH) for c in holeContoursRaw]
    teebox = scaleAndCenterPoints(getContourPoints(teeboxMask), origW, origH, canvasW, canvasH)
    fairway = scaleAndCenterPoints(getContourPoints(fairwayMask), origW, origH, canvasW, canvasH)
    green = scaleAndCenterPoints(getContourPoints(greenMask), origW, origH, canvasW, canvasH)
    sandtrapsRaw = getAllContours(sandtrapMask)
    sandtraps = [scaleAndCenterPoints(c, origW, origH, canvasW, canvasH) for c in sandtrapsRaw]


    outlines = {
        'teebox': [teebox],
        'fairway': [fairway],
        'green': [green],
        'sandtrap': sandtraps,  # <- now a list of multiple contours
        'outline': holeContours
    }   

    return outlines

print(getHoleOutlines(imagePath))