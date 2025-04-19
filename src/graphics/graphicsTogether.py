from cmu_graphics import *
import sprites 

def onAppStart(app):
    app.startPage = True 
    app.hole1 = False


def reDrawAll (app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawHole1(app)

def drawHole1(app):
    pass


def drawStart(app):
    drawRect()

def onStep(app):
    pass


# def onMousePress(app, mouseX, mouseY):
#     if pressPlay(app, mouseX, mouseY):
#         app.startPage 