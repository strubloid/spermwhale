#!/usr/bin/env python3
"""
Spermwhale Startup Script
Provides a clean entry point with environment checking and helpful messages.
"""

import sys
import os

def check_dependencies():
    """Check if critical dependencies are installed."""
    missing = []
    
    try:
        import dotenv
    except ImportError:
        missing.append("python-dotenv")
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    try:
        import pyaudio
    except ImportError:
        missing.append("pyaudio")
    
    try:
        import openai
    except ImportError:
        missing.append("openai")
    
    if missing:
        print("❌ Missing required dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n💡 Install with: pip install " + " ".join(missing))
        return False
    
    return True

def main():
    """Main entry point with environment validation."""
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run main application
    try:
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
