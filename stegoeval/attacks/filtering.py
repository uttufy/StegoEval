import cv2
import numpy as np

def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply Gaussian blur to an image.
    """
    # Kernel size must be odd and positive
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply Median filter to an image.
    """
    # Kernel size must be odd and positive
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)

def apply_motion_blur(image: np.ndarray, size: int = 5, angle: float = 0.0) -> np.ndarray:
    """
    Apply Motion blur to an image.
    """
    # Generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    # Fill the middle row (horizontal motion)
    kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size
    
    # Rotate kernel for angle
    rotation_matrix = cv2.getRotationMatrix2D((size/2 -0.5 , size/2 -0.5 ) , angle, 1.0)
    kernel_motion_blur = cv2.warpAffine(kernel_motion_blur, rotation_matrix, (size, size))

    return cv2.filter2D(image, -1, kernel_motion_blur)
