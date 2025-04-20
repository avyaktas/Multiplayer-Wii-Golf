from cmu_graphics import *
from holeSketch import getHoleOutlines
from physics import calculateVelocity
import math

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5

def getClubPower(club):
    """
    Returns the power of the club.
    """
    clubPower = {
        'driver': 100,
        'wood': 80,
        'iron': 60,
        'wedge': 40,
        'putter': 20
    }
    return clubPower.get(club, 0)

def onAppStart(app):
    app.startPage = True 
    app.hole1 = False
    app.cardPage = False
    app.width = 1000
    app.height = 600
    app.scrollX = 500
    app.scrollY = 650
    app.courseWidth = 3000
    app.courseHeight = 1800
    # Play button dimensions
    app.playButtonX = app.width // 2
    app.playButtonY = app.height // 2
    app.playButtonWidth = 200
    app.playButtonHeight = 60
    app.cardButtonX = 30 
    app.cardButtonY = 30
    app.cardButtonWidth = 100
    app.cardButtonHeight = 30
    app.holeButtonX = app.cardButtonX
    app.holeButtonY = app.cardButtonY
    app.holeButtonWidth = app.cardButtonWidth
    app.holeButtonHeight = app.cardButtonHeight
    
    # Ball state remains the same
    app.ballX = 100
    app.ballY = 615
    app.ballZ = 0
    app.ballVelocityX = 0
    app.ballVelocityY = 0
    app.ballVelocityZ = 0
    app.gravity = 9.81
    app.timeStep = 0.1
    app.ballInMotion = False
    app.ballRadius = 3
    app.onTeebox = False
    app.clubs = ['driver', 'wood', 'iron', 'wedge', 'putter']
    app.clubIndex = 0
    app.selectedClub = app.clubs[0]

    app.targetX, app.targetY = findHoleCenter()
    app.aimAngle = math.atan2(app.targetY - app.ballY,
                              app.targetX - app.ballX)
    app.stepsPerSecond = 10

def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.hole1:
        drawCliff(app)
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
        



def getScreenCoords(app, x, y):
    screenX = x - app.scrollX + app.width / 2
    screenY = y - app.scrollY + app.height / 3
    return screenX, screenY

def getHoleData():
    imagePath = 'Hole.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines

def flatten(points):
    return [coord for point in points for coord in point]

def drawHole1(app):
    drawRect(0, 0, app.width, app.height, fill='darkBlue')
    outlines = getHoleData()

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
    cliffPoints = [
        (0, 0), (app.courseWidth, 0), 
        (app.courseWidth, app.courseHeight), 
        (0, app.courseHeight)
    ]
    screenPoints = [getScreenCoords(app, x, y) for x, y in cliffPoints]
    drawPolygon(
        *flatten(screenPoints),
        fill='tan', border='black', borderWidth=2
    )
    
def isInPlayButton(app, x, y):
    return (abs(x - app.playButtonX) <= app.playButtonWidth//2 and
            abs(y - app.playButtonY) <= app.playButtonHeight//2)

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
    app.ballVelocityX = velocity * math.cos(app.aimAngle)
    app.ballVelocityY = velocity * math.sin(app.aimAngle)
    app.ballVelocityZ = velocity * math.sin(angle)
    
    app.ballInMotion = True
    app.onTeebox = False

def onStep(app):
    if app.ballInMotion:
        step = (1/app.stepsPerSecond)
        app.ballX += app.ballVelocityX * step
        app.ballY += app.ballVelocityY * step
        app.ballZ += app.ballVelocityZ * step
        
        # Apply gravity to Z velocity
        app.ballVelocityZ -= app.gravity * app.timeStep
        
        # Check if ball has landed
        if app.ballZ <= 0 and app.ballVelocityZ < 0:
            app.ballZ = 0
            app.ballInMotion = False
            app.aimAngle = math.atan2(app.targetY - app.ballY,
                              app.targetX - app.ballX)


def drawBall(app):

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
                app.ballInMotion = True
                app.showClubSelection = False
                takeShot(app, 100, 45)


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
    if app.showClubSelection:
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
        if app.selectedClub:
            # Power meter
            powerBarWidth = menuWidth - 40
            powerBarHeight = 10
            powerBarX = menuX + 20
            powerTextY = menuY + topOffset + len(app.clubs) * lineHeight + 10
            powerBarY = powerTextY + 15
            powerWidth = menuWidth - 40
            
            # Club power values (0-100)
            clubPower = {
                'driver': 100,
                'wood': 80,
                'iron': 60,
                'wedge': 40,
                'putter': 20
            }
            
            # Draw power bar background
            drawRect(powerBarX, powerBarY, powerBarWidth, powerBarHeight, 
                    fill='lightGray')
            
            # Draw power level
            power = clubPower.get(app.selectedClub, 0)
            drawRect(powerBarX, powerBarY, 
                    powerBarWidth * (power/100), powerBarHeight,
                    fill='green')
            
            # Draw power label
            drawLabel(f'Power: {power}%',
                     menuX + menuWidth//2,
                     powerBarY - 10,
                     size=12)
            
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
    cardTopY = 80
    cardWidth = 900
    cardHeight = 470
    drawRect(cardTopX, cardTopY, cardWidth, cardHeight,
            fill='white', border='black', borderWidth=2)
    for i in range(6): 
        drawLine(cardTopX, cardTopY + i * 80,
                cardTopX + cardWidth, cardTopY + i * 80,
                fill='black', lineWidth=2)
        
    for i in range(18): 
        drawLine(cardTopX + i * 50, cardTopY,
                cardTopX + i * 50, cardTopY + cardHeight,
                fill='black', lineWidth=2)  


runApp()

