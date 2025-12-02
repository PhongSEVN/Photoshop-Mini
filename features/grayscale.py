from PIL import Image

def apply_grayscale(img):
    return img.convert("L").convert("RGBA")
