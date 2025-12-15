import numpy as np
from PIL import Image
from features import laplace_processing
import traceback

def verify():
    print("Verifying Laplace Features")
    
    img_arr = np.zeros((100, 100), dtype=np.uint8)
    img_arr[30:70, 30:70] = 200
    
    print("Image created.")
    
    try:
        print("Testing Laplace 9.1...")
        res4n = laplace_processing.apply_laplace(img_arr, '4n_neg')
        if res4n.dtype != np.uint8:
            print(f"FAILED: res4n dtype is {res4n.dtype}")
        else:
            print("   Laplace 4n_neg OK")
            
        res8n = laplace_processing.apply_laplace(img_arr, '8n_neg')
        if res8n.dtype != np.uint8:
             print(f"FAILED: res8n dtype is {res8n.dtype}")
        else:
            print("   Laplace 8n_neg OK")
            
        print("Testing LoG 9.2...")
        log_res = laplace_processing.apply_log(img_arr, '4n_neg')
        print("   LoG OK")
        
        print("Test Smooth Sobel 9.3")
        print("Testing Smooth Sobel 9.3...")
        sog_res = laplace_processing.apply_smooth_sobel(img_arr)
        print("   Smooth Sobel OK")
        
        print("Testing Sharpen 9.4...")
        s1 = laplace_processing.apply_sharpening(img_arr, '4n_neg')
        s2 = laplace_processing.apply_sharpening(img_arr, '8n_neg')
        s3 = laplace_processing.apply_sharpening(img_arr, '4n_pos')
        s4 = laplace_processing.apply_sharpening(img_arr, '8n_pos')
        print("   Sharpen OK")
        
        print("\nSUCCESS: All Laplace features ran without exception.")
        
    except Exception as e:
        print(f"\nFAILED with Exception: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    verify()
