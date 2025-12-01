# Spermwhale

A high-performance real-time transcription and audio processing system architected for low latency and optimized browser performance. This project demonstrates advanced audio pipeline design with AI-based analysis and scalable frontend architecture.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 🚀 Quick start guide for new users |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ System design and technical details |
| **[DIAGRAMS.md](DIAGRAMS.md)** | 📊 Visual system architecture and data flow |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 📋 Command and configuration cheat sheet |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 🤝 Developer guide for extending the system |
| **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** | 📝 Recent improvements and changes |

---

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

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS
- **Optional**: CUDA-capable GPU for accelerated processing
- **Dependencies**: Listed in `setup.py` and `pyproject.toml`

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/strubloid/translate.git
cd translate
```

### 2. Install Dependencies
```bash
pip install .
```

### 3. Install PyTorch with CUDA Support (Optional but Recommended)
For GPU acceleration:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Or force reinstall if needed:
```bash
pip install --force-reinstall --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Configure the Application
On first run, the application will guide you through an interactive setup:
```bash
python main.py
```

The setup wizard will prompt you for:
- **OpenAI API Key** (required for GPT translator and Whisper)
- **Translation Engine** (gpt, helsinki, or facebook)
- **Target Language** (pt, es, fr, etc.)
- **Optional settings** (model size, microphone, etc.)

Alternatively, copy and configure manually:
```bash
cp .env-sample .env
# Edit .env with your preferred settings
```

### 5. Run the Application
```bash
python main.py
```

## Configuration

### Translation Engine Options

The system supports three translation engines, configurable via the `TRANSLATOR_ENGINE` setting:

| Engine | Description | Quality | Speed | Cost | Requires API |
|--------|-------------|---------|-------|------|--------------|
| **gpt** | OpenAI GPT models | Highest | Medium | Per API call | Yes |
| **helsinki** | Helsinki NLP MarianMT | High | Fast | Free | No |
| **facebook** | Facebook NLLB-200 | High | Medium | Free | No |

### Key Configuration Options

All settings are stored in `.env` file:

```bash
# Required
OPENAI_API_KEY=your-key-here
TRANSLATOR_ENGINE=helsinki
TRANSLATION_LANGUAGE=pt

# Optional
MODEL_SIZE=small                    # Whisper: tiny, base, small, medium, large
MICROPHONE=1                         # Auto-selected if not specified
VERBOSE=True                         # Enable detailed logging
FROM_TRANSLATION_LANGUAGE=en        # Source language
```

See `.env-sample` for complete configuration template.

## Usage

### Basic Workflow
1. Start the application: `python main.py`
2. Speak into your microphone
3. The system automatically:
   - Detects voice activity
   - Transcribes speech using Whisper
   - Translates text using selected engine
   - Saves results to `generated/` directory

### Output Files
- `generated/transcription.txt` - Raw transcribed text
- `generated/translation.txt` - Translated text

### Changing Translator at Runtime
Simply update the `TRANSLATOR_ENGINE` in your `.env` file:
```bash
TRANSLATOR_ENGINE=helsinki  # Switch to local Helsinki translator
TRANSLATOR_ENGINE=gpt       # Switch to OpenAI GPT
TRANSLATOR_ENGINE=facebook  # Switch to Facebook NLLB
```

## Project Structure

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

```
translate/
├── main.py                 # Application entry point
├── packages/               # Core modules
│   ├── Config/            # Configuration management
│   ├── Microphone/        # Audio capture
│   ├── Whisper/           # Transcription engine
│   ├── Translator/        # Translation engines
│   ├── OpenAI/            # API integration
│   └── Log/               # Logging
├── generated/             # Output files
└── test-tools/            # Development utilities
```

## Advanced Topics

### GPU Acceleration
The system automatically detects and uses CUDA when available:
- Whisper transcription acceleration
- Local translator models (Helsinki, Facebook)
- Check CUDA status in startup logs: `🗣️ CUDA Available: True`

### Adding Custom Translators
See [ARCHITECTURE.md](ARCHITECTURE.md#adding-a-new-translator-engine) for guide on extending the system with new translation engines.

### Performance Tuning
- **Model Size**: Smaller Whisper models (tiny/base) are faster but less accurate
- **Translator Choice**: Helsinki is fastest for European languages; GPT is highest quality
- **CUDA**: Enable GPU support for 3-5x performance improvement

## Troubleshooting

### "OPENAI_API_KEY not found"
Run the interactive setup: `python main.py` or manually add the key to `.env`

### Microphone Not Detected
Run the microphone test tool:
```bash
python test-tools/mic-avaiable-list.py
```

### Poor Transcription Quality
Increase Whisper model size in `.env`:
```bash
MODEL_SIZE=medium  # or large for best quality
```

### Translation Errors with GPT
Ensure your API key is valid and has sufficient credits. Consider switching to free local translators:
```bash
TRANSLATOR_ENGINE=helsinki
```