"""
Unit tests for classify endpoint and vision providers
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.unit
class TestClassifyEndpoint:
    """Unit tests for the /classify endpoint"""
    
    async def test_classify_success(self, client: AsyncClient):
        """Test successful animal classification"""
        with patch('routes.get_vision_provider') as mock_provider:
            # Mock provider response
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": ["cat", "dog"],
                "error": None
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "animals" in data
            assert "cat" in data["animals"]
            assert "dog" in data["animals"]
            assert data["error"] is None
    
    async def test_classify_no_animals(self, client: AsyncClient):
        """Test classification when no animals detected"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": [],
                "error": "No animals detected in the image"
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/nature.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["animals"] == []
            assert "No animals detected" in data["error"]
    
    async def test_classify_invalid_url(self, client: AsyncClient):
        """Test classification with invalid URL format"""
        response = await client.post(
            "/classify",
            json={"imgUrl": "not-a-valid-url"}
        )
        
        assert response.status_code == 400
        assert "Invalid image URL" in response.json()["detail"]
    
    async def test_classify_missing_api_key(self, client: AsyncClient):
        """Test classification when API key is not configured"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "openrouter"
            mock_settings.OPENROUTER_API_KEY = ""
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            assert response.status_code == 500
            assert "API key not configured" in response.json()["detail"]
    
    async def test_classify_api_error(self, client: AsyncClient):
        """Test classification when API returns error"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": [],
                "error": "API request failed: 429 Too Many Requests"
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["animals"] == []
            assert "API request failed" in data["error"]
    
    async def test_classify_unknown_provider(self, client: AsyncClient):
        """Test classification with unknown provider type"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "unknown_provider"
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            assert response.status_code == 500
            assert "Unknown vision provider" in response.json()["detail"]


@pytest.mark.unit
class TestVisionProviders:
    """Unit tests for vision provider implementations"""
    
    @pytest.mark.asyncio
    async def test_mock_provider_cat(self):
        """Test mock provider with cat image"""
        from providers import MockProvider
        
        provider = MockProvider()
        result = await provider.classify_image("https://example.com/cat.jpg")
        
        assert result["animals"] == ["cat"]
        assert result.get("error") is None
    
    @pytest.mark.asyncio
    async def test_mock_provider_dog(self):
        """Test mock provider with dog image"""
        from providers import MockProvider
        
        provider = MockProvider()
        result = await provider.classify_image("https://example.com/dog-photo.jpg")
        
        assert result["animals"] == ["dog"]
    
    @pytest.mark.asyncio
    async def test_mock_provider_bird(self):
        """Test mock provider with bird image"""
        from providers import MockProvider
        
        provider = MockProvider()
        result = await provider.classify_image("https://example.com/bird-picture.jpg")
        
        assert result["animals"] == ["bird"]
    
    @pytest.mark.asyncio
    async def test_mock_provider_no_animals(self):
        """Test mock provider with no animal keywords"""
        from providers import MockProvider
        
        provider = MockProvider()
        result = await provider.classify_image("https://example.com/landscape.jpg")
        
        assert result["animals"] == []
        assert "No animals detected" in result["error"]
    
    @pytest.mark.asyncio
    async def test_mock_provider_supports_both_capabilities(self):
        """Test that mock provider supports both image generation and classification"""
        from providers import MockProvider
        
        provider = MockProvider(delay_seconds=0.1)
        
        # Test image generation
        images = await provider.generate_images("a cute cat", 2)
        assert len(images) == 2
        
        # Test classification
        result = await provider.classify_image("https://example.com/cat.jpg")
        assert "animals" in result
    
    @pytest.mark.asyncio
    async def test_provider_factory_openrouter(self):
        """Test factory creates OpenRouter provider"""
        from providers import get_vision_provider, OpenRouterProvider
        
        provider = get_vision_provider(
            provider_type="openrouter",
            api_key="test-key",
            model="test-model"
        )
        
        assert isinstance(provider, OpenRouterProvider)
        assert provider.api_key == "test-key"
        assert provider.vision_model == "test-model"
    
    @pytest.mark.asyncio
    async def test_provider_factory_mock(self):
        """Test factory creates Mock provider"""
        from providers import get_vision_provider, MockProvider
        
        provider = get_vision_provider(provider_type="mock")
        
        assert isinstance(provider, MockProvider)
    
    @pytest.mark.asyncio
    async def test_provider_factory_invalid(self):
        """Test factory raises error for invalid provider"""
        from providers import get_vision_provider
        
        with pytest.raises(ValueError) as exc_info:
            get_vision_provider(provider_type="invalid")
        
        assert "Unknown provider type" in str(exc_info.value)
