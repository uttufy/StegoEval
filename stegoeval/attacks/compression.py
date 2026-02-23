import cv2
import numpy as np

def apply_jpeg_compression(image: np.ndarray, quality: int = 95) -> np.ndarray:
    """
    Apply JPEG compression to an image.
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded_image = cv2.imencode('.jpg', image, encode_param)
    decoded_image = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
    return decoded_image

def apply_webp_compression(image: np.ndarray, quality: int = 95) -> np.ndarray:
    """
    Apply WebP compression to an image.
    """
    encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), quality]
    _, encoded_image = cv2.imencode('.webp', image, encode_param)
    decoded_image = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
    return decoded_image
