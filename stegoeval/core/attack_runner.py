import inspect
import numpy as np

# Import all attack functions
from stegoeval.attacks.compression import apply_jpeg_compression, apply_webp_compression
from stegoeval.attacks.noise import apply_gaussian_noise, apply_salt_pepper_noise, apply_speckle_noise, apply_poisson_noise
from stegoeval.attacks.filtering import apply_gaussian_blur, apply_median_filter, apply_motion_blur
from stegoeval.attacks.geometric import apply_rotation, apply_scaling, apply_cropping, apply_resize


class AttackRunner:
    def __init__(self):
        # Map attack names to their corresponding functions
        self.attack_registry = {
            "compression": {
                "jpeg": apply_jpeg_compression,
                "webp": apply_webp_compression
            },
            "noise": {
                "gaussian": apply_gaussian_noise,
                "salt_pepper": apply_salt_pepper_noise,
                "speckle": apply_speckle_noise,
                "poisson": apply_poisson_noise
            },
            "filtering": {
                "gaussian_blur": apply_gaussian_blur,
                "median": apply_median_filter,
                "motion": apply_motion_blur
            },
            "geometric": {
                "rotation": apply_rotation,
                "scaling": apply_scaling,
                "cropping": apply_cropping,
                "resize": apply_resize
            }
        }

    def run_single_attack(self, image: np.ndarray, category: str, attack_name: str, params: dict) -> np.ndarray:
        """
        Run a single attack on an image.
        
        Args:
            image: Input image as numpy.ndarray
            category: Attack category (compression, noise, filtering, geometric)
            attack_name: Name of the attack
            params: Dictionary of parameters for the attack
            
        Returns:
            Attacked image as numpy.ndarray
        """
        if category not in self.attack_registry:
            raise ValueError(f"Unknown attack category: {category}")
        
        if attack_name not in self.attack_registry[category]:
            raise ValueError(f"Unknown attack '{attack_name}' in category '{category}'")
        
        attack_func = self.attack_registry[category][attack_name]
        
        try:
            # Check if params is a dict or a single value
            if isinstance(params, dict):
                attacked_img = attack_func(image, **params)
            else:
                # Single implicit value - inspect function to get parameter name
                sig = inspect.signature(attack_func)
                first_kwarg = list(sig.parameters.keys())[1]
                kwargs = {first_kwarg: params}
                attacked_img = attack_func(image, **kwargs)
            return attacked_img
        except Exception as e:
            raise RuntimeError(f"Attack {attack_name}.{category} failed: {e}")

    def run_attacks(self, image: np.ndarray, config: dict):
        """
        Runs a series of attacks on an image based on the provided configuration.
        Yields (attack_category, attack_name, params_str, attacked_image)
        """
        if "attacks" not in config or not config["attacks"]:
            return

        for category, attacks in config["attacks"].items():
            if category not in self.attack_registry:
                print(f"Warning: Unknown attack category '{category}'")
                continue

            for attack_name, param_list in attacks.items():
                if attack_name not in self.attack_registry[category]:
                    print(f"Warning: Unknown attack '{attack_name}' in category '{category}'")
                    continue

                attack_func = self.attack_registry[category][attack_name]

                # param_list could be a list of values (if single parameter like quality) 
                # or a list of dicts (if multiple parameters)
                if not isinstance(param_list, list):
                    param_list = [param_list]

                for params in param_list:
                    try:
                        if isinstance(params, dict):
                            # Dictionary of explicit kwargs
                            attacked_img = attack_func(image, **params)
                            param_str = "_".join(f"{k}={v}" for k, v in params.items())
                        else:
                            # Single implicit value (e.g. quality=95)
                            # Let's inspect the function to get the first kwarg name
                            sig = inspect.signature(attack_func)
                            # Skip the first param (image)
                            first_kwarg = list(sig.parameters.keys())[1]
                            kwargs = {first_kwarg: params}
                            attacked_img = attack_func(image, **kwargs)
                            param_str = f"{first_kwarg}={params}"
                            
                        yield category, attack_name, param_str, attacked_img
                    except Exception as e:
                        print(f"Error applying {attack_name}.{category} with params {params}: {e}")
