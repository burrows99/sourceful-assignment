"""
Template for adding a new vision provider
Copy this file and implement the required methods for your provider
"""

from providers import BaseVisionProvider, VisionProvider
import httpx


# Option 1: Inherit from BaseVisionProvider (Recommended)
# Use this when the provider uses OpenAI-compatible chat/completions format
class MyCustomProvider(BaseVisionProvider):
    """
    Custom provider implementation using BaseVisionProvider
    
    This inherits common functionality, you only need to override
    what's different for your specific provider.
    """
    
    def __init__(self, api_key: str, model: str = "default-model", timeout: float = 30.0):
        """
        Initialize your custom provider
        
        Args:
            api_key: API key for authentication
            model: Model identifier (use your provider's model name)
            timeout: Request timeout in seconds
        """
        # Initialize base with your API endpoint
        super().__init__(
            api_key=api_key,
            model=model,
            api_url="https://api.yourprovider.com/v1/vision",  # Your endpoint
            timeout=timeout
        )
        # Add any provider-specific initialization here
        self.custom_param = "value"
    
    def _build_headers(self) -> dict:
        """
        Override if your provider uses different headers
        Default: {"Authorization": "Bearer <key>", "Content-Type": "application/json"}
        """
        headers = super()._build_headers()
        # Add custom headers if needed
        headers["X-Custom-Header"] = "value"
        return headers
    
    def _build_payload(self, image_url: str, prompt: str) -> dict:
        """
        Override if your provider uses different request format
        
        Default format (OpenAI-compatible):
        {
            "model": "...",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "..."},
                        {"type": "image_url", "image_url": {"url": "..."}}
                    ]
                }
            ]
        }
        """
        # If format is the same, you don't need to override
        # Otherwise, return your custom format:
        return {
            "model": self.model,
            "prompt": prompt,
            "image": image_url,
            # Add your custom fields
        }
    
    def _parse_response(self, response_data: dict) -> str:
        """
        Override to parse your provider's response format
        Should return the text content from the AI response
        
        Default extracts: response["choices"][0]["message"]["content"]
        """
        # Example for different format:
        return response_data.get("result", {}).get("text", "")


# Option 2: Implement VisionProvider directly (Advanced)
# Use this when your provider is very different from the standard format
class MyCompletelyDifferentProvider(VisionProvider):
    """
    Custom provider implementing VisionProvider from scratch
    
    Use this when your provider has a completely different API structure
    that doesn't fit the BaseVisionProvider pattern.
    """
    
    def __init__(self, api_key: str, model: str = "default", **kwargs):
        self.api_key = api_key
        self.model = model
        # Add any custom initialization
    
    async def classify_image(self, image_url: str) -> dict:
        """
        Implement the classification logic
        
        Must return:
        {
            "animals": ["animal1", "animal2", ...],  # List of detected animals
            "error": "error message" or None          # Optional error message
        }
        """
        try:
            # Your custom API call logic here
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Make your API request
                response = await client.post(
                    "https://api.yourprovider.com/classify",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"image_url": image_url, "model": self.model}
                )
                response.raise_for_status()
                
                # Parse your response
                data = response.json()
                animals = data.get("detected_animals", [])
                
                if not animals:
                    return {"animals": [], "error": "No animals detected in the image"}
                
                return {"animals": animals}
                
        except httpx.HTTPStatusError as e:
            return {"animals": [], "error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"animals": [], "error": f"Classification failed: {str(e)}"}


# ============================================================================
# Integration Steps After Creating Your Provider
# ============================================================================

"""
1. Add to providers.py:
   - Import your class
   - OR implement it directly in providers.py

2. Update get_vision_provider() factory in providers.py:

    def get_vision_provider(...):
        # ... existing code ...
        
        elif provider_type == "mycustom":
            return MyCustomProvider(
                api_key=api_key,
                model=model or "default-model",
                timeout=timeout
            )

3. Update config.py:

    class Settings(BaseSettings):
        # ... existing code ...
        
        # MyCustom Settings (when VISION_PROVIDER=mycustom)
        MYCUSTOM_API_KEY: str = ""

4. Update routes.py classify_image():

    elif provider_type == "mycustom":
        api_key = settings.MYCUSTOM_API_KEY
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="MyCustom API key not configured."
            )

5. Update .env and .env.example:

    # MyCustom API Configuration (when VISION_PROVIDER=mycustom)
    MYCUSTOM_API_KEY=your_api_key_here

6. Update docker-compose.yml:

    environment:
      - MYCUSTOM_API_KEY=${MYCUSTOM_API_KEY:-}

7. Test your provider:

    # Update .env
    VISION_PROVIDER=mycustom
    MYCUSTOM_API_KEY=your-key
    
    # Restart
    docker-compose restart backend
    
    # Test
    curl -X POST http://localhost:8000/classify \
      -H "Content-Type: application/json" \
      -d '{"imgUrl": "https://example.com/test.jpg"}'

8. Document your provider in PROVIDER_ARCHITECTURE.md
"""
