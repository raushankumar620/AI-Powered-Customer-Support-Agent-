#!/usr/bin/env python3
"""
Live Testing Guide for NextCore AI Voice Agent
Complete step-by-step process for going live with Exotel
"""

import time
import subprocess
import requests
from datetime import datetime

def print_live_testing_guide():
    """Print complete live testing instructions"""
    
    print("🎯 NextCore AI Voice Agent - LIVE TESTING GUIDE")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Your system is ready for live testing!")
    print("=" * 60)
    
    print("\n🚀 STEP 1: Start Your Server")
    print("-" * 30)
    print("Command: python start_exotel.py")
    print("Expected: Server running on http://localhost:8000")
    print("Status: ✅ Ready to execute")
    
    print("\n🌐 STEP 2: Start ngrok Tunnel")
    print("-" * 30)
    print("Command: ngrok http 8000")
    print("Expected: Public HTTPS URL (e.g., https://abc123.ngrok.io)")
    print("Action: Copy the HTTPS URL")
    print("Status: ⏳ Ready to execute")
    
    print("\n📱 STEP 3: Configure Exotel Dashboard")
    print("-" * 30)
    print("1. Login to your Exotel account")
    print("2. Go to 'Numbers' section")
    print("3. Select your ExoPhone number")
    print("4. Find 'Flow' or 'Passthru' settings")
    print("5. Set Passthru URL: https://your-ngrok-url.ngrok.io/exotel-voice-webhook")
    print("6. Set Method: POST")
    print("7. 🚨 CRITICAL: DISABLE PIN authentication!")
    print("8. Save settings")
    print("Status: ⏳ Waiting for manual setup")
    
    print("\n📞 STEP 4: Test Call Flow")
    print("-" * 30)
    print("1. Call your Exotel number from any phone")
    print("2. Expected response: 'Hello! Welcome to NextCore AI...'")
    print("3. NO PIN should be asked!")
    print("4. Speak your question or press keys")
    print("5. AI should respond professionally")
    print("Status: ⏳ Ready for testing")
    
    print("\n🔍 STEP 5: Monitor & Debug")
    print("-" * 30)
    print("Commands to check status:")
    print("• python verify_system.py")
    print("• python diagnose_exotel.py") 
    print("• Check server logs")
    print("• Check Exotel dashboard logs")
    print("Status: ✅ Tools ready")

def test_server_readiness():
    """Test if server is ready for live testing"""
    
    print("\n🧪 TESTING SERVER READINESS...")
    print("-" * 40)
    
    try:
        # Test main endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Server: Running")
        else:
            print(f"❌ Server: Error {response.status_code}")
            return False
            
        # Test webhook endpoint
        webhook_params = {
            "From": "07061901464",
            "CallSid": "live_test_123"
        }
        response = requests.get("http://localhost:8000/exotel-voice-webhook", 
                              params=webhook_params, timeout=10)
        if response.status_code == 200:
            print("✅ Webhook: Ready")
        else:
            print(f"❌ Webhook: Error {response.status_code}")
            return False
            
        print("✅ Server is ready for live testing!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server not running!")
        print("💡 Start with: python start_exotel.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def provide_troubleshooting_tips():
    """Provide troubleshooting tips for common issues"""
    
    print("\n🔧 TROUBLESHOOTING TIPS")
    print("-" * 30)
    
    print("\n❌ If call asks for PIN:")
    print("   → Go to Exotel dashboard")
    print("   → Numbers → Settings")
    print("   → Disable PIN authentication")
    print("   → Save and try again")
    
    print("\n❌ If call disconnects immediately:")
    print("   → Check ngrok URL is correct")
    print("   → Verify webhook URL in Exotel")
    print("   → Check server logs for errors")
    
    print("\n❌ If AI doesn't respond:")
    print("   → Fallback system should work")
    print("   → Check OpenAI quota (if needed)")
    print("   → Verify knowledge base loaded")
    
    print("\n❌ If webhook not receiving calls:")
    print("   → Restart ngrok: ngrok http 8000")
    print("   → Update new URL in Exotel")
    print("   → Check Exotel flow configuration")

def main():
    """Main live testing function"""
    
    print_live_testing_guide()
    
    print("\n🔍 Checking server readiness...")
    if test_server_readiness():
        print("\n🎉 SYSTEM IS READY FOR LIVE TESTING!")
        print("\n🚀 Execute these commands in order:")
        print("1. python start_exotel.py")
        print("2. ngrok http 8000")
        print("3. Configure Exotel dashboard")
        print("4. Test call!")
    else:
        print("\n⚠️ Server needs to be started first")
        print("Run: python start_exotel.py")
    
    provide_troubleshooting_tips()
    
    print("\n📞 EXPECTED CALL FLOW:")
    print("┌─────────────────────────────────────┐")
    print("│ 📞 Customer calls Exotel number    │")
    print("│ 🤖 'Hello! Welcome to NextCore AI' │")
    print("│ 👤 Customer speaks question        │")
    print("│ 🤖 AI responds with information    │")
    print("│ 📞 Conversation continues          │")
    print("└─────────────────────────────────────┘")
    
    print("\n🎯 SUCCESS CRITERIA:")
    print("✅ No PIN asked")
    print("✅ AI greeting plays")
    print("✅ Customer can speak")
    print("✅ AI responds professionally")
    print("✅ Call doesn't disconnect")

if __name__ == "__main__":
    main()
