def pixelate_image(image, pixel_size):
    height, width = image.shape[:2]
    # Resize the image to a smaller size
    temp = cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
    # Resize it back to original size
    pixelated = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return pixelated

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Image not found!")
    return image

def save_image(image, output_path):
    cv2.imwrite(output_path, image)