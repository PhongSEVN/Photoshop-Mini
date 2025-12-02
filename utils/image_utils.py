from PIL import Image, ImageTk
import tkinter as tk


def resize_for_display(canvas, pil_image):
    """Resize image để hiển thị trên canvas"""
    w = canvas.winfo_width() or 800
    h = canvas.winfo_height() or 600
    img_w, img_h = pil_image.size
    ratio = min(w / img_w, h / img_h, 1.0)
    new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
    return pil_image.resize(new_size, Image.LANCZOS)


def check_alpha_channel(img):
    """Kiểm tra xem ảnh có kênh Alpha không"""
    try:
        return "A" in img.getbands()
    except Exception:
        return False

