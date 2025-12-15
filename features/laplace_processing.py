import numpy as np
from features import convolution, edge_detection

def get_kernels():
    # Laplace Kernels
    # 4-neighbor (Center -4)
    laplace4n_neg = np.array([[0, 1, 0], 
                              [1, -4, 1], 
                              [0, 1, 0]])
    
    # 8-neighbor (Center -8)
    laplace8n_neg = np.array([[1, 1, 1], 
                              [1, -8, 1], 
                              [1, 1, 1]])
    
    # Opposite signs for 9.4 Sharpening
    laplace4n_pos = np.array([[0, -1, 0], 
                              [-1, 4, -1], 
                              [0, -1, 0]])
                              
    laplace8n_pos = np.array([[-1, -1, -1], 
                              [-1, 8, -1], 
                              [-1, -1, -1]])
                              
    # 1 2 1
    # 2 4 2
    # 1 2 1 (/16)
    gaussian_3x3 = np.array([[1, 2, 1], 
                             [2, 4, 2], 
                             [1, 2, 1]]) / 16.0
                             
    return {
        'laplace4n_neg': laplace4n_neg,
        'laplace8n_neg': laplace8n_neg,
        'laplace4n_pos': laplace4n_pos,
        'laplace8n_pos': laplace8n_pos,
        'gaussian': gaussian_3x3
    }

def apply_laplace(image, method='4n_neg'):

    kernels = get_kernels()
    k_name = f'laplace{method}'
    kernel = kernels.get(k_name)
    
    if kernel is None:
        raise ValueError(f"Unknown method {method}")
        
    # Convolve
    # my_convolution returns float or int usually, need to handle
    conv_res = convolution.my_convolution(image, kernel)
    
    abs_res = np.abs(conv_res)
    
    result = np.clip(abs_res, 0, 255).astype(np.uint8)
    
    return result

def apply_gaussian_smooth(image):
    kernels = get_kernels()
    kernel = kernels['gaussian']
    
    res = convolution.my_convolution(image, kernel)
    res = np.clip(res, 0, 255).astype(np.uint8)
    return res

def apply_log(image, method='4n_neg'):

    smooth = apply_gaussian_smooth(image)
    
    res = apply_laplace(smooth, method)
    return res

def apply_smooth_sobel(image):

    smooth = apply_gaussian_smooth(image)
    res = edge_detection.apply_sobel(smooth)
    return res

def apply_sharpening(image, method='4n_neg'):
    kernels = get_kernels()
    k_name = f'laplace{method}'
    kernel = kernels.get(k_name)
    
    # Raw convolution result (can be negative)
    laplace_res = convolution.my_convolution(image, kernel)
    
    img_float = image.astype(float)
    
    if 'neg' in method:
        # Subtract
        sharpened = img_float - laplace_res
    else:
        # Add
        sharpened = img_float + laplace_res
        
    result = np.clip(sharpened, 0, 255).astype(np.uint8)
    return result
