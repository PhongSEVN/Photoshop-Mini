import numpy as np
from PIL import Image

def add_salt_and_pepper_noise(image, salt_ratio=0.02, pepper_ratio=0.02):
    if image.mode != 'L':
        image = image.convert('L')
    
    arr = np.array(image)
    noisy_arr = arr.copy()
    
    h, w = arr.shape
    num_pixels = h * w
    
    num_salt = int(num_pixels * salt_ratio)
    coords_salt = [np.random.randint(0, i - 1, num_salt) for i in arr.shape]
    noisy_arr[tuple(coords_salt)] = 255
    
    num_pepper = int(num_pixels * pepper_ratio)
    coords_pepper = [np.random.randint(0, i - 1, num_pepper) for i in arr.shape]
    noisy_arr[tuple(coords_pepper)] = 0
    
    return Image.fromarray(noisy_arr)

def apply_average_filter(image, size=3):
    if image.mode != 'L':
        image = image.convert('L')
        
    arr = np.array(image, dtype=float)
    h, w = arr.shape
    pad = size // 2
    
    padded = np.pad(arr, ((pad, pad), (pad, pad)), mode='reflect')
    output = np.zeros_like(arr)
    
    kernel_size = size * size
    
    for i in range(h):
        for j in range(w):
            region = padded[i:i+size, j:j+size]
            output[i, j] = np.sum(region) / kernel_size
            
    return Image.fromarray(output.astype(np.uint8))

def apply_median_filter(image, size=3):
    if image.mode != 'L':
        image = image.convert('L')
        
    arr = np.array(image, dtype=float)
    h, w = arr.shape
    pad = size // 2
    
    padded = np.pad(arr, ((pad, pad), (pad, pad)), mode='reflect')
    output = np.zeros_like(arr)
    
    for i in range(h):
        for j in range(w):
            region = padded[i:i+size, j:j+size]
            output[i, j] = np.median(region)
            
    return Image.fromarray(output.astype(np.uint8))
