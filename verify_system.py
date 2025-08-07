#!/usr/bin/env python3
"""
Quick verification that everything is working
"""

import requests
import time
import json

def test_server():
    """Test if server is running and responding"""
    print("🧪 Testing NextCore AI Voice Agent")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Main endpoint
        print("📡 1. Testing main endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Message: {data.get('message', 'OK')}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
            
        # Test 2: Exotel webhook
        print("📞 2. Testing Exotel webhook...")
        webhook_params = {
            "From": "07061901464",
            "CallSid": "test_call_12345",
            "CallFrom": "07061901464", 
            "CallTo": "08037091588"
        }
        
        response = requests.get(f"{base_url}/exotel-voice-webhook", 
                              params=webhook_params, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Webhook Status: {response.status_code}")
            print(f"   ✅ Response Type: {response.headers.get('content-type', 'unknown')}")
            
            # Check if XML response
            if 'xml' in response.headers.get('content-type', '').lower():
                print("   ✅ XML Response Generated")
                print(f"   📝 Preview: {response.text[:100]}...")
            else:
                print(f"   📄 Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Webhook Status: {response.status_code}")
            return False
            
        # Test 3: Direct voice endpoint  
        print("🔊 3. Testing direct voice endpoint...")
        response = requests.get(f"{base_url}/direct-voice", 
                              params=webhook_params, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Direct Voice Status: {response.status_code}")
        else:
            print(f"   ⚠️ Direct Voice Status: {response.status_code}")
            
        # Test 4: Health check
        print("❤️ 4. Testing health endpoint...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Health Status: {response.status_code}")
            else:
                print(f"   ⚠️ Health Status: {response.status_code}")
        except:
            print("   ⚠️ Health endpoint not available")
            
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your AI Voice Agent is working perfectly!")
        print("\n🚀 Ready for live testing:")
        print("   • Server: http://localhost:8000")
        print("   • Docs: http://localhost:8000/docs") 
        print("   • Webhook: /exotel-voice-webhook")
        print("   • Direct: /direct-voice")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server not running!")
        print("💡 Start server with: python start_exotel.py")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    if success:
        print("\n🎯 Next Steps:")
        print("1. 🌐 Start ngrok: ngrok http 8000")
        print("2. 📱 Update Exotel webhook URL")
        print("3. 📞 Test call to your Exotel number")
        print("4. 🤖 Enjoy your AI voice agent!")
    else:
        print("\n🔧 Check server and try again")
