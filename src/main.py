from cmu_graphics import *
from holeSketch import getHoleOutlines
from physics import calculateVelocity
import math, random
from playerClass import Player

def onAppStart(app):
    restart(app)

def restart(app):
    oceanStart(app)
    landingPageApp(app)
    windApp(app)
    whichPageApp(app)
    audioStart(app)
    cardPageApp(app)
    physicsApp(app)
    clubApp(app)
    scoreKeeperApp(app)
    randomApp(app)

def randomApp(app):
    app.cachedHoleOutlines = dict()
    app.width = 1000
    app.height = 600
    app.scrollX = 500
    app.scrollY = 650
    app.courseWidth = 3000
    app.courseHeight = 1800
    app.ballRadius = 3
    app.players = []
    app.stepsPerSecond = 10

def scoreKeeperApp(app):
    app.scores = [
        ['Par', 4, 3, 5, 4, 4, 3, 5, 4, 4, 36],
        ['Player 1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 2', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Player 4', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ]
    app.score = 0
    app.strokeCount = 0 

def clubApp(app):
    app.currentIdx = 0                
    app.clubs = ['driver', 'wood', 'iron', 'wedge', 'putter']
    app.clubIndex = 0
    app.selectedClub = app.clubs[0]

def physicsApp(app):
    app.velocity = 0
    app.gravity = 9.81
    app.angle = 0
    app.putting = False
    app.rollingDeceleration = 3.0
    app.onGreen = False

def cardPageApp(app):
    app.cardButtonX = 20 
    app.cardButtonY = 20
    app.cardButtonWidth = 140
    app.cardButtonHeight = 40
    app.restartButtonX = app.cardButtonX + app.width / 1.2
    app.restartButtonY = 30
    app.restartButtonWidth = 280
    app.restartButtonHeight = 40
    app.holeButtonX = app.cardButtonX
    app.holeButtonY = app.cardButtonY
    app.holeButtonWidth = app.cardButtonWidth
    app.holeButtonHeight = app.cardButtonHeight

def audioStart(app):
    app.music = 'music.mp3'
    playMusic(app)
    app.taylor = ['15112-taylor0.mp3', '15112-taylor1.mp3', 
                  '15112-taylor2.mp3', '15112-taylor3.mp3']
    app.koz = ['15112-koz0.mp3', '15112-koz1.mp3', 
               '15112-koz2.mp3', '15112-koz3.mp3', '15112-koz4.mp3']
    app.playedKozSound = False

def whichPageApp(app):
    app.startPage = True 
    app.instructionsPage = False
    app.hole1 = False
    app.cardPage = False
    app.nextHole = False
    app.landingPage = False
    app.connectionBad = False 

def windApp(app):
    app.windSpeed = random.uniform(0, 5)          
    app.windDirection = random.uniform(0, 2*math.pi)

def landingPageApp(app):
    app.startButtonX = app.width//2 - 70
    app.startButtonY = app.height - 80
    app.startButtonWidth = 180
    app.startButtonHeight = 40
    app.nameIndex = 0
    app.ipAddress = ''
    app.ipBoxSelected = False
    app.nameBoxSelected = False
    app.selectedNumPlayers = 1
    app.playerNames = ['' for i in range(5)]
    app.currentHole = 1
    app.podium = False
    app.ballStarts = [(190,570), (90, 580), (160,620), (40,880), (150, 675),
                      (330, 620), (380, 638), (130, 615),(120, 670)]

def oceanStart(app):
    app.frames = ["15112-ocean0.jpg", "15112-ocean1.jpg"]
    app.currentFrameIndex = 0
    app.tileWidth = 500  # Width of each tile
    app.tileHeight = 500  # Height of each tile
    app.offsetX = 0  # Horizontal offset for wave movement
    app.offsetY = 0  # Vertical offset for wave movement
    app.offsetSpeed = 5  # Speed of the diagonal movement
    app.count = 0
    
# All on app start is contained prior to this comment. Next will be all drawing
# logic.

def redrawAll(app):
    if app.startPage:
        drawStart(app)
    elif app.instructionsPage:
        drawInstructionsPage(app)
    elif app.landingPage:
        drawLandingPage(app)
    elif app.hole1:
        drawOcean(app)
        drawCliff(app)
        drawHole(app)
        if app.players and 0 <= app.currentIdx < len(app.players):
            current = app.players[app.currentIdx]
        if current.velX == 0 and current.velY == 0 and current.velZ == 0:
            drawAimLine(app)
            drawClubSelection(app)
        drawBall(app)  # Only call once now, it handles everything
        drawWindIndicator(app)
        drawCardButton(app)
        if app.connectionBad:
            drawReconnect(app)
            drawRestartButton(app)
    elif app.cardPage:
        drawCardPage(app)
        drawHoleButton(app)
        drawRestartButton(app)
    elif app.podium:
        drawPodium(app)
# All cliff logic is below.
def drawCliff(app):
    outlines = getHoleData(app)['outline']
    for poly in outlines:
        cliff = makeCliffBetter(poly, baseDepth=15, jag=1.5)
        coords = []
        for (worldX, worldY) in cliff:
            screenX,screenY = getScreenCoords(app, worldX, worldY)
            coords += [screenX, screenY]
        color = gradient('cornsilk', 'saddleBrown', start='top')# Pretty color!
        drawPolygon(*coords,
                    fill=color, border='black')
        for second in range(12):
            i = random.randrange(len(poly)) # Randomly make jagged edges
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
    # This functions essentially moves the cliff to give the illusion of water
    # crashing against it.
# Cliff logic ends here.

# Draws the ocean! flips between two images and move them to the bottom right
# corner to give the look of a moving ocean.
def drawOcean(app):
    # Display the current frame in chunks
    currentFrame = app.frames[app.currentFrameIndex]
    for x in range(-app.tileWidth, app.width, app.tileWidth): 
        # X values loop
        for y in range(-app.tileHeight, app.height, app.tileHeight): 
            # Y values loop
            drawImage(currentFrame, x+app.offsetX, y+app.offsetY, 
                      width=app.tileWidth, height=app.tileHeight)
    # Note, openAI helped with the idea of how to move the ocean to the
    # bottom right, and with debugging.
# All ocean logic ends here.

# All the logic for getting the holes using openCV is below.
def getScreenCoords(app, x, y):
    screenX = x - app.scrollX + app.width / 2
    screenY = y - app.scrollY + app.height / 3
    return screenX, screenY

def getHoleData(app):
    #USED CHATGPT TO CACHE THE HOLES
    if app.currentHole not in app.cachedHoleOutlines:
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
        app.cachedHoleOutlines[app.currentHole] = outlines
    return app.cachedHoleOutlines[app.currentHole]


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
                     fill='green', border='black')
    drawPolygons(app, outlines['fairway'], fill='forestGreen', border=None)
    drawPolygons(app, outlines['sandtrap'], fill='tan', border='black')
    drawPolygons(app, outlines['green'], fill='yellowGreen', border='black')
    drawPolygons(app, outlines['teebox'], fill='forestGreen', border='black')
    drawHoleAndFlag(app, outlines)

def drawHoleAndFlag(app, outlines):
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
            drawLine(screenX, screenY, screenX, screenY - 25, fill='white', 
                    lineWidth=2)
            drawPolygon(screenX, screenY - 15, screenX - 15, screenY - 20,
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
# All openCV logic ends here.

# The following chunk contains the drawing of all the pages and their 
# respective button logic.
def drawStart(app):
    # First, draw the title page.
    drawImage("titleScreen.png", 0, 0, width=app.width, height=app.height)
    
    titleX = app.width // 2
    titleY = app.height // 6
    baseFontSize = 75
    factor = min(app.width / 1000, app.height / 600)
    titleFontSize = int(baseFontSize * factor)

    drawLabel('Wii Golf 112', titleX-7, titleY-3, 
             size=titleFontSize, fill='black', font='impact')
    drawLabel('Wii Golf 112', titleX, titleY,
             size=titleFontSize, fill='cornSilk', font='impact')
    
    factor = min(app.width / 1000, app.height / 600)
    # Note, the idea of a factor was from OpenAI and is implemented in many
    # functions, this makes the screen size responsive.
    playButtonWidth = int(400 * factor)
    playButtonHeight = int(50 * factor)
    playButtonX = app.width // 2
    playButtonY = int(app.height // 1.3)

    # Draw play button.
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
    # This ends the title Page.

    # Secondly, this will draw the instruction page and provide logic for such.

def getInstructions():
    instructions = [
        '1. Download "phyphox" on your cellPhone.',
        '2. Turn on your WIFI Hotspot on your cellPhone.',
        "3. Connect to your cellPhone's Hotspot on your computer.",
        '4. Enter the IP address of your cellPhone in the box on the' 
            'page following.',
        '6. Press space to initalize phyphox, you then have 7 seconds'
            'to take your shot.',
        '5. You must enter at least 1 player name.',
        '6. Use arrow keys to navigate the game.',
        "7. Press 'w' and 's' to select clubs and Press 'a' and 'd' to aim"]
    return instructions
def drawInstructionsPage(app):
    drawImage('15112-instructionsPage.png',0 , 0, width=app.width, 
              height=app.height)
    titleY = app.height * 0.1 - 10
    titleSize = int(app.height * 0.15)
    drawLabel("Instructions",
              app.width / 2 -3, titleY-3,size=titleSize, 
              bold=True, fill='black',font='impact')
    drawLabel("Instructions",
              app.width / 2, titleY,size=titleSize, 
              bold=True, fill='cornSilk', font='impact')

    instructions = getInstructions() 
    startY = app.height * 0.25
    lineHeight = app.height * 0.08
    textSize = int(app.height * 0.03)
    for i, line in enumerate(instructions):
        drawLabel(line, app.width / 2-1.5, startY + i * lineHeight - 25,
                  size=textSize, fill='black')
        drawLabel(line, app.width / 2, startY + i * lineHeight - 25,
                  size=textSize, fill='cornSilk')

    # Continue button (centered)
    btnW = app.width  * 0.20
    btnH = app.height * 0.08
    btnX = (app.width  - btnW) / 2
    btnY = app.height * 0.80
    txtY = btnY + btnH / 2
    txtSz = int(app.height * 0.04)
    drawRect(btnX, btnY, btnW, btnH,
             fill='darkGreen', border='white', borderWidth=2)
    drawLabel("Continue",
              app.width / 2, txtY,
              size=txtSz, fill='white')
    # This is the end of the instructions page.

    # Thirdly, this will draw the landing page and provide logic for such.
    # This was particularly grueling due to the need to bound all boxes.
def drawLandingPage(app):
    scaleX = app.width  / 1000
    scaleY = app.height / 600

    drawImage('15112-LandingPage.png', 0, 0, 
              width=app.width, height=app.height)

    drawLabel('Choose Number of Players',
              app.width//2 - 3, 80 * scaleY - 3, 
              size=int(30 * scaleY)+30, bold=True, 
              font='Impact', fill='black')
    
    drawLabel('Choose Number of Players',
              app.width//2, 80 * scaleY,
              size=int(30 * scaleY)+30, bold=True, 
              font='Impact', fill='darkOliveGreen')
    drawPlayerBoxes(app, scaleX, scaleY)

def getSizes(scaleX, scaleY):
    labelX = 300 * scaleX
    inputX = 500 * scaleX
    inputW = 180 * scaleX
    inputH = 40 * scaleY
    return labelX, inputX, inputW, inputH

def drawPlayerBoxes(app, scaleX, scaleY):
    baseOffset = -150 
    spacing = 60
    boxSize = 50

    for i in range(1, 5):
        cx = app.width/2 + (baseOffset + i*spacing) * scaleX
        cy = 140 * scaleY
        w  = boxSize * scaleX
        h = boxSize * scaleY
        fill = 'lightGreen' if app.selectedNumPlayers == i else 'cornSilk'

        drawRect(cx - w/2, cy - h/2,
                 w, h, fill=fill, border='darkOlivegreen', borderWidth=2)
        drawLabel(str(i), cx, cy, size=int(20 * scaleY) + 5, 
                  bold=True, font='American TypeWriter')
    labelX, inputX, inputW, inputH = getSizes(scaleX, scaleY)
    for i in range(app.selectedNumPlayers):
        labelY = (230 + i*60) * scaleY
        yRect  = (210 + i*60) * scaleY

        drawLabel(f"Enter Name for Player {i+1}:",
                  labelX-2.5, labelY-2.5, size=int(16 * scaleY)+20, 
                  font='HeadlineA', fill='darkOlivegreen', bold=True)
        drawLabel(f"Enter Name for Player {i+1}:",
                  labelX, labelY, size=int(16 * scaleY)+20, font='HeadlineA', 
                  fill='cornSilk', bold=True)

        drawRect(inputX, yRect, inputW, inputH,
                 fill='cornSilk', border='darkOliveGreen', borderWidth=4)

        drawLabel(app.playerNames[i],
                  inputX + inputW/2, labelY, size=int(16 * scaleY)+15,
                  align='center', font='nanum pen script')
        drawIPAndStart(app, scaleX, scaleY, labelX, inputW, inputH, inputX)

def drawIPAndStart(app, scaleX, scaleY, labelX, inputW, inputH, inputX):
    # IP-address box
    yLabelIP = 470 * scaleY
    yRectIP  = 450 * scaleY

    drawLabel('Enter IP Address Here:',
              labelX-2.5, yLabelIP-2.5, size=int(16 * scaleY)+20, 
              font='HeadLineA', fill='darkOlivegreen', bold=True)
    drawLabel('Enter IP Address Here:',
              labelX, yLabelIP, size=int(16 * scaleY)+20, 
              font='HeadLineA', fill='cornSilk', bold=True)

    drawRect(inputX, yRectIP, inputW, inputH,
             fill='cornSilk', border='darkOliveGreen', borderWidth=4)

    drawLabel(app.ipAddress, inputX + inputW/2, yLabelIP,
              size=int(16 * scaleY)+5, align='center', 
              font='American Typewriter', bold=True)

    # Start button
    btnW = 180 * scaleX
    btnH =  40 * scaleY
    btnX = app.width/2 - btnW/2
    btnY = app.height - 80 * scaleY

    drawRect(btnX, btnY, btnW, btnH, fill='cornSilk',
             border='darkOliveGreen', borderWidth=6)

    drawLabel("START", app.width//2, app.height - 60 * scaleY,
              size=int(20 * scaleY)+15, fill='darkOliveGreen', 
              bold=True, font='Modak')
    # This marks the end of the launch page.
    # Fourthly, this will draw the card page and provide logic for such.

def getCardBounds(app, margin):
    cardLeft = margin
    cardTop = margin
    cardWidth  = app.width - margin - cardLeft
    cardHeight = app.height - margin - cardTop
    return cardLeft, cardTop, cardWidth, cardHeight

def getHeaderColAndRow(app, cardHeight, cardWidth):
    rows = len(app.scores)
    cols = len(app.scores[0])
    # Make header bigger
    headerHeight = cardHeight * 0.2
    gridHeight   = cardHeight - headerHeight
    colWidth  = cardWidth  / cols
    rowHeight = gridHeight / rows
    return rows, cols, headerHeight, gridHeight, colWidth, rowHeight

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
             
    rows = len(app.scores)
    cols = len(app.scores[0])
    
    # Make header bigger
    headerHeight = cardHeight * 0.2
    gridHeight   = cardHeight - headerHeight
    
    colWidth  = cardWidth  / cols
    rowHeight = gridHeight / rows
    
    # draw Labels
    holeLabels = [''] + [str(i+1) for i in range(9)] + ['TOTAL', '+/-']
    holeLabels = holeLabels[:cols]
    
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
                  size=int(headerHeight * 0.25)+3,
                  bold=True, fill='ivory', font='HeadLineA', border='black',
                  borderWidth=0.75)
    
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
                      font='HeadLineA', bold=True) 
    drawLabel('Score Card', app.width//2-3, 50-2, size=64, bold=True, 
              fill='white', font='American Typewriter')
    drawLabel('Score Card', app.width//2, 50, size=64, bold=True, 
              fill='black', font='American Typewriter')
    
    for i in range(1, len(app.scores)): 
        row = app.scores[i]
        row[10] = 0 # This should be the TOTAL
        row[11] = 0 # This should be the O/U
        for j in range(1, 10): 
            score = row[j]
            par = app.scores[0][j]
            if isinstance(score, int): 
                row[10] += score 
                row[11] += (score - par) 

def isInCardButton(app, x, y): 
    return (app.cardButtonX <= x <= app.cardButtonX + app.cardButtonWidth and
            app.cardButtonY <= y <= app.cardButtonY + app.cardButtonHeight)

def isInHoleButton(app, x, y):
    return (app.holeButtonX <= x <= app.holeButtonX + app.holeButtonWidth and
            app.holeButtonY <= y <= app.holeButtonY + app.holeButtonHeight)

def isInRestartButton(app,x, y):  
    width = app.restartButtonWidth
    height = app.restartButtonHeight
    X = (app.width - width) // 2
    Y = app.height - height - 20  

    return ( X<= x <= X + width and
            Y <= y <= Y + height)

def isInNextHoleButton(app, x, y):
    nextX = app.cardButtonX + app.width / 1.2
    nextY = app.cardButtonY + app.height / 1.15
    w = app.cardButtonWidth + 5
    h = app.cardButtonHeight + 5
    return (nextX <= x <= nextX + w) and (nextY <= y <= nextY + h)

def isInStartButton(app, x, y):
    scaleX = app.width  / 1000
    scaleY = app.height / 600
    btnW = 180 * scaleX
    btnH =  40 * scaleY
    btnX = app.width/2 - btnW/2
    btnY = app.height - 80 * scaleY
    return (btnX <= x <= btnX+btnW and
            btnY <= y <= btnY+btnH)

def drawRestartButton(app): 
    if app.cardPage or app.connectionBad:
        x = (app.width - app.restartButtonWidth) // 2
        y = app.height - app.restartButtonHeight - 20
        
        drawRect(x, y,  
                app.restartButtonWidth, app.restartButtonHeight,
                fill='lemonChiffon', border='black', borderWidth=4.5,
                opacity = 95)
        
        drawLabel('Restart Game', app.restartButtonWidth//2 + x,
                 app.restartButtonHeight//2 + y,
                 size=26, fill='darkOliveGreen', font='American Typewriter', 
                 italic=True)
def drawHoleButton(app): 
    if app.cardPage:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='lemonChiffon', border='black', borderWidth=4.5,
                opacity = 95)
        
        drawLabel('Back', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=26, fill='darkOliveGreen', font='American Typewriter', 
                 italic=True)
        # Next hole button!
        nextHoleX = app.cardButtonX + app.width / 1.2
        nextHoleY = app.cardButtonY + app.height / 1.15
        drawRect(nextHoleX, nextHoleY, 
                 app.cardButtonWidth+5, app.cardButtonHeight+5,
                fill='lemonChiffon', border='black', borderWidth=4.5)
        if app.currentHole < 9:
            drawLabel('Next Hole!', nextHoleX + 3 + app.cardButtonWidth//2,
                 nextHoleY + app.cardButtonHeight//2,
                 size=24, fill='darkOliveGreen', font='American Typewriter', 
                 italic=True,)
        elif app.currentHole == 9: 
            drawLabel('Podium!', nextHoleX + 3 + app.cardButtonWidth//2,
                 nextHoleY + app.cardButtonHeight//2,
                 size=24, fill='darkOliveGreen', font='American Typewriter', 
                 italic=True,)
                 
