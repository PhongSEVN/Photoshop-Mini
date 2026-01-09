
import sys
import os
import numpy as np

# Add parent directory to path so we can import features
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from features import convolution
    print("Successfully imported convolution module")
except ImportError as e:
    print(f"Failed to import convolution module: {e}")
    sys.exit(1)

def verify():
    print("--- Verifying Convolution Feature ---")
    
    # 1. Get sample matrices
    I, K = convolution.get_sample_matrices()
    print(f"I shape: {I.shape}")
    print(f"K shape: {K.shape}")
    
    if I.shape != (5, 5):
        print("FAIL: I should be 5x5")
        return
    if K.shape != (3, 3):
        print("FAIL: K should be 3x3")
        return

    # 2. Run convolution
    I_conv = convolution.my_convolution(I, K)
    print(f"I_conv shape: {I_conv.shape}")
    
    if I_conv.shape != (5, 5):
        print("FAIL: I_conv should be 5x5")
        return

    # 3. Manual verification check
    # Check center pixel (2, 2) (0-indexed) which corresponds to (3,3) 1-indexed
    # I at (2,2) is surrounded by 10s and 0s.
    # The sample matrix I has:
    # 10 10 10 0 0
    # 10 10 10 0 0
    # 10 10 10 0 0
    # 10 10 10 0 0
    # 10 10 10 0 0
    
    # At (2,2) (center of 5x5), the window is I[1:4, 1:4]
    # 10 10 0
    # 10 10 0
    # 10 10 0
    # Sum of these is 60.
    
    # Let's see what the code says
    val, text = convolution.manual_verification(I, K, 2, 2)
    print(f"Computed value at (2,2): {val}")
    print(f"Explanation text: {text}")
    
    if val == I_conv[2, 2]:
        print("SUCCESS: Manual verification matches I_conv result")
    else:
        print(f"FAIL: Manual {val} != I_conv {I_conv[2,2]}")

if __name__ == "__main__":
    verify()
