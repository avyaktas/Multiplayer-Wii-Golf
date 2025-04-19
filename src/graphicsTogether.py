from cmu_graphics import *
from holeSketch import getHoleOutlines

def onAppStart(app):
    app.startPage = True 
    app.hole1 = False
    app.width = 800
    app.height = 600
    # Play button dimensions
    app.playButtonX = app.width // 2
    app.playButtonY = app.height // 2
    app.playButtonWidth = 200
    app.playButtonHeight = 60

def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawHole1(app)

def getHoleData():
    imagePath = 'google earth.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines


def drawHole1(app):
    # Get the hole outlines
    outlines = getHoleData()
    
    # Draw each feature in order (bottom to top layer)
    if outlines['fairway']:
        drawPolygon(*outlines['fairway'], fill='lightGreen')
    
    if outlines['sandtrap']:
        drawPolygon(*outlines['sandtrap'], fill='tan')
    
    if outlines['green']:
        drawPolygon(*outlines['green'], fill='green')
    
    if outlines['teebox']:
        drawPolygon(*outlines['teebox'], fill='darkGreen')
    
    # Draw hole outline last to ensure it's visible
    if outlines['hole']:
        drawPolygon(*outlines['hole'], fill=None, border='white')


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


def isInPlayButton(app, x, y):
    return (abs(x - app.playButtonX) <= app.playButtonWidth//2 and
            abs(y - app.playButtonY) <= app.playButtonHeight//2)

def onMousePress(app, mouseX, mouseY):
    if app.startPage and isInPlayButton(app, mouseX, mouseY):
        app.startPage = False
        app.hole1 = True

runApp()

