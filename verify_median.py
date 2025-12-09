
import sys
import os
import numpy as np
from PIL import Image

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from features import noise
    print("Successfully imported noise module")
except ImportError as e:
    print(f"Failed to import noise module: {e}")
    sys.exit(1)

def verify():
    print("--- Verifying Median vs Average Filter ---")
    
    # 1. Create a dummy image (constant color) with Noise
    img = Image.new('L', (100, 100), color=128)
    noisy_img = noise.add_salt_and_pepper_noise(img, salt_ratio=0.1, pepper_ratio=0.1) # Heavy noise
    arr_noisy = np.array(noisy_img)
    print(f"Noisy image std dev: {np.std(arr_noisy)}")

    # 2. Apply Filters
    avg_3 = noise.apply_average_filter(noisy_img, 3)
    median_3 = noise.apply_median_filter(noisy_img, 3)
    
    avg_5 = noise.apply_average_filter(noisy_img, 5)
    median_5 = noise.apply_median_filter(noisy_img, 5)

    # 3. Check specific pixel (if possible) or statistics
    # Salt & Pepper noise creates 0 and 255. 
    # Median filter should completely remove them if density is low enough.
    # Average filter will smear them.
    
    arr_avg_3 = np.array(avg_3)
    arr_median_3 = np.array(median_3)
    
    # Check if median has fewer extreme values than average
    # Extreme values in original were 0 and 255. 
    # Average will have values slightly away from 128 but not 0/255 usually, but smeared.
    # Median should be very close to 128 everywhere.
    
    std_avg_3 = np.std(arr_avg_3)
    std_median_3 = np.std(arr_median_3)
    
    print(f"Avg 3x3 std dev: {std_avg_3}")
    print(f"Median 3x3 std dev: {std_median_3}")
    
    if std_median_3 < std_avg_3:
        print("SUCCESS: Median 3x3 has lower variance than Average 3x3 (removed noise better)")
    else:
        print("FAIL: Median 3x3 failed to outperform Average 3x3")
        
    std_avg_5 = np.std(np.array(avg_5))
    std_median_5 = np.std(np.array(median_5))
    
    print(f"Avg 5x5 std dev: {std_avg_5}")
    print(f"Median 5x5 std dev: {std_median_5}")
    
    if std_median_5 < std_avg_5:
        print("SUCCESS: Median 5x5 has lower variance than Average 5x5")
    else:
        print("FAIL: Median 5x5 failed to outperform Average 5x5")

if __name__ == "__main__":
    verify()
