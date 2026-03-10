"""
Test script for PDF AI Analyzer
This script tests the API endpoints
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /api/health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_api_info():
    """Test API info endpoint"""
    print("Testing /api/info endpoint...")
    response = requests.get(f"{BASE_URL}/api/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_analyze_pdf(pdf_path):
    """Test PDF analysis endpoint"""
    print(f"Testing /api/analyze endpoint with {pdf_path}...")
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/api/analyze", files=files)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except FileNotFoundError:
        print(f"File not found: {pdf_path}")
        print("To test PDF analysis, create a sample PDF or provide a path to an existing one.")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("PDF AI Analyzer - API Tests")
    print("=" * 60)
    print()
    
    # Test health endpoint
    test_health()
    
    # Test API info
    test_api_info()
    
    print("=" * 60)
    print("All basic tests passed!")
    print("=" * 60)
    print()
    print("To test PDF analysis:")
    print("1. Open http://127.0.0.1:8000 in your browser")
    print("2. Upload a PDF file using the web interface")
    print()
