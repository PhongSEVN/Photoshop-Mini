from PIL import Image

def extract_red(img):
    rgb = img.convert("RGB")
    r, g, b = rgb.split()
    zero = Image.new("L", r.size, 0)
    return Image.merge("RGB", (r, zero, zero)).convert("RGBA")
