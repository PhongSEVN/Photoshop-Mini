import numpy as np


def compute_metrics_from_array(arr: np.ndarray):
    """Tính 4 chỉ số: độ sáng, độ tương phản, entropy, độ sắc nét"""
    a = np.asarray(arr, dtype=float)

    mean = float(np.mean(a))
    contrast = float(np.std(a))

    vals = a.ravel()
    if np.issubdtype(a.dtype, np.integer) or np.all(np.mod(vals, 1) == 0):
        unique, counts = np.unique(vals, return_counts=True)
        probs = counts / counts.sum()
    else:
        counts, _ = np.histogram(vals, bins=256, range=(vals.min(), vals.max()))
        probs = counts / counts.sum()
    probs = probs[probs > 0]
    entropy = float(-(probs * np.log2(probs)).sum())

    # Laplacian
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], float)
    pad = np.pad(a, pad_width=1, mode='edge')

    h, w = a.shape
    gx = np.zeros_like(a)
    gy = np.zeros_like(a)

    for y in range(h):
        for x in range(w):
            region = pad[y:y+3, x:x+3]
            gx[y, x] = np.sum(region * sobel_x)
            gy[y, x] = np.sum(region * sobel_y)

    sharpness = float(np.mean(np.sqrt(gx**2 + gy**2)))

    return {
        "mean": mean,
        "contrast": contrast,
        "entropy": entropy,
        "sharpness": sharpness
    }


def format_metrics(name: str, metrics: dict):
    """Định dạng metrics để hiển thị"""
    return (
        f"{name}:\n"
        f"  • Độ sáng trung bình: {metrics['mean']:.4f}\n"
        f"  • Độ tương phản: {metrics['contrast']:.4f}\n"
        f"  • Entropy: {metrics['entropy']:.6f}\n"
        f"  • Độ sắc nét (Laplacian): {metrics['sharpness']:.6f}\n"
    )


def get_test_matrix():
    """Trả về ma trận M mẫu"""
    return np.array([
        [1,1,1,1,1,1,1,1,1,1],
        [1,2,2,3,1,1,1,7,2,1],
        [1,2,3,2,1,1,5,3,6,1],
        [1,3,2,2,1,1,0,4,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,1,1,1,1,1],
        [1,0,7,7,1,1,1,1,1,1],
        [1,0,7,7,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
    ], dtype=float)


def get_submatrices():
    """Trả về các ma trận con A, B, C"""
    M = get_test_matrix()
    A = M[1:4, 1:4]
    B = M[6:9, 1:4]
    C = M[1:4, 5:8]
    return A, B, C
