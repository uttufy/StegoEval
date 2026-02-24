# StegoEval Exclusions & Limitations

StegoEval is designed specifically as an evaluation benchmark framework, not a production tool for embedding data. As such, it operates under defined limitations.

## What is NOT Tested

The current evaluation pipeline focuses on static robustness and visual distortion. It does **not** evaluate or test:

1.  **Steganalysis / Detection Success:** The framework does not include neural networks or statistical analysis tools designed to detect *if* an image contains a payload. It evaluates distortion conceptually (SSIM/PSNR), but does not run simulated steganalysis attacks (like StegExpose or SRNet).
2.  **Execution Performance:** The execution time, CPU/GPU utilization, or algorithmic complexity (Big O) of the steganography algorithms are not formally benched or scored by the `Evaluator`. Time-to-embed and time-to-extract are excluded from the main CSVs.
3.  **Real-Time / Streaming Applications:** StegoEval operates on static datasets of images in a synchronous loop. It cannot evaluate real-time streaming implementations (e.g., video steganography or network-packet stego).
4.  **Payload Security/Encryption:** The framework uses raw strings from the `wonderwords` library. It does not test if the encryption layer of an algorithm is secure; it only verifies if the extracted raw bytes match the embedded raw bytes.
5.  **Adversarial Tampering:** The framework applies standard, generalized attacks (e.g., standard motion blur, standard JPEG compression). It does not calculate or test *Adversarial Attacks* where an attacker intelligently optimizes image noise specifically to destroy the steganographic payload while preserving the image visual state.

## Metric Limitations

*   **PSNR "Infinity":** For the `results-{run_name}-clean.csv` baseline test (where no attack is applied), if an algorithm embeds a payload without altering the cover image at all, the Mean Squared Error (MSE) is 0. Mathematical division for PSNR will result in an `inf` reading. 
*   **Normalized Scoring Cap:** While theoretical PSNR can climb infinitely high on minimal distortions, the `StegnoEval Score` strictly caps the PSNR impact at 50 dB (100 points). Any result over 50 dB is considered "perfectly imperceptible" for human vision, so scores do not differentiate between 60 dB and 80 dB.
