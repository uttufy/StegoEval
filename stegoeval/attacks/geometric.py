import cv2
import numpy as np

def apply_rotation(image: np.ndarray, angle: float = 5.0) -> np.ndarray:
    """
    Rotate the image and optionally crop it to remove black borders.
    """
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
    
    # Calculate the rotation matrix
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Determine the bounding box size
    cos = np.abs(matrix[0, 0])
    sin = np.abs(matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # Adjust matrix to account for translation
    matrix[0, 2] += (new_w / 2) - center[0]
    matrix[1, 2] += (new_h / 2) - center[1]
    
    # Perform rotation
    rotated = cv2.warpAffine(image, matrix, (new_w, new_h))
    
    return rotated

def apply_scaling(image: np.ndarray, scale_factor: float = 1.5) -> np.ndarray:
    """
    Scale (resize) the image by a scale factor.
    """
    h, w = image.shape[:2]
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

def apply_cropping(image: np.ndarray, percentage: float = 0.1) -> np.ndarray:
    """
    Crop the image uniformly by a given percentage from all sides.
    """
    h, w = image.shape[:2]
    
    crop_h = int(h * percentage)
    crop_w = int(w * percentage)
    
    # Return original if crop is too aggressive
    if crop_h >= h // 2 or crop_w >= w // 2:
        return image.copy()
        
    return image[crop_h:h-crop_h, crop_w:w-crop_w]

def apply_resize(image: np.ndarray, size: tuple) -> np.ndarray:
    """
    Resize the image to specific dimensions.
    size: (width, height)
    """
    return cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)
