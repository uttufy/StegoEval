import numpy as np

def apply_gaussian_noise(image: np.ndarray, mean: float = 0.0, var: float = 0.01) -> np.ndarray:
    """
    Apply Gaussian noise to an image.
    """
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, image.shape)
    
    noisy_image = image.astype(np.float32) + (gaussian * 255)
    noisy_image = np.clip(noisy_image, 0, 255)
    
    return noisy_image.astype(np.uint8)

def apply_salt_pepper_noise(image: np.ndarray, amount: float = 0.05, salt_vs_pepper: float = 0.5) -> np.ndarray:
    """
    Apply Salt and Pepper noise to an image.
    """
    noisy_image = np.copy(image)
    
    # Salt mode
    num_salt = np.ceil(amount * image.size * salt_vs_pepper)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[tuple(coords)] = 255

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - salt_vs_pepper))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[tuple(coords)] = 0
    
    return noisy_image

def apply_speckle_noise(image: np.ndarray, var: float = 0.04) -> np.ndarray:
    """
    Apply Speckle noise (multiplicative) to an image.
    """
    sigma = var ** 0.5
    gauss = np.random.normal(0, sigma, image.shape)
    
    noisy_image = image.astype(np.float32) + image.astype(np.float32) * gauss
    noisy_image = np.clip(noisy_image, 0, 255)
    
    return noisy_image.astype(np.uint8)

def apply_poisson_noise(image: np.ndarray) -> np.ndarray:
    """
    Apply Poisson noise to an image.
    """
    vals = len(np.unique(image))
    vals = 2 ** np.ceil(np.log2(vals))
    
    # Adding a small constant to prevent division by zero or zeros turning into nan
    noisy_image = np.random.poisson((image.astype(np.float32) + 1e-6) * vals) / float(vals)
    noisy_image = np.clip(noisy_image, 0, 255)
    
    return noisy_image.astype(np.uint8)
