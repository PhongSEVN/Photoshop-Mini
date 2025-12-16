import numpy as np

def DFT_Fourier(image):
    """
    Thực hiện biến đổi DFT 2D thủ công.
    Để tối ưu, sử dụng tính chất tách biến (Separability):
    DFT 2D có thể tính bằng cách:
    1. Tính DFT 1D cho từng hàng.
    2. Tính DFT 1D cho từng cột của kết quả bước 1.
    Hoặc dùng ma trận transform: F = W_M . I . W_N
    """
    image = np.array(image, dtype=float)
    M, N = image.shape
    
    # Tạo ma trận DFT cho hàng và cột
    
    # Ma trận W_M (M x M): W_M[u, x] = exp(-j * 2*pi * u * x / M)
    x = np.arange(M)
    u = np.arange(M)
    # Outer product for grid
    U, X = np.meshgrid(u, x, indexing='ij')
    W_M = np.exp(-1j * 2 * np.pi * U * X / M)
    
    # Ma trận W_N (N x N): W_N[y, v] = exp(-j * 2*pi * y * v / N)
    v = np.arange(N)
    y = np.arange(N)
    V, Y = np.meshgrid(v, y, indexing='ij')
    W_N = np.exp(-1j * 2 * np.pi * Y * V / N)
    
    y = np.arange(N).reshape(-1, 1) # col vector 0..N-1
    v = np.arange(N).reshape(1, -1) # row vector 0..N-1
    D_N = np.exp(-1j * 2 * np.pi * y * v / N)
    
    # Matrix for rows (M x M)
    # We need to sum over x.
    # F = W_M @ (I @ D_N)
    # Entry (u, x) -> exp(-j 2 pi u x / M)
    u = np.arange(M).reshape(-1, 1)
    x = np.arange(M).reshape(1, -1)
    W_M = np.exp(-1j * 2 * np.pi * u * x / M)
    
    F = W_M @ (image @ D_N)
    
    return F

def shifted(F):
    """
    Dịch chuyển tâm phổ:
    Chia F thành 4 góc phần tư và tráo đổi chéo.
    Q1 | Q2
    -------
    Q3 | Q4
    
    Result:
    Q4 | Q3
    -------
    Q2 | Q1
    """
    M, N = F.shape
    cM, cN = M // 2, N // 2
    
    F_shifted = np.zeros_like(F)
    
    # Q1 (Top-Left) -> Q4 (Bottom-Right)
    F_shifted[cM:, cN:] = F[:cM, :cN]
    
    # Q4 (Bottom-Right) -> Q1 (Top-Left)
    F_shifted[:cM, :cN] = F[cM:, cN:]
    
    # Q2 (Top-Right) -> Q3 (Bottom-Left)
    F_shifted[cM:, :cN] = F[:cM, cN:]
    
    # Q3 (Bottom-Left) -> Q2 (Top-Right)
    F_shifted[:cM, cN:] = F[cM:, :cN]
    
    return F_shifted
    

def F_shifted_transform(image):
    """
    Biến đổi Fourier kết hợp dịch chuyển tâm phổ bằng cách nhân (-1)^(x+y) trước.
    F_shifted(u,v) = DFT{ f(x,y) * (-1)^(x+y) }
    """
    image = np.array(image, dtype=float)
    M, N = image.shape
    
    # Create multiplication matrix (-1)^(x+y)
    x = np.arange(M).reshape(-1, 1)
    y = np.arange(N).reshape(1, -1)
    
    # (-1)^(x+y) = (-1)^x * (-1)^y
    # This creates a checkerboard pattern
    scaler = np.power(-1.0, x + y)
    
    processed_image = image * scaler
    
    # Apply standard DFT
    Fs2 = DFT_Fourier(processed_image)
    
    return Fs2

def compute_spectrum(F):
    """
    Tính ảnh phổ biên độ (Magnitude Spectrum) để hiển thị.
    Spectrum = log(1 + |F|)
    """
    # Magnitude
    mag = np.abs(F)
    # Log scale
    spectrum = np.log(1 + mag)
    
    # Normalize 0-255
    if spectrum.max() > 0:
        spectrum = spectrum / spectrum.max() * 255
    else:
        spectrum = spectrum * 0
        
    return spectrum.astype(np.uint8)

def I_shifted(F):
    """
    Dịch chuyển ngược (Inverse shift).
    Vì hàm shift là hoán đổi góc phần tư đối xứng qua tâm, nên inverse shift chính là shift.
    Shift(Shift(F)) = F
    """
    return shifted(F)

def IDFT_Fourier(F):
    """
    Biến đổi Fourier Ngược 2D (IDFT).
    f(x,y) = (1/MN) * sum_u sum_v F(u,v) * exp(j * 2pi * (ux/M + vy/N))
    """
    F = np.array(F, dtype=complex)
    M, N = F.shape
    
    # Ma trận IDFT cột (N x N)
    # D_inv[v, y] = exp(j * 2pi * v * y / N)
    v = np.arange(N).reshape(-1, 1)
    y = np.arange(N).reshape(1, -1)
    D_inv_N = np.exp(1j * 2 * np.pi * v * y / N)
    
    # Ma trận IDFT hàng (M x M)
    # W_inv[x, u] = exp(j * 2pi * x * u / M)
    x = np.arange(M).reshape(-1, 1)
    u = np.arange(M).reshape(1, -1)
    W_inv_M = np.exp(1j * 2 * np.pi * x * u / M)
    
    # IDFT = W_inv_M @ F @ D_inv_N
    # Note: F needs to be multiplied correctly.
    # Rows first: F @ D_inv_N (Sum over v) -> Result (u, y) ?? No.
    # D_inv_N is (N x N), entry (v, y). F is (M, N).
    # F @ D_inv_N gives sum_v F(u,v) * exp(...) -> result(u, y). Correct.
    
    # Then Cols: W_inv_M @ Result
    # W_inv_M is (M x M), entry (x, u). Result is (u, y).
    # W_inv_M @ Result gives sum_u exp(...) * Result(u,y) -> Final(x, y). Correct.
    
    reconstructed = W_inv_M @ (F @ D_inv_N)
    
    # Scale by 1/(MN)
    reconstructed = reconstructed / (M * N)
    
    # Return real part (assuming original image was real)
    return np.real(reconstructed)
