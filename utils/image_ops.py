from PIL import Image, ImageTk
import numpy as np

def resize_for_display(canvas, pil_image):
    w = canvas.winfo_width() or 800
    h = canvas.winfo_height() or 600

    iw, ih = pil_image.size
    ratio = min(w/iw, h/ih, 1.0)
    new_size = (max(1, int(iw*ratio)), max(1, int(ih*ratio)))

    return pil_image.resize(new_size, Image.LANCZOS)
