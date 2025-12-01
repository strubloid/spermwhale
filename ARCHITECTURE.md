# Project Structure

## Overview
Spermwhale is architected with a modular, scalable design following clean architecture principles. Each component is isolated with clear responsibilities, enabling easy maintenance and extensibility.

## Directory Structure

```
translate/
├── main.py                          # Application entry point and orchestration
├── setup.py                         # Package installation configuration
├── pyproject.toml                   # Project metadata and dependencies
├── .env-sample                      # Configuration template
├── .env                            # User configuration (gitignored)
├── README.md                        # Project documentation
│
├── packages/                        # Core application modules
│   ├── __init__py                  # Package initialization
│   │
│   ├── Config/                     # Configuration management layer
│   │   ├── __init__py             # Module exports
│   │   ├── ConfigObject.py        # Configuration data model
│   │   └── ConfigUI.py            # Interactive configuration setup
│   │
│   ├── Microphone/                 # Audio capture layer
│   │   ├── __init__py             # Module exports
│   │   └── MicrophoneObject.py    # Audio input handling and VAD
│   │
│   ├── Whisper/                    # Transcription engine layer
│   │   ├── __init__py             # Module exports
│   │   └── WhisperObject.py       # OpenAI Whisper integration
│   │
│   ├── OpenAI/                     # OpenAI API integration layer
│   │   ├── __init__py             # Module exports
│   │   └── OpenAIObject.py        # API client management
│   │
│   ├── Translator/                 # Translation engine layer
│   │   ├── __init__.py            # Module exports
│   │   ├── Translator.py          # Abstract base class
│   │   ├── TranslatorFactory.py   # Factory pattern implementation
│   │   ├── TranslatorGPT.py       # OpenAI GPT translator
│   │   ├── TranslatorHelsinki.py  # Helsinki NLP translator
│   │   ├── TranslatorFacebook.py  # Facebook NLLB translator
│   │   ├── LanguageMap.py         # Language code mapping
│   │   ├── languageMap.json       # Language mappings data
│   │   └── nllbLanguageMap.json   # NLLB language mappings
│   │
│   └── Log/                        # Logging and monitoring layer
│       ├── __init__py             # Module exports
│       └── LogObject.py           # Centralized logging
│
├── generated/                      # Runtime output directory
│   ├── transcription.txt          # Raw transcription output
│   └── translation.txt            # Translated text output
│
└── test-tools/                     # Development utilities
    ├── mic-avaiable-list.py       # Microphone detection tool
    ├── test-helsinki.py           # Translation engine testing
    └── compress-video.py          # Video processing utility
```

## Architecture Layers

### 1. Configuration Layer (`Config/`)
**Responsibility**: Centralized configuration management and interactive setup

- `ConfigObject.py`: Loads and manages all application settings from environment variables
- `ConfigUI.py`: Interactive CLI for configuring missing or incomplete settings
  - Validates required configurations
  - Prompts users for missing values
  - Provides options for translator selection
  - Saves configurations to `.env` file

**Key Design Patterns**: 
- Singleton-like configuration object
- Interactive setup wizard
- Environment variable management

### 2. Audio Capture Layer (`Microphone/`)
**Responsibility**: Real-time audio input and voice activity detection

- `MicrophoneObject.py`: Handles microphone access, recording, and silence detection
  - Voice Activity Detection (VAD) using WebRTC
  - Automatic microphone selection
  - Buffer management for streaming audio

**Key Features**:
- Low-latency audio capture
- Intelligent silence detection
- Dynamic microphone configuration

### 3. Transcription Layer (`Whisper/`)
**Responsibility**: Speech-to-text conversion using AI models

- `WhisperObject.py`: OpenAI Whisper model integration
  - Model loading and caching
  - GPU acceleration support
  - Configurable model sizes (tiny → large)

**Performance Considerations**:
- CUDA optimization when available
- Model size vs. accuracy trade-offs
- Memory-efficient processing

### 4. Translation Layer (`Translator/`)
**Responsibility**: Multi-engine text translation with flexible backend selection

**Abstract Design**:
- `Translator.py`: Base class defining translation interface
- `TranslatorFactory.py`: Factory pattern for translator instantiation

**Concrete Implementations**:
- `TranslatorGPT.py`: Cloud-based translation using OpenAI GPT models
  - Highest quality
  - Requires API key
  - Supports streaming responses
  
- `TranslatorHelsinki.py`: Local translation using Helsinki NLP MarianMT
  - Fast and free
  - GPU-accelerated
  - Good for European languages
  
- `TranslatorFacebook.py`: Local translation using Facebook NLLB-200
  - Supports 200+ languages
  - Free and local
  - High quality for diverse language pairs

