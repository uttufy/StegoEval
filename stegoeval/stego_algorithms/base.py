from abc import ABC, abstractmethod
import numpy as np


class StegoAlgorithm(ABC):
    """
    Abstract base class for all steganography algorithms in StegoEval.
    """

    @abstractmethod
    def embed(self, cover: np.ndarray, payload: str) -> np.ndarray:
        """
        Embed a secret payload into the cover image.

        Args:
            cover (np.ndarray): The cover image (grayscale or RGB) as a numpy array.
            payload (str): The secret message or binary string to embed.

        Returns:
            np.ndarray: The resulting stego image.
        """
        pass

    @abstractmethod
    def extract(self, stego: np.ndarray) -> str:
        """
        Extract the secret payload from a stego image.

        Args:
            stego (np.ndarray): The stego image as a numpy array.

        Returns:
            str: The extracted secret message or binary string.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        Return the unique name of the algorithm.

        Returns:
            str: Algorithm name.
        """
        pass
