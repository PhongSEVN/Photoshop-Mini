from PIL import Image

def extract_red(img):
    # Chuyển ảnh sang RGB
    rgb = img.convert("RGB")

    # Tách ảnh sang 3 kênh màu
    r, g, b = rgb.split()

    # Tạo ảnh đen
    zero = Image.new("L", r.size, 0)
    
    # Trả về ảnh chỉ kênh đỏ bằng cách set 2 kênh xanh là 0
    return Image.merge("RGB", (r, zero, zero)).convert("RGBA")
