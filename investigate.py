import transformers
import sys
import os

print("--- PYTHON INVESTIGATION REPORT ---")
try:
    print(f"Transformers Version: {transformers.__version__}")
    print(f"Loading From File:    {transformers.__file__}")
except Exception as e:
    print(f"Could not import transformers: {e}")

print("\n--- Python Executable ---")
print(sys.executable)

print("\n--- System Path (Where Python is searching) ---")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

print("\n--- PYTHONPATH Environment Variable ---")
print(os.environ.get('PYTHONPATH', '*** NOT SET ***'))
print("---------------------------------")