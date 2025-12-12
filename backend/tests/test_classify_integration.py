"""
Integration tests for classify endpoint with real provider behavior
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.integration
class TestClassifyIntegration:
    """Integration tests for the classify endpoint"""
    
    async def test_classify_with_mock_provider(self, client: AsyncClient):
        """Test classify endpoint using mock provider (no API calls)"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            # Test with cat in URL
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/cat-photo.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "cat" in data["animals"]
    
    async def test_classify_with_different_animals(self, client: AsyncClient):
        """Test classify with different animal types"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            # Test dog
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/dog-image.jpg"}
            )
            assert response.status_code == 200
            assert "dog" in response.json()["animals"]
            
            # Test bird
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/bird-flying.jpg"}
            )
            assert response.status_code == 200
            assert "bird" in response.json()["animals"]
    
    async def test_classify_no_animals_detected(self, client: AsyncClient):
        """Test classify when no animals in image"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/landscape.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["animals"] == []
            assert "No animals detected" in data["error"]
    
    async def test_classify_response_structure(self, client: AsyncClient):
        """Test that classify returns correct response structure"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/cat.jpg"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "animals" in data
            assert "error" in data
            assert isinstance(data["animals"], list)
    
    async def test_classify_provider_switching(self, client: AsyncClient):
        """Test that provider can be switched via configuration"""
        # Test with mock provider for cat
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/cat-picture.jpg"}
            )
            
            assert response.status_code == 200
            assert "cat" in response.json()["animals"]
        
        # Test with mock provider for dog
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/dog-picture.jpg"}
            )
            
            assert response.status_code == 200
            assert "dog" in response.json()["animals"]
    
    async def test_classify_url_validation(self, client: AsyncClient):
        """Test URL validation in integration context"""
        response = await client.post(
            "/classify",
            json={"imgUrl": "invalid-url"}
        )
        
        assert response.status_code == 400
        assert "Invalid image URL" in response.json()["detail"]
    
    async def test_classify_concurrent_requests(self, client: AsyncClient):
        """Test multiple concurrent classify requests"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "mock"
            mock_settings.VISION_MODEL = ""
            mock_settings.VISION_TIMEOUT = 30.0
            
            # Make multiple requests
            responses = []
            for animal in ["cat", "dog", "bird"]:
                response = await client.post(
                    "/classify",
                    json={"imgUrl": f"https://example.com/{animal}.jpg"}
                )
                responses.append(response)
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
                assert len(response.json()["animals"]) > 0
