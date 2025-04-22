from cmu_graphics import *

def onAppStart(app):
    app.frames = ["15112-ocean0.jpg", "15112-ocean1.jpg"]
    app.currentFrameIndex = 0
    app.stepsPerSecond = 2
    app.tileWidth = 200  # Width of each tile
    app.tileHeight = 200  # Height of each tile
    app.offsetX = 0  # Horizontal offset for wave movement
    app.offsetY = 0  # Vertical offset for wave movement
    app.offsetSpeed = 5  # Speed of the diagonal movement

def onStep(app):
    # Alternate between the frames
    app.currentFrameIndex = (app.currentFrameIndex + 1) % len(app.frames)
    
    # Update the offsets to create diagonal movement
    app.offsetX = (app.offsetX + app.offsetSpeed) % app.tileWidth
    app.offsetY = (app.offsetY + app.offsetSpeed) % app.tileHeight

def redrawAll(app):
    # Display the current frame in tiled chunks with offsets
    currentFrame = app.frames[app.currentFrameIndex]
    for x in range(-app.tileWidth, app.width, app.tileWidth):
        for y in range(-app.tileHeight, app.height, app.tileHeight):
            drawImage(currentFrame, x + app.offsetX, y + app.offsetY, 
                      width=app.tileWidth, height=app.tileHeight)

runApp()