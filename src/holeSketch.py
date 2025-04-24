import cv2
import numpy as np

# the use of open Cv here was highly aided by chatGBT 
def getHoleOutlines(imagePath):
    # Read the image
    img = cv2.imread(imagePath)
    if img is None:
        raise Exception("Image not found!")
    
    # Convert to HSV color space for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    
    # PINK (outline/background area)
    pinkLower = np.array([130, 80, 80])
    pinkUpper = np.array([170, 255, 255])

    # ORANGE (fairway)
    orangeLower = np.array([10, 100, 100])
    orangeUpper = np.array([25, 255, 255])

    # RED (teebox) — red wraps in HSV so use two ranges
    redLower1 = np.array([0, 100, 100])
    redUpper1 = np.array([10, 255, 255])
    redLower2 = np.array([170, 100, 100])
    redUpper2 = np.array([180, 255, 255])

    # PURPLE (sandtraps)
    purpleLower = np.array([130, 50, 50])
    purpleUpper = np.array([155, 255, 255])

    # BLUE (green)
    blueLower = np.array([90, 100, 100])
    blueUpper = np.array([120, 255, 255])
 

    # Create masks for each color
    holeMask = cv2.inRange(hsv, pinkLower, pinkUpper)
    fairwayMask = cv2.inRange(hsv, orangeLower, orangeUpper)
    redMask1 = cv2.inRange(hsv, redLower1, redUpper1)
    redMask2 = cv2.inRange(hsv, redLower2, redUpper2)
    teeboxMask = redMask1 | redMask2
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
        contours, _ = cv2.findContours(mask, 
                                        cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []
        largest = max(contours, key=cv2.contourArea)
        return [(int(pt[0][0]), int(pt[0][1])) for pt in largest]

    
    def getAllContours(mask):
        contours, _ = cv2.findContours(mask, 
                                       cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        allContours = []
        for contour in contours:
            if len(contour) >= 3:  # skip too-small ones
                pts = [(int(x), int(y)) for [[x, y]] in contour]
                allContours.append(pts)
        return allContours
    
    origW, origH = img.shape[1], img.shape[0]
    canvasW, canvasH = 2000, 1200
    
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
