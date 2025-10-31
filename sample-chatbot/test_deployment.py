#!/usr/bin/env python3
"""
Test script for Sample Chatbot deployment
Run this to verify your chatbot is working correctly
"""

import requests
import json
import sys
from typing import Dict, Any

def test_health_endpoint(base_url: str) -> bool:
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat_endpoint(base_url: str) -> bool:
    """Test the chat functionality"""
    print("💬 Testing chat endpoint...")
    try:
        test_message = {
            "message": "Hello, can you introduce yourself?",
            "history": []
        }
        
        response = requests.post(
            f"{base_url}/api/chat",
            json=test_message,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat test passed!")
            print(f"🤖 AI Response: {data.get('response', 'No response')}")
            print(f"⏰ Timestamp: {data.get('timestamp', 'No timestamp')}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_models_endpoint(base_url: str) -> bool:
    """Test the models listing endpoint"""
    print("🧪 Testing models endpoint...")
    try:
        response = requests.get(f"{base_url}/api/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Models endpoint passed: {len(models)} models available")
            if models:
                print(f"📋 Available models: {', '.join(models[:3])}...")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def test_ui_accessibility(base_url: str) -> bool:
    """Test if the UI is accessible"""
    print("🎨 Testing UI accessibility...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if "chat-container" in content and "Sample Chatbot" in content:
                print("✅ UI is accessible and contains expected elements")
                return True
            else:
                print("❌ UI accessible but content may be incomplete")
                return False
        else:
            print(f"❌ UI accessibility failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ UI accessibility error: {e}")
        return False

def run_comprehensive_test(base_url: str) -> Dict[str, bool]:
    """Run all tests and return results"""
    print(f"🚀 Starting comprehensive test for: {base_url}")
    print("=" * 50)
    
    results = {
        "health": test_health_endpoint(base_url),
        "chat": test_chat_endpoint(base_url),
        "models": test_models_endpoint(base_url),
        "ui": test_ui_accessibility(base_url)
    }
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name.capitalize()}: {status}")
    
    print(f"\n🎯 Overall Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is working correctly!")
        return results
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return results

def interactive_test():
    """Interactive test mode"""
    print("🤖 Sample Chatbot - Interactive Test Mode")
    print("=" * 40)
    
    base_url = input("Enter your chatbot URL (e.g., https://your-app.up.railway.app): ").strip()
    
    if not base_url:
        print("❌ URL is required!")
        return
    
    # Add protocol if missing
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    results = run_comprehensive_test(base_url)
    
    # Save results to file
    with open('test_results.json', 'w') as f:
        json.dump({
            'timestamp': '2025-10-31T05:40:49Z',
            'url': base_url,
            'results': results,
            'all_passed': all(results.values())
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: test_results.json")

def main():
    """Main function"""
    print("🤖 Sample Chatbot - Deployment Test Script")
    print("=" * 45)
    print()
    
    if len(sys.argv) > 1:
        # Command line mode
        base_url = sys.argv[1]
        results = run_comprehensive_test(base_url)
        sys.exit(0 if all(results.values()) else 1)
    else:
        # Interactive mode
        interactive_test()

if __name__ == "__main__":
    main()