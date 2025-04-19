from cmu_graphics import *

def redrawAll(app):
    drawRect(0, 0, 100, 100, fill='red')

runApp(redrawAll=redrawAll)
cmu_graphics.run()