def drawCardButton(app): 
    if app.hole1:
        drawRect(app.cardButtonX, app.cardButtonY, 
                app.cardButtonWidth, app.cardButtonHeight,
                fill='lemonChiffon', border='black', borderWidth=4.5,
                opacity = 95)
        
        drawLabel('Score Card', app.cardButtonX + app.cardButtonWidth//2,
                 app.cardButtonY + app.cardButtonHeight//2,
                 size=22, fill='darkOliveGreen', font='American Typewriter', 
                 italic=True)
    # This marks the end of the card page.
    # Fifthly, this will draw the podium page and provide logic for such.
def drawReconnect(app):
    drawImage('badConnection.png', 0, 0, width=app.width, height=app.height)
    drawLabel('Connection Issue!', app.width//2-3, app.height//6-2, size = 80,
              fill='cornSilk', bold=True, font='HeadLineA', align='center')
    drawLabel('Connection Issue!', app.width//2, app.height//6, size = 80,
              fill='maroon', bold=True, font='HeadLineA', align='center')
    drawLabel('Please restart your app and verify your connection.', 
              app.width//2-2, app.height//1.5-2, font='HeadLineA', 
              fill='cornSilk', bold=True, size=40)
    drawLabel('Please restart your app and verify your connection.', 
              app.width//2, app.height//1.5, font='HeadLineA', 
              fill='maroon', bold=True, size=40, align='center')
    drawLabel('We are sorry. :(', 
              app.width//2-2, app.height//1.3-2, font='HeadLineA', 
              fill='cornSilk', bold=True, size=40)
    drawLabel('We are sorry. :(', app.width//2, app.height//1.3, 
              font='HeadLineA', fill='maroon', bold=True, 
              size=40, align='center')
    # This marks the end of the reconnect page.
    # Sixthly, this will draw the club selection page and provide 
    # logic for such.
