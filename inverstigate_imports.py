import sys
import os

print("--- STARTING IMPORT INVESTIGATION ---")
print("This will test which library is breaking your environment.")

def check_transformers():
    """
    A function to re-import transformers and check its version.
    """
    try:
        # We have to remove it from cache to force a re-import
        # This is the most important part
        if 'transformers' in sys.modules:
            del sys.modules['transformers']
            
        import transformers
        print(f"  > SUCCESS: Transformers {transformers.__version__} is loaded from: {transformers.__file__}\n")
    except Exception as e:
        print(f"  > FAILED to import transformers: {e}\n")

# --- Test 1 ---
print("--- 1. Checking baseline (clean) import ---")
check_transformers()

# --- Test 2 ---
print("--- 2. Importing json ---")
try:
    import json
    print("   > Imported json (standard library).")
    check_transformers()
except Exception as e:
    print(f"   > FAILED to import json: {e}\n")


# --- Test 3 ---
print("--- 3. Importing torch ---")
try:
    import torch
    print("   > Imported torch.")
    check_transformers()
except Exception as e:
    print(f"   > FAILED to import torch: {e}\n")

# --- Test 4 ---
print("--- 4. Importing random ---")
try:
    import random
    print("   > Imported random (standard library).")
    check_transformers()
except Exception as e:
    print(f"   > FAILED to import random: {e}\n")

# --- Test 5 ---
print("--- 5. Importing sklearn ---")
try:
    from sklearn.model_selection import train_test_split
    print("   > Imported sklearn.")
    check_transformers()
except Exception as e:
    print(f"   > FAILED to import sklearn: {e}\n")

# --- Test 6: The Final Test ---
print("--- 6. Importing TrainingArguments (THE FINAL TEST) ---")
try:
    from transformers import TrainingArguments
    print("  > SUCCESS: Successfully imported TrainingArguments.\n")
except TypeError as e:
    print(f"  > !!! FAILED !!! Got the original TypeError: {e}\n")
except Exception as e:
    print(f"  > !!! FAILED !!! Got a different error: {e}\n")

print("--- INVESTIGATION COMPLETE ---")