# StegoEval Scoring System

StegoEval computes a single, overarching **StegoEval Score** (out of 100) for each tested algorithm. This score aims to provide a comparable, holistic metric that balances two competing interests in steganography: Imperceptibility (Distortion) and Survivability (Robustness).

## The Score Formula

The global StegoEval score is a weighted sum:

`Overall Score = (Distortion Score × 0.4) + (Robustness Score × 0.6)`

StegoEval weighs Robustness lightly higher (60%) because an algorithm that maintains a perfect cover image is useless if the payload is instantly destroyed by standard saving processes (like JPEG compression or resizing).

### 1. Distortion Score Component (40% Weight)

The distortion score evaluates how well the algorithm preserves the original image quality. It merges the two most widely accepted image quality metrics: Structural Similarity Index Measure (SSIM) and Peak Signal-to-Noise Ratio (PSNR).

`Distortion Score = (SSIM × 100 × 0.7) + (Normalized PSNR × 0.3)`

*   **SSIM**: An SSIM of 1.0 means structural perfection. An SSIM of 0.95 gives 95 points. SSIM is heavily weighted (70%) as it best matches human perceptual differences.
*   **Normalized PSNR**: 
    - A PSNR `> 50 dB` maxes out at **100 points**, as changes above 50 dB are mathematically imperceptible to the human eye.
    - A PSNR `< 20 dB` scores **0 points**, as the image is considered visibly ruined.
    - Results between 20-50 dB are linearly scaled.

### 2. Robustness Score Component (60% Weight)

The robustness score evaluates if the hidden payload survived the assigned test (or attack).

`Robustness Score = (1 - BER) × 100 (if payload was recovered)`

*   **BER (Bit Error Rate)**: The ratio of corrupted bits. 
    - If BER = 0.0, the payload is perfectly intact, scoring **100 points**. 
    - If BER = 0.5 (half corrupted), it scores **50 points**.
*   **Recovery Requirement**: If the algorithm's standard `extract()` function completely crashes or fails to execute, the test scores **0 points** regardless of visual quality.

## Category Breakdown

StegoEval also produces intermediate scores by summarizing these components across specific types of real-world trials:
*   `compression_score`
*   `blur_score`
*   `noise_score`
*   `geometric_score`
*   `capacity_score` (Using the maximum successful text length achieved)

Algorithms that score high across all categories are considered highly versatile and production-ready for general steganography usage.
