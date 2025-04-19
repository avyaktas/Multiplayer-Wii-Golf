import cv2

def pixelateImage(imagePath, pixelSize):
    image = cv2.imread(imagePath)
    if image is None:
        raise Exception("image not found!")
    height, width = image.shape[:2]
    # Resize the image to a smaller size
    temp = cv2.resize(image, (width // pixelSize, height // pixelSize), 
                      interpolation=cv2.INTER_LINEAR)
    # Resize it back to original size
    pixelated = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return pixelated

def loadImage(imagePath):
    image = cv2.imread(imagePath)
    if image is None:
        raise Exception("Image not found!")
    return image

if __name__ == "__main__":
    root = Tk()
    app = PixelGolfApp(root)
    root.mainloop()