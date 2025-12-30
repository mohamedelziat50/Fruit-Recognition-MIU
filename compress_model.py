import joblib

print("Loading 2GB model...")
model = joblib.load('fruit_model.joblib')

print("Saving with compression...")
joblib.dump(model, 'fruit_model_compressed.joblib', compress=('gzip', 3))

import os
original = os.path.getsize('fruit_model.joblib')
compressed = os.path.getsize('fruit_model_compressed.joblib')
print(f"Original: {original/1e9:.1f} GB")
print(f"Compressed: {compressed/1e9:.1f} GB")
print(f"Reduction: {(1 - compressed/original)*100:.1f}%")