from cmu_graphics import *
from holeSketch import getHoleOutlines

def onAppStart(app):
    app.startPage = True 
    app.hole1 = False
    app.width = 1000
    app.height = 600
    app.scrollX = 0
    app.scrollY = 0
    app.courseWidth = 2000
    app.courseHeight = 1200
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
    imagePath = 'Hole.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines

def flatten(points):
    return [coord for point in points for coord in point]

def drawHole1(app):
    outlines = getHoleData()
    print(outlines)

    def drawCoursePolygon(app, poly, fill, border): 
        shifted = [(x - app.scrollX, y- app.scrollY) for (x, y) in poly]
        drawPolygon(*flatten(shifted), fill = fill, border = border)
    
    def drawPolygons(app, polygons, fill, border=None):
        for poly in polygons:
            drawCoursePolygon(app, poly, fill, border)

    if 'outline' in outlines: 
        drawPolygons(app, outlines['outline'], fill = 'green', border = 'white')
    
    drawPolygons(app, outlines['fairway'], fill='limeGreen', border = None)
    drawPolygons(app, outlines['sandtrap'], fill='tan', border = None)
    drawPolygons(app, outlines['green'], fill='lightGreen', border = None)
    drawPolygons(app, outlines['teebox'], fill='lightGreen', border = None)
    if 'hole' in outlines:
        drawPolygons(app, outlines['hole'], fill=None, border='white')


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

def onKeyHold(app, keys): 
    move = 10
    if 'left' in keys: app.scrollX -= move
    if 'right' in keys: app.scrollX += move
    if 'up' in keys: app.scrollY -= move
    if 'down' in keys: app.scrollY += move

    app.scrollX = max(0, min(app.scrollX, app.courseWidth - app.width))
    app.scrollY = max(0, min(app.scrollY, app.courseHeight - app.height))



runApp()

