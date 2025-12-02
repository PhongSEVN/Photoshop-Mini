import numpy as np
from PIL import Image
from tkinter import messagebox


def contrast_stretch_linear(arr, r_min, r_max):
    """Kéo dãn độ tương phản tuyến tính"""
    arr = arr.astype(float)

    # tránh chia cho 0
    if r_max <= r_min:
        return arr

    out = (arr - r_min) * (255.0 / (r_max - r_min))

    # pixel < r_min → 0
    out[arr < r_min] = 0

    # pixel > r_max → 255
    out[arr > r_max] = 255

    return np.clip(out, 0, 255)


def contrast_stretch_piecewise(arr, r_min, r_max, l0=50, l1=200):
    """Kéo dãn độ tương phản từng phần"""
    arr = arr.astype(float)
    out = np.zeros_like(arr)

    # tối
    mask1 = arr <= r_min
    out[mask1] = (arr[mask1] / r_min) * l0

    # giữa
    mask2 = (arr > r_min) & (arr <= r_max)
    out[mask2] = ((arr[mask2] - r_min) / (r_max - r_min)) * (l1 - l0) + l0

    # sáng
    mask3 = arr > r_max
    out[mask3] = ((arr[mask3] - r_max) / (255 - r_max)) * (255 - l1) + l1

    return np.clip(out, 0, 255)


def apply_contrast_stretch(original_image, mode, r_min, r_max, l0, l1):
    """Áp dụng kéo dãn độ tương phản"""
    if original_image is None:
        messagebox.showwarning("Lỗi", "Chưa có ảnh!")
        return None

    img = original_image.convert("RGB")
    arr = np.array(img, float)
    out = np.zeros_like(arr)

    for ch in range(3):
        channel = arr[:, :, ch]
        if mode == "linear":
            out[:, :, ch] = contrast_stretch_linear(channel, r_min, r_max)
        else:
            out[:, :, ch] = contrast_stretch_piecewise(channel, r_min, r_max, l0, l1)

    out = np.clip(out, 0, 255).astype(np.uint8)
    result = Image.fromarray(out, "RGB").convert("RGBA")

    return result