def getMenuSizes(app):
    menuX = 20
    menuY = app.height - 300
    menuWidth = 180
    menuHeight = 270
    lineHeight = 28
    topOffset = 50
    return menuX, menuY, menuWidth, menuHeight, lineHeight, topOffset

def drawClubSelection(app):
    menuX, menuY, menuWidth, menuHeight, lineHeight, topOffset =(
        getMenuSizes(app))
    # Draw main menu panel
    drawRect(menuX + 5, menuY + 5, menuWidth - 10, menuHeight, 
            fill='cornSilk', opacity=85, 
            border='darkOliveGreen', borderWidth=3.5)
    
    # Draw title
    drawLabel('Club Selection', 
                menuX + menuWidth//2-1, menuY + 30-1, 
                size=20, bold=True, fill='black', font='Snell Roundhand')
    drawLabel('Club Selection', 
                menuX + menuWidth//2, menuY + 30, size=20, 
                bold=True, fill='darkOliveGreen', font='Snell Roundhand')
    # Draw club options
    for i, club in enumerate(app.clubs):
        # Highlight selected club
        if i == app.clubIndex:
            # Draw highlight background
            drawRect(menuX + 10, 
                    menuY + topOffset + i* lineHeight, 160, 30, 
                    fill='darkOliveGreen', border='black', borderWidth=2)
            textColor = 'cornSilk'
        else:
            textColor = 'darkOliveGreen'
        # Draw club name
        drawLabel(club.title(),
                    menuX + menuWidth//2, menuY + 60 + i*30,
                    fill=textColor, font='American Typewriter',
                    size=18, bold=True)
    # Draw instructions at bottom
    drawLabel('Press w and s to select', menuX + menuWidth//2, 
                menuY + menuHeight - 30, size=14, font='American Typewriter',
                fill='darkOliveGreen', italic=True)
    
    drawLabel('Press SPACE to confirm', menuX + menuWidth//2, 
                menuY + menuHeight - 10, size=14, font='American Typewriter',
                fill='darkOliveGreen', italic=True)
    # This marks the end of the club selection page.
    # Seventhly, this will draw the podium page and provide logic for such.
