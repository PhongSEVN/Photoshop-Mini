import numpy as np
from PIL import Image
import os


def get_gray_matrix(image):
    """Chuyển ảnh sang ảnh xám và trả về ma trận mức xám"""
    if image is None:
        return None
    
    gray = image.convert("L")
    return np.array(gray, dtype=np.uint8)


def get_color_channels(image):
    """Tách ảnh màu thành 3 kênh R, G, B"""
    if image is None:
        return None, None, None
    
    rgb = image.convert("RGB")
    r, g, b = rgb.split()
    return np.array(r, dtype=np.uint8), np.array(g, dtype=np.uint8), np.array(b, dtype=np.uint8)


def is_color_image(image):
    """Kiểm tra xem ảnh có phải ảnh màu không"""
    if image is None:
        return False
    return image.mode in ('RGB', 'RGBA', 'P')


def save_matrix_to_txt(matrix, filename="image_matrix.txt", channel_name=""):
    """Lưu ma trận ảnh ra file txt"""
    if matrix is None:
        return None
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            h, w = matrix.shape
            channel_label = f" - Kênh {channel_name}" if channel_name else ""
            f.write(f"Ma trận ảnh I ({h}x{w}){channel_label}:\n")
            f.write("=" * 50 + "\n")
            for y in range(h):
                row = ' '.join(str(int(matrix[y, x])) for x in range(w))
                f.write(row + "\n")
        return filename
    except Exception as e:
        return None


def save_rgb_matrix_to_txt(r_matrix, g_matrix, b_matrix, filename="image_matrix_rgb.txt"):
    """Lưu ma trận RGB sau khi xử lý vào 1 file"""
    if r_matrix is None or g_matrix is None or b_matrix is None:
        return None
    
    try:
        h, w = r_matrix.shape
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Ma trận ảnh RGB sau khi cân bằng histogram ({h}x{w}):\n")
            f.write("=" * 70 + "\n")
            f.write("Định dạng: Mỗi pixel được biểu diễn dưới dạng (R, G, B)\n")
            f.write("=" * 70 + "\n\n")
            
            for y in range(h):
                row_parts = []
                for x in range(w):
                    r_val = int(r_matrix[y, x])
                    g_val = int(g_matrix[y, x])
                    b_val = int(b_matrix[y, x])
                    row_parts.append(f"({r_val:3d},{g_val:3d},{b_val:3d})")
                f.write(' '.join(row_parts) + "\n")
        return filename
    except Exception as e:
        return None


def step1_count_pixels(matrix):
    """Bước 1: Thống kê số lượng pixel nk cho từng mức xám rk (0-255)"""
    if matrix is None:
        return None
    
    nk = np.zeros(256, dtype=np.int32)
    h, w = matrix.shape
    
    for y in range(h):
        for x in range(w):
            gray_level = int(matrix[y, x])
            nk[gray_level] += 1
    
    return nk


def step2_calculate_cdf(nk, total_pixels):
    """Bước 2: Tính hàm phân bố tích lũy (cdf)"""
    if nk is None:
        return None
    
    cdf = np.zeros(256, dtype=np.float64)
    cdf[0] = nk[0] / total_pixels
    
    for k in range(1, 256):
        cdf[k] = cdf[k-1] + (nk[k] / total_pixels)
    
    return cdf


def step3_calculate_output_levels(cdf):
    """Bước 3: Tính các mức xám đầu ra sk"""
    if cdf is None:
        return None
    
    sk = np.zeros(256, dtype=np.uint8)
    for k in range(256):
        sk[k] = np.round(cdf[k] * 255).astype(np.uint8)
    
    return sk


def step4_count_output_pixels(nk, sk):
    """Bước 4: Tính số lượng pixel cho các mức xám sk"""
    if nk is None or sk is None:
        return None
    
    nk_new = np.zeros(256, dtype=np.int32)
    
    for k in range(256):
        s_value = sk[k]
        nk_new[s_value] += nk[k]
    
    return nk_new


def step5_create_equalized_image(matrix, sk):
    """Tạo ảnh mới bằng cách thay thế các giá trị cũ rk bằng sk"""
    if matrix is None or sk is None:
        return None
    
    h, w = matrix.shape
    new_matrix = np.zeros_like(matrix, dtype=np.uint8)
    
    for y in range(h):
        for x in range(w):
            old_value = int(matrix[y, x])
            new_matrix[y, x] = sk[old_value]
    
    return Image.fromarray(new_matrix, mode='L').convert("RGBA")


