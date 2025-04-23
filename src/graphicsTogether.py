from cmu_graphics import *
from holeSketch import getHoleOutlines
from physics import calculateVelocity
import math, random
from playerClass import Player



def onAppStart(app):
    # Initialize the app
    app.startPage = True 
    app.hole1 = False
    app.cardPage = False
    app.landingPage = False
    app.width = 1000
    app.height = 600
    app.scrollX = 500
    app.scrollY = 650
    app.courseWidth = 3000
    app.courseHeight = 1800
    app.cardButtonX = 20 
    app.cardButtonY = 20
    app.cardButtonWidth = 140
    app.cardButtonHeight = 40
    app.holeButtonX = app.cardButtonX
    app.holeButtonY = app.cardButtonY
    app.holeButtonWidth = app.cardButtonWidth
    app.holeButtonHeight = app.cardButtonHeight
    app.startButtonX = app.width//2 - 70
    app.startButtonY = app.height - 80
    app.startButtonWidth = 140
    app.startButtonHeight = 40
    app.nameIndex = 0
    app.ipAddress = ''
    app.ipBoxSelected = False
    app.nameBoxSelected = False
    app.selectedNumPlayers = 1
    app.playerNames = ['', '', '', '']
    app.currentHole = 6
    app.podium = False
    app.ballStarts = [(190,570), (90, 580), (160,620), (40,880), (120, 600),
                      (330, 620), (380, 638), (130, 615),(120, 670)]
    app.ballRadius = 3
    app.gravity = 9.81

    # build 4 players
    app.players = [
        Player(f"Player {i+1}", app.ballStarts[app.currentHole -1])
        for i in range(app.selectedNumPlayers)
    ]
    app.currentIdx = 0                  # which player's turn
    # give first player an initial aimAngle
    first = app.players[0]
    holeX, holeY = findHoleCenter(app)
    first.aimAngle = math.atan2(holeY - first.ballY, holeX - first.ballX)

    app.clubs = ['driver', 'wood', 'iron', 'wedge', 'putter']
    app.clubIndex = 0
    app.selectedClub = app.clubs[0]

    app.stepsPerSecond = 10
    app.scores = [
        ['Par', 4, 3, 5, 4, 4, 3, 5, 4, 4, 36, 72],
        ['Player 1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 2', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 4', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ]

    app.score = 0
    app.velocity = 0
    app.angle = 0
    app.putting = False
    app.rollingDeceleration = 3.0
    app.onGreen = False
    app.strokeCount = 0 
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
    

def drawCliff(app):
    outlines = getHoleData(app)['outline']
    for poly in outlines:
        # 1) build a jagged drop
        cliff = makeCliffBetter(poly, baseDepth=15, jag=1.5)
        # 2) draw the cliff face with a vertical rock‑tone gradient
        coords = []
        for (worldX, worldY) in cliff:
            screenX,screenY = getScreenCoords(app, worldX, worldY)
            coords += [screenX, screenY]
        color = gradient('cornsilk', 'saddleBrown', start='top')
        drawPolygon(*coords,
                    fill=color, border='black')
        # 3) rock‐strata lines
        for _ in range(12):
            i = random.randrange(len(poly))
            x,y = poly[i]
            depth = 15 + random.uniform(-5,5)
            sx1, sy1 = getScreenCoords(app, x, y)
            sx2, sy2 = getScreenCoords(app, x, y+depth)
            drawLine(sx1, sy1, sx2, sy2,
                     lineWidth=1, fill='darkSlateGray', opacity=50)

def makeCliffBetter(poly, baseDepth=20, jag=1):
    top = poly
    bottom = [(x, y + baseDepth + random.uniform(-jag, jag)) for (x,y) in poly]
    return top + bottom[::-1]  # top + bottom in reverse order

def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.landingPage:
        drawLandingPage(app)
    elif app.hole1:
        drawOcean(app)
        drawCliff(app)
        drawHole(app)
        drawBall(app)  # Only call once now, it handles everything
        
        current = app.players[app.currentIdx]
        if current.velX == 0 and current.velY == 0 and current.velZ == 0:
            drawAimLine(app)
            drawClubSelection(app)

        drawCardButton(app)

    elif app.cardPage:
        drawCardPage(app)
        drawHoleButton(app)
    # Draw the score card
        
def drawOcean(app):
    # Display the current frame in chunks
    currentFrame = app.frames[app.currentFrameIndex]
    for x in range(-app.tileWidth, app.width, app.tileWidth): 
        # X values loop
        for y in range(-app.tileHeight, app.height, app.tileHeight): 
            # Y values loop
            drawImage(currentFrame, x+app.offsetX, y+app.offsetY, 
                      width=app.tileWidth, height=app.tileHeight)

def getScreenCoords(app, x, y):
    screenX = x - app.scrollX + app.width / 2
    screenY = y - app.scrollY + app.height / 3
    return screenX, screenY

def getHoleData(app):
    if app.currentHole == 1:
        imagePath = 'Hole1.jpg'
    elif app.currentHole == 2:
        imagePath = 'Hole2.jpg'
    elif app.currentHole == 3:
        imagePath = 'Hole3.jpg'
    elif app.currentHole == 4:
        imagePath = 'Hole4.jpg'
    elif app.currentHole == 5:
        imagePath = 'Hole5.jpg'
    elif app.currentHole == 6:
        imagePath = 'Hole6.jpg'
    elif app.currentHole == 7:
        imagePath = 'Hole7.jpg'
    elif app.currentHole == 8:
        imagePath = 'Hole8.jpg'
    elif app.currentHole == 9:
        imagePath = 'Hole9.jpg'
    outlines = getHoleOutlines(imagePath)
    return outlines

def findAimAngle(app):
    app.targetX, app.targetY = findHoleCenter(app)
    return math.atan2(app.targetY - app.ballY, app.targetX - app.ballX)
#used chatGPT for the flatten function

def flatten(points):
    return [coord for point in points for coord in point]

def drawHole(app):
    outlines = getHoleData(app)

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
        drawPolygon(*flattenedCoords, fill=fill, border=border,
                    borderWidth=3.5)
    
    def drawPolygons(app, polygons, fill, border):
        for poly in polygons:
            drawCoursePolygon(app, poly, fill, border)

    # Draw course features in 2D
    if 'outline' in outlines:
        drawPolygons(app, outlines['outline'], 
                     fill='forestGreen', border='black')
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
    drawLabel('Press Here To Begin', playButtonX-2.5, playButtonY-2,
              size=int(30 * factor), fill='black', bold=True, font='Phosphate')
    drawLabel('Press Here To Begin', playButtonX, playButtonY,
              size=int(30 * factor), fill='cornSilk', font='Phosphate')

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

def isInStartButton(app, x, y):
    return (app.startButtonX <= x <= app.startButtonX + app.startButtonWidth and
            app.startButtonY <= y <= app.startButtonY + app.startButtonHeight)

def onMousePress(app, mouseX, mouseY):
    if app.startPage and isInPlayButton(app, mouseX, mouseY):
        app.startPage = False
        app.landingPage = True
    elif app.landingPage: 
        landingMousePress(app, mouseX, mouseY)
        if isInStartButton(app, mouseX, mouseY):
            app.landingPage = False
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
    
    player = app.players[app.currentIdx]
    if player.velX==0 and player.velY==0 and player.velZ==0:
        if 'a' in keys:
            player.aimAngle -= math.radians(3)
        if 'd' in keys:
            player.aimAngle += math.radians(3)

    app.scrollX = max(0, min(app.scrollX, app.courseWidth - app.width))
    app.scrollY = max(0, min(app.scrollY, app.courseHeight - app.height))

def takeShot(app, player, velocity, angle):
    # Set initial ball position to teebox location
    # These values should match your teebox position
    # Set initial velocities  # 45 degree launch angle
    if getBallTerrain(app) == 'green':
        player.putting = True
    player.velZ = velocity * math.sin(angle)
    flatVelocity = velocity * math.cos(angle)
    player.velX = flatVelocity * math.cos(player.aimAngle)
    player.velY = flatVelocity * math.sin(player.aimAngle)
    player.onTeebox = False
    player.strokes += 1

def takeBounce(app, player, velocity, angle):
    if getBallTerrain(app) == 'sandtrap':
        player.velX = player.velY = player.velZ = 0

    elif getBallTerrain(app) == 'out of bounds':
        player.strokes += 1
        player.ballX, player.ballY = player.shadowOverLandX, player.shadowOverLandY
    elif getBallTerrain(app) == 'rough':
        xMultiplier = 0.1
        player.velZ = velocity * math.sin(angle)
        flatVelocity = velocity * math.cos(angle)
        player.velX = flatVelocity * math.cos(player.aimAngle) * xMultiplier
        player.velY = flatVelocity * math.sin(player.aimAngle)
    else:
        xMultiplier = 0.4
        player.velZ = velocity * math.sin(angle)
        flatVelocity = velocity * math.cos(angle)
        player.velX = flatVelocity * math.cos(player.aimAngle) * xMultiplier
        player.velY = flatVelocity * math.sin(player.aimAngle)

def onStep(app):
    app.count += 1
    player = app.players[app.currentIdx]
    step = 1 / app.stepsPerSecond

    if player.velX != 0 or player.velY != 0 or player.velZ != 0:
        # In motion
        if player.putting:
            # Putting logic
            player.velZ = 0
            player.ballX += player.velX * step
            player.ballY += player.velY * step
            app.scrollX += player.velX * step
            app.scrollY += player.velY * step

            decel = app.rollingDeceleration
            player.velX -= decel * math.cos(player.aimAngle) * step
            player.velY -= decel * math.sin(player.aimAngle) * step

            if abs(player.velX) < 0.5 and abs(player.velY) < 0.5:
                player.velX = player.velY = 0
                player.putting = False
            holeX, holeY = findHoleCenter(app)
            if dist(player.ballX, player.ballY, holeX, holeY) <= (app.ballRadius):
                player.putting = False
                player.holed = True
        else:
            # Flying logic
            player.ballX += player.velX * step
            player.ballY = player.ballY - (player.velZ * step) + (player.velY * step)
            player.ballZ += player.velZ * step
            player.shadowY += player.velY * step
            if getShadowTerrain(app) != 'out of bounds':
                player.shadowOverLandX = player.ballX
                player.shadowOverLandY = player.shadowY
            app.scrollX += player.velX * step
            app.scrollY = app.scrollY - (player.velZ * step) + (player.velY * step)

            player.velZ -= app.gravity * step

            if player.ballZ <= 0 and player.velZ < 0:
                player.ballZ = 0
                player.shadowY = player.ballY
                player.velZ = 0
                app.velocity /= 3
                if app.velocity > 10:
                    takeBounce(app, player, app.velocity, app.angle)
                else:
                    player.velX = player.velY = player.velZ = 0
                    alivePlayers = []
                    for p in app.players:
                        if not p.holed:
                            alivePlayers.append(p)
                    if alivePlayers:
                        holeX, holeY = findHoleCenter(app)
                        farthest = None
                        maxD = -1
                        for p in alivePlayers:
                            d = dist(p.ballX, p.ballY, holeX, holeY)
                            if d > maxD:
                                maxD, farthest = d, p
                    everyoneHoled = True
                    for i in range(app.selectedNumPlayers): 
                        if not app.players[i].holed: 
                            everyoneHoled = False
                            break
                    if everyoneHoled: 
                        for i in range(app.selectedNumPlayers):
                            app.scores[i+1][app.currentHole] = app.players[i].strokes
                            app.hole1 = False
                            app.cardPage = True
                        if app.currentHole < 9:
                            app.currentHole += 1
                        else:
                            app.podium = True 
                        for p in app.players:
                            holeX, holeY = findHoleCenter(app)
                            aimAngle = math.atan2(holeY - p.ballY,
                                            holeX - p.ballX)
                            p.resetForHole(aimAngle)
                    app.currentIdx = app.players.index(farthest)
                    farthest.aimAngle = math.atan2(holeY - farthest.ballY,
                                        holeX - farthest.ballX)
                    centerOnPlayer(app, farthest)
                        
    else:
        # Check for holed
        holeX, holeY = findHoleCenter(app)
        if dist(player.ballX, player.ballY, holeX, holeY) <= (app.ballRadius):
            player.holed = True
            player.velX = player.velY = player.velZ = 0

        # Ball stopped – find next player
       

    # Ocean frame animation
    if not app.startPage:
        if app.count % 5 == 0:
            app.currentFrameIndex = (app.currentFrameIndex + 1) % len(app.frames)
            app.offsetX = (app.offsetX + app.offsetSpeed) % app.tileWidth
            app.offsetY = (app.offsetY + app.offsetSpeed) % app.tileHeight
            app.count = 0

def centerOnPlayer(app, player):
    # want ball at (app.width/2, app.height/3) on screen
    targetScrollX = player.ballX - app.width/2
    targetScrollY = player.ballY - app.height/3
    # clamp to course bounds
    app.scrollX = max(0, min(targetScrollX, app.courseWidth - app.width))
    app.scrollY = max(0, min(targetScrollY, app.courseHeight - app.height))


def drawBall(app):
    current = app.players[app.currentIdx]
    if current.velX != 0 or current.velY != 0 or current.velZ != 0:
        shadowX, shadowY = getScreenCoords(app, current.ballX, current.shadowY)
        drawCircle(shadowX, shadowY, app.ballRadius, fill='black', opacity=60)
    # Display current player info
    playerName = app.playerNames[app.currentIdx]
    drawLabel(f'{playerName} - Shots: {current.strokes}', 900, 30, size = 20, 
              fill='white', bold=True)

    # Draw all other players first
    for i, player in enumerate(app.players):
        if player == current:
            continue  # Skip current player for now

        sx, sy = getScreenCoords(app, player.ballX, player.ballY)
        drawCircle(sx, sy, app.ballRadius, fill='gray')

    # Then draw current player's ball last (on top)
    sx, sy = getScreenCoords(app, current.ballX, current.ballY)
    drawCircle(sx, sy, app.ballRadius, fill='white')

    # Shadow (only for current player if ball is in motion)
    
    

def onKeyPress(app, key):
    if app.landingPage: 
        if app.ipBoxSelected:
            if key == 'backspace': 
                app.ipAddress = app.ipAddress[:-1]
            elif len(key) == 1 and len(app.ipAddress) <= 15:
                app.ipAddress += key
            return
        elif app.nameBoxSelected:
            if key == 'backspace': 
                app.playerNames[app.nameIndex] = app.playerNames[app.nameIndex][:-1]
            elif len(key) == 1 and len(app.playerNames[app.nameIndex]) <= 12:
                app.playerNames[app.nameIndex] += key
            return
    if app.hole1:
        player = app.players[app.currentIdx]
    # Only allow input when the current player's ball is at rest
        if player.velX == 0 and player.velY == 0 and player.velZ == 0:

            # Club selection
            if key == 'w':
                app.clubIndex = (app.clubIndex - 1) % len(app.clubs)
                app.selectedClub = app.clubs[app.clubIndex]
            elif key == 's':
                app.clubIndex = (app.clubIndex + 1) % len(app.clubs)
                app.selectedClub = app.clubs[app.clubIndex]

            # Aiming left/right
            elif key == 'a':
                player.aimAngle -= math.radians(3)
            elif key == 'd':
                player.aimAngle += math.radians(3)

            # Taking the shot
            elif key == 'space':
                app.showClubSelection = False
                velocity, angle, dev = calculateVelocity(app.selectedClub)
                app.velocity, app.angle = velocity, angle
                player.aimAngle += dev
                takeShot(app, player, velocity, angle)


    



def drawAimLine(app):
    player = app.players[app.currentIdx]
    if player.velX == 0 and player.velY == 0 and player.velZ == 0:
        sx, sy = getScreenCoords(app, player.ballX, player.ballY)
        length = 60
        ex = sx + length * math.cos(player.aimAngle)
        ey = sy + length * math.sin(player.aimAngle)
        drawLine(sx, sy, ex, ey, fill='white', lineWidth=2)

def findHoleCenter(app):
    """
    Reads outlines with getHoleOutlines, grabs the first green polygon,
    and returns its centroid.
    """
    outlines = getHoleData(app) 
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

def pointInPolygon(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i+1) % n]
        # check if edge straddles horizontal ray at y
        if ((y0 > y) != (y1 > y)):
            # find x coordinate of intersection
            t = (y - y0) / (y1 - y0)
            xi = x0 + t * (x1 - x0)
            if xi >= x:
                inside = not inside
    return inside

def normalizePolygons(raw):
    out = []
    for entry in raw:
        if isinstance(entry, dict) and 'points' in entry:
            out.append(entry['points'])
        else:
            out.append(entry)
    return out

def getBallTerrain(app):
    player = app.players[app.currentIdx]
    bx, by = player.ballX, player.ballY
    outlines = getHoleData(app) 

    # check in this priority order
    for terrain in ('teebox', 'green', 'sandtrap', 'fairway', 'outline'):
        raw = outlines.get(terrain, [])
        for poly in normalizePolygons(raw):
            if pointInPolygon(bx, by, poly):
                # map 'outline' → 'rough'
                return 'rough' if terrain == 'outline' else terrain

    return 'out of bounds'

def getShadowTerrain(app):
    player = app.players[app.currentIdx]
    bx, by = player.ballX, player.shadowY
    outlines = getHoleData(app) 

    # check in this priority order
    for terrain in ('teebox', 'green', 'sandtrap', 'fairway', 'outline'):
        raw = outlines.get(terrain, [])
        for poly in normalizePolygons(raw):
            if pointInPolygon(bx, by, poly):
                # map 'outline' → 'rough'
                return 'rough' if terrain == 'outline' else terrain

    return 'out of bounds'



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
            
def drawCardButton(app): 
    if app.hole1:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='lemonChiffon', border='black', borderWidth=4.5,
                opacity = 95)
        
        drawLabel('Score Card', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=22, fill='black', font='American Typewriter', italic=True,
                 border='green')
        
