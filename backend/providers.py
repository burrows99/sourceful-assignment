# Unified provider interface for AI models
# Supports both text-to-image generation and image-to-text classification

from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio


class BaseProvider(ABC):
    """
    Unified base provider for all AI model capabilities
    Providers can implement one or both capabilities: image generation and vision classification
    """
    
    @abstractmethod
    async def generate_images(self, prompt: str, num_images: int) -> List[str]:
        """
        Generate images based on a prompt (text-to-image)
        
        Args:
            prompt: The text prompt for image generation
            num_images: Number of images to generate
            
        Returns:
            List of image URLs or base64 data URLs
        """
        raise NotImplementedError("This provider does not support image generation")
    
    @abstractmethod
    async def classify_image(self, image_url: str) -> dict:
        """
        Classify/analyze an image (image-to-text)
        
        Args:
            image_url: URL of the image to classify
            
        Returns:
            Dictionary with classification results (e.g., {'animals': [...], 'error': '...'})
        """
        raise NotImplementedError("This provider does not support image classification")


class OpenRouterProvider(BaseProvider):
    """
    Unified OpenRouter provider supporting both image generation and vision classification
    Can use different models for each task or a multimodal model for both
    """
    
    def __init__(self, 
                 api_key: str,
                 image_model: str = "sourceful/riverflow-v2-max-preview",
                 vision_model: str = "openai/gpt-4o-mini",
                 site_url: str = "",
                 site_name: str = "",
                 timeout: float = 60.0):
        """
        Initialize OpenRouter unified provider
        
        Args:
            api_key: OpenRouter API key
            image_model: Model to use for image generation (text-to-image)
            vision_model: Model to use for image classification (image-to-text)
            site_url: Optional site URL for rankings on openrouter.ai
            site_name: Optional site name for rankings on openrouter.ai
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.image_model = image_model
        self.vision_model = vision_model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.site_url = site_url
        self.site_name = site_name
        self.timeout = timeout
    
    def _build_headers(self) -> dict:
        """Build headers for OpenRouter API request"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.site_name:
            headers["X-Title"] = self.site_name
        return headers
    
    async def generate_images(self, prompt: str, num_images: int) -> List[str]:
        """
        Generate images using OpenRouter API (text-to-image)
        
        Args:
            prompt: The text prompt for image generation
            num_images: Number of images to generate (currently generates 1 per request)
            
        Returns:
            List of base64-encoded data URLs in format: data:image/png;base64,<data>
            These can be directly used in <img> tags or saved to files
        """
        import httpx
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.image_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "modalities": ["image", "text"]
                }
                
                response = await client.post(
                    self.api_url,
                    headers=self._build_headers(),
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                message = result.get("choices", [{}])[0].get("message", {})
                
                # Extract image URLs from the response
                image_urls = []
                if "images" in message:
                    for image in message["images"]:
                        image_url = image.get("image_url", {}).get("url", "")
                        if image_url:
                            image_urls.append(image_url)
                
                # If we need multiple images, we would need to make multiple requests
                # For now, return what we got (usually 1 image per request)
                if not image_urls:
                    raise ValueError("No images generated in response")
                
                return image_urls
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API request failed: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    async def classify_image(self, image_url: str) -> dict:
        """
        Classify animals in an image using OpenRouter API (image-to-text)
        
        Args:
            image_url: URL of the image to classify
            
        Returns:
            Dictionary with 'animals' list and optional 'error' message
        """
        import httpx
        
        prompt = "Identify all animals in this image. List only the animal names, separated by commas. If there are no animals, respond with 'NONE'."
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.vision_model,
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
                
                response = await client.post(
                    self.api_url,
                    headers=self._build_headers(),
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Parse response
                if "NONE" in content.upper() or "NO ANIMAL" in content.upper():
                    return {"animals": [], "error": "No animals detected in the image"}
                
                animals = [animal.strip() for animal in content.split(",") if animal.strip()]
                
                if not animals:
                    return {"animals": [], "error": "No animals detected in the image"}
                
                return {"animals": animals}
                
        except httpx.HTTPStatusError as e:
            return {"animals": [], "error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"animals": [], "error": f"Classification failed: {str(e)}"}


class MockProvider(BaseProvider):
    """
    Unified mock provider for testing both image generation and vision classification
    Simulates API calls with delays and returns placeholder data
    """
    
    def __init__(self, delay_seconds: float = 2.0):
        """
        Initialize mock provider
        
        Args:
            delay_seconds: Simulated API call delay
        """
        self.delay_seconds = delay_seconds
    
    async def generate_images(self, prompt: str, num_images: int) -> List[str]:
        """
        Simulate image generation with a delay (text-to-image)
        
        Args:
            prompt: The text prompt (e.g., "a cute cat")
            num_images: Number of images to generate
            
        Returns:
            List of placeholder image URLs
        """
        # Simulate API call delay
        await asyncio.sleep(self.delay_seconds * num_images)
        
        # Generate placeholder URLs
        base_url = "https://placehold.co/512x512/png"
        return [
            f"{base_url}?text={prompt.replace(' ', '+')}+{i+1}"
            for i in range(num_images)
        ]
    
    async def classify_image(self, image_url: str) -> dict:
        """
        Return mock classification results (image-to-text)
        
        Args:
            image_url: URL of the image to classify
            
        Returns:
            Dictionary with 'animals' list and optional 'error' message
        """
        # Simulate network delay
        await asyncio.sleep(0.5)
        
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


# Unified factory function
def get_provider(
    provider_type: str = "mock",
    api_key: str = "",
    image_model: str = "",
    vision_model: str = "",
    site_url: str = "",
    site_name: str = "",
    timeout: float = 60.0,
    delay_seconds: float = 2.0
) -> BaseProvider:
    """
    Unified factory function to instantiate a provider with both capabilities
    
    This design makes it easy to swap providers by changing configuration.
    All providers support both image generation and vision classification.
    
    Args:
        provider_type: Type of provider ("openrouter", "mock")
        api_key: API key for authentication
        image_model: Model for image generation (provider-specific defaults if empty)
        vision_model: Model for vision classification (provider-specific defaults if empty)
        site_url: Optional site URL (for OpenRouter rankings)
        site_name: Optional site name (for OpenRouter rankings)
        timeout: Request timeout in seconds
        delay_seconds: Delay for mock provider
        
    Returns:
        Configured BaseProvider instance with both capabilities
        
    Examples:
        # OpenRouter with both capabilities
        provider = get_provider(
            "openrouter",
            api_key="sk-...",
            image_model="sourceful/riverflow-v2-max-preview",
            vision_model="openai/gpt-4o-mini"
        )
        
        # Mock for testing
        provider = get_provider("mock", delay_seconds=2.0)
        
        # Use the same provider for both tasks:
        images = await provider.generate_images("a cute cat", 1)
        animals = await provider.classify_image(images[0])
    """
    provider_type = provider_type.lower()
    
    if provider_type == "openrouter":
        if not api_key:
            raise ValueError("OpenRouter API key is required")
        return OpenRouterProvider(
            api_key=api_key,
            image_model=image_model or "sourceful/riverflow-v2-max-preview",
            vision_model=vision_model or "openai/gpt-4o-mini",
            site_url=site_url,
            site_name=site_name,
            timeout=timeout
        )
    
    elif provider_type == "mock":
        return MockProvider(delay_seconds=delay_seconds)
    
    else:
        raise ValueError(
            f"Unknown provider type: {provider_type}. "
            f"Supported types: openrouter, mock"
        )


# Backward compatibility aliases
def get_image_provider(
    provider_type: str = "mock",
    api_key: str = "",
    model: str = "",
    site_url: str = "",
    site_name: str = "",
    timeout: float = 60.0,
    delay_seconds: float = 2.0
) -> BaseProvider:
    """Legacy function for image generation - use get_provider() instead"""
    return get_provider(
        provider_type=provider_type,
        api_key=api_key,
        image_model=model,
        vision_model="",
        site_url=site_url,
        site_name=site_name,
        timeout=timeout,
        delay_seconds=delay_seconds
    )


def get_vision_provider(
    provider_type: str = "openrouter",
    api_key: str = "",
    model: str = "",
    site_url: str = "",
    site_name: str = "",
    timeout: float = 30.0
) -> BaseProvider:
    """Legacy function for vision classification - use get_provider() instead"""
    return get_provider(
        provider_type=provider_type,
        api_key=api_key,
        image_model="",
        vision_model=model,
        site_url=site_url,
        site_name=site_name,
        timeout=timeout,
        delay_seconds=2.0
    )
