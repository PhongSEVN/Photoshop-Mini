
import sys
import os
import numpy as np
from PIL import Image

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from features import noise
    print("Successfully imported noise module")
except ImportError as e:
    print(f"Failed to import noise module: {e}")
    sys.exit(1)

def verify():
    print("--- Verifying Noise and Average Filter ---")
    
    # 1. Create a dummy image (constant color)
    # 100x100 gray image
    img = Image.new('L', (100, 100), color=128)
    arr_orig = np.array(img)
    std_orig = np.std(arr_orig)
    print(f"Original image std dev: {std_orig}") # Should be 0
    
    # 2. Add Noise
    noisy_img = noise.add_salt_and_pepper_noise(img, salt_ratio=0.05, pepper_ratio=0.05)
    arr_noisy = np.array(noisy_img)
    std_noisy = np.std(arr_noisy)
    print(f"Noisy image std dev: {std_noisy}")
    
    if std_noisy > std_orig:
        print("SUCCESS: Noise increased variance")
    else:
        print("FAIL: Noise did not increase variance")
        return

    # 3. Filter 3x3
    filtered_3 = noise.apply_average_filter(noisy_img, size=3)
    arr_3 = np.array(filtered_3)
    std_3 = np.std(arr_3)
    print(f"Filtered 3x3 std dev: {std_3}")
    
    # 4. Filter 5x5
    filtered_5 = noise.apply_average_filter(noisy_img, size=5)
    arr_5 = np.array(filtered_5)
    std_5 = np.std(arr_5)
    print(f"Filtered 5x5 std dev: {std_5}")
    
    if std_3 < std_noisy:
        print("SUCCESS: 3x3 filter reduced noise (variance)")
    else:
        print(f"FAIL: 3x3 filter did not reduce variance significantly: {std_3} vs {std_noisy}")

    if std_5 < std_3:
        print("SUCCESS: 5x5 filter smoothed more than 3x3")
    else:
        print(f"FAIL: 5x5 filter did not smooth more than 3x3: {std_5} vs {std_3}")

if __name__ == "__main__":
    verify()