def drawPodium(app):
    drawImage('winner.png', 0, 0, 
              width=app.width, height=app.height)

    drawLabel('FINAL RANKINGS', app.width//2-4, 60-4,
              size=80, fill='black', bold=True, font='Impact', 
              border='black', borderWidth=2)
    drawLabel('FINAL RANKINGS', app.width//2, 60,
              size=80, fill='gold', bold=True, font='Impact', 
              border='black', borderWidth=2)

    playerTotals = []
    for i in range(len(app.players)): 
        player = app.players[i]
        total = 0
        for hole in range(1, 10): 
            score = app.scores[i+1][hole]
            if isinstance(score, int):
                total += score
        playerTotals.append([player.name.strip(), total])

    for i in range(len(playerTotals)):
        for j in range(len(playerTotals)): 
            if playerTotals[j][1] < playerTotals[i][1]:
                playerTotals[i], playerTotals[j] = (
                    playerTotals[j], playerTotals[i])

    for i in range(len(playerTotals)): 
        name = playerTotals[i][0]
        if name == '' or name == '.':
            name = 'Unnamed Player'
        strokes = playerTotals[i][1]
        if i == 0: 
            place = 'First Place'
            color = 'gold'
        elif i == 1: 
            place = 'Second Place'
            color = 'silver'
        elif i == 2: 
            place = 'Third Place'
            color = 'darkGoldenrod'
        else: 
            place = 'Fourth Place'
            color = 'white'

        size = 55 - i * 5
        y = 150 + i * 50
        drawLabel(f'{place}: {name} - {strokes} strokes', app.width//2-2, y-2,
                  size=size, fill='black', bold=True, font='Impact')
        drawLabel(f'{place}: {name} - {strokes} strokes',
                  app.width//2, y,
                  size=size, fill=color, bold=True,
                  font='Impact', border='black')
    # This marks the end of the podium.
    # Eighthly, this will draw the wind indicator.
