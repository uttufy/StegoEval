import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_plots(df: pd.DataFrame, output_dir: str):
    """Generates visual plots from the evaluation results."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    algorithms = df['algorithm'].unique()
    sns.set_theme(style="whitegrid")

    # 1. PSNR vs JPEG quality (Compression Attack)
    jpeg_df = df[(df['attack_category'] == 'compression') & (df['attack_name'] == 'jpeg')].copy()
    if not jpeg_df.empty:
        # Extract quality from params string "quality=95"
        jpeg_df['quality'] = jpeg_df['attack_params'].apply(lambda x: int(x.split('=')[1]))
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=jpeg_df, x='quality', y='psnr', hue='algorithm', marker='o')
        plt.title('PSNR vs JPEG Quality')
        plt.xlabel('JPEG Quality')
        plt.ylabel('PSNR (dB)')
        plt.savefig(os.path.join(output_dir, 'psnr_vs_jpeg.png'))
        plt.close()

    # 2. BER vs Noise Variance
    noise_df = df[(df['attack_category'] == 'noise') & (df['attack_name'].isin(['gaussian', 'speckle']))].copy()
    if not noise_df.empty:
        # We assume single var parameter or similar for x-axis. Using attack_params string directly as categorical might be messy,
        # but for simplicity let's plot BER by attack name and algorithm.
        plt.figure(figsize=(12, 6))
        sns.barplot(data=noise_df, x='attack_name', y='ber', hue='algorithm')
        plt.title('Bit Error Rate (BER) across Noise Attacks')
        plt.xlabel('Noise Type')
        plt.ylabel('BER')
        plt.savefig(os.path.join(output_dir, 'ber_vs_noise.png'))
        plt.close()

    # 3. SSIM vs Rotation Angle
    rot_df = df[(df['attack_category'] == 'geometric') & (df['attack_name'] == 'rotation')].copy()
    if not rot_df.empty:
        rot_df['angle'] = rot_df['attack_params'].apply(lambda x: float(x.split('=')[1]))
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=rot_df, x='angle', y='ssim', hue='algorithm', marker='s')
        plt.title('SSIM vs Rotation Angle')
        plt.xlabel('Angle (Degrees)')
        plt.ylabel('SSIM')
        plt.savefig(os.path.join(output_dir, 'ssim_vs_rotation.png'))
        plt.close()
        
    print(f"Plots generated in {output_dir}")
