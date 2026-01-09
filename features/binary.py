from PIL import Image


def apply_binary(gray_img, threshold):
    """Áp dụng ngưỡng nhị phân cho ảnh xám"""
    return gray_img.point(lambda p: 255 if p >= threshold else 0).convert("RGBA")
    # Nếu điểm ảnh p lớn hơn ngưỡng ngưỡng thì chuyển thành trắng (255), ngược lại chuyển thành đen (0)