def drawWindIndicator(app):
    x0, y0 = app.width - 80, 60
    length = 40
    dx = length * math.cos(app.windDirection)
    dy = length * math.sin(app.windDirection)
    # arrow line
    drawLine(x0, y0, x0+dx, y0-dy, lineWidth=3, fill='cornSilk', 
             arrowEnd = True)
    # speed label
    drawLabel(f'{app.windSpeed:.1f} mph',
              x0, y0+30, size=22, fill='cornSilk', font='American Typewriter',
              border='black', borderWidth=0.25, bold=True)
    # This marks the end of the wind indicator.
    # Ninthly, this will draw the ball and its shadow.
def drawBall(app):
    current = app.players[app.currentIdx]
    if current.velX != 0 or current.velY != 0 or current.velZ != 0:
        shadowX, shadowY = getScreenCoords(app, current.ballX, current.shadowY)
        drawCircle(shadowX, shadowY, app.ballRadius, fill='black', opacity=60)
    # Display current Hole 
    drawLabel(f'Hole {app.currentHole}',
              app.width//1.05, app.height//1.12,
              size=32, fill='cornSilk', bold=True,
              font='American Typewriter', border='black',
              borderWidth=0.5, align='right')
    # Display current player info
    playerName = app.playerNames[app.currentIdx]
    drawLabel(f'{playerName} - Shots Taken: {current.strokes}', app.width//1.05, 
              app.height//1.05, size=32, fill='cornSilk', bold=True, 
              font='American Typewriter', border='black', 
              borderWidth=0.5, align='right')
    # Draw all other players first
    for i, player in enumerate(app.players):
        if player == current:
            continue  # Skip current player for now
        sx, sy = getScreenCoords(app, player.ballX, player.ballY)
        drawCircle(sx, sy, app.ballRadius, fill='gray')
    # Then draw current player's ball last (on top)
    sx, sy = getScreenCoords(app, current.ballX, current.ballY)
    drawCircle(sx, sy, app.ballRadius, fill='white', border='black',
               borderWidth=0.75)

    # Shadow (only for current player if ball is in motion)
    # This marks the end of the ball and its shadow!
    # Finally, we draw aim line.