def step5_create_equalized_color_image(r_matrix, g_matrix, b_matrix, r_sk, g_sk, b_sk):
    """Tạo ảnh màu mới bằng cách cân bằng từng kênh"""
    if r_matrix is None or g_matrix is None or b_matrix is None:
        return None
    if r_sk is None or g_sk is None or b_sk is None:
        return None
    
    h, w = r_matrix.shape
    r_new = np.zeros_like(r_matrix, dtype=np.uint8)
    g_new = np.zeros_like(g_matrix, dtype=np.uint8)
    b_new = np.zeros_like(b_matrix, dtype=np.uint8)
    
    for y in range(h):
        for x in range(w):
            r_old = int(r_matrix[y, x])
            g_old = int(g_matrix[y, x])
            b_old = int(b_matrix[y, x])
            
            r_new[y, x] = r_sk[r_old]
            g_new[y, x] = g_sk[g_old]
            b_new[y, x] = b_sk[b_old]
    
    # Merge các kênh lại
    r_img = Image.fromarray(r_new, mode='L')
    g_img = Image.fromarray(g_new, mode='L')
    b_img = Image.fromarray(b_new, mode='L')
    
    return Image.merge("RGB", (r_img, g_img, b_img)).convert("RGBA"), r_new, g_new, b_new


def format_step_results(nk, cdf, sk, nk_new, total_pixels, channel_name=""):
    """Định dạng kết quả các bước để hiển thị"""
    lines = []
    channel_label = f" - Kênh {channel_name}" if channel_name else ""
    lines.append("=" * 60)
    lines.append(f"BƯỚC 1: Thống kê số lượng pixel nk cho từng mức xám rk{channel_label}")
    lines.append("=" * 60)
    lines.append("Mức xám (rk) | Số lượng pixel (nk)")
    lines.append("-" * 40)
    
    # Hiển thị một số mức xám mẫu (0, 50, 100, 150, 200, 255)
    sample_levels = [0, 50, 100, 150, 200, 255]
    for rk in sample_levels:
        lines.append(f"     {rk:3d}      |      {nk[rk]:8d}")
    lines.append("...")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"BƯỚC 2: Hàm phân bố tích lũy (CDF){channel_label}")
    lines.append("=" * 60)
    lines.append("Mức xám (rk) | CDF(rk)")
    lines.append("-" * 40)
    for rk in sample_levels:
        lines.append(f"     {rk:3d}      |  {cdf[rk]:.6f}")
    lines.append("...")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"BƯỚC 3: Các mức xám đầu ra sk{channel_label}")
    lines.append("=" * 60)
    lines.append("Mức xám cũ (rk) | Mức xám mới (sk)")
    lines.append("-" * 40)
    for rk in sample_levels:
        lines.append(f"      {rk:3d}       |       {sk[rk]:3d}")
    lines.append("...")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"BƯỚC 4: Số lượng pixel cho các mức xám sk mới{channel_label}")
    lines.append("=" * 60)
    lines.append("Mức xám (sk) | Số lượng pixel (nk_new)")
    lines.append("-" * 40)
    
    # Tìm các mức xám sk có pixel
    sk_with_pixels = []
    for s in range(256):
        if nk_new[s] > 0:
            sk_with_pixels.append(s)
    
    # Hiển thị một số mức xám mẫu
    sample_sk = sk_with_pixels[:10] if len(sk_with_pixels) >= 10 else sk_with_pixels
    for s in sample_sk:
        lines.append(f"     {s:3d}      |        {nk_new[s]:8d}")
    if len(sk_with_pixels) > 10:
        lines.append("...")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"THỐNG KÊ TỔNG QUAN{channel_label}")
    lines.append("=" * 60)
    lines.append(f"Tổng số pixel: {total_pixels}")
    lines.append(f"Số mức xám được sử dụng (trước): {np.count_nonzero(nk)}")
    lines.append(f"Số mức xám được sử dụng (sau): {np.count_nonzero(nk_new)}")
    
    return "\n".join(lines)


def format_color_step_results(r_results, g_results, b_results):
    """Định dạng kết quả cho ảnh màu (gộp 3 kênh)"""
    lines = []
    lines.append("=" * 70)
    lines.append("CÂN BẰNG HISTOGRAM CHO ẢNH MÀU (Xử lý từng kênh R, G, B)")
    lines.append("=" * 70)
    lines.append("")
    lines.append("KÊNH MÀU ĐỎ (R):")
    lines.append("-" * 70)
    lines.append(r_results)
    lines.append("")
    lines.append("=" * 70)
    lines.append("KÊNH MÀU XANH LÁ (G):")
    lines.append("-" * 70)
    lines.append(g_results)
    lines.append("")
    lines.append("=" * 70)
    lines.append("KÊNH MÀU XANH DƯƠNG (B):")
    lines.append("-" * 70)
    lines.append(b_results)
    
    return "\n".join(lines)


def calculate_histogram_data(matrix):
    """Tính toán dữ liệu histogram cho việc vẽ biểu đồ"""
    if matrix is None:
        return None
    
    nk = step1_count_pixels(matrix)
    return nk
