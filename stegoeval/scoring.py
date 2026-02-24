"""
StegnoEval Score Calculator

Calculates a composite score (0-100) for each algorithm based on:
- Distortion metrics (SSIM, PSNR)
- Robustness metrics (BER, recovery rate)

Score Formula:
Overall Score = (Distortion Score * 0.4) + (Robustness Score * 0.6)

Where:
- Distortion Score = SSIM * 100 (higher is better)
- Robustness Score = (1 - avg_BER) * recovery_rate * 100
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


def calculate_distortion_score(ssim: float, psnr: float) -> float:
    """
    Calculate distortion score based on SSIM and PSNR.
    Higher SSIM = better quality = higher score (0-100)
    """
    # SSIM is already 0-1, scale to 0-100
    ssim_score = ssim * 100
    
    # PSNR typically ranges from 20-50+ dB for images
    # Normalize to 0-100 scale
    if psnr > 50:
        psnr_score = 100
    elif psnr < 20:
        psnr_score = 0
    else:
        psnr_score = ((psnr - 20) / 30) * 100
    
    # Weight: SSIM is more important for perceptual quality
    return (ssim_score * 0.7) + (psnr_score * 0.3)


def calculate_robustness_score(ber: float, recovered: bool) -> float:
    """
    Calculate robustness score based on BER and recovery status.
    Lower BER = better = higher score (0-100)
    """
    if not recovered:
        return 0.0
    
    # BER of 0 = perfect, 1 = completely corrupted
    ber_score = (1 - ber) * 100
    return ber_score


def calculate_stegnoeval_score(
    distortion_score: float, 
    robustness_score: float,
    distortion_weight: float = 0.4,
    robustness_weight: float = 0.6
) -> float:
    """
    Calculate the overall StegnoEval score.
    
    Args:
        distortion_score: Score from distortion metrics (0-100)
        robustness_score: Score from robustness metrics (0-100)
        distortion_weight: Weight for distortion (default 0.4)
        robustness_weight: Weight for robustness (default 0.6)
    
    Returns:
        Overall StegnoEval score (0-100)
    """
    return (distortion_score * distortion_weight) + (robustness_score * robustness_weight)


def calculate_scores_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate scores for each algorithm grouped by attack category.
    
    Returns DataFrame with columns:
    - algorithm
    - attack_category
    - compression_score (for compression attacks)
    - blur_score (for filtering attacks)  
    - noise_score (for noise attacks)
    - geometric_score (for geometric attacks)
    - overall_score
    - images_tested
    - payloads_recovered
    - recovery_rate
    """
    if df.empty:
        return pd.DataFrame()
    
    results = []
    
    # Group by algorithm and attack_category
    for algo in df['algorithm'].unique():
        algo_df = df[df['algorithm'] == algo]
        
        # Get all attack categories
        categories = algo_df['attack_category'].unique()
        
        for category in categories:
            cat_df = algo_df[algo_df['attack_category'] == category]
            
            # Skip "none" (clean) - it's not an attack
            if category == 'none':
                continue
            
            # Calculate metrics
            avg_ssim = cat_df['ssim'].mean() if 'ssim' in cat_df else 0
            avg_psnr = cat_df['psnr'].mean() if 'psnr' in cat_df else 0
            avg_ber = cat_df['ber'].mean() if 'ber' in cat_df else 1.0
            recovery_rate = cat_df['payload_recovered'].mean() if 'payload_recovered' in cat_df else 0
            
            # Calculate scores
            distortion_score = calculate_distortion_score(avg_ssim, avg_psnr)
            robustness_score = calculate_robustness_score(avg_ber, recovery_rate > 0)
            overall_score = calculate_stegnoeval_score(distortion_score, robustness_score)
            
            results.append({
                'algorithm': algo,
                'attack_category': category,
                'avg_ssim': avg_ssim,
                'avg_psnr': avg_psnr,
                'avg_ber': avg_ber,
                'recovery_rate': recovery_rate,
                'distortion_score': distortion_score,
                'robustness_score': robustness_score,
                'overall_score': overall_score,
                'images_tested': len(cat_df)
            })
    
    return pd.DataFrame(results)


def calculate_overall_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate overall scores for each algorithm across all attacks.
    
    Returns DataFrame with columns:
    - algorithm
    - compression_score
    - blur_score  
    - noise_score
    - geometric_score
    - combo_score
    - capacity_score
    - overall_score
    - total_images
    - total_payloads_recovered
    - overall_recovery_rate
    """
    if df.empty:
        return pd.DataFrame()
    
    results = []
    
    for algo in df['algorithm'].unique():
        algo_df = df[df['algorithm'] == algo]
        
        # Scores by category
        compression_df = algo_df[algo_df['attack_category'] == 'compression']
        blur_df = algo_df[algo_df['attack_category'].isin(['filtering', 'blur'])]
        noise_df = algo_df[algo_df['attack_category'] == 'noise']
        geometric_df = algo_df[algo_df['attack_category'] == 'geometric']
        combo_df = algo_df[algo_df['attack_category'] == 'combo']
        capacity_df = algo_df[algo_df['attack_category'] == 'capacity']
        
        # Calculate scores for each category
        def get_category_score(cat_df):
            if cat_df.empty:
                return None
            avg_ssim = cat_df['ssim'].mean()
            avg_psnr = cat_df['psnr'].mean()
            avg_ber = cat_df['ber'].mean()
            recovery_rate = cat_df['payload_recovered'].mean()
            
            distortion = calculate_distortion_score(avg_ssim, avg_psnr)
            robustness = calculate_robustness_score(avg_ber, recovery_rate > 0)
            return calculate_stegnoeval_score(distortion, robustness)
        
        compression_score = get_category_score(compression_df)
        blur_score = get_category_score(blur_df)
        noise_score = get_category_score(noise_df)
        geometric_score = get_category_score(geometric_df)
        combo_score = get_category_score(combo_df)
        capacity_score = get_category_score(capacity_df)
        
        # Overall metrics (excluding clean)
        attack_df = algo_df[algo_df['attack_category'] != 'none']
        
        if not attack_df.empty:
            overall_ssim = attack_df['ssim'].mean()
            overall_psnr = attack_df['psnr'].mean()
            overall_ber = attack_df['ber'].mean()
            overall_recovery = attack_df['payload_recovered'].mean()
            
            overall_distortion = calculate_distortion_score(overall_ssim, overall_psnr)
            overall_robustness = calculate_robustness_score(overall_ber, overall_recovery > 0)
            overall_score = calculate_stegnoeval_score(overall_distortion, overall_robustness)
        else:
            overall_score = None
            overall_recovery = 0
        
        results.append({
            'algorithm': algo,
            'compression_score': compression_score,
            'blur_score': blur_score,
            'noise_score': noise_score,
            'geometric_score': geometric_score,
            'combo_score': combo_score,
            'capacity_score': capacity_score,
            'overall_score': overall_score,
            'total_images': len(algo_df),
            'total_payloads_recovered': int(algo_df['payload_recovered'].sum()) if 'payload_recovered' in algo_df else 0,
            'overall_recovery_rate': overall_recovery
        })
    
    return pd.DataFrame(results)