def drawAimLine(app):
    player = app.players[app.currentIdx]
    if player.velX == 0 and player.velY == 0 and player.velZ == 0:
        sx, sy = getScreenCoords(app, player.ballX, player.ballY)
        length = 60
        ex = sx + length * math.cos(player.aimAngle)
        ey = sy + length * math.sin(player.aimAngle)
        drawLine(sx, sy, ex, ey, fill='fireBrick', lineWidth=2, dashes=True)
    # This marks the end of all the drawing functions. (yay!)
# The next chunk will cotain all mouse logic.
def onMousePress(app, mouseX, mouseY):
    if app.startPage and isInPlayButton(app, mouseX, mouseY):
        app.startPage = False
        app.instructionsPage = True
    elif app.instructionsPage:
        instructionsPageMousePress(app, mouseX, mouseY)
    elif app.landingPage: 
        landingMousePress(app, mouseX, mouseY)
        if isInStartButton(app, mouseX, mouseY):
            app.players = []
            teeX, teeY = app.ballStarts[app.currentHole - 1]
            for i in range(app.selectedNumPlayers):
                name = app.playerNames[i]
                app.players.append(Player(name, (teeX, teeY)))

            parRow = ['Par', 4, 3, 5, 4, 4, 3, 5, 4, 4, 36, '-']
            playerRows = [
                        [name] + ['-' for j in range(len(parRow) - 1)]
                            for name in app.playerNames
                        ]
            app.scores = [parRow] + playerRows[:app.selectedNumPlayers]
            # Reset turn order:
            app.currentIdx = 0
            # Give everyone an initial aimAngle toward the hole:
            holeX, holeY = findHoleCenter(app)
            for p in app.players:
                p.aimAngle = math.atan2(holeY - p.ballY,
                                        holeX - p.ballX)
            app.landingPage = False
            app.hole1 = True
            app.onTeebox = True 
            app.showClubSelection = True
    elif app.hole1 and isInCardButton(app, mouseX, mouseY):
        app.hole1 = False
        app.cardPage = True
    elif app.cardPage:
        if isInHoleButton(app, mouseX, mouseY):
            app.cardPage = False
            app.hole1 = True
        elif isInRestartButton(app, mouseX, mouseY):
            restart(app)
        elif isInNextHoleButton(app, mouseX, mouseY):
            if app.currentHole < 9:
                app.currentHole += 1
                app.cardPage = False
                app.hole1 = True
                app.windSpeed = random.uniform(0, 5)
                app.windDirection = random.uniform(0, 2*math.pi)
                teeX, teeY = app.ballStarts[app.currentHole - 1]
                for p in app.players:
                    p.ballX, p.ballY = teeX, teeY
                    p.shadowX = teeX
                    p.shadowY = teeY
                    p.shadowOverHoleX = teeX
                    p.shadowOverHoleY = teeY
                    p.ballZ = 0
                    p.putting = False
                    p.strokes = 0
                    p.velX = p.velY = p.velZ = 0
                    p.holed = False
                x, y = findHoleCenter(app)
                for p in app.players:
                    p.aimAngle = (math.atan2(y - p.ballY, x - p.ballX))
                centerOnPlayer(app, app.players[0])
            elif app.currentHole >= 9:
                app.cardPage = False
                app.podium = True
    elif app.connectionBad:
        if isInRestartButton(app, mouseX, mouseY):
            app.cardPage = False
            app.startPage = True

def onKeyHold(app, keys): 
    if not app.hole1 or not app.players:
        return
    move = 25
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

