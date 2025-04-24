# First chatGPT was used to get open cv to work better after perliminary 
#  Later used chatGPT to reFormt inorder to pass style checker. 
import cv2
import numpy as np

def getContourPoints(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return []
    largest = max(contours, key=cv2.contourArea)
    return [(int(pt[0][0]), int(pt[0][1])) for pt in largest]

def getAllContours(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    valid = []
    for contour in contours:
        if len(contour) >= 3:
            valid.append([(int(x), int(y)) for [[x, y]] in contour])
    return valid

def scaleAndCenterPoints(points, origW, origH, canvasW, canvasH):
    scale = min(canvasW / origW, canvasH / origH)
    offsetX = (canvasW - origW * scale) / 2
    offsetY = (canvasH - origH * scale) / 2
    return [
        (int(x * scale + offsetX), int(y * scale + offsetY))
        for x, y in points
    ]

def getHoleOutlines(imagePath):
    img = cv2.imread(imagePath)
    if img is None:
        raise FileNotFoundError(f"Cannot load '{imagePath}'")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ranges = {
        'outline': ([130, 80, 80], [170, 255, 255]),
        'fairway': ([10, 100, 100], [25, 255, 255]),
        'teebox1': ([0, 100, 100], [10, 255, 255]),
        'teebox2': ([170, 100, 100], [180, 255, 255]),
        'sandtrap': ([130, 50, 50], [155, 255, 255]),
        'green': ([90, 100, 100], [120, 255, 255])
    }

    masks = {}
    for key, (low, high) in ranges.items():
        masks[key] = cv2.inRange(hsv, np.array(low), np.array(high))
    masks['teebox'] = masks.pop('teebox1') | masks.pop('teebox2')

    origW, origH = img.shape[1], img.shape[0]
    canvasW, canvasH = 2000, 1200

    return {
        'outline': [
            scaleAndCenterPoints(c, origW, origH, canvasW, canvasH)
            for c in getAllContours(masks['outline'])
        ],
        'fairway': [
            scaleAndCenterPoints(getContourPoints(masks['fairway']),
                                 origW, origH, canvasW, canvasH)
        ],
        'teebox': [
            scaleAndCenterPoints(getContourPoints(masks['teebox']),
                                 origW, origH, canvasW, canvasH)
        ],
        'green': [
            scaleAndCenterPoints(getContourPoints(masks['green']),
                                 origW, origH, canvasW, canvasH)
        ],
        'sandtrap': [
            scaleAndCenterPoints(c, origW, origH, canvasW, canvasH)
            for c in getAllContours(masks['sandtrap'])
        ]
    }
