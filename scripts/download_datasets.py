import os
import urllib.request
import zipfile
import numpy as np
from PIL import Image, ImageDraw
import urllib.error

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PICSUM_GRAY_DIR = os.path.join(DATA_DIR, "picsum_gray")
PICSUM_COLOR_DIR = os.path.join(DATA_DIR, "picsum_color")
SYNTHETIC_DIR = os.path.join(DATA_DIR, "synthetic")

# URLs for datasets (using smaller subsets or direct links where possible)
# For benchmarking with 100 unique images, we use Lorem Picsum to generate unique images.
# Grayscale images and Color images proxies.
PICSUM_URL_GRAY = "https://picsum.photos/512/512?grayscale"
PICSUM_URL_COLOR = "https://picsum.photos/512/512"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def download_image(url, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading {url} to {save_path}...")
        try:
            import requests
            # Use stream=True and a small delay to avoid overwhelming the server
            response = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False
    else:
        print(f"File already exists: {save_path}")
        return True

def create_synthetic_images(num_images=5, size=(512, 512)):
    ensure_dir(SYNTHETIC_DIR)
    for i in range(num_images):
        save_path = os.path.join(SYNTHETIC_DIR, f"synth_{i:03d}.png")
        if os.path.exists(save_path):
            continue

        print(f"Generating synthetic image {save_path}...")
        # Create a random RGB image or geometric patterns
        if i % 2 == 0:
            img_array = np.random.randint(0, 256, (size[1], size[0], 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
        else:
            img = Image.new("RGB", size, (255, 255, 255))
            draw = ImageDraw.Draw(img)
            for _ in range(10):
                x0, y0 = np.random.randint(0, size[0] // 2), np.random.randint(0, size[1] // 2)
                x1, y1 = np.random.randint(size[0] // 2, size[0]), np.random.randint(size[1] // 2, size[1])
                color = tuple(np.random.randint(0, 256, 3))
                if np.random.random() > 0.5:
                    draw.rectangle([x0, y0, x1, y1], fill=color)
                else:
                    draw.ellipse([x0, y0, x1, y1], fill=color)
        
        img.save(save_path)

def download_picsum_gray(num_images=100):
    ensure_dir(PICSUM_GRAY_DIR)
    print(f"Downloading {num_images} unique grayscale images from Picsum...")
    for i in range(num_images):
        save_path = os.path.join(PICSUM_GRAY_DIR, f"picsum_gray_{i:03d}.jpg")
        # Appending unique identifier to prevent caching
        download_image(f"{PICSUM_URL_GRAY}&random={i}", save_path)
    print("Picsum grayscale subset complete.")

def download_picsum_color(num_images=100):
    ensure_dir(PICSUM_COLOR_DIR)
    print(f"Downloading {num_images} unique color images from Picsum...")
    for i in range(num_images):
        save_path = os.path.join(PICSUM_COLOR_DIR, f"picsum_color_{i:03d}.jpg")
        download_image(f"{PICSUM_URL_COLOR}?random={i}", save_path)
    print("Picsum color subset complete.")

if __name__ == "__main__":
    print(f"Setting up test data in {DATA_DIR}...")
    ensure_dir(DATA_DIR)
    
    download_picsum_gray(num_images=100)
    download_picsum_color(num_images=100)
    create_synthetic_images(num_images=5)
    
    print("Test data preparation complete.")
