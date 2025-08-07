#!/usr/bin/env python3
"""
NextCore AI Voice Agent - Exotel Integration
Main startup script for production-ready voice agent
"""

import uvicorn
import logging
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "api/main.py",
        "api/exotel_webhook.py", 
        "api/fallback_agent.py",
        ".env"
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing required files: {missing}")
        return False
    return True

def start_server():
    """Start the FastAPI server for Exotel integration"""
    
    print("🎙️ NextCore AI Voice Agent - Exotel Edition")
    print("=" * 60)
    
    # Check requirements first
    if not check_requirements():
        sys.exit(1)
    
    print("🚀 Starting production server...")
    print("📞 Exotel webhook: /exotel-voice-webhook") 
    print("� Direct voice: /direct-voice")
    print("📋 API docs: http://localhost:8000/docs")
    print("🌐 Server: http://localhost:8000")
    print("=" * 60)
    print("✅ Ready for Exotel integration!")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def print_setup_instructions():
    """Print Exotel setup instructions"""
    
    print("\n🔧 EXOTEL SETUP INSTRUCTIONS:")
    print("=" * 50)
    print("1. Start ngrok: ngrok http 8000")
    print("2. Copy HTTPS URL (e.g., https://abc123.ngrok.io)")
    print("3. In Exotel dashboard:")
    print("   • Go to Numbers → Settings")
    print("   • Set Passthru URL: https://your-ngrok.ngrok.io/exotel-voice-webhook")
    print("   • Method: POST")
    print("   • DISABLE PIN authentication")
    print("4. Test call to your Exotel number!")
    print("=" * 50)
    print("🚨 IMPORTANT: Disable PIN in Exotel dashboard for AI to work!")
    print("=" * 50)

if __name__ == "__main__":
    print_setup_instructions()
    input("\nPress Enter to start the server...")
    start_server()
