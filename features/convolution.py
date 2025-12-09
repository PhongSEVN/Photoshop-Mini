import numpy as np

def get_sample_matrices():
    I = np.array([
        [10, 10, 10, 0, 0],
        [10, 10, 10, 0, 0],
        [10, 10, 10, 0, 0],
        [10, 10, 10, 0, 0],
        [10, 10, 10, 0, 0]
    ], dtype=int)
    
    K = np.ones((3, 3), dtype=int)
    
    return I, K

def convolve_step(image, kernel):
    h_i, w_i = image.shape
    h_k, w_k = kernel.shape
    
    pad_h = h_k // 2
    pad_w = w_k // 2
    
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    output = np.zeros_like(image)
    
    for i in range(h_i):
        for j in range(w_i):
            region = padded_image[i:i+h_k, j:j+w_k]
            val = np.sum(region * kernel)
            output[i, j] = val
            
    return output

def manual_verification(image, kernel, center_x=2, center_y=2):
    h, w = kernel.shape
    pad_h = h // 2
    pad_w = w // 2
    
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    region = padded[center_x:center_x+h, center_y:center_y+w]
    
    result_val = np.sum(region * kernel)
    
    formula_parts = []
    flat_region = region.flatten()
    flat_kernel = kernel.flatten()
    
    for i in range(len(flat_region)):
        formula_parts.append(f"{flat_region[i]}*{flat_kernel[i]}")
        
    formula_str = " + ".join(formula_parts)
    full_str = f"I({center_x+1},{center_y+1}) = {formula_str} = {result_val}"
    
    return result_val, full_str
