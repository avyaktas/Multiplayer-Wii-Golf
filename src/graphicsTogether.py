from cmu_graphics import *
from holeSketch import getHoleOutlines
import math

def onAppStart(app):
    app.startPage = True 
    app.hole1 = False
    app.width = 1000
    app.height = 600
    app.scrollX = 0
    app.scrollY = 0
    app.courseWidth = 3000
    app.courseHeight = 1800
    # Play button dimensions
    app.playButtonX = app.width // 2
    app.playButtonY = app.height // 2
    app.playButtonWidth = 200
    app.playButtonHeight = 60
    # all isometric view logic
    app.zoom = 1.0
    angle = math.radians(30)
    app.cos30 = math.cos(angle)
    app.sin30 = math.sin(angle)

def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawCliff(app)
        drawHole1(app)
    x, y = getIsometric(app, 100, 100)

def getIsometric(app, x, y, z=0):
    xWorld = x - app.scrollX
    yWorld = y - app.scrollY
    isoX = (xWorld - yWorld) * app.cos30
    isoY = (xWorld + yWorld) * app.sin30 - z
    #zoom logic
    isoX *= app.zoom
    isoY *= app.zoom
    # centering logic
    displayX = isoX + app.width / 2
    displayY = isoY + app.height / 3
    return displayX, displayY

def getHoleData():
    imagePath = 'Hole.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines

def flatten(points):
    return [coord for point in points for coord in point]

def drawHole1(app):
    drawRect(0,0, app.width, app.height, fill = 'darkBlue')
    outlines = getHoleData()
    print(outlines) #maybe should remove this line it is not doing anything

    def drawCoursePolygon(app, poly, fill, border, z=0): 
        shifted = []
        for (x, y) in poly:
            isoX, isoY = getIsometric(app, x, y, z)
            shifted.append((isoX, isoY))
        flattenedCoords = []
        for point in shifted:
            flattenedCoords.append(point[0])
            flattenedCoords.append(point[1])
        drawPolygon(*flattenedCoords, fill = fill, border = border)
    
    def drawPolygons(app, polygons, fill, border='None', z=0):
        for poly in polygons:
            drawCoursePolygon(app, poly, fill, border, z)

    if 'outline' in outlines: 
        drawPolygons(app, outlines['outline'], 
                     fill = 'forestGreen', border='black', z=0)
    drawPolygons(app, outlines['fairway'], fill='green', 
                 border = None, z=2)
    drawPolygons(app, outlines['sandtrap'], fill='tan', 
                 border = 'black', z=-1)
    drawPolygons(app, outlines['green'], fill='forestGreen', 
                 border = 'black', z=4)
    drawPolygons(app, outlines['teebox'], fill='forestGreen', 
                 border='black', z=5)
    if 'hole' in outlines:
        drawPolygons(app, outlines['hole'], fill='black', 
                     border='black', z=6)
    if 'green' in outlines:
        for green in outlines['green']:
            # Check if green is a list of points directly
            if isinstance(green, list):
                points = green  # Treat green as the list of points
            elif isinstance(green, dict) and 'points' in green:
                points = green['points']  # Extract points from the dictionary
            else:
                print("Error: Invalid green structure:", green)
                continue

            # Get the center of the green polygon in world coordinates
            centerX, centerY = getHole(points)

            # Transform the center to screen coordinates using getIsometric
            screenX, screenY = getIsometric(app, centerX, centerY)

            # Draws the actual golf hole on the green
            drawOval(screenX, screenY, 8.5, 7, fill='black', border='white', 
                     borderWidth=1)
            # Draws the flagpole
            drawLine(screenX, screenY, screenX, screenY - 25, 
                     fill='white', lineWidth=2)
            
            # Draws the flag
            flagTipX = screenX - 5
            flagBottomX = screenX
            flagBottomY = screenY - 25 + 10
            flagTopY = screenY - 25
            drawPolygon(flagBottomX, flagBottomY, flagTipX-10, flagTopY+5, 
                        screenX, screenY - 25, fill='red', border='black',
                        borderWidth=1.25)

def getHole(points):
    """
    Calculates the center of a polygon.
    """
    # Calculate the center of the polygon
    centerX = sum(x for x, y in points) / len(points)
    centerY = sum(y for x, y in points) / len(points)
    
    # Return the center as a tuple
    return centerX, centerY


def drawStart(app):
    # Draw background
    drawRect(0, 0, app.width, app.height, fill='darkGreen')
    
    # Draw title
    drawLabel('Wii Golf 112', app.width//2, 150, 
             size=50, fill='white', bold=True)
    
    # Draw play button
    drawRect(app.playButtonX - app.playButtonWidth//2,
            app.playButtonY - app.playButtonHeight//2,
            app.playButtonWidth, app.playButtonHeight,
            fill='lightGreen', border='white', borderWidth=3)
    
    drawLabel('PLAY', app.playButtonX, app.playButtonY,
             size=30, fill='white', bold=True)


def drawCliff(app):
    """
    Draws a cliff edge around the border of the island.
    """
    # Define the points for the cliff edge (example: a rectangle around the island)
def drawCliff(app):
    cliffPoints = [
        (0, 0), (app.courseWidth, 0), (app.courseWidth, app.courseHeight), 
        (0, app.courseHeight)]
    isoPoints = [getIsometric(app, x, y) for x, y in cliffPoints]
    drawPolygon(
        *flatten(isoPoints),
        fill='tan', border='black', borderWidth=2)
    
def isInPlayButton(app, x, y):
    return (abs(x - app.playButtonX) <= app.playButtonWidth//2 and
            abs(y - app.playButtonY) <= app.playButtonHeight//2)

def onMousePress(app, mouseX, mouseY):
    if app.startPage and isInPlayButton(app, mouseX, mouseY):
        app.startPage = False
        app.hole1 = True

def onKeyHold(app, keys): 
    move = 20
    if 'left' in keys: app.scrollX -= move
    if 'right' in keys: app.scrollX += move
    if 'up' in keys: app.scrollY -= move
    if 'down' in keys: app.scrollY += move

    app.scrollX = max(0, min(app.scrollX, app.courseWidth - app.width))
    app.scrollY = max(0, min(app.scrollY, app.courseHeight - app.height))



runApp()

