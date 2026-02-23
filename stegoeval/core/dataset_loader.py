import os
import cv2
import glob

class DatasetLoader:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.image_paths = []
        self._load_image_paths()

    def _load_image_paths(self):
        """Scans the dataset path recursively for common image formats."""
        if not os.path.exists(self.dataset_path):
            print(f"Warning: Dataset path does not exist: {self.dataset_path}")
            return
            
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']
        for ext in extensions:
            # Search recursively using **
            pattern = os.path.join(self.dataset_path, "**", ext)
            pattern_upper = os.path.join(self.dataset_path, "**", ext.upper())
            
            self.image_paths.extend(glob.glob(pattern, recursive=True))
            self.image_paths.extend(glob.glob(pattern_upper, recursive=True))
        
        # Remove duplicates and sort
        self.image_paths = sorted(list(set(self.image_paths)))
        print(f"Found {len(self.image_paths)} images in {self.dataset_path}")

    def get_images(self, limit: int = None):
        """Yields images and their filenames."""
        paths_to_load = self.image_paths[:limit] if limit else self.image_paths
        
        for path in paths_to_load:
            # imread reads as BGR if color, or grayscale if grayscale.
            # Using IMREAD_UNCHANGED keeps original channels (B&W or RGB)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                yield os.path.basename(path), img
            else:
                print(f"Failed to load image: {path}")

    def __len__(self):
        return len(self.image_paths)
