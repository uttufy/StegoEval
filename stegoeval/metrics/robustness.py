import difflib
import numpy as np

def calculate_ber(original_payload: str, extracted_payload: str) -> float:
    """Bit Error Rate for strings. Evaluates binary strings explicitly."""
    # Convert text to binary string if not already
    if not all(c in '01' for c in original_payload):
        bin_orig = ''.join(format(ord(i), '08b') for i in original_payload)
    else:
        bin_orig = original_payload
        
    if not all(c in '01' for c in extracted_payload):
        bin_ext = ''.join(format(ord(i), '08b') for i in extracted_payload)
    else:
        bin_ext = extracted_payload

    # Align lengths by zero-padding the shorter one
    max_len = max(len(bin_orig), len(bin_ext))
    if max_len == 0:
        return 0.0
        
    bin_orig = bin_orig.ljust(max_len, '0')
    bin_ext = bin_ext.ljust(max_len, '0')
    
    errors = sum(1 for a, b in zip(bin_orig, bin_ext) if a != b)
    return errors / max_len

def calculate_ncc_text(original_payload: str, extracted_payload: str) -> float:
    """Normalized Cross-Correlation based on SequenceMatcher ratio for text"""
    # A simple proxy for NCC on strings
    return difflib.SequenceMatcher(None, original_payload, extracted_payload).ratio()

# Metrics specifically for when payload is itself an image matrix
# For StegoEval MVP, we assume text/binary payloads based on the interface.
def calculate_npcr(original_payload_img: np.ndarray, extracted_payload_img: np.ndarray) -> float:
    """
    Number of Pixels Change Rate (usually for image payloads or cryptography).
    Using proxy variables.
    """
    if original_payload_img.shape != extracted_payload_img.shape:
        return 1.0 # Max difference conceptually
    
    diff = original_payload_img != extracted_payload_img
    return np.sum(diff) / float(original_payload_img.size)

def calculate_uaci(original_payload_img: np.ndarray, extracted_payload_img: np.ndarray) -> float:
    """
    Unified Average Changing Intensity (usually for image payloads).
    """
    if original_payload_img.shape != extracted_payload_img.shape:
        return 1.0 # Max conceptually
        
    diff = np.abs(original_payload_img.astype(float) - extracted_payload_img.astype(float))
    return np.sum(diff) / (255.0 * original_payload_img.size)
