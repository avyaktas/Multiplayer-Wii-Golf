from cmu_graphics import *


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

def reDrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawHole1(app)

def drawHole1(app):
    # Clear the background
    drawRect(0, 0, app.width, app.height, fill='forestGreen')
    drawLabel('Hole 1', app.width//2, 50, size=30, fill='white')

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
