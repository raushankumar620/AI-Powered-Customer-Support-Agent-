#!/usr/bin/env python3
"""
Setup script for NextCore AI Voice Agent
This script initializes the knowledge base and sets up the environment
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    if not env_path.exists():
        logger.error("❌ .env file not found! Please create it with your API keys.")
        return False
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=your_" in content or var not in content:
                missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Please set these environment variables in .env: {missing_vars}")
        return False
    
    logger.info("✅ Environment file configured")
    return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        logger.info("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "agent/db",
        "data/call_logs",
        "data/recordings",
        "temp_audio"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created directory: {directory}")

def initialize_knowledge_base():
    """Initialize the vector database with knowledge base"""
    try:
        logger.info("🧠 Initializing knowledge base...")
        from agent.load_documents import load_knowledge_base
        load_knowledge_base()
        logger.info("✅ Knowledge base initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize knowledge base: {e}")
        return False

def test_system():
    """Test the system components"""
    try:
        logger.info("🧪 Testing system...")
        from agent.query_agent import query_agent
        
        test_response = query_agent("What is NextCore AI?")
        if test_response and len(test_response) > 10:
            logger.info("✅ System test passed")
            logger.info(f"Sample response: {test_response[:100]}...")
            return True
        else:
            logger.error("❌ System test failed - empty response")
            return False
    except Exception as e:
        logger.error(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Starting NextCore AI Voice Agent setup...")
    
    # Check environment
    if not check_env_file():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Initialize knowledge base
    if not initialize_knowledge_base():
        return False
    
    # Test system
    if not test_system():
        return False
    
    logger.info("🎉 Setup completed successfully!")
    logger.info("To start the server, run: python -m uvicorn api.main:app --reload")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
