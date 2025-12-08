# Abstract provider interface for image generation
# This allows swapping between different image generation providers (DALL-E, Stable Diffusion, etc.)

from abc import ABC, abstractmethod
from typing import List
import time


class ImageProvider(ABC):
    """Abstract base class for image generation providers"""
    
    @abstractmethod
    async def generate_images(self, prompt: str, num_images: int) -> List[str]:
        """
        Generate images based on a prompt
        
        Args:
            prompt: The text prompt for image generation
            num_images: Number of images to generate
            
        Returns:
            List of image URLs
        """
        pass


class MockImageProvider(ImageProvider):
    """
    Mock image provider for development/testing
    Simulates API calls with delays and returns placeholder URLs
    
    To replace with a real provider (e.g., DALL-E, Stable Diffusion):
    1. Create a new class that inherits from ImageProvider
    2. Implement the generate_images method with actual API calls
    3. Update the provider instance in config.py
    
    Example for DALL-E:
    ```python
    class DallEProvider(ImageProvider):
        def __init__(self, api_key: str):
            self.client = openai.OpenAI(api_key=api_key)
            
        async def generate_images(self, prompt: str, num_images: int) -> List[str]:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=num_images,
                size="1024x1024"
            )
            return [img.url for img in response.data]
    ```
    """
    
    def __init__(self, delay_seconds: float):
        """
        Initialize mock provider
        
        Args:
            delay_seconds: Simulated API call delay
        """
        self.delay_seconds = delay_seconds
    
    async def generate_images(self, prompt: str, num_images: int) -> List[str]:
        """
        Simulate image generation with a delay
        
        Args:
            prompt: The text prompt (e.g., "a cute cat")
            num_images: Number of images to generate
            
        Returns:
            List of placeholder image URLs
        """
        # Simulate API call delay
        time.sleep(self.delay_seconds)
        
        # Generate placeholder URLs
        # In production, these would be actual URLs from the image generation service
        base_url = "https://placehold.co/512x512/png"
        return [
            f"{base_url}?text={prompt.replace(' ', '+')}+{i+1}"
            for i in range(num_images)
        ]


# Factory function to get the appropriate provider
def get_image_provider(delay_seconds: float = 2.0) -> ImageProvider:
    """
    Factory function to instantiate the image provider
    
    To switch providers, modify this function:
    - For development/testing: return MockImageProvider(delay_seconds)
    - For production with DALL-E: return DallEProvider(api_key=os.getenv("OPENAI_API_KEY"))
    - For Stable Diffusion: return StableDiffusionProvider(api_key=os.getenv("SD_API_KEY"))
    
    Args:
        delay_seconds: Delay for mock provider
    """
    return MockImageProvider(delay_seconds=delay_seconds)
