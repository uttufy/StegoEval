import numpy as np
import random
from tqdm import tqdm
from typing import Dict, Any, List, Tuple
from itertools import product

from stegoeval.core.dataset_loader import DatasetLoader
from stegoeval.core.attack_runner import AttackRunner
from stegoeval.stego_algorithms.base import StegoAlgorithm

# Import metrics
from stegoeval.metrics.distortion import (
    calculate_mse, calculate_rmse, calculate_psnr, 
    calculate_ssim, calculate_aad, calculate_nad, calculate_correlation_coefficient
)
from stegoeval.metrics.robustness import calculate_ber, calculate_ncc_text
from stegoeval.attacks.compression import apply_jpeg_compression


class Evaluator:
    def __init__(self, config: dict, algorithms: List[StegoAlgorithm]):
        self.config = config
        self.algorithms = algorithms
        self.dataset_loader = DatasetLoader(config.get("dataset_path", "./data"))
        self.attack_runner = AttackRunner()
        self.limit = config.get("dataset_limit", None)
        self.run_name = config.get("run_name", "benchmark")
        self.combo_attacks = config.get("combo_attacks", False)
        
        # Results storage: List of dicts
        self.results = []

    def _generate_random_payload(self, length: int) -> str:
        """Generates a random payload using varied English words and numbers."""
        from wonderwords import RandomWord
        
        r = RandomWord()
        words = []
        current_len = 0
        
        # Parts of speech to choose from
        pos_keys = ['noun', 'verb', 'adjective']
        
        # Generate words until we reach the desired length
        while current_len < length:
            # Randomly choose a part of speech for variety
            pos = random.choice(pos_keys)
            word = r.word(include_parts_of_speech=[pos])
            
            words.append(word)
            current_len += len(word) + 1  # +1 for space
        
        # Trim to exact length and add a number
        payload = " ".join(words)[:length]
        if len(payload) < length:
            payload += str(random.randint(0, 9999))
        
        return payload[:length]

    def _get_attack_configurations(self) -> List[Tuple[str, str, Any]]:
        """Extract all attack configurations from config."""
        attacks_config = self.config.get("attacks", {})
        attack_configs = []
        
        for category, attacks in attacks_config.items():
            if not isinstance(attacks, dict):
                continue
            for attack_name, param_list in attacks.items():
                if not isinstance(param_list, list):
                    param_list = [param_list]
                for params in param_list:
                    # Pass the raw parameter value (could be int, float, or dict)
                    attack_configs.append((category, attack_name, params))
        
        return attack_configs

    def _run_single_attack(self, image: np.ndarray, category: str, attack_name: str, params: Any) -> np.ndarray:
        """Run a single attack on an image."""
        # Pass params as-is to AttackRunner - it handles both dict and simple values
        return self.attack_runner.run_single_attack(image, category, attack_name, params)

    def _generate_combinations(self, attack_configs: List[Tuple[str, str, Any]]) -> List[List[Tuple[str, str, Any]]]:
        """Generate all possible combinations of attacks."""
        if not attack_configs:
            return []
        
        # Group by category for meaningful combinations
        by_category = {}
        for cat, name, params in attack_configs:
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((cat, name, params))
        
        # Generate combinations - pick one from each category
        categories = list(by_category.keys())
        combinations = []
        
        for combo in product(*[by_category[cat] for cat in categories]):
            combinations.append(list(combo))
        
        return combinations

    def _evaluate_image_algorithm(self, img_name: str, cover_img: np.ndarray, algo: StegoAlgorithm, 
                                   payload: str) -> List[Dict[str, Any]]:
        """Evaluate a single image-algorithm-payload combination."""
        algo_name = algo.name()
        results = []
        
        # 1. Embed payload
        try:
            stego_img = algo.embed(cover_img, payload)
        except Exception as e:
            return [{"image": img_name, "algorithm": algo_name, "error": f"Embed failed: {e}"}]
        
        # 2. Compute Cover vs Stego metrics (Distortion) - Clean/No attack
        base_result = {
            "image": img_name,
            "algorithm": algo_name,
            "payload_size": len(payload),
            "attack_category": "none",
            "attack_name": "clean",
            "attack_params": "none",
            
            # Distortion metrics (cover vs stego)
            "mse": calculate_mse(cover_img, stego_img),
            "rmse": calculate_rmse(cover_img, stego_img),
            "psnr": calculate_psnr(cover_img, stego_img),
            "ssim": calculate_ssim(cover_img, stego_img),
            "aad": calculate_aad(cover_img, stego_img),
            "nad": calculate_nad(cover_img, stego_img),
            "ncc_image": calculate_correlation_coefficient(cover_img, stego_img),
            
            # Robustness metrics
            "ber": 0.0,
            "ncc_secret": 1.0,
            "payload_recovered": True,
            "embedded_payload": payload,
            "extracted_payload": ""
        }
        
        # Extract clean payload
        try:
            clean_extracted = algo.extract(stego_img)
            base_result["extracted_payload"] = clean_extracted
            base_result["ber"] = calculate_ber(payload, clean_extracted)
            base_result["ncc_secret"] = calculate_ncc_text(payload, clean_extracted)
            base_result["payload_recovered"] = base_result["ber"] == 0.0
        except Exception as e:
            base_result["extracted_payload"] = f"ERROR: {e}"
            base_result["ber"] = 1.0
            base_result["ncc_secret"] = 0.0
            base_result["payload_recovered"] = False
        
        results.append(base_result)
        
        # 3. Run individual attacks
        attack_configs = self._get_attack_configurations()
        
        for category, attack_name, params in attack_configs:
            try:
                attacked_stego = self._run_single_attack(stego_img, category, attack_name, params)
                
                # Compute metrics relative to cover image
                result = {
                    "image": img_name,
                    "algorithm": algo_name,
                    "payload_size": len(payload),
                    "attack_category": category,
                    "attack_name": attack_name,
                    "attack_params": str(params),
                    
                    # Distortion metrics (cover vs attacked stego)
                    "mse": calculate_mse(cover_img, attacked_stego),
                    "rmse": calculate_rmse(cover_img, attacked_stego),
                    "psnr": calculate_psnr(cover_img, attacked_stego),
                    "ssim": calculate_ssim(cover_img, attacked_stego),
                    "aad": calculate_aad(cover_img, attacked_stego),
                    "nad": calculate_nad(cover_img, attacked_stego),
                    "ncc_image": calculate_correlation_coefficient(cover_img, attacked_stego),
                    
                    # Robustness metrics
                    "ber": base_result["ber"],  # Will be updated below
                    "ncc_secret": base_result["ncc_secret"],  # Will be updated below
                    "payload_recovered": False,
                    "embedded_payload": payload,
                    "extracted_payload": ""
                }
                
                # Try to extract payload from attacked image
                try:
                    attacked_extracted = algo.extract(attacked_stego)
                    result["extracted_payload"] = attacked_extracted
                    result["ber"] = calculate_ber(payload, attacked_extracted)
                    result["ncc_secret"] = calculate_ncc_text(payload, attacked_extracted)
                    result["payload_recovered"] = result["ber"] == 0.0
                except Exception as e:
                    result["extracted_payload"] = f"ERROR: {e}"
                    result["ber"] = 1.0
                    result["ncc_secret"] = 0.0
                    result["payload_recovered"] = False
                
                results.append(result)
                
            except Exception as e:
                # Skip failed attacks
                print(f"Warning: Attack {attack_name}.{category} failed: {e}")
                continue
        
        # 4. Run combination attacks if enabled
        if self.combo_attacks and attack_configs:
            combinations = self._generate_combinations(attack_configs)
            
            for combo in combinations:
                try:
                    # Apply all attacks in combination sequentially
                    attacked_img = stego_img.copy()
                    combo_params = []
                    
                    for category, attack_name, params in combo:
                        attacked_img = self._run_single_attack(attacked_img, category, attack_name, params)
                        combo_params.append(f"{attack_name}")
                    
                    combo_name = "+".join(combo_params)
                    combo_category = "combo"
                    
                    result = {
                        "image": img_name,
                        "algorithm": algo_name,
                        "payload_size": len(payload),
                        "attack_category": combo_category,
                        "attack_name": combo_name,
                        "attack_params": str({cat: name for cat, name, _ in combo}),
                        
                        # Distortion metrics
                        "mse": calculate_mse(cover_img, attacked_img),
                        "rmse": calculate_rmse(cover_img, attacked_img),
                        "psnr": calculate_psnr(cover_img, attacked_img),
                        "ssim": calculate_ssim(cover_img, attacked_img),
                        "aad": calculate_aad(cover_img, attacked_img),
                        "nad": calculate_nad(cover_img, attacked_img),
                        "ncc_image": calculate_correlation_coefficient(cover_img, attacked_img),
                        
                        # Robustness metrics
                        "ber": 1.0,
                        "ncc_secret": 0.0,
                        "payload_recovered": False,
                        "embedded_payload": payload,
                        "extracted_payload": ""
                    }
                    
                    # Try to extract payload
                    try:
                        combo_extracted = algo.extract(attacked_img)
                        result["extracted_payload"] = combo_extracted
                        result["ber"] = calculate_ber(payload, combo_extracted)
                        result["ncc_secret"] = calculate_ncc_text(payload, combo_extracted)
                        result["payload_recovered"] = result["ber"] == 0.0
                    except Exception as e:
                        result["extracted_payload"] = f"ERROR: {e}"
                        result["ber"] = 1.0
                        result["ncc_secret"] = 0.0
                        result["payload_recovered"] = False
                    
                    results.append(result)
                    
                except Exception as e:
                    print(f"Warning: Combo attack failed: {e}")
                    continue
        
        return results

    def _evaluate_max_text_length(self, img_name: str, cover_img: np.ndarray, algo: StegoAlgorithm) -> Dict[str, Any]:
        """
        Uses binary search to find the maximum text length that can be embedded
        and successfully extracted (BER == 0.0) without error.
        """
        algo_name = algo.name()
        
        # Pull bounds from config, fallback to defaults
        capacity_config = self.config.get("capacity", {})
        upper_bound = capacity_config.get("max_payload", 100000)
        tolerance = capacity_config.get("tolerance", 50)
        
        low = 1
        high = upper_bound
        max_valid_length = 0
        
        # Binary search for maximum capacity
        while low <= high:
            mid = (low + high) // 2
            payload = self._generate_random_payload(mid)
            
            # Fast fail check if it's too large to even embed
            success = False
            try:
                stego_img = algo.embed(cover_img, payload)
                extracted_payload = algo.extract(stego_img)
                ber = calculate_ber(payload, extracted_payload)
                success = (ber == 0.0)
            except Exception:
                success = False
                
            if success:
                max_valid_length = mid
                low = mid + 1
                # Optimization: if we found an upper limit within tolerance, stop early
                if (high - low) <= tolerance:
                    break
            else:
                high = mid - 1
                
        # Now that we've found the max_valid_length, let's calculate the real metrics
        mse, rmse, psnr, ssim, aad, nad, ncc_image = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if max_valid_length > 0:
            final_payload = self._generate_random_payload(max_valid_length)
            try:
                final_stego = algo.embed(cover_img, final_payload)
                mse = calculate_mse(cover_img, final_stego)
                rmse = calculate_rmse(cover_img, final_stego)
                psnr = calculate_psnr(cover_img, final_stego)
                ssim = calculate_ssim(cover_img, final_stego)
                aad = calculate_aad(cover_img, final_stego)
                nad = calculate_nad(cover_img, final_stego)
                ncc_image = calculate_correlation_coefficient(cover_img, final_stego)
            except Exception:
                pass # If it fails here, keep metric as 0.0
                
        # Format the result similar to an attack, but specific for capacity
        return {
            "image": img_name,
            "algorithm": algo_name,
            "payload_size": max_valid_length,  # The identified max length
            "attack_category": "capacity",
            "attack_name": "max_text_length",
            "attack_params": f"max_bound={upper_bound}",
            
            # Distortion metrics
            "mse": mse,
            "rmse": rmse,
            "psnr": psnr,
            "ssim": ssim,
            "aad": aad,
            "nad": nad,
            "ncc_image": ncc_image,
            
            # Robustness metrics
            "ber": 0.0,     # By definition, the max valid length has 0 BER
            "ncc_secret": 1.0,
            "payload_recovered": True,
            "embedded_payload": f"<Payload of length {max_valid_length}>",
            "extracted_payload": f"<Extracted length {max_valid_length}>"
        }

    def evaluate(self) -> List[Dict[str, Any]]:
        # Payload sizes to test
        payload_sizes = self.config.get("payload_sizes", [10, 100, 1000, 5000])
        
        images = list(self.dataset_loader.get_images(limit=self.limit))
        if not images:
            print("No images found to evaluate.")
            return self.results

        # Calculate total iterations
        total_attacks = len(self._get_attack_configurations())
        combo_multiplier = len(self._generate_combinations(self._get_attack_configurations())) if self.combo_attacks else 0
        
        
        capacity_enabled = self.config.get("capacity", {}).get("enabled", False)
        
        if self.combo_attacks and combo_multiplier > 0:
            total_steps = len(images) * len(self.algorithms) * len(payload_sizes) * (1 + total_attacks + combo_multiplier)
        else:
            total_steps = len(images) * len(self.algorithms) * len(payload_sizes) * (1 + total_attacks)
            
        # Add capacity test steps if enabled
        if capacity_enabled:
            total_steps += len(images) * len(self.algorithms)
        
        with tqdm(total=total_steps, desc="Evaluating", unit="step") as pbar:
            for img_name, cover_img in images:
                # Add Baseline Test for the pure cover image (simulating a standard 95% JPEG save)
                try:
                    baseline_img = apply_jpeg_compression(cover_img, quality=95)
                    baseline_result = {
                        "image": img_name,
                        "algorithm": "COVER_IMAGE_BASELINE",
                        "payload_size": 0,
                        "attack_category": "baseline",
                        "attack_name": "clean_jpeg_save",
                        "attack_params": "quality=95",
                        
                        # Baseline Distortion metrics (cover vs clean save)
                        "mse": calculate_mse(cover_img, baseline_img),
                        "rmse": calculate_rmse(cover_img, baseline_img),
                        "psnr": calculate_psnr(cover_img, baseline_img),
                        "ssim": calculate_ssim(cover_img, baseline_img),
                        "aad": calculate_aad(cover_img, baseline_img),
                        "nad": calculate_nad(cover_img, baseline_img),
                        "ncc_image": calculate_correlation_coefficient(cover_img, baseline_img),
                        
                        # Robustness metrics (N/A for baseline)
                        "ber": 0.0,
                        "ncc_secret": 0.0,
                        "payload_recovered": False,
                        "embedded_payload": "N/A",
                        "extracted_payload": "N/A"
                    }
                    self.results.append(baseline_result)
                except Exception as e:
                    print(f"Warning: Baseline calculation failed for {img_name}: {e}")

                for algo in self.algorithms:
                    algo_name = algo.name()
                    
                    for size in payload_sizes:
                        payload = self._generate_random_payload(size)
                        
                        # Run evaluation for this image-algorithm-payload
                        results = self._evaluate_image_algorithm(img_name, cover_img, algo, payload)
                        self.results.extend(results)
                        
                        pbar.update(1 + total_attacks)  # Clean + individual attacks
                        if self.combo_attacks:
                            pbar.update(combo_multiplier)
                    
                    # Error handling - if payload too large
                    if any("error" in r for r in self.results[-len(payload_sizes):]):
                        remaining = len(payload_sizes) - 1
                        pbar.update(remaining)
                        
                    # Run Capacity test if enabled for this image & algorithm
                    if capacity_enabled:
                        capacity_result = self._evaluate_max_text_length(img_name, cover_img, algo)
                        self.results.append(capacity_result)
                        pbar.update(1)
                        
        return self.results
