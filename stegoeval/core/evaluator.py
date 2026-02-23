import numpy as np
from tqdm import tqdm
from typing import Dict, Any, List

from stegoeval.core.dataset_loader import DatasetLoader
from stegoeval.core.attack_runner import AttackRunner
from stegoeval.stego_algorithms.base import StegoAlgorithm

# Import metrics
from stegoeval.metrics.distortion import (
    calculate_mse, calculate_rmse, calculate_psnr, 
    calculate_ssim, calculate_aad, calculate_nad, calculate_correlation_coefficient
)
from stegoeval.metrics.robustness import calculate_ber, calculate_ncc_text

class Evaluator:
    def __init__(self, config: dict, algorithms: List[StegoAlgorithm]):
        self.config = config
        self.algorithms = algorithms
        self.dataset_loader = DatasetLoader(config.get("dataset_path", "./data"))
        self.attack_runner = AttackRunner()
        self.limit = config.get("dataset_limit", None)
        
        # Results storage: List of dicts
        self.results = []

    def evaluate(self) -> List[Dict[str, Any]]:
        payload = self.config.get("payload", "STEGOEVAL_DEFAULT_PAYLOAD")
        
        images = list(self.dataset_loader.get_images(limit=self.limit))
        if not images:
            print("No images found to evaluate.")
            return self.results

        # Total iterations: images * algorithms
        total_steps = len(images) * len(self.algorithms)
        
        with tqdm(total=total_steps, desc="Evaluating", unit="image-algo") as pbar:
            for img_name, cover_img in images:
                for algo in self.algorithms:
                    algo_name = algo.name()
                    
                    try:
                        # 1. Embed payload
                        stego_img = algo.embed(cover_img, payload)
                        
                        # 2. Compute Cover vs Stego metrics (Distortion)
                        base_result = {
                            "image": img_name,
                            "algorithm": algo_name,
                            "attack_category": "none",
                            "attack_name": "clean",
                            "attack_params": "none",
                            
                            # Distortion metrics
                            "mse": calculate_mse(cover_img, stego_img),
                            "rmse": calculate_rmse(cover_img, stego_img),
                            "psnr": calculate_psnr(cover_img, stego_img),
                            "ssim": calculate_ssim(cover_img, stego_img),
                            "aad": calculate_aad(cover_img, stego_img),
                            "nad": calculate_nad(cover_img, stego_img),
                            "ncc_image": calculate_correlation_coefficient(cover_img, stego_img),
                            
                            # Robustness (Clean extraction)
                            "ber": 0.0,
                            "ncc_secret": 1.0,
                            "extracted_payload": ""
                        }
                        
                        # Extract clean payload
                        clean_extracted = algo.extract(stego_img)
                        base_result["extracted_payload"] = clean_extracted
                        base_result["ber"] = calculate_ber(payload, clean_extracted)
                        base_result["ncc_secret"] = calculate_ncc_text(payload, clean_extracted)
                        
                        self.results.append(base_result)
                        
                        # 3. Run Attacks and calculate robustness
                        for cat, atk_name, params_str, attacked_stego in self.attack_runner.run_attacks(stego_img, self.config):
                            attacked_extracted = algo.extract(attacked_stego)
                            
                            attack_result = base_result.copy()
                            attack_result.update({
                                "attack_category": cat,
                                "attack_name": atk_name,
                                "attack_params": params_str,
                                "psnr_attacked": calculate_psnr(cover_img, attacked_stego), # PSNR relative to cover
                                "ssim_attacked": calculate_ssim(cover_img, attacked_stego), # SSIM relative to cover
                                "extracted_payload": attacked_extracted,
                                "ber": calculate_ber(payload, attacked_extracted),
                                "ncc_secret": calculate_ncc_text(payload, attacked_extracted)
                            })
                            self.results.append(attack_result)
                            
                    except Exception as e:
                        print(f"\nError processing {img_name} with {algo_name}: {e}")
                    
                    pbar.update(1)
                    
        return self.results
