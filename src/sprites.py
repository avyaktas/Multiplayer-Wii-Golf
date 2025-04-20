import random as random_module
from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image, ImageDraw

def createOceanSprite():
    """
    Creates a CMUImage for the ocean sprite.
    """
    # Create a 16x16 pixel canvas for the sprite
    oceanCanvas = Image.new('RGBA', (16, 16), 'navy')  # Base color for the ocean

    # Draw a few small, irregular white ripples
    draw = ImageDraw.Draw(oceanCanvas)
    draw.arc((4, 6, 12, 10), start=0, end=180, fill='white', width=1)  # Ripple 1
    draw.arc((2, 8, 10, 12), start=0, end=180, fill='white', width=1)  # Ripple 2
    draw.point((6, 6), fill='white')  # Small highlight
    draw.point((10, 9), fill='white')  # Small highlight

    # Convert the canvas to a CMUImage
    return CMUImage(oceanCanvas)

def drawBackground(app):
    """
    Draws the ocean background with randomly placed waves.
    """
    for _ in range(100):  # Adjust the number of waves as needed
        x = random.randint(0, app.width - 16)  # Random x-coordinate
        y = random.randint(0, app.height - 16)  # Random y-coordinate
        drawImage(app.oceanSprite, x, y)

def onAppStart(app):
    """
    Initializes the app and creates the ocean sprite.
    """
    app.oceanSprite = createOceanSprite()

def redrawAll(app):
    """
    Redraws the entire screen.
    """
    drawBackground(app)  # Draw the ocean background

def main():
    runApp(width=800, height=600)

main()