def drawHoleButton(app): 
    if app.cardPage:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='lemonChiffon', border='black', borderWidth=4.5,
                opacity = 95)
        
        drawLabel('Back', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=26, fill='black', font='American Typewriter', italic=True,
                 border='green')
        
def drawCardPage(app):
    # Draw Background
    drawImage('15112-LandingPage.png', 0, 0, 
              width=app.width, height=app.height)
    
    # Score Card margins
    margin = 0.2 * min(app.width, app.height)
    
    # Card bounds
    cardLeft = margin
    cardTop = margin
    cardRight = app.width - margin
    cardBottom = app.height - margin
    
    cardWidth  = cardRight  - cardLeft
    cardHeight = cardBottom - cardTop
    
    #  Outer white box with black border
    drawRect(cardLeft, cardTop,
             cardWidth, cardHeight,
             fill='lemonChiffon',
             border='black', borderWidth=4)
    rows = len(app.scores)
    cols = len(app.scores[0])
    
    # Make header bigger
    headerHeight = cardHeight * 0.2
    gridHeight   = cardHeight - headerHeight
    
    colWidth  = cardWidth  / cols
    rowHeight = gridHeight / rows
    
    # draw Labels
    holeLabels = [''] + [str(i+1) for i in range(9)] + ['OUT','TOTAL']
    holeLabels = holeLabels[:cols]  # ensure it matches your number of columns
    
    for c in range(cols):
        x = cardLeft + c * colWidth
        y = cardTop
        drawRect(x, y,
                 colWidth, headerHeight,
                 fill='silver',
                 border='black', borderWidth=2)
        drawLabel(holeLabels[c],
                  x + colWidth/2,
                  y + headerHeight/2,
                  size=int(headerHeight * 0.25),
                  bold=True, fill='ivory', font='Phosphate')
    
    # Draw the score cells
    for row in range(rows):
        for col in range(cols):
            x = cardLeft + col * colWidth
            y = cardTop + headerHeight + row * rowHeight
            drawRect(x, y,
                     colWidth, rowHeight,
                     fill='lemonChiffon', border='black', borderWidth=2)
            drawLabel(str(app.scores[row][col]),
                      x + colWidth/2, y + rowHeight/2,
                      size=int(rowHeight * 0.25), fill='black',
                      font='Phosphate', bold=True) 
    drawLabel('Score Card', app.width//2-3, 50-2, size=64, bold=True, 
              fill='white', font='American Typewriter')
    drawLabel('Score Card', app.width//2, 50, size=64, bold=True, 
              fill='black', font='American Typewriter')

                     
