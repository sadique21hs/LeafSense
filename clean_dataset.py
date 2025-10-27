from PIL import Image
import os

# Paths to your training and testing folders inside D:\ai\leafSense
folders = [
    r"D:\ai\leafSense\Plant Village Dataset\Train",
    r"D:\ai\leafSense\Plant Village Dataset\Test"
]

for folder in folders:
    print(f"🔍 Checking folder: {folder}")
    for subdir, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(subdir, file)
            try:
                # Try to open and verify the image
                with Image.open(path) as img:
                    img.verify()
            except Exception:
                print("❌ Removing corrupted file:", path)
                os.remove(path)

print("✅ Dataset cleaning complete!")
