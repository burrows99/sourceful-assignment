# Abstract provider interface for image generation
# This allows swapping between different image generation providers (DALL-E, Stable Diffusion, etc.)

from abc import ABC, abstractmethod
from typing import List
import asyncio


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
        # Simulate API call delay (use asyncio.sleep for proper async behavior)
        await asyncio.sleep(self.delay_seconds * num_images)
        
        # Generate placeholder URLs
        # In production, these would be actual URLs from the image generation service
        base_url = "https://placehold.co/512x512/png"
        return [
            f"{base_url}?text={prompt.replace(' ', '+')}+{i+1}"
            for i in range(num_images)
        ]


class VisionProvider(ABC):
    """Abstract base class for vision/image classification providers"""
    
    @abstractmethod
    async def classify_image(self, image_url: str) -> dict:
        """
        Classify animals in an image
        
        Args:
            image_url: URL of the image to classify
            
        Returns:
            Dictionary with 'animals' list and optional 'error' message
        """
        pass


class BaseVisionProvider(VisionProvider):
    """
    Base implementation with common functionality for vision providers
    Subclasses only need to implement API-specific details
    """
    
    def __init__(self, api_key: str, model: str, api_url: str, timeout: float = 30.0):
        """
        Initialize base vision provider
        
        Args:
            api_key: API key for authentication
            model: Model identifier
            api_url: API endpoint URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.api_url = api_url
        self.timeout = timeout
    
    def _build_headers(self) -> dict:
        """Build headers for API request. Override in subclasses if needed."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def _build_payload(self, image_url: str, prompt: str) -> dict:
        """Build request payload. Override in subclasses for different formats."""
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        }
    
    def _parse_response(self, response_data: dict) -> str:
        """Parse API response to extract content. Override for different response formats."""
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    def _parse_animals(self, content: str) -> dict:
        """Parse AI response to extract animal names"""
        if "NONE" in content.upper() or "NO ANIMAL" in content.upper():
            return {"animals": [], "error": "No animals detected in the image"}
        
        # Extract animal names from the response
        animals = [animal.strip() for animal in content.split(",") if animal.strip()]
        
        if not animals:
            return {"animals": [], "error": "No animals detected in the image"}
        
        return {"animals": animals}
    
    async def classify_image(self, image_url: str) -> dict:
        """
        Classify animals in an image using the configured vision model
        
        Args:
            image_url: URL of the image to classify
            
        Returns:
            Dictionary with 'animals' list and optional 'error' message
        """
        import httpx
        
        prompt = "Identify all animals in this image. List only the animal names, separated by commas. If there are no animals, respond with 'NONE'."
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=self._build_headers(),
                    json=self._build_payload(image_url, prompt)
                )
                response.raise_for_status()
                
                result = response.json()
                content = self._parse_response(result)
                
                return self._parse_animals(content)
                
        except httpx.HTTPStatusError as e:
            return {"animals": [], "error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"animals": [], "error": f"Classification failed: {str(e)}"}


class OpenRouterVisionProvider(BaseVisionProvider):
    """
    OpenRouter provider with support for multiple vision models
    Easy to swap between models: GPT-4o, GPT-4o-mini, Claude, etc.
    """
    
    def __init__(self, api_key: str, model: str = "openai/gpt-4o-mini", 
                 site_url: str = "", site_name: str = "", timeout: float = 30.0):
        """
        Initialize OpenRouter provider
        
        Args:
            api_key: OpenRouter API key
            model: Model to use (e.g., "openai/gpt-4o-mini", "anthropic/claude-3-5-sonnet")
            site_url: Optional site URL for rankings on openrouter.ai
            site_name: Optional site name for rankings on openrouter.ai
            timeout: Request timeout in seconds
        """
        super().__init__(api_key, model, "https://openrouter.ai/api/v1/chat/completions", timeout)
        self.site_url = site_url
        self.site_name = site_name
    
    def _build_headers(self) -> dict:
        """Add OpenRouter-specific headers"""
        headers = super()._build_headers()
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.site_name:
            headers["X-Title"] = self.site_name
        return headers


class OpenAIVisionProvider(BaseVisionProvider):
    """
    Direct OpenAI provider (if you want to use OpenAI directly instead of through OpenRouter)
    Example of how easy it is to add a new provider
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", timeout: float = 30.0):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model: Model to use (e.g., "gpt-4o-mini", "gpt-4o")
            timeout: Request timeout in seconds
        """
        super().__init__(api_key, model, "https://api.openai.com/v1/chat/completions", timeout)


class MockVisionProvider(VisionProvider):
    """
    Mock provider for testing without API calls
    Returns predefined responses based on image URL patterns
    """
    
    async def classify_image(self, image_url: str) -> dict:
        """Return mock classification results"""
        await asyncio.sleep(0.5)  # Simulate network delay
        
        # Simple pattern matching for testing
        url_lower = image_url.lower()
        if "cat" in url_lower:
            return {"animals": ["cat"]}
        elif "dog" in url_lower:
            return {"animals": ["dog"]}
        elif "bird" in url_lower:
            return {"animals": ["bird"]}
        else:
            return {"animals": [], "error": "No animals detected in the image"}


# Factory function to get the appropriate provider
def get_image_provider(delay_seconds: float = 20.0) -> ImageProvider:
    """
    Factory function to instantiate the image provider
    
    To switch providers, modify this function:
    - For development/testing: return MockImageProvider(delay_seconds)
    - For production with DALL-E: return DallEProvider(api_key=os.getenv("OPENAI_API_KEY"))
    - For Stable Diffusion: return StableDiffusionProvider(api_key=os.getenv("SD_API_KEY"))
    
    Args:
        delay_seconds: Delay per image for mock provider (default 5s simulates realistic API calls)
    """
    return MockImageProvider(delay_seconds=delay_seconds)


def get_vision_provider(
    provider_type: str = "openrouter",
    api_key: str = "",
    model: str = "",
    site_url: str = "",
    site_name: str = "",
    timeout: float = 30.0
) -> VisionProvider:
    """
    Factory function to instantiate the vision provider
    
    This design makes it easy to swap providers by changing configuration.
    Add new providers by:
    1. Create a new class inheriting from VisionProvider or BaseVisionProvider
    2. Add a case in this factory function
    3. Update configuration settings
    
    Args:
        provider_type: Type of provider ("openrouter", "openai", "mock")
        api_key: API key for authentication
        model: Model identifier (provider-specific defaults if empty)
        site_url: Optional site URL (for OpenRouter rankings)
        site_name: Optional site name (for OpenRouter rankings)
        timeout: Request timeout in seconds
        
    Returns:
        Configured VisionProvider instance
        
    Examples:
        # OpenRouter with GPT-4o-mini (default)
        provider = get_vision_provider("openrouter", api_key="sk-...")
        
        # OpenRouter with Claude
        provider = get_vision_provider("openrouter", api_key="sk-...", model="anthropic/claude-3-5-sonnet")
        
        # Direct OpenAI
        provider = get_vision_provider("openai", api_key="sk-...")
        
        # Mock for testing
        provider = get_vision_provider("mock")
    """
    provider_type = provider_type.lower()
    
    if provider_type == "openrouter":
        default_model = model or "openai/gpt-4o-mini"
        return OpenRouterVisionProvider(
            api_key=api_key,
            model=default_model,
            site_url=site_url,
            site_name=site_name,
            timeout=timeout
        )
    
    elif provider_type == "openai":
        default_model = model or "gpt-4o-mini"
        return OpenAIVisionProvider(
            api_key=api_key,
            model=default_model,
            timeout=timeout
        )
    
    elif provider_type == "mock":
        return MockVisionProvider()
    
    else:
        raise ValueError(
            f"Unknown provider type: {provider_type}. "
            f"Supported types: openrouter, openai, mock"
        )
