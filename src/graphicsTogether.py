from cmu_graphics import *
from holeSketch import getHoleOutlines
from physics import calculateVelocity
import math

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5


def onAppStart(app):
    # Initialize the app
    app.startPage = True 
    app.hole1 = False
    app.cardPage = False
    app.width = 1000
    app.height = 600
    app.scrollX = 500
    app.scrollY = 650
    app.courseWidth = 3000
    app.courseHeight = 1800
    app.cardButtonX = 30 
    app.cardButtonY = 30
    app.cardButtonWidth = 100
    app.cardButtonHeight = 30
    app.holeButtonX = app.cardButtonX
    app.holeButtonY = app.cardButtonY
    app.holeButtonWidth = app.cardButtonWidth
    app.holeButtonHeight = app.cardButtonHeight
    
    # Ball state remains the same
    app.ballStartX = 100
    app.ballStartY = 615
    app.ballX = 100
    app.ballY = 615
    app.shadowY = 615
    app.ballZ = 0
    app.ballVelocityX = 0
    app.ballVelocityY = 0
    app.ballVelocityZ = 0
    app.gravity = 9.81
    app.ballInMotion = False
    app.ballRadius = 3
    app.onTeebox = False
    app.clubs = ['driver', 'wood', 'iron', 'wedge', 'putter']
    app.clubIndex = 0
    app.selectedClub = app.clubs[0]
    app.targetX, app.targetY = findHoleCenter()
    app.aimAngle = math.atan2(app.targetY - app.ballY, app.targetX - app.ballX)
    app.stepsPerSecond = 10
    app.scores = [
        ['Par', 4, 3, 5, 4, 4, 3, 5, 4, 4, 36, 72],
        ['Player 1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 2', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 4', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ]

    app.score = 0 

    oceanStart(app)
def oceanStart(app):
    app.frames = ["15112-ocean0.jpg", "15112-ocean1.jpg"]
    app.currentFrameIndex = 0
    app.tileWidth = 500  # Width of each tile
    app.tileHeight = 500  # Height of each tile
    app.offsetX = 0  # Horizontal offset for wave movement
    app.offsetY = 0  # Vertical offset for wave movement
    app.offsetSpeed = 5  # Speed of the diagonal movement
    app.count = 0


def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawOcean(app)
        # drawCliff(app)
        drawHole1(app)
        drawBall(app)
        if not app.ballInMotion:
            drawAimLine(app)  # Draw the ball in every frame
            drawClubSelection(app)
        drawAimLine(app)
        drawBall(app)  # Draw the ball in every frame
        drawCardButton(app)
    elif app.cardPage:
        drawCardPage(app)
        drawHoleButton(app)
        
def drawOcean(app):
    # Display the current frame in tiled chunks
    currentFrame = app.frames[app.currentFrameIndex]
    for x in range(-app.tileWidth, app.width, app.tileWidth):
        for y in range(-app.tileHeight, app.height, app.tileHeight):
            drawImage(currentFrame, x+app.offsetX, y+app.offsetY, 
                      width=app.tileWidth, height=app.tileHeight)

# def drawCliff(app):
#     # Dynamically calculate the cliff's position and size
#     cliffHeight = app.height * 0.2  # Cliff height as 20% of the screen height
#     bottomLeftX, bottomLeftY = getScreenCoords(app, -app.tileWidth, app.height)
#     bottomRightX, bottomRightY = getScreenCoords(app, app.width + app.tileWidth, app.height)
#     topRightX, topRightY = getScreenCoords(app, app.width + app.tileWidth, app.height - cliffHeight)
#     topLeftX, topLeftY = getScreenCoords(app, 0, app.height - cliffHeight)
#     cliffPoints = [
#         (bottomLeftX, bottomLeftY),
#         (bottomRightX, bottomRightY),
#         (topRightX, topRightY),
#         (topLeftX, topLeftY)
#     ]
#     drawPolygon(*flatten(cliffPoints), fill='saddlebrown', border='black')

def getScreenCoords(app, x, y):
    screenX = x - app.scrollX + app.width / 2
    screenY = y - app.scrollY + app.height / 3
    return screenX, screenY

def getHoleData():
    imagePath = 'Hole.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines

#used chatGPT for the flatten function

def flatten(points):
    return [coord for point in points for coord in point]

def drawHole1(app):
    outlines = getHoleData()

    #Used chatGPT to help with the drawCoursePolygon function
    def drawCoursePolygon(app, poly, fill, border): 
        shifted = []
        for (x, y) in poly:
            screenX, screenY = getScreenCoords(app, x, y)
            shifted.append((screenX, screenY))
        flattenedCoords = []
        for point in shifted:
            flattenedCoords.append(point[0])
            flattenedCoords.append(point[1])
        drawPolygon(*flattenedCoords, fill=fill, border=border)
    
    def drawPolygons(app, polygons, fill, border='None'):
        for poly in polygons:
            drawCoursePolygon(app, poly, fill, border)

    # Draw course features in 2D
    if 'outline' in outlines:
        drawPolygons(app, outlines['outline'], fill='forestGreen', border='black')
    drawPolygons(app, outlines['fairway'], fill='green', border=None)
    drawPolygons(app, outlines['sandtrap'], fill='tan', border='black')
    drawPolygons(app, outlines['green'], fill='forestGreen', border='black')
    drawPolygons(app, outlines['teebox'], fill='forestGreen', border='black')
    
    # Draw hole and flag in 2D
    if 'green' in outlines:
        for green in outlines['green']:
            if isinstance(green, list):
                points = green
            elif isinstance(green, dict) and 'points' in green:
                points = green['points']
            else:
                continue

            centerX, centerY = getHole(points)
            screenX, screenY = getScreenCoords(app, centerX, centerY)

            # Draw hole
            drawCircle(screenX, screenY, 4, fill='black', border='white')
            
            # Draw flag
            drawLine(screenX, screenY, screenX, screenY - 25, fill='white', lineWidth=2)
            drawPolygon(screenX, screenY - 15, 
                       screenX - 15, screenY - 20,
                       screenX, screenY - 25,
                       fill='red', border='black')

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
    # Draw background image scaled to fill the screen
    drawImage("titleScreen.png", 0, 0, width=app.width, height=app.height)
    
    # Draw title
    titleX = app.width // 2
    titleY = app.height // 6
    baseFontSize = 75
    factor = min(app.width / 1000, app.height / 600)
    titleFontSize = int(baseFontSize * factor)

    drawLabel('Wii Golf 112', titleX-7, titleY-3, 
             size=titleFontSize, fill='black', font='impact')
    drawLabel('Wii Golf 112', titleX, titleY,
             size=titleFontSize, fill='cornSilk', font='impact')
    
    # Calculate scaling factor
    factor = min(app.width / 1000, app.height / 600)

    # Adjust play button dimensions and position
    playButtonWidth = int(400 * factor)
    playButtonHeight = int(50 * factor)
    playButtonX = app.width // 2
    playButtonY = int(app.height // 1.3)

    # Draw play button
    color = gradient('darkGreen', 'lightGreen')
    drawRect(playButtonX - playButtonWidth // 2,
             playButtonY - playButtonHeight // 2,
             playButtonWidth, playButtonHeight,
             fill=color, border='cornSilk', borderWidth=3)
    drawLabel('Press the here to begin', playButtonX-2.5, playButtonY-2,
              size=int(30 * factor), fill='black', bold=True, font='impact')
    drawLabel('Press the here to begin', playButtonX, playButtonY,
              size=int(30 * factor), fill='cornSilk', font='impact')

def getPlayButtonCoord(app):
    playButtonX = app.width // 2
    playButtonY = int(app.height // 1.3)
    return (playButtonX, playButtonY)

def getPlayButtonSize(app):
    factor = min(app.width / 1000, app.height / 600)
    playButtonWidth = int(400 * factor)
    playButtonHeight = int(50 * factor)
    return (playButtonWidth, playButtonHeight)

def isInPlayButton(app, x, y):
    playButtonX, playButtonY = getPlayButtonCoord(app)
    playButtonWidth, playButtonHeight = getPlayButtonSize(app)
    return (playButtonX - playButtonWidth // 2 <= x <= 
            playButtonX + playButtonWidth // 2 and
            playButtonY - playButtonHeight // 2 <= y <= 
            playButtonY + playButtonHeight // 2)

def isInCardButton(app, x, y): 
    return (app.cardButtonX <= x <= app.cardButtonX + app.cardButtonWidth and
            app.cardButtonY <= y <= app.cardButtonY + app.cardButtonHeight)

def isInHoleButton(app, x, y):
    return (app.holeButtonX <= x <= app.holeButtonX + app.holeButtonWidth and
            app.holeButtonY <= y <= app.holeButtonY + app.holeButtonHeight)


def onMousePress(app, mouseX, mouseY):
    if app.startPage and isInPlayButton(app, mouseX, mouseY):
        app.startPage = False
        app.hole1 = True
        app.onTeebox = True 
        app.showClubSelection = True
    elif app.hole1 and isInCardButton(app, mouseX, mouseY):
        app.hole1 = False
        app.cardPage = True
    elif app.cardPage and isInHoleButton(app, mouseX, mouseY): 
        app.cardPage = False
        app.hole1 = True

def onKeyHold(app, keys): 
    move = 20
    if 'left' in keys: app.scrollX -= move
    if 'right' in keys: app.scrollX += move
    if 'up' in keys: app.scrollY -= move
    if 'down' in keys: app.scrollY += move

    app.scrollX = max(0, min(app.scrollX, app.courseWidth - app.width))
    app.scrollY = max(0, min(app.scrollY, app.courseHeight - app.height))

def takeShot(app, velocity, angle):
    # Set initial ball position to teebox location
    # These values should match your teebox position
    # Set initial velocities  # 45 degree launch angle
    app.ballVelocityZ = velocity * math.sin(angle)
    flatVelocity = velocity * math.cos(angle)
    app.ballVelocityX = flatVelocity * math.cos(app.aimAngle)
    app.ballVelocityY = flatVelocity * math.sin(app.aimAngle)
    
    app.ballInMotion = True
    app.onTeebox = False
    app.score += 1 

def onStep(app):
    app.count += 1
    if app.ballInMotion:
        step = (1/app.stepsPerSecond)
        app.ballX += app.ballVelocityX * step
        app.ballY = app.ballY - (app.ballVelocityZ * step) - (app.ballVelocityY * step)
        app.ballZ += app.ballVelocityZ * step
        app.shadowX = app.ballX
        app.shadowY -= app.ballVelocityY * step
        
        # Apply gravity to Z velocity
        app.ballVelocityZ -= (app.gravity * step)
        app.scrollX += app.ballVelocityX * step
        app.scrollY -= app.ballVelocityZ * step
        # Check if ball has landed
        if app.ballZ <= 0 and app.ballVelocityZ < 0:
            app.ballZ = 0
            app.ballInMotion = False
            app.ballVelocityZ = 0 
            app.aimAngle = math.atan2(app.targetY - app.ballY,
                              app.targetX - app.ballX)
    if not app.ballInMotion:
        app.ballVelocityX = 0
        app.ballVelocityY = 0 
        holeX, holeY = findHoleCenter()
        if distance(app.ballX, app.ballY, holeX, holeY) <= app.ballRadius:
            app.cardPage = True 
    # Draws the ocean
    if not app.startPage:
        if app.count % 5 == 0: # Only updates every 5 steps
            app.currentFrameIndex = (app.currentFrameIndex + 1) % len(app.frames)
            app.offsetX = (app.offsetX + app.offsetSpeed) % app.tileWidth
            app.offsetY = (app.offsetY + app.offsetSpeed) % app.tileHeight
    



def drawBall(app):
    if app.ballInMotion:
        shadowX, shadowY = getScreenCoords(app, app.ballX, app.shadowY)
        drawCircle(shadowX, shadowY, app.ballRadius, fill='black', opacity = 60)
    screenX, screenY = getScreenCoords(app, app.ballX, app.ballY)
    drawCircle(screenX, screenY, app.ballRadius, fill='white')
    

def onKeyPress(app, key):
    if not app.ballInMotion:
        if key == 'w':
            app.clubIndex = (app.clubIndex - 1) % len(app.clubs)
            app.selectedClub = app.clubs[app.clubIndex]
        elif key == 's':
            app.clubIndex = (app.clubIndex + 1) % len(app.clubs)
            app.selectedClub = app.clubs[app.clubIndex]
        if key == 'a':                # turn left
            app.aimAngle -= math.radians(3)
        elif key == 'd':              # turn right
            app.aimAngle += math.radians(3)
        if key == 'space':
                app.showClubSelection = False
                velocity, angle, aimDeviation = calculateVelocity(app.selectedClub)
                app.aimAngle += aimDeviation
                takeShot(app, velocity, angle)
                app.ballInMotion = True


def drawAimLine(app):
    if not app.ballInMotion:
        sx, sy = getScreenCoords(app, app.ballX, app.ballY)
        length = 60
        ex = sx + length * math.cos(app.aimAngle)
        ey = sy + length * math.sin(app.aimAngle)
        drawLine(sx, sy, ex, ey, fill='white', lineWidth=2)

def findHoleCenter():
    """
    Reads outlines with getHoleOutlines, grabs the first green polygon,
    and returns its centroid.
    """
    outlines = getHoleOutlines('Hole.jpg')
    greens   = outlines.get('green', [])
    if not greens:
        return 0, 0
    # handle dict vs list for outlines
    first = greens[0]
    pts = first['points'] if isinstance(first, dict) else first
    # compute centroid
    cx = sum(x for x,y in pts) / len(pts)
    cy = sum(y for x,y in pts) / len(pts)
    return cx, cy


def drawClubSelection(app):

    # Draw semi-transparent background panel
    menuX = 20  # Position menu on right side
    menuY = app.height - 300  # Position from top
    menuWidth = 180
    menuHeight = 270
    lineHeight = 28
    topOffset = 50
    # menuX, menuY = getScreenCoords(app, menuX, menuY)
    
    # Draw main menu panel
    drawRect(menuX + 5, menuY + 5, menuWidth - 10, menuHeight, 
            fill='white', opacity=80)
    
    # Draw title
    drawLabel('Club Selection', 
                menuX + menuWidth//2, menuY + 30, 
                size=16, bold=True, fill='black')
    
    
    
    # Draw club options
    for i, club in enumerate(app.clubs):
        # Highlight selected club
        if i == app.clubIndex:
            # Draw highlight background
            drawRect(menuX + 10, 
                    menuY + topOffset + i* lineHeight,  # Vertical spacing
                    160, 30,  # Size of highlight
                    fill='lightGreen')
            textColor = 'darkGreen'
        else:
            textColor = 'black'
        
        # Draw club name
        drawLabel(club.title(),  # Capitalize club name
                    menuX + menuWidth//2, 
                    menuY + 60 + i*30,  # Vertical spacing
                    fill=textColor)
    
    # Draw instructions at bottom
    drawLabel('w,s to select', 
                menuX + menuWidth//2, 
                menuY + menuHeight - 30,
                size=12)
    drawLabel('SPACE to confirm', 
                menuX + menuWidth//2, 
                menuY + menuHeight - 10,
                size=12)
    
    # Draw club stats (optional)
    # if app.selectedClub:
    #     # Power meter
    #     powerBarWidth = menuWidth - 40
    #     powerBarHeight = 10
    #     powerBarX = menuX + 20
    #     powerTextY = menuY + topOffset + len(app.clubs) * lineHeight + 10
    #     powerBarY = powerTextY + 15
    #     powerWidth = menuWidth - 40
        
    #     # Club power values (0-100)
    #     clubPower = {
    #         'driver': 100,
    #         'wood': 80,
    #         'iron': 60,
    #         'wedge': 40,
    #         'putter': 20
    #     }
        
    #     # Draw power bar background
    #     drawRect(powerBarX, powerBarY, powerBarWidth, powerBarHeight, 
    #             fill='lightGray')
        
    #     # Draw power level
    #     power = clubPower.get(app.selectedClub, 0)
    #     drawRect(powerBarX, powerBarY, 
    #             powerBarWidth * (power/100), powerBarHeight,
    #             fill='green')
        
    #     # Draw power label
    #     drawLabel(f'Power: {power}%',
    #                 menuX + menuWidth//2,
    #                 powerBarY - 10,
    #                 size=12)
            
def drawCardButton(app): 
    if app.hole1:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='white', border='black', borderWidth=2,
                opacity = 80)
        
        drawLabel('Card', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=16, fill='black', bold=True)
        
def drawHoleButton(app): 
    if app.cardPage:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='white', border='black', borderWidth=2,
                opacity = 80)
        
        drawLabel('Hole', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=16, fill='black', bold=True)
        
def drawCardPage(app): 
    drawRect(0, 0, app.width, app.height, fill = 'green')
    cardTopX = 50
    cardTopY = 180
    cardColWidth = 75
    cardRowHeight = 60

    rows, cols = len(app.scores), len(app.scores[0])
    
    holeLabels = [''] + [str(i+1) for i in range(9)] + ['OUT', 'TOTAL']
    for col in range(cols):
        x = cardTopX + col * cardColWidth
        drawRect(x, cardTopY - cardRowHeight, cardColWidth, cardRowHeight, fill='gray', border='black')
        drawLabel(holeLabels[col], x + cardColWidth//2, cardTopY - cardRowHeight//2, size=14, bold=True, fill='white')
        drawRect(cardTopX, cardTopY, 
            cardColWidth * cols, cardRowHeight * rows,
            fill='white', border='black', borderWidth=2)
    
    for row in range(rows):
        for col in range(cols): 
            x = cardTopX + col * cardColWidth
            y = cardTopY + row * cardRowHeight
            drawRect(x, y, cardColWidth, cardRowHeight,
                    fill='white', border='black', borderWidth=2)
            drawLabel(str(app.scores[row][col]), 
                    x + cardColWidth//2, y + cardRowHeight//2,
                    size=16, fill='black', bold=True)
            
    drawLabel('112 Country Club Front 9', app.width//2, 80, size = 30, 
              bold = True, fill = 'white')
                     

    

runApp()

