# Spermwhale

A high-performance real-time transcription and audio processing system architected for low latency and optimized browser performance. This project demonstrates advanced audio pipeline design with AI-based analysis and scalable frontend architecture.

## Architecture Overview

Spermwhale is engineered as a production-grade system combining Python-based audio processing with a modern web frontend, delivering real-time transcription and translation with minimal latency.

### Key Technical Achievements

- **Real-Time Audio Processing Pipeline**: Architected a low-latency system leveraging OpenAI Whisper for transcription with optimized buffer management and streaming capabilities.
- **AI-Integrated Translation**: Implemented multi-model translation support (OpenAI GPT, Facebook NLLB, Helsinki NLP) with intelligent fallback mechanisms.
- **Scalable Architecture**: Designed modular Python backend with clean separation of concerns across audio capture, AI processing, and translation layers.
- **Performance Optimization**: Applied game-engine-inspired rendering techniques for efficient data streaming and caching strategies.
- **WebSocket-Ready Design**: Built with event-driven architecture supporting instant feedback and fluid user interactions.

## Features

- **Real-time Transcription**: OpenAI Whisper integration with configurable model sizes for performance tuning
- **Multi-Engine Translation**: Support for GPT-4, Facebook NLLB, and Helsinki NLP models with automatic language detection
- **Modular Configuration**: Centralized configuration management for easy deployment and scaling
- **Robust Logging**: Comprehensive logging system for monitoring and debugging production systems
- **Extensible Design**: Plugin-style architecture allowing easy integration of additional AI models

## Requirements

- Python 3.8 or higher
- Dependencies listed in `setup.py` or `pyproject.toml`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/strubloid-translate.git
   cd strubloid-translate
   ```

2. Installation
   ```bash
      pip install .
    ```

3. Extra commands
   ```bash
      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

      or

      pip install --force-reinstall --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

   ```