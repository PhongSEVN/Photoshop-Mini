import numpy as np
from PIL import Image
from tkinter import messagebox


def apply_pixel_transform(original_image, has_alpha, op: str, c: float, base: float, gamma: float):
    """Áp dụng biến đổi pixel: invert, log, invlog, gamma"""
    if original_image is None:
        messagebox.showwarning("Chưa có ảnh", "Hãy tải ảnh trước.")
        return None

    img = original_image.convert("RGB")
    arr = np.array(img, dtype=float)
    out = np.zeros_like(arr)

    for ch in range(3):
        r = arr[:, :, ch]

        if op == "invert":
            s = 255 - r

        elif op == "log":
            x = r / 255
            if base <= 0 or base == 1:
                messagebox.showerror("Lỗi", "Cơ số log không hợp lệ.")
                return None
            ln = np.log(1 + x)
            s = c * (ln / np.log(base))
            s = (s - s.min()) / (s.max() - s.min()) * 255

        elif op == "invlog":
            x = r / 255
            s = base ** (x / c) - 1
            s = (s - s.min()) / (s.max() - s.min()) * 255

        elif op == "gamma":
            x = r / 255
            s = (x ** gamma) * 255

        out[:, :, ch] = s

    out = np.clip(out, 0, 255).astype(np.uint8)

    if has_alpha:
        alpha = np.array(original_image.split()[3])
        result = Image.fromarray(out, "RGB").convert("RGBA")
        result.putalpha(Image.fromarray(alpha))
    else:
        result = Image.fromarray(out, "RGB").convert("RGBA")

    return result
