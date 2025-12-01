# Getting Started with Spermwhale

## Welcome! 🎉

This guide will help you set up and run Spermwhale in minutes.

## Installation Steps

### Step 1: Prerequisites

Ensure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/strubloid/translate.git
cd translate

# Install the package
pip install .

# Install PyTorch with CUDA support (recommended for performance)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Step 3: First Run - Interactive Setup

Simply run the application:
```bash
python main.py
```

On first run, you'll see an interactive configuration wizard:

```
⚙️  Configuration Setup
============================================================
Some required configurations are missing. Let's set them up.

🔧 OpenAI API Key (required for GPT translator and Whisper)
   Enter OpenAI API Key: sk-...

🔧 Translation Engine
   Options:
   → 1. helsinki
     2. gpt
     3. facebook
   Select option (1-3) [default: helsinki]: 1

🔧 Target Translation Language (e.g., pt, es, fr)
   Enter value [default: pt]: pt

✓ Saved: TRANSLATOR_ENGINE = helsinki
✓ Saved: TRANSLATION_LANGUAGE = pt

✅ Configuration complete!
```

### Step 4: Start Using

After configuration, the system will start automatically:

```
🤖 Whisper Model: small
🎤 Microphone
🔧 Initializing HELSINKI translator...
🌐 Translator: HELSINKI → pt
🗣️ CUDA Available: True

🎙️ Ready to listen. Speak into the microphone...
```

Speak into your microphone and watch the magic happen!

## Configuration Options

### Quick Reference

| Setting | Description | Options | Default |
|---------|-------------|---------|---------|
| `TRANSLATOR_ENGINE` | Translation backend | gpt, helsinki, facebook | helsinki |
| `TRANSLATION_LANGUAGE` | Target language | pt, es, fr, de, etc. | pt |
| `MODEL_SIZE` | Whisper model size | tiny, base, small, medium, large | small |
| `OPENAI_API_KEY` | OpenAI API key | Your API key | - |

### Translator Comparison

#### Helsinki NLP (Recommended for Most Users)
- ✅ **Free** - No API costs
- ✅ **Fast** - Local processing
- ✅ **Private** - No data sent to cloud
- ⚡ GPU accelerated
- 🌍 Great for European languages

**Best for**: Cost-conscious users, privacy concerns, European languages

#### OpenAI GPT
- ✅ **Highest Quality** - Best translation accuracy
- ✅ **Most Languages** - Broad language support
- 💰 **Costs Money** - API charges apply
- ☁️ Cloud-based
- 📝 Supports context and nuance

**Best for**: Professional use, highest quality requirements

#### Facebook NLLB
- ✅ **Free** - No API costs
- ✅ **200+ Languages** - Widest language support
- ✅ **Private** - Local processing
- ⚡ GPU accelerated
- 🌍 Great for non-European languages

**Best for**: Multilingual projects, rare languages

## Common Workflows

### Workflow 1: Quick Transcription (No Translation)

If you only need transcription without translation, you can still use the system:

1. Set any translator engine
2. The transcription will be saved to `generated/transcription.txt`
3. Check the file for raw speech-to-text output

### Workflow 2: Switching Languages

Edit `.env` file:
```bash
TRANSLATION_LANGUAGE=es  # Switch to Spanish
```

Restart the application:
```bash
python main.py
```

### Workflow 3: Trying Different Translators

Compare translation quality by switching engines:

```bash
# Try Helsinki (fast, local)
TRANSLATOR_ENGINE=helsinki

# Try GPT (high quality, cloud)
TRANSLATOR_ENGINE=gpt

# Try Facebook NLLB (200+ languages)
TRANSLATOR_ENGINE=facebook
```

### Workflow 4: Performance Optimization

For fastest processing:
```bash
MODEL_SIZE=tiny              # Fastest Whisper model
TRANSLATOR_ENGINE=helsinki   # Fastest translator
```

For best quality:
```bash
MODEL_SIZE=large            # Most accurate Whisper model
TRANSLATOR_ENGINE=gpt       # Best translator
```

## Tips & Tricks

### 🎤 Microphone Selection

If your default microphone isn't working:

1. List available microphones:
   ```bash
   python test-tools/mic-avaiable-list.py
   ```

2. Update `.env`:
   ```bash
   MICROPHONE=2  # Use the index from the list
   ```

### 🚀 GPU Acceleration

Check if CUDA is detected on startup:
```
🗣️ CUDA Available: True
```

If False but you have an NVIDIA GPU:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 📝 Verbose Logging

Enable detailed logs for debugging:
```bash
VERBOSE=True
```

Disable for cleaner output:
```bash
VERBOSE=False
```

### 💰 Managing API Costs

To avoid OpenAI API costs:
1. Use `helsinki` or `facebook` translator (free, local)
2. Only use `gpt` when you need highest quality

## Troubleshooting

### Problem: "OPENAI_API_KEY not found"
**Solution**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys) and add it to `.env`

### Problem: No sound detected
**Solution**: 
1. Check microphone permissions
2. Run `python test-tools/mic-avaiable-list.py`
3. Update `MICROPHONE` setting in `.env`

### Problem: Poor transcription quality
**Solution**: Increase Whisper model size:
```bash
MODEL_SIZE=medium  # or large
```

### Problem: Slow performance
**Solution**: 
1. Use smaller Whisper model: `MODEL_SIZE=small`
2. Use Helsinki translator: `TRANSLATOR_ENGINE=helsinki`
3. Ensure CUDA is enabled for GPU acceleration

### Problem: Translation errors
**Solution**:
1. Check target language code is valid (ISO 639-1)
2. Try different translator engine
3. For GPT: Verify API key and credits

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Explore [README.md](README.md) for advanced configuration
- Customize settings in `.env` for your use case

## Getting Help

- Check existing documentation in this repository
- Review error messages - they're designed to be helpful
- Test components individually using tools in `test-tools/`

---

**Ready to build something amazing? Let's go! 🚀**