def onStep(app):
    if not app.hole1 or not app.players:
        return
    app.count += 1
    player = app.players[app.currentIdx]
    step = 1 / app.stepsPerSecond

    windAx = app.windSpeed * math.cos(app.windDirection)
    windAy = app.windSpeed * math.sin(app.windDirection)

    player = app.players[app.currentIdx]

    if player.velZ != 0:
        player.velX += windAx * step
        player.velY -= windAy * step

    if player.velX != 0 or player.velY != 0 or player.velZ != 0:
        # In motion
        if player.putting:
            # Putting logic
            player.velZ = 0
            player.ballX += player.velX * step
            player.ballY += player.velY * step
            app.scrollX += player.velX * step
            app.scrollY += player.velY * step
            player.shadowX = player.ballX
            player.shadowY = player.ballY
            player.shadowOverLandX = player.ballX
            player.shadowOverLandY = player.shadowY
            decel = app.rollingDeceleration
            if getBallTerrain(app) != 'green':
                app.clubIndex = 3
                app.selectedClub = app.clubs[app.clubIndex]
                decel = app.rollingDeceleration * 4
            player.velX -= decel * math.cos(player.aimAngle) * step
            player.velY -= decel * math.sin(player.aimAngle) * step

            if abs(player.velX) < 0.5 and abs(player.velY) < 0.5:
                player.velX = player.velY = 0
                player.putting = False
                if getBallTerrain(app) == 'green':
                    app.clubIndex = 4
                    app.selectedClub = app.clubs[app.clubIndex]
            holeX, holeY = findHoleCenter(app)
            if dist(player.ballX, player.ballY, holeX, holeY) <= (
                app.ballRadius):
                player.putting = False
                player.holed = True
        else:
            # Flying logic
            player.ballX += player.velX * step
            player.ballY = player.ballY - (
                (player.velZ * step) + (player.velY * step))
            player.ballZ += player.velZ * step
            player.shadowY += player.velY * step
            if getShadowTerrain(app) != 'out of bounds':
                player.shadowOverLandX = player.ballX
                player.shadowOverLandY = player.shadowY
            app.scrollX += player.velX * step
            app.scrollY = app.scrollY - (player.velZ * step) + (
                (player.velY * step))

            player.velZ -= app.gravity * step

            if player.ballZ <= 0 and player.velZ < 0:
                # Audio determination
                terrain = getBallTerrain(app)
                if terrain == 'green' and not app.onGreenPlayed:
                    playSound(app, app.taylor)
                    app.onGreenPlayed = True
                elif (terrain == 'sandtrap') or (terrain == 'out of bounds'):
                    if not app.playedKozSound:
                        playSound(app, app.koz)
                        app.playedKozSound = True
                else:
                    player.playedKozSound = False
                    
                player.ballZ = 0
                player.shadowY = player.ballY
                player.velZ = 0
                holeX, holeY = findHoleCenter(app)
                if dist(player.ballX, player.ballY, holeX, holeY) <= (
                    (app.ballRadius)):
                    player.putting = False
                    player.holed = True
                    player.velX = player.velY = player.velZ = 0
                #flatSpeed = (player.velX**2 + player.velY**2)**0.5
                app.velocity //= 3
                if app.velocity  > 10:
                    takeBounce(app, player, app.velocity, app.angle)
                else:
                    player.velX = player.velY = player.velZ = 0
                    if getBallTerrain(app) == 'green':
                        app.clubIndex = 4
                        app.selectedClub = app.clubs[app.clubIndex]
                    alivePlayers = []
                    for p in app.players:
                        if not p.holed:
                            alivePlayers.append(p)
                    if alivePlayers:
                        # pick the farthest-out ball
                        holeX, holeY = findHoleCenter(app)
                        farthest = None
                        maxD = -1
                        for p in alivePlayers:
                            d = dist(p.shadowOverLandX, 
                                     p.shadowOverLandY, holeX, holeY)
                            if d > maxD:
                                maxD = d
                                farthest = p
                        # switch to that player
                        app.currentIdx = app.players.index(farthest)
                        farthest.aimAngle = math.atan2(
                            holeY - farthest.ballY,
                            holeX - farthest.ballX
                        )
                        centerOnPlayer(app, farthest)
                        if getBallTerrain(app) == 'green':
                            app.clubIndex = 4
                            app.selectedClub = app.clubs[app.clubIndex]
                    else:
                        # everyone holed → record scores and flip to card
                        app.clubIndex = 0
                        app.selectedClub = app.clubs[app.clubIndex]
                        for i in range(app.selectedNumPlayers):
                            app.scores[i+1][app.currentHole] = (
                                app.players[i].strokes)
                        app.hole1 = False
                        app.cardPage = True
    else:
        # Check for holed
        holeX, holeY = findHoleCenter(app)
        if dist(player.ballX, player.ballY, holeX, holeY) <= (app.ballRadius):
            playSound(app, app.taylor)
            player.holed = True
            player.velX = player.velY = player.velZ = 0

        # Ball stopped – find next player
    # Ocean frame animation
    if not app.startPage:
        if app.count % 5 == 0:
            app.currentFrameIndex = (app.currentFrameIndex + 1) % (
                len(app.frames))
            app.offsetX = (app.offsetX + app.offsetSpeed) % app.tileWidth
            app.offsetY = (app.offsetY + app.offsetSpeed) % app.tileHeight
            app.count = 0

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
                app.playerNames[app.nameIndex] =(
                    app.playerNames[app.nameIndex][:-1])
            elif len(key) == 1 and len(app.playerNames[app.nameIndex]) <= 2:
                app.playerNames[app.nameIndex] += key
            return
    if app.hole1:
        player = app.players[app.currentIdx]
    # Only allow input when the current player's ball is at rest
        if player.velX == 0 and player.velY == 0 and player.velZ == 0:

            # Club selection
            if key == 'w':
                if getBallTerrain(app) != 'green':
                    app.clubIndex = (app.clubIndex - 1) % (len(app.clubs) - 1)
                    app.selectedClub = app.clubs[app.clubIndex]
            elif key == 's':
                if getBallTerrain(app) != 'green':
                    app.clubIndex = (app.clubIndex + 1) % (len(app.clubs) - 1)
                    app.selectedClub = app.clubs[app.clubIndex]

            # Aiming left/right
            elif key == 'a':
                player.aimAngle -= math.radians(3)
            elif key == 'd':
                player.aimAngle += math.radians(3)

            # Taking the shot
            elif key == 'space':
                app.showClubSelection = False
                if app.ipAddress == '':
                    app.connectionBad = True
                if app.ipAddress: 
                    try:
                        velocity, angle, dev = (
                            calculateVelocity(app.selectedClub, app.ipAddress))
                        app.velocity, app.angle = velocity, angle
                        player.aimAngle += dev
                        takeShot(app, player, velocity, angle)
                    except:
                        app.connectionBad = True

