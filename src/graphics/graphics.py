'''this file will have all the graphics related code, we can make another 
for scanning the courses however, this will just contain the style which the
user will see following the conversion. -tommy'''
import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
from imageConverter import pixelate_image

class PixelGolfApp:
    def __init__(self, master):
        self.master = master
        master.title("Pixel Golf Image Converter")

        self.label = Label(master, text="Upload a golf course image to pixelate:")
        self.label.pack()

        self.upload_button = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.process_button = Button(master, text="Process Image", command=self.process_image)
        self.process_button.pack()

        self.image_label = Label(master)
        self.image_label.pack()

        self.image_path = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.display_image(self.image_path)

    def display_image(self, path):
        image = Image.open(path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def process_image(self):
        if self.image_path:
            pixelated_image = pixelate_image(self.image_path)
            self.display_image(pixelated_image)

if __name__ == "__main__":
    root = Tk()
    app = PixelGolfApp(root)
    root.mainloop()