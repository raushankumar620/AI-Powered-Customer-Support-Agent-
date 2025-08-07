#!/usr/bin/env python3
"""
NextCore AI Voice Agent - Quick Test Script
Test individual components without needing API keys
"""

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    try:
        import fastapi
        import uvicorn 
        import twilio
        import langchain
        import chromadb
        import openai
        print("✅ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    import os
    
    required_files = [
        "agent/config.py",
        "agent/load_documents.py", 
        "agent/query_agent.py",
        "agent/knowledge_base/services.md",
        "api/main.py",
        "api/call_response.py",
        "voice/audio_utils.py",
        "voice/speech_to_text.py",
        "voice/text_to_speech.py",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_app_creation():
    """Test FastAPI app creation"""
    print("\n🌐 Testing FastAPI app...")
    try:
        from api.main import app
        print("✅ FastAPI app created successfully")
        print(f"📍 Available routes: {[route.path for route in app.routes]}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def test_knowledge_base_file():
    """Test if knowledge base file can be read"""
    print("\n📚 Testing knowledge base...")
    try:
        with open("agent/knowledge_base/services.md", "r", encoding="utf-8") as f:
            content = f.read()
            word_count = len(content.split())
            print(f"✅ Knowledge base loaded: {word_count} words")
            return True
    except Exception as e:
        print(f"❌ Knowledge base error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎙️ NextCore AI Voice Agent - System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_file_structure, 
        test_app_creation,
        test_knowledge_base_file
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 System is ready!")
        print("\n📋 Next Steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Add your Twilio credentials to .env file") 
        print("3. Run: python -m uvicorn api.main:app --reload")
        print("4. Test with ngrok for local Twilio webhook")
        return True
    else:
        print("❌ System has issues - please fix them first")
        return False

if __name__ == "__main__":
    main()
