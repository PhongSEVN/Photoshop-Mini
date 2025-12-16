import numpy as np
from features import fourier
import traceback

def verify():
    print("--- Verifying DFT Features ---")
    
    # 1. Create dummy image (small 16x16)
    size = 16
    img_arr = np.zeros((size, size), dtype=float)
    img_arr[4:12, 4:12] = 255.0
    
    print("1. Image created.")
    
    try:
        # 2. Test DFT
        print("2. Testing DFT_Fourier...")
        F = fourier.DFT_Fourier(img_arr)
        
        # Verify against numpy fft
        F_np = np.fft.fft2(img_arr)
        
        # Note: DFT definitions can vary by scaling factor (1/MN).
        # Our implementation is sum sum f(x,y) exp... which matches numpy's unscaled definition?
        # Numpy: A_km = sum sum a_nm exp ...
        if np.allclose(F, F_np, atol=1e-5):
            print("   DFT matches np.fft.fft2")
        else:
            diff = np.max(np.abs(F - F_np))
            print(f"   DFT differs from np.fft.fft2. Max diff: {diff}")
            
        # 3. Test Shifted
        print("3. Testing shifted...")
        Fs1 = fourier.shifted(F)
        Fs1_np = np.fft.fftshift(F)
        if np.allclose(Fs1, Fs1_np, atol=1e-5):
            print("   shifted matches np.fft.fftshift")
        else:
             print("   shifted differs from np.fft.fftshift")
             
        # 4. Test Shifted Transform
        print("4. Testing F_shifted_transform...")
        Fs2 = fourier.F_shifted_transform(img_arr)
        
        # Fs2 should equal Fs1
        if np.allclose(Fs1, Fs2, atol=1e-5):
             print("   Fs1 (shifted F) == Fs2 (DFT of modulated img). Property holding.")
        else:
            diff = np.max(np.abs(Fs1 - Fs2))
            print(f"   Fs1 != Fs2. Max diff: {diff}")
            
        print("\nSUCCESS: DFT features ran.")
        
    except Exception as e:
        print(f"\nFAILED with Exception: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    verify()
