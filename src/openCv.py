import cv2            # OpenCV’s Python bindings
import numpy as np    # For array manipulation
from tkinker import Tk  # For GUI
from tkinker.filedialog import askopenfilename  # For file dialog
from PIL import Image, ImageTk  # For image handling
image = cv2.imread('image.jpg')  # Load an image
if image == None:
    raise Exception("Image not found!")
