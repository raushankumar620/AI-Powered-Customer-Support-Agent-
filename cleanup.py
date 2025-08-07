#!/usr/bin/env python3
"""
Project Cleanup Utility
Run this to clean duplicate files and organize the project
"""

import os
import shutil
from pathlib import Path

def clean_cache_files():
    """Remove Python cache files and directories"""
    cache_patterns = ["__pycache__", "*.pyc", "*.pyo", ".pytest_cache"]
    
    for pattern in cache_patterns:
        if pattern.startswith("__"):
            # Remove cache directories
            for root, dirs, files in os.walk("."):
                for dir_name in dirs[:]:  # Use slice to avoid modifying during iteration
                    if dir_name == pattern:
                        cache_path = os.path.join(root, dir_name)
                        print(f"🗑️ Removing cache: {cache_path}")
                        shutil.rmtree(cache_path, ignore_errors=True)
                        dirs.remove(dir_name)
        else:
            # Remove cache files
            for cache_file in Path(".").rglob(pattern):
                print(f"🗑️ Removing: {cache_file}")
                cache_file.unlink(missing_ok=True)

def organize_files():
    """Organize project files"""
    print("📁 Organizing project structure...")
    
    # Ensure directories exist
    os.makedirs("data/call_logs", exist_ok=True)
    os.makedirs("data/recordings", exist_ok=True)
    
    print("✅ Project structure organized")

def list_project_files():
    """List essential project files"""
    essential_files = {
        "🚀 Main Files": [
            "start_exotel.py",
            "requirements.txt", 
            "README.md",
            ".env"
        ],
        "🎙️ API Files": [
            "api/main.py",
            "api/exotel_webhook.py",
            "api/fallback_agent.py"
        ],
        "🤖 Agent Files": [
            "agent/config.py",
            "agent/load_documents.py",
            "agent/query_agent.py"
        ],
        "🔊 Voice Files": [
            "voice/audio_utils.py",
            "voice/speech_to_text.py", 
            "voice/text_to_speech.py"
        ],
        "🧪 Test Files": [
            "test_system.py",
            "test_exotel.py",
            "test_xml.py",
            "diagnose_exotel.py",
            "final_status_check.py"
        ],
        "📚 Documentation": [
            "EXOTEL_SETUP.md",
            "FINAL_TESTING_GUIDE.md"
        ]
    }
    
    print("\n📋 Essential Project Files:")
    print("=" * 50)
    
    for category, files in essential_files.items():
        print(f"\n{category}:")
        for file_path in files:
            if os.path.exists(file_path):
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} (missing)")

def main():
    """Main cleanup function"""
    print("🧹 NextCore AI Project Cleanup")
    print("=" * 40)
    
    clean_cache_files()
    organize_files()
    list_project_files()
    
    print("\n✨ Cleanup complete!")
    print("🚀 Ready to run: python start_exotel.py")

if __name__ == "__main__":
    main()
