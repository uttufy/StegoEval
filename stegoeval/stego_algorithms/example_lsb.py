import numpy as np
from .base import StegoAlgorithm


class LSBStego(StegoAlgorithm):
    """
    A simple Least Significant Bit (LSB) steganography algorithm.
    Embeds a binary payload into the LSB of the cover image pixels.
    This is a basic example algorithm and is typically not robust against attacks.
    """

    def name(self) -> str:
        return "example_lsb"

    def embed(self, cover: np.ndarray, payload: str) -> np.ndarray:
        """
        Embed the payload into the cover image.
        Assumes payload is a binary string of '0's and '1's.
        """
        # Convert string to binary if it's not already
        if not all(c in '01' for c in payload):
            # Convert text to binary string
            binary_payload = ''.join(format(ord(i), '08b') for i in payload)
        else:
            binary_payload = payload

        # Add a null terminator to denote end of message
        binary_payload += '00000000'

        stego = cover.copy()
        
        # Flatten image for easier manipulation
        flat_stego = stego.flatten()
        
        if len(binary_payload) > len(flat_stego):
            raise ValueError(f"Payload too large for cover image. Max bits: {len(flat_stego)}")

        # Embed payload into the LSB
        for i, bit in enumerate(binary_payload):
            # Clear the LSB and set it to the payload bit
            # Use bitwise mask 254 (0xFE) to clear the LSB safely for uint8
            flat_stego[i] = (flat_stego[i] & 254) | int(bit)

        # Reshape back to original dimensions
        return flat_stego.reshape(cover.shape)

    def extract(self, stego: np.ndarray) -> str:
        """
        Extract the payload from the stego image.
        Extracts until a null byte ('00000000') is found.
        """
        flat_stego = stego.flatten()
        extracted_bits = []
        
        for pixel in flat_stego:
            # Extract LSB
            extracted_bits.append(str(pixel & 1))
            
            # Check for null terminator every 8 bits
            if len(extracted_bits) >= 8 and len(extracted_bits) % 8 == 0:
                last_byte = ''.join(extracted_bits[-8:])
                if last_byte == '00000000':
                    # Null terminator found, stop extraction
                    extracted_bits = extracted_bits[:-8]
                    break
                    
        # Convert binary string back to characters
        binary_str = ''.join(extracted_bits)
        chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]
        return ''.join(chars)
