from PIL import Image
from tkinter import messagebox


def get_alpha_info(original_image, original_mode, has_alpha):
    """Lấy thông tin và ma trận alpha"""
    if original_image is None:
        return None, None, None

    info_lines = []
    w, h = original_image.size
    info_lines.append(f"Kích thước: {w} x {h}")
    info_lines.append(f"Chế độ ban đầu: {original_mode}")
    info_lines.append(f"Có kênh Alpha: {has_alpha}")

    if not has_alpha:
        info_lines.append("")
        info_lines.append("Ảnh không có kênh Alpha")
        return None, '\n'.join(info_lines), None

    try:
        alpha = original_image.split()[3]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tách kênh Alpha:\n{e}")
        return None, None, None

    alpha_img_for_display = alpha.convert("L").convert("RGBA")

    max_cells = 2000
    total = w * h
    info_lines.append("")
    if total <= max_cells:
        info_lines.append("Ma trận Alpha (0-255) theo hàng:")
        pixels = list(alpha.getdata())
        for y in range(h):
            row = pixels[y * w:(y + 1) * w]
            info_lines.append(' '.join(str(p) for p in row))
    else:
        info_lines.append("Ảnh quá lớn để hiện ma trận đầy đủ. Hiển thị mẫu 10x10:")
        sample_w = min(10, w)
        sample_h = min(10, h)
        pixels = list(alpha.getdata())
        for y in range(sample_h):
            row = pixels[y * w:y * w + sample_w]
            info_lines.append(' '.join(str(p) for p in row))

    return alpha_img_for_display, '\n'.join(info_lines), None
