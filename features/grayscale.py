from PIL import Image

def apply_grayscale(img):
    # print("Check Grayscale")
    return img.convert("L").convert("RGBA") # Func L chuyển về kênh xám sau đó lại chuyển về RGBA
