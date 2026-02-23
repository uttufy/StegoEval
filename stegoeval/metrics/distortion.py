import numpy as np
import cv2
from skimage.metrics import structural_similarity

def _match_dims(cover: np.ndarray, stego: np.ndarray) -> np.ndarray:
    if cover.shape != stego.shape:
        # Resize stego back to cover shape for comparison
        h, w = cover.shape[:2]
        return cv2.resize(stego, (w, h), interpolation=cv2.INTER_LINEAR)
    return stego

def calculate_mse(cover: np.ndarray, stego: np.ndarray) -> float:
    """Mean Squared Error"""
    stego = _match_dims(cover, stego)
    err = np.sum((cover.astype("float") - stego.astype("float")) ** 2)
    err /= float(cover.size)
    return float(err)

def calculate_rmse(cover: np.ndarray, stego: np.ndarray) -> float:
    """Root Mean Squared Error"""
    stego = _match_dims(cover, stego)
    return float(np.sqrt(calculate_mse(cover, stego)))

def calculate_psnr(cover: np.ndarray, stego: np.ndarray) -> float:
    """Peak Signal-to-Noise Ratio"""
    stego = _match_dims(cover, stego)
    mse = calculate_mse(cover, stego)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return float(psnr)

def calculate_ssim(cover: np.ndarray, stego: np.ndarray) -> float:
    """Structural Similarity Index"""
    stego = _match_dims(cover, stego)
    
    # Calculate appropriate window size based on image dimensions
    min_dim = min(cover.shape[:2])
    # Ensure win_size is odd and smaller than image dimensions, fallback to 3 or 7
    win_size = min(7, min_dim)
    if win_size % 2 == 0:
        win_size -= 1
    if win_size < 3:
        win_size = 3
        
    if len(cover.shape) == 3:
        return float(structural_similarity(cover, stego, channel_axis=-1, data_range=255, win_size=win_size))
    else:
        return float(structural_similarity(cover, stego, data_range=255, win_size=win_size))


def calculate_aad(cover: np.ndarray, stego: np.ndarray) -> float:
    """Average Absolute Difference"""
    stego = _match_dims(cover, stego)
    return float(np.mean(np.abs(cover.astype(float) - stego.astype(float))))

def calculate_nad(cover: np.ndarray, stego: np.ndarray) -> float:
    """Normalized Absolute Error / Difference"""
    stego = _match_dims(cover, stego)
    diff_sum = np.sum(np.abs(cover.astype(float) - stego.astype(float)))
    ref_sum = np.sum(np.abs(cover.astype(float)))
    if ref_sum == 0:
        return 0.0
    return float(diff_sum / ref_sum)

def calculate_correlation_coefficient(cover: np.ndarray, stego: np.ndarray) -> float:
    """Correlation Coefficient between cover and stego images"""
    stego = _match_dims(cover, stego)
    flat_cover = cover.flatten()
    flat_stego = stego.flatten()
    try:
        res = np.corrcoef(flat_cover, flat_stego)[0, 1]
        if np.isnan(res):
            return 0.0
        return float(res)
    except Exception:
        return 0.0