**Key Design Patterns**:
- Factory pattern for translator creation
- Abstract base class for common interface
- Strategy pattern for swappable engines

### 5. OpenAI Integration Layer (`OpenAI/`)
**Responsibility**: API client management and authentication

- `OpenAIObject.py`: Manages OpenAI API client lifecycle
  - API key validation
  - Client initialization
  - Error handling

### 6. Logging Layer (`Log/`)
**Responsibility**: Centralized logging and monitoring

- `LogObject.py`: Unified logging interface
  - Configurable verbosity
  - Console output formatting
  - Debugging support

## Data Flow

```
┌─────────────────┐
│  User Speech    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Microphone Layer       │  ← Audio capture + VAD
│  (MicrophoneObject)     │
└────────┬────────────────┘
         │ Raw Audio
         ▼
┌─────────────────────────┐
│  Whisper Layer          │  ← Speech-to-Text
│  (WhisperObject)        │
└────────┬────────────────┘
         │ Transcribed Text
         ▼
┌─────────────────────────┐
│  Configuration Layer    │  ← Selects translator
│  (ConfigObject)         │
└────────┬────────────────┘
         │ Translator Engine
         ▼
┌─────────────────────────┐
│  Translator Factory     │  ← Creates translator instance
│  (TranslatorFactory)    │
└────────┬────────────────┘
         │
         ▼
    ┌────┴────┬────────────┬──────────┐
    │         │            │          │
    ▼         ▼            ▼          ▼
┌─────┐  ┌─────────┐  ┌────────┐  Other
│ GPT │  │Helsinki │  │Facebook│  Engines
└──┬──┘  └────┬────┘  └───┬────┘
   │          │            │
   └──────────┴────────────┘
              │ Translated Text
              ▼
        ┌───────────┐
        │  Output   │  ← Files + Console
        └───────────┘
```

## Configuration Flow

```
┌──────────────┐
│ Application  │
│   Startup    │
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│  ConfigUI.check()      │  ← Check for .env file
└──────┬─────────────────┘
       │
       ▼
   ┌───────┐
   │ .env  │  Exists?
   │ file  │
   └───┬───┘
       │
   ┌───┴────┐
   │        │
 YES       NO
   │        │
   │        ▼
   │   ┌─────────────────┐
   │   │  Create .env    │
   │   │  Interactive    │
   │   │  Setup Wizard   │
   │   └────────┬────────┘
   │            │
   └────────┬───┘
            │
            ▼
    ┌──────────────────┐
    │ Load ConfigObject│
    └──────────────────┘
```

## Extension Points

### Adding a New Translator Engine

1. Create new translator class in `packages/Translator/`:
   ```python
   from packages.Translator.Translator import Translator
   
   class TranslatorNewEngine(Translator):
       def __init__(self, config):
           super().__init__(config)
           # Initialize your engine
       
       def translate(self, text, client):
           # Implement translation logic
           pass
   ```

2. Register in `TranslatorFactory.py`:
   ```python
   SUPPORTED_ENGINES = {
       'gpt': TranslatorGPT,
       'helsinki': TranslatorHelsinki,
       'facebook': TranslatorFacebook,
       'newengine': TranslatorNewEngine  # Add here
   }
   ```

3. Update `ConfigUI.py` options:
   ```python
   'TRANSLATOR_ENGINE': {
       'options': ['gpt', 'helsinki', 'facebook', 'newengine']
   }
   ```

### Adding New Configuration Options

1. Add to `ConfigObject.py`:
   ```python
   self.newSetting = os.getenv("NEW_SETTING", "default_value")
   
   def getNewSetting(self):
       return self.newSetting
   ```

2. Add to `ConfigUI.py`:
   ```python
   'NEW_SETTING': {
       'description': 'Description of setting',
       'required': False,
       'default': 'default_value'
   }
   ```

3. Update `.env-sample` with documentation

## Design Principles Applied

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility
2. **Dependency Inversion**: Components depend on abstractions (Translator base class)
3. **Factory Pattern**: Centralized object creation for translators
4. **Configuration Management**: Externalized configuration with interactive setup
5. **Extensibility**: Easy to add new translators or modify existing ones
6. **Clean Code**: Clear naming, proper documentation, type hints

## Performance Optimizations

- **GPU Acceleration**: Automatic CUDA detection for Whisper and local translators
- **Model Caching**: Models loaded once and reused
- **Streaming Processing**: Audio processed in chunks with VAD
- **Efficient I/O**: Minimal file operations, temporary file cleanup
- **Lazy Loading**: Components initialized only when needed
