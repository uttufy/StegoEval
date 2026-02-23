import os
import subprocess
import tempfile
import cv2
import numpy as np
from typing import Any

from stegoeval.stego_algorithms.base import StegoAlgorithm

class GenericCLIAdapter(StegoAlgorithm):
    """
    An adapter that integrates an external CLI-based steganography technique 
    (like a paper's demo script requiring generated side-channel files) into StegoEval.
    """
    def __init__(self, cli_script_path: str, venv_python_path: str = None):
        self.cli_script_path = cli_script_path
        # If the external script has its own virtual environment, point to its python executable
        # Default to system 'python3' if not provided
        self.python_exec = venv_python_path if venv_python_path else "python3"
        
        # We need a place to store intermediate files (e.g., a .npy key, or a .txt config)
        # between embed and extract.
        self.temp_dir = tempfile.mkdtemp(prefix="stegoeval_cli_")
        
        # Example: if the CLI requires storing a side-channel key file
        self.key_path = os.path.join(self.temp_dir, "original_key.npy")

    def name(self) -> str:
        return "Generic_CLI_Wrapper"

    def embed(self, cover_image: np.ndarray, payload: str) -> np.ndarray:
        """
        Since the CLI takes file paths, we must save the ndarray to disk,
        run the CLI, and then read the resulting stego image back into an ndarray.
        """
        # 1. Save cover_image (ndarray) to a temporary file
        cover_path = os.path.join(self.temp_dir, "temp_cover.png")
        stego_path = os.path.join(self.temp_dir, "temp_stego.png")
        
        cv2.imwrite(cover_path, cv2.cvtColor(cover_image, cv2.COLOR_RGB2BGR))

        # 2. Run the external CLI embed command using its own Python environment
        # Syntax: /path/to/their/.venv/bin/python script.py embed <cover> "Payload" -o <stego> -k <key>
        # Customize this command list to match the target CLI's actual expected arguments!
        command = [
            self.python_exec, self.cli_script_path, 
            "embed", cover_path, payload, 
            "-o", stego_path, 
            "-k", self.key_path
        ]
        
        try:
            # We use check=True to raise an error if the CLI fails
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"CLI Embed failed: {e.stderr}")

        # 3. Read the generated stego image back into an ndarray
        # The CLI should have generated stego_path and self.key_path
        stego_bgr = cv2.imread(stego_path)
        if stego_bgr is None:
            raise FileNotFoundError(f"CLI did not produce outputs at {stego_path}")

        # Convert back to RGB for StegoEval
        stego_image = cv2.cvtColor(stego_bgr, cv2.COLOR_BGR2RGB)
        
        # We keep self.key_path saved on disk for the extract step!
        return stego_image

    def extract(self, stego_image: np.ndarray) -> str:
        """
        Saves the potentially attacked stego image to disk, runs the CLI
        using the saved key file, and parses the output text.
        """
        stego_path = os.path.join(self.temp_dir, "attacked_stego.png")
        cv2.imwrite(stego_path, cv2.cvtColor(stego_image, cv2.COLOR_RGB2BGR))

        # 4. Run the external CLI extract command using its own Python environment
        # Syntax: /path/to/their/.venv/bin/python script.py extract <stego> <key>
        # Customize this command list to match the target CLI's actual expected arguments!
        command = [
            self.python_exec, self.cli_script_path, 
            "extract", stego_path, self.key_path
        ]
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            # The CLI prints to stdout. We assume the output is the text message.
            # You might need to parse `result.stdout` to slice out "Extracted: {"}"
            extracted_text = result.stdout.strip()
            
            # Example parsing if stdout is: "Successfully extracted: Secret Message"
            if "Secret Message" in extracted_text:
                pass # Parse accordingly
            
            return extracted_text
            
        except subprocess.CalledProcessError as e:
            # Under heavy attacks, the CLI script might crash/fail, so we handle it gracefully
            return "" # Empty string means complete extraction failure (BER 1.0)
            
    def cleanup(self):
        """Optional: Cleans up the temp directories after the benchmark."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
