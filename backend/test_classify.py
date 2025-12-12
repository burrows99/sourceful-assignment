#!/usr/bin/env python3
"""
Test script for the /classify endpoint
Demonstrates how to use the animal classification API
"""

import httpx
import asyncio
import json


async def test_classify_endpoint():
    """Test the classify endpoint with sample images"""
    
    base_url = "http://localhost:8000"
    
    test_cases = [
        {
            "name": "Cat image",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        },
        {
            "name": "Dog image",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Collage_of_Nine_Dogs.jpg/1200px-Collage_of_Nine_Dogs.jpg"
        },
        {
            "name": "Nature boardwalk (no animals)",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
        },
        {
            "name": "Multiple animals",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Welshcorgipembroke.JPG/1200px-Welshcorgipembroke.JPG"
        }
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("Testing /classify endpoint...\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}: {test_case['name']}")
            print(f"URL: {test_case['url']}")
            
            try:
                response = await client.post(
                    f"{base_url}/classify",
                    json={"imgUrl": test_case['url']}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Status: {response.status_code}")
                    print(f"Animals detected: {result['animals']}")
                    if result.get('error'):
                        print(f"Error: {result['error']}")
                else:
                    print(f"❌ Status: {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Request failed: {str(e)}")
            
            print("-" * 60)
            print()


if __name__ == "__main__":
    print("=" * 60)
    print("Animal Classification API Test")
    print("=" * 60)
    print()
    asyncio.run(test_classify_endpoint())
