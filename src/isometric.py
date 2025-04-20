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