#These are the onMousePresses for the landing page & instructions page.
def landingMousePress(app, x, y):
    scaleX, scaleY = app.width  / 1000, app.height / 600

    baseOffset = -150
    spacing, boxSize = 60, 50
    for i in range(1, 5):
        cx = app.width/2 + (baseOffset + i*spacing) * scaleX
        cy = 140 * scaleY
        w, h = boxSize * scaleX, boxSize * scaleY
        if (cx - w/2 <= x <= cx + w/2 and
            cy - h/2 <= y <= cy + h/2):
            app.selectedNumPlayers = i
            app.playerNames = ['' for i in range(app.selectedNumPlayers)]
            return

    inputX = 500 * scaleX
    inputW, inputH = 180 * scaleX, 40 * scaleY
    for i in range(app.selectedNumPlayers):
        yRect = (210 + i*60) * scaleY
        if (inputX <= x <= inputX + inputW and
            yRect <= y <= yRect + inputH):
            app.nameIndex = i
            app.nameBoxSelected = True
            app.ipBoxSelected = False
            return

    ipX, ipY = 500 * scaleX, 450 * scaleY
    if (ipX <= x <= ipX + inputW and
        ipY <= y <= ipY + inputH):
        app.ipBoxSelected = True
        app.nameBoxSelected = False
        return
    # else deselect IP
    app.ipBoxSelected = False

def instructionsPageMousePress(app, mouseX, mouseY):
    btnW = app.width  * 0.20
    btnH = app.height * 0.08
    btnX = (app.width  - btnW) / 2
    btnY = app.height * 0.80

    if btnX <= mouseX <= btnX + btnW and btnY <= mouseY <= btnY + btnH:
        app.instructionsPage = False
        app.landingPage = True
# This marks the end of any mouse logic.
# This chunk contains all physics & logisitics.
def findHoleCenter(app):
    """
    Reads outlines with getHoleOutlines, grabs the first green polygon,
    and returns its centroid.
    """
    outlines = getHoleData(app) 
    greens = outlines.get('green', [])
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

def centerOnPlayer(app, player):
    targetScrollX = player.ballX
    targetScrollY = player.ballY
    halfW = app.width/2
    halfH = app.height/3
    minScrollX =  halfW
    maxScrollX =  app.courseWidth  - halfW
    minScrollY =  halfH
    maxScrollY =  app.courseHeight - halfH

    app.scrollX = max(minScrollX, min(targetScrollX, maxScrollX))
    app.scrollY = max(minScrollY, min(targetScrollY, maxScrollY))
    
def takeShot(app, player, velocity, angle):
    # Set initial ball position to teebox location
    # These values should match your teebox position
    # Set initial velocities  # 45 degree launch anglex
    app.onGreenPlayed = False
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
        player.velX = player.velY = player.velZ = 0.01

    elif getBallTerrain(app) == 'out of bounds':
        player.velX = player.velY = player.velZ = 0.01
        player.strokes += 1
        player.ballX, player.ballY = (
            player.shadowOverLandX, player.shadowOverLandY)
        player.shadowX = player.ballX
        player.shadowY = player.ballY
    elif getBallTerrain(app) == 'rough':
        xMultiplier = 0.1
        yMultiplier = 0.2
        player.velZ = velocity * math.sin(angle)
        flatVelocity = velocity * math.cos(angle)
        player.velX = flatVelocity * math.cos(player.aimAngle) * xMultiplier
        player.velY = flatVelocity * math.sin(player.aimAngle) * yMultiplier
    else:
        xMultiplier = 0.4
        yMultiplier = 0.6
        player.velZ = velocity * math.sin(angle)
        flatVelocity = velocity * math.cos(angle)
        player.velX = flatVelocity * math.cos(player.aimAngle) * xMultiplier
        player.velY = flatVelocity * math.sin(player.aimAngle) * yMultiplier

def dist(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5

# Lastly, all audio is contained in the chunk below.
def findAimAngle(app):
    app.targetX, app.targetY = findHoleCenter(app)
    return math.atan2(app.targetY - app.ballY, app.targetX - app.ballX)  

def playSound(app, soundList):
    if soundList == app.koz:
        audioIndex = random.randint(0, 4)
        audio = app.koz[audioIndex]
        audio = Sound(audio)
        audio.play()
        return
    elif soundList == app.taylor and not app.cardPage == False:
        audioIndex = random.randint(0, 3)
        audio = app.taylor[audioIndex]
        audio = Sound(audio)
        audio.play()
        return
    
def playMusic(app):
    audio = Sound(app.music)
    audio.play(loop=True)

runApp()

