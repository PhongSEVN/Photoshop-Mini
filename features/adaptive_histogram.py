import numpy as np
from PIL import Image


def _box_sum(mat: np.ndarray, win: int) -> np.ndarray:
    """Tính tổng trên cửa sổ win x win bằng integral image; giữ đúng kích thước h x w."""
    pad = win // 2
    padded = np.pad(mat, pad_width=pad, mode="reflect")
    # integral với biên 0 ở trên/trái để dùng chỉ số offset 1
    integral = np.pad(padded, ((1, 0), (1, 0)), mode="constant", constant_values=0).cumsum(axis=0).cumsum(axis=1)

    h, w = mat.shape
    y1 = np.arange(win, win + h)
    x1 = np.arange(win, win + w)
    y0 = y1 - win
    x0 = x1 - win

    total = (
        integral[np.ix_(y1, x1)]
        - integral[np.ix_(y0, x1)]
        - integral[np.ix_(y1, x0)]
        + integral[np.ix_(y0, x0)]
    )
    return total


def _local_mean_var(gray: np.ndarray, win: int):
    """Tính trung bình và phương sai cục bộ cho mỗi pixel."""
    gray_f = gray.astype(np.float32)
    sum_local = _box_sum(gray_f, win)
    sum_sq_local = _box_sum(gray_f ** 2, win)
    area = float(win * win)
    mean = sum_local / area
    var = sum_sq_local / area - mean ** 2
    return mean, var


def adaptive_histogram_equalization(img, tile_size=3,
                                    k0=0.0, k1=0.25,
                                    k2=0.0, k3=0.1,
                                    C=50.0):
    """
    Cân bằng histogram cục bộ theo slide trên kênh độ sáng (Y), giữ màu:
      - Tính m, σ² toàn cục trên Y.
      - Với mỗi vùng UxV: tính m_s, σ_s².
      - Nếu k0*m <= m_s <= k1*m và k2*σ² <= σ_s² <= k3*σ² thì f'(x,y)=round(C*f(x,y)), ngược lại giữ nguyên.
      - Ghép lại với Cr/Cb gốc để giữ màu.
    """
    if tile_size < 3:
        tile_size = 3
    if tile_size % 2 == 0:
        tile_size += 1  # ép lẻ

    # Tách YCrCb
    ycc = img.convert("YCbCr")
    y, cb, cr = ycc.split()
    y_arr = np.array(y, dtype=np.float32)

    m_global = float(y_arr.mean())
    sigma2_global = float(((y_arr - m_global) ** 2).mean())

    mean_local, var_local = _local_mean_var(y_arr, tile_size)

    mask = (
        (mean_local >= k0 * m_global) & (mean_local <= k1 * m_global) &
        (var_local >= k2 * sigma2_global) & (var_local <= k3 * sigma2_global)
    )

    out_y = y_arr.copy()
    out_y[mask] = np.clip(np.round(C * out_y[mask]), 0, 255)
    out_y_img = Image.fromarray(out_y.astype(np.uint8), mode="L")

    merged = Image.merge("YCbCr", (out_y_img, cb, cr)).convert("RGB")
    return merged.convert("RGBA")
