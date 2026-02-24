# Default Attack Configurations

StegoEval includes predefined YAML configuration files located in the `config/` directory. These configurations simulate standard, real-world conditions that a steganographic image might encounter on the internet or modern file systems.

## 1. Capacity Limits (`capacity:`)
*   `max_payload: 1000` (Characters)
*   **Why**: A standard social media post, short email, or hidden URL fits comfortably within ~1,000 characters. Finding the absolute upper limit of an algorithm is useful, but ensuring it can seamlessly handle 1,000 text characters is the standard baseline test for "useful" payload sizes.

## 2. Compression Attacks (`compression:`)
*   `jpeg` & `webp` quality limits: `[10, 20, 50, 60, 80, 90]`
*   **Why**: 90% is transparent near-lossless compression (standard for high-quality web images). 60% represents standard social media aggressive downsampling (like Twitter/X or Facebook dropping image file sizes). 10-20% tests extreme survivability against harsh auto-compression pipelines found in messaging apps (like WhatsApp).

## 3. Filtering & Blurs (`filtering:`)
*   `gaussian_blur`: Kernel sizes `[3, 5, 7, 9, 11]`
*   **Why**: Blurring simulates re-sampling, basic image manipulation by users (like Instagram filters), or print-and-scan degradations. A kernel of 3 is a slight smoothing effect; 11 is a massive blur that visually obscures sharp edges.

## 4. Geometric Limits (`geometric:`)
*   `scaling`: `[0.5, 0.8, 1.2, 1.5, 2.0]`
*   **Why**: 0.5 simulates a user downloading an image and shrinking it to a mobile-friendly thumbnail. 2.0 simulates an upscale using browser zooming or basic interpolation. Both actions destroy pixel-perfect embeddings (like standard LSB).
*   `cropping`: `[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]`
*   **Why**: Users frequently crop screenshots to remove headers/footers. A 10% (0.1) crop is a standard aesthetic crop. A 50% (0.5) crop removes half the image real-estate, testing if the payload was distributed globally across the image rather than stored sequentially.
