
class Player:
    def __init__(self, name, startPos, ballRadius):
        self.name = name
        self.startX, self.startY = startPos
        self.ballX = self.startX
        self.ballY = self.startY
        self.ballZ = 0
        self.shadowY = self.ballY
        self.velX = self.velY = self.velZ = 0
        self.onTeebox = True
        self.strokes = 0
        self.holed = False
        self.aimAngle = 0

    def reset_for_hole(self, aimAngle):
        self.ballX, self.ballY = self.startX, self.startY
        self.ballZ = self.shadowY = 0
        self.velX = self.velY = self.velZ = 0
        self.onTeebox = True
        self.strokes = 0
        self.holed = False
        self.aimAngle = aimAngle


