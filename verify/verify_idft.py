import numpy as np
from features import fourier
import traceback

def verify_idft():
    print("--- Verifying IDFT Features ---")
    
    # 1. Create dummy image (small 16x16)
    size = 16
    I = np.zeros((size, size), dtype=float)
    I[4:12, 4:12] = 255.0
    
    print("1. Image created.")
    
    try:
        # 2. Compute DFT
        print("2. Computing DFT & Shift...")
        F = fourier.DFT_Fourier(I)
        Fs1 = fourier.shifted(F)
        
        # 3. Test I_shifted
        print("3. Testing I_shifted (inverse shift)...")
        F_restored = fourier.I_shifted(Fs1)
        if np.allclose(F, F_restored, atol=1e-5):
             print("   I_shifted(Fs1) == F. OK.")
        else:
             print("   I_shifted failed.")
             
        # 4. Test IDFT
        print("4. Testing IDFT_Fourier(F)...")
        I1 = fourier.IDFT_Fourier(F)
        # Should match I
        if np.allclose(I, I1, atol=1e-5):
             print("   IDFT(F) == I. Perfect Reconstruction.")
        else:
             max_diff = np.max(np.abs(I - I1))
             print(f"   IDFT(F) != I. Max diff: {max_diff}")
        
        # 5. Test IDFT(Fs1) -> I2
        print("5. Testing IDFT_Fourier(Fs1)...")
        I2 = fourier.IDFT_Fourier(Fs1)
        
        # 6. Correct I2 -> I3
        M, N = I2.shape
        x = np.arange(M).reshape(-1, 1)
        y = np.arange(N).reshape(1, -1)
        scaler = np.power(-1.0, x + y)
        I3 = I2 * scaler
        
        # Check I3 vs I
        if np.allclose(I, I3, atol=1e-5):
             print("   I3 (corrected I2) == I. Modulation property confirmed.")
        else:
             max_diff = np.max(np.abs(I - I3))
             print(f"   I3 != I. Max diff: {max_diff}")
             
        print("\nSUCCESS: IDFT features verified.")
        
    except Exception as e:
        print(f"\nFAILED with Exception: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    verify_idft()
