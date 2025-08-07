#!/usr/bin/env python3
"""
Test Exotel Integration for NextCore AI Voice Agent
"""

async def test_exotel_greeting():
    """Test the Exotel greeting generation"""
    try:
        from api.exotel_webhook import generate_greeting
        
        print("🧪 Testing Exotel greeting generation...")
        greeting = await generate_greeting("+91-9876543210")
        print(f"✅ Generated greeting: {greeting}")
        return True
        
    except Exception as e:
        print(f"❌ Greeting test failed: {e}")
        return False

async def test_exotel_response():
    """Test Exotel AI response generation"""
    try:
        from api.exotel_webhook import generate_ai_response
        
        print("\n🤖 Testing AI response generation...")
        response = await generate_ai_response("+91-9876543210", "What services do you offer?")
        print(f"✅ Generated response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ AI response test failed: {e}")
        return False

def test_xml_generation():
    """Test Exotel XML response generation"""
    try:
        from api.exotel_webhook import create_exotel_response
        
        print("\n📄 Testing XML response generation...")
        xml = create_exotel_response("Hello! Welcome to NextCore AI.")
        print(f"✅ Generated XML: {xml[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ XML generation test failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base integration"""
    try:
        from agent.query_agent import query_agent
        
        print("\n📚 Testing knowledge base...")
        response = query_agent("What is NextCore AI?")
        print(f"✅ Knowledge base response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

async def main():
    """Run all Exotel integration tests"""
    print("🎙️ NextCore AI - Exotel Integration Test")
    print("=" * 50)
    
    # Test knowledge base first
    kb_success = test_knowledge_base()
    
    if not kb_success:
        print("\n❌ Knowledge base not working. Run: python -m agent.load_documents")
        return False
    
    # Test XML generation
    xml_success = test_xml_generation()
    
    # Test async functions
    greeting_success = await test_exotel_greeting()
    response_success = await test_exotel_response()
    
    results = [kb_success, xml_success, greeting_success, response_success]
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if all(results):
        print("🎉 Exotel integration is ready!")
        print("\n📋 Next Steps:")
        print("1. Start server: uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Start ngrok: ngrok http 8000")
        print("3. Copy ngrok URL to Exotel webhook: https://your-url.ngrok.io/exotel-voice-webhook")
        print("4. Test by calling your Exotel number!")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
