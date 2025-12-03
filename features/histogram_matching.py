import numpy as np
from PIL import Image


def _match_channel(src_arr, ref_arr):
    """Match histogram cho 1 kênh (0-255)."""
    hist_src, _ = np.histogram(src_arr.flatten(), bins=256, range=[0, 256])
    hist_ref, _ = np.histogram(ref_arr.flatten(), bins=256, range=[0, 256])

    cdf_src = np.cumsum(hist_src) / src_arr.size
    cdf_ref = np.cumsum(hist_ref) / ref_arr.size

    mapping = np.zeros(256, dtype=np.uint8)
    j = 0
    for i in range(256):
        while j < 255 and cdf_ref[j] < cdf_src[i]:
            j += 1
        mapping[i] = j
    return mapping[src_arr]


def histogram_matching(src_img, ref_img):
    """
    src_img: ảnh nguồn (PIL RGB/RGBA hoặc L)
    ref_img: ảnh tham chiếu (PIL RGB/RGBA hoặc L)
    return: ảnh sau khi khớp histogram, giữ màu (PIL RGBA)
    """
    # Chuẩn hoá RGB 3 kênh
    src_rgb = src_img.convert("RGB")
    ref_rgb = ref_img.convert("RGB")

    src_channels = [np.array(ch) for ch in src_rgb.split()]
    ref_channels = [np.array(ch) for ch in ref_rgb.split()]

    matched_channels = [_match_channel(s, r) for s, r in zip(src_channels, ref_channels)]

    matched_rgb = Image.merge(
        "RGB",
        [Image.fromarray(mc.astype(np.uint8), mode="L") for mc in matched_channels]
    )
    return matched_rgb.convert("RGBA")