def dist(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5

def drawLandingPage(app): 
    drawImage('15112-LandingPage.png', 0, 0, 
              width=app.width, height=app.height)
    drawLabel('Choose Number of Players', app.width//2, 80, size=30, bold=True)

    for i in range(1, 5):
        x = app.width//2 - 150 + i*60
        y = 140
        drawRect(x-25, y-25, 50, 50, fill='white' if app.selectedNumPlayers != i else 'lightGreen', border='black')
        drawLabel(str(i), x, y, size=20, bold=True)

    for i in range(app.selectedNumPlayers):
        drawLabel(f"Enter Name for Player {i+1}:", 300, 230 + i*60, size=16)
        drawRect(500, 210 + i*60, 180, 40, fill='white', border='black')
        drawLabel(app.playerNames[i], 590, 230 + i*60, size=16, align='center')

    drawRect(500, 450, 180, 40, fill='white', border='black')
    drawLabel(app.ipAddress, 590, 470, size=16, fill='black', align='center')
    drawLabel('Enter IP Address Here:', 300, 470, size=16)  

    drawRect(app.startButtonX, app.startButtonY, app.startButtonWidth, 
             app.startButtonHeight, fill='darkGreen', 
             border='white', borderWidth=2)
    drawLabel("Start Game", app.width//2, app.height - 60,
              size=20, fill='white', bold=True)


def landingMousePress(app, x, y):
    for i in range(1, 5):
        boxX = app.width//2 - 150 + i*60
        if (boxX - 25 <= x <= boxX + 25 and 115 <= y <= 165):
            app.selectedNumPlayers = i
            return
    for i in range(app.selectedNumPlayers):
        if (500 <= x <= 680 and 210 + i*60 <= y <= 250 + i*60):
            app.nameIndex = i
            app.nameBoxSelected = True
            app.ipBoxSelected = False
            return
        
    ipBoxX, ipBoxY = 500, 450
    if ipBoxX <= x <= ipBoxX + 180 and ipBoxY <= y <= ipBoxY + 40:
        app.ipBoxSelected = True
        app.nameBoxSelected = False
    else: 
        app.ipBoxSelected = False

        
    


runApp()

