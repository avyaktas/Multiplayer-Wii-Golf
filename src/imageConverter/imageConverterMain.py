'''N.B., a marginal amoung this code is sourced was sourced from co-pilot,
more details are available on particular lines. -tommy''' 
import numpy as np
import cv2 as cv # OpenCV library for image processing
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
from imageConverter import pixelateImage # all just simple imports 

class PixelGolfApp: # Opens the main application window for the conversion
    def __init__(self, grand):
        self.grand = grand
        grand.title("Pixel Golf Image Converter")

        self.label = Label(grand, text="Upload a golf course image to pixelate:")
        self.label.pack()

        self.uploadButton = Button(grand, text="Upload Image", command=self.uploadImage)
        self.uploadButton.pack()

        self.processButton = Button(grand, text="Process Image", command=self.processImage)
        self.processButton.pack()

        self.imageLabel = Label(grand)
        self.imageLabel.pack()

        self.imagePath = None

    def uploadImage(self):
        self.imagePath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.imagePath:
            self.displayImage(self.imagePath)

    def displayImage(self, path):
        img = Image.open(path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        imgTinker = ImageTk.PhotoImage(img)
        self.imageLabel.config(image=imgTinker)
        self.imageLabel.image = imgTinker

    def processImage(self):
        if self.imagePath:
            # Call pixelateImage with the file path and pixel size
            pixelatedImage = pixelateImage(self.imagePath, pixelSize=10)
            
            # Save the pixelated image to a temporary file
            tempPath = "temp_pixelated_image.jpg"
            cv.imwrite(tempPath, pixelatedImage)
            
            # Display the pixelated image
            self.displayImage(tempPath)

if __name__ == "__main__":
    root = Tk()
    app = PixelGolfApp(root)
    root.mainloop()