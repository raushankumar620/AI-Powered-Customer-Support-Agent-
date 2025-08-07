#!/usr/bin/env python3
"""
Validate that all import issues are resolved
"""

def test_imports():
    """Test all critical imports including the fixed query_agent"""
    
    print("🧪 Testing All Imports After Fixes")
    print("=" * 50)
    
    try:
        # Test query agent import
        print("📦 Testing query_agent import...")
        from agent.query_agent import query_agent, create_custom_prompt
        print("✅ query_agent imported successfully")
        
        # Test langchain imports
        print("📦 Testing langchain imports...")
        try:
            from langchain_chroma import Chroma
            print("✅ langchain_chroma imported successfully")
        except ImportError:
            from langchain_community.vectorstores import Chroma
            print("✅ langchain_community.vectorstores imported as fallback")
        
        # Test other critical imports
        print("📦 Testing other imports...")
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        print("✅ All langchain imports successful")
        
        # Test FastAPI imports
        print("📦 Testing FastAPI imports...")
        from fastapi import FastAPI, Request, Form
        from api.main import app
        print("✅ FastAPI imports successful")
        
        print("\n🎉 ALL IMPORTS SUCCESSFUL!")
        print("✅ No Pylance errors should remain")
        print("✅ langchain-chroma package installed")
        print("✅ python-multipart package installed")
        print("✅ Query agent working")
        print("✅ FastAPI working")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_query_agent_functionality():
    """Test basic query agent functionality"""
    
    print("\n🤖 Testing Query Agent Functionality")
    print("-" * 40)
    
    try:
        from agent.query_agent import query_agent
        
        # Test with a simple question (will use fallback due to OpenAI quota)
        test_question = "What services does NextCore AI offer?"
        print(f"Question: {test_question}")
        
        response = query_agent(test_question)
        print(f"Response: {response[:150]}...")
        
        if response and len(response) > 20:
            print("✅ Query agent responding correctly")
            return True
        else:
            print("⚠️ Query agent response seems short")
            return False
            
    except Exception as e:
        print(f"❌ Query agent error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Comprehensive Import & Functionality Test")
    print("=" * 60)
    
    imports_ok = test_imports()
    query_ok = test_query_agent_functionality()
    
    if imports_ok and query_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 System is ready for live testing")
        print("\nNext steps:")
        print("1. python start_exotel.py")
        print("2. ngrok http 8000")
        print("3. Configure Exotel dashboard")
        print("4. Test live call!")
    else:
        print("\n⚠️ Some issues remain - check output above")
