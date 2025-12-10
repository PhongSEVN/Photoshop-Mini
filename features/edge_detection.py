import numpy as np
from features import convolution

def apply_sobel(image, threshold=None):
    # Sobel kernels
    Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    # Calculate derivatives using my_convolution
    Ix = convolution.my_convolution(image, Gx)
    Iy = convolution.my_convolution(image, Gy)
    
    # Combine (Gradient magnitude)
    magnitude = np.sqrt(Ix**2 + Iy**2)
    
    # Apply Threshold if provided
    if threshold is not None:
        result = np.where(magnitude > threshold, 255, 0).astype(np.uint8)
    else:
        # Normalize to 0-255
        result = np.clip(magnitude, 0, 255).astype(np.uint8)
        
    return result

def apply_prewitt(image, threshold=None):
    # Prewitt kernels
    Gx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    Gy = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    
    Ix = convolution.my_convolution(image, Gx)
    Iy = convolution.my_convolution(image, Gy)
    
    magnitude = np.sqrt(Ix**2 + Iy**2)
    
    if threshold is not None:
        result = np.where(magnitude > threshold, 255, 0).astype(np.uint8)
    else:
        result = np.clip(magnitude, 0, 255).astype(np.uint8)
    return result

def apply_roberts(image, threshold=None):
    # Robert kernels (2x2)
    Gx = np.array([[1, 0], [0, -1]])
    Gy = np.array([[0, 1], [-1, 0]])
    
    Ix = convolution.my_convolution(image, Gx)
    Iy = convolution.my_convolution(image, Gy)
    
    magnitude = np.sqrt(Ix**2 + Iy**2)
    
    if threshold is not None:
        result = np.where(magnitude > threshold, 255, 0).astype(np.uint8)
    else:
        result = np.clip(magnitude, 0, 255).astype(np.uint8)
    return result

def apply_kirsch(image, threshold=None):
    # 8 Kirsh kernels
    kernels = [
        np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),   # North
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),   # North West
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),   # West
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),   # South West
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),   # South
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),   # South East
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),   # East
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])    # North East
    ]
    
    results = []
    for k in kernels:
        res = convolution.my_convolution(image, k)
        results.append(res)
        
    # Take max response across all directions
    max_response = np.max(np.stack(results), axis=0)
    
    if threshold is not None:
        result = np.where(max_response > threshold, 255, 0).astype(np.uint8)
    else:
        result = np.clip(max_response, 0, 255).astype(np.uint8)
    return result
