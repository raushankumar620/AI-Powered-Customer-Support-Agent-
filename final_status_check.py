#!/usr/bin/env python3
"""
Final Status Check for NextCore AI Voice Agent
Comprehensive verification of all components
"""

import requests
import json
import asyncio
from datetime import datetime

def check_status():
    """Check all components of the AI Voice Agent"""
    
    print("🎯 NextCore AI Voice Agent - Final Status Check")
    print("=" * 60)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Status tracking
    status = {}
    
    # 1. Check FastAPI Server
    print("🌐 1. FastAPI Server Status")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ FastAPI server is running")
            status['fastapi'] = True
        else:
            print(f"   ❌ FastAPI server error: {response.status_code}")
            status['fastapi'] = False
    except requests.RequestException as e:
        print(f"   ❌ FastAPI server not accessible: {str(e)}")
        status['fastapi'] = False
    
    # 2. Check Exotel Webhook Endpoint
    print("\n📞 2. Exotel Webhook Endpoint")
    try:
        response = requests.get("http://localhost:8000/exotel-voice-webhook", timeout=5)
        if response.status_code == 200:
            print("   ✅ Exotel webhook endpoint is accessible")
            status['webhook'] = True
        else:
            print(f"   ❌ Webhook error: {response.status_code}")
            status['webhook'] = False
    except requests.RequestException as e:
        print(f"   ❌ Webhook not accessible: {str(e)}")
        status['webhook'] = False
    
    # 3. Check ngrok URL (if available)
    print("\n🌍 3. ngrok Public URL")
    ngrok_url = "https://43ed2a0ee1b4.ngrok-free.app"
    try:
        response = requests.get(f"{ngrok_url}/", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ ngrok URL is active: {ngrok_url}")
            status['ngrok'] = True
        else:
            print(f"   ❌ ngrok URL error: {response.status_code}")
            status['ngrok'] = False
    except requests.RequestException as e:
        print(f"   ❌ ngrok URL not accessible: {str(e)}")
        status['ngrok'] = False
    
    # 4. Test Fallback Agent
    print("\n🤖 4. AI Agent Response System")
    try:
        from api.fallback_agent import query_agent
        response = query_agent("What services do you offer?")
        if len(response) > 10:
            print("   ✅ AI agent is responding")
            print(f"   📝 Sample response: {response[:80]}...")
            status['ai_agent'] = True
        else:
            print("   ❌ AI agent response too short")
            status['ai_agent'] = False
    except Exception as e:
        print(f"   ❌ AI agent error: {str(e)}")
        status['ai_agent'] = False
    
    # 5. Test XML Generation
    print("\n📄 5. Exotel XML Response Generation")
    try:
        from api.exotel_webhook import create_exotel_response
        xml = create_exotel_response("Hello! This is a test message.")
        if "<Response>" in xml and "<Say>" in xml:
            print("   ✅ XML generation working")
            print(f"   📝 XML length: {len(xml)} characters")
            status['xml'] = True
        else:
            print("   ❌ Invalid XML format")
            status['xml'] = False
    except Exception as e:
        print(f"   ❌ XML generation error: {str(e)}")
        status['xml'] = False
    
    # 6. Environment Variables
    print("\n🔑 6. Environment Configuration")
    try:
        from agent.config import OPENAI_API_KEY
        if OPENAI_API_KEY and len(OPENAI_API_KEY) > 10:
            print("   ✅ OpenAI API key configured")
            status['env'] = True
        else:
            print("   ❌ OpenAI API key missing")
            status['env'] = False
    except Exception as e:
        print(f"   ❌ Environment error: {str(e)}")
        status['env'] = False
    
    # Final Status Summary
    print("\n" + "=" * 60)
    print("📊 FINAL STATUS SUMMARY")
    print("=" * 60)
    
    total_checks = len(status)
    passed_checks = sum(status.values())
    
    for component, is_working in status.items():
        emoji = "✅" if is_working else "❌"
        print(f"{emoji} {component.replace('_', ' ').title()}")
    
    success_rate = (passed_checks / total_checks) * 100
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({passed_checks}/{total_checks})")
    
    if success_rate >= 80:
        print("\n🎉 SYSTEM READY FOR LIVE TESTING!")
        print("\n📞 Your Exotel Setup:")
        print(f"   • Webhook URL: {ngrok_url}/exotel-voice-webhook")
        print("   • Method: POST")
        print("   • Expected: Customer calls → AI responds")
        
        print("\n🔄 Expected Call Flow:")
        print("   1. Customer dials your Exotel number")
        print("   2. Exotel forwards to your webhook")
        print("   3. AI greets and asks how to help")
        print("   4. Customer speaks their question")
        print("   5. AI responds with relevant information")
        print("   6. Conversation continues until hang-up")
        
        print("\n✨ NextCore AI Voice Agent is LIVE!")
        
    else:
        print("\n❌ SYSTEM NEEDS FIXES BEFORE GOING LIVE")
        print("   Please resolve the failed components above.")
    
    return success_rate >= 80

if __name__ == "__main__":
    check_status()
