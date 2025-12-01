# 🎯 Quick Reference Card

## Starting the Application

```bash
python main.py
```

## Configuration File (`.env`)

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
TRANSLATOR_ENGINE=helsinki          # or gpt, facebook
TRANSLATION_LANGUAGE=pt              # pt, es, fr, de, etc.

# Optional
MODEL_SIZE=small                     # tiny, base, small, medium, large
MICROPHONE=1                         # Auto if blank
VERBOSE=True                         # Logging detail
FROM_TRANSLATION_LANGUAGE=en        # Source language
```

## Translator Engines

| Engine | Type | Speed | Quality | Cost | Languages |
|--------|------|-------|---------|------|-----------|
| `helsinki` | Local | ⚡⚡⚡ | ⭐⭐⭐ | Free | European |
| `gpt` | Cloud | ⚡⚡ | ⭐⭐⭐⭐ | $$ | All |
| `facebook` | Local | ⚡⚡ | ⭐⭐⭐ | Free | 200+ |

## Common Commands

```bash
# List microphones
python test-tools/mic-avaiable-list.py

# Test translator
python test-tools/test-helsinki.py

# Reinstall with fresh config
rm .env
python main.py
```

## Whisper Model Sizes

| Size | Speed | Accuracy | RAM | VRAM |
|------|-------|----------|-----|------|
| `tiny` | Fastest | Basic | ~1GB | ~1GB |
| `base` | Fast | Good | ~1GB | ~1GB |
| `small` | Medium | Better | ~2GB | ~2GB |
| `medium` | Slow | Great | ~5GB | ~5GB |
| `large` | Slowest | Best | ~10GB | ~10GB |

## Output Files

```
generated/
├── transcription.txt    # Raw speech-to-text
└── translation.txt      # Translated result
```

## Architecture Components

```
┌─────────────────┐
│  Config Layer   │  ConfigObject, ConfigUI
├─────────────────┤
│  Audio Layer    │  MicrophoneObject
├─────────────────┤
│  Whisper Layer  │  WhisperObject (transcription)
├─────────────────┤
│  Factory Layer  │  TranslatorFactory
├─────────────────┤
│  Translator     │  GPT | Helsinki | Facebook
└─────────────────┘
```

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| No API key | Add `OPENAI_API_KEY` to `.env` |
| No microphone | Run `mic-avaiable-list.py`, set `MICROPHONE` |
| Poor quality | Increase `MODEL_SIZE` |
| Too slow | Decrease `MODEL_SIZE`, use `helsinki` |
| Translation error | Check `TRANSLATION_LANGUAGE` code |

## Language Codes (Common)

```
en = English       pt = Portuguese    es = Spanish
fr = French        de = German        it = Italian
ja = Japanese      zh = Chinese       ru = Russian
ar = Arabic        hi = Hindi         ko = Korean
```

## Switching Translators

**Edit `.env`:**
```bash
TRANSLATOR_ENGINE=helsinki  # Fast, free, local
TRANSLATOR_ENGINE=gpt       # Best quality, paid
TRANSLATOR_ENGINE=facebook  # Most languages, free
```

**Restart:**
```bash
python main.py
```

## GPU Acceleration

**Check CUDA:**
```
🗣️ CUDA Available: True  ← GPU enabled ✅
🗣️ CUDA Available: False ← CPU only
```

**Install CUDA PyTorch:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Documentation

- 📖 **README.md** - Overview & features
- 🚀 **GETTING_STARTED.md** - Quick start guide
- 🏗️ **ARCHITECTURE.md** - Technical design
- 📝 **REFACTORING_SUMMARY.md** - What changed

## Status Indicators

- 🤖 Whisper model loaded
- 🎤 Microphone ready
- 🔧 Translator initializing
- 🌐 Translation engine active
- 🗣️ CUDA status
- 🎙️ Listening for audio
- ⏱️ Processing time
- ✅ Success
- ❌ Error
- ⚠️ Warning
