from cmu_graphics import *

def onAppStart(app):
    app.frames = ["15112-ocean0.jpg", "15112-ocean1.jpg"]
    app.currentFrameIndex = 0
    app.stepsPerSecond = 2
    app.tileWidth = 200  # Width of each tile
    app.tileHeight = 200  # Height of each tile

def onStep(app):
    # Alternate between the frames
    app.currentFrameIndex = (app.currentFrameIndex + 1) % len(app.frames)

def redrawAll(app):
    # Display the current frame in tiled chunks
    currentFrame = app.frames[app.currentFrameIndex]
    for x in range(0, app.width, app.tileWidth):
        for y in range(0, app.height, app.tileHeight):
            drawImage(currentFrame, x, y, width=app.tileWidth, height=app.tileHeight)

runApp()