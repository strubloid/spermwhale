# Contributing to Spermwhale

Thank you for your interest in contributing to Spermwhale! This document provides guidelines for extending and improving the project.

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/yourusername/translate.git
cd translate
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies
```bash
pip install -e .
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Configure for Development
```bash
cp .env-sample .env
# Edit .env with your settings
```

## Project Structure

```
translate/
├── main.py                    # Application entry point
├── packages/                  # Core modules
│   ├── Config/               # Configuration layer
│   ├── Microphone/           # Audio capture
│   ├── Whisper/              # Transcription
│   ├── Translator/           # Translation engines
│   ├── OpenAI/               # API integration
│   └── Log/                  # Logging
├── test-tools/               # Development utilities
└── docs/                     # Documentation
```

## How to Contribute

### Adding a New Translation Engine

1. **Create Translator Class**

Create `packages/Translator/TranslatorYourEngine.py`:

```python
from packages.Translator.Translator import Translator

class TranslatorYourEngine(Translator):
    """
    Translation using Your Engine.
    
    Attributes:
        model: The loaded translation model
        device: Computing device (cuda/cpu)
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize your model
        self.model = load_your_model()
        
        # GPU support
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
    
    def translate(self, text, client=None):
        """
        Translate text using your engine.
        
        Args:
            text: Text to translate
            client: Optional API client (if cloud-based)
            
        Returns:
            str: Translated text
        """
        # Your translation logic here
        translated = self.model.translate(text)
        
        # Save to file
        self._writeToFile(translated)
        
        return translated
```

2. **Register in Factory**

Edit `packages/Translator/TranslatorFactory.py`:

```python
from packages.Translator.TranslatorYourEngine import TranslatorYourEngine

class TranslatorFactory:
    SUPPORTED_ENGINES = {
        'gpt': TranslatorGPT,
        'helsinki': TranslatorHelsinki,
        'facebook': TranslatorFacebook,
        'yourengine': TranslatorYourEngine,  # Add here
    }
```

3. **Add to Configuration Options**

Edit `packages/Config/ConfigUI.py`:

```python
'TRANSLATOR_ENGINE': {
    'description': 'Translation Engine',
    'required': True,
    'options': ['gpt', 'helsinki', 'facebook', 'yourengine'],
    'default': 'helsinki'
}
```

4. **Update Factory Info**

Edit `TranslatorFactory.get_engine_info()`:

```python
'yourengine': {
    'name': 'Your Engine',
    'description': 'Description of your engine',
    'requires_api_key': False,  # or True
    'quality': 'High',
    'speed': 'Fast',
    'cost': 'Free'
}
```

5. **Update Documentation**

Add your engine to:
- `README.md` - Feature list
- `GETTING_STARTED.md` - Engine comparison
- `QUICK_REFERENCE.md` - Quick reference table

### Adding New Configuration Options

1. **Update ConfigObject**

Edit `packages/Config/ConfigObject.py`:

```python
def __init__(self):
    # ... existing configs ...
    self.yourNewSetting = os.getenv("YOUR_NEW_SETTING", "default_value")

def getYourNewSetting(self):
    return self.yourNewSetting
```

2. **Add to ConfigUI**

Edit `packages/Config/ConfigUI.py`:

```python
REQUIRED_CONFIGS = {
    # ... existing configs ...
    'YOUR_NEW_SETTING': {
        'description': 'Description of your setting',
        'required': False,
        'secret': False,
        'default': 'default_value',
        'options': ['option1', 'option2']  # Optional
    }
}
```

3. **Update .env-sample**

Add documentation:
```bash
# Your New Setting
# Description and usage information
YOUR_NEW_SETTING=default_value
```

### Improving Audio Processing

Edit `packages/Microphone/MicrophoneObject.py`:

- Adjust VAD sensitivity
- Implement better silence detection
- Add audio preprocessing

### Enhancing Transcription

Edit `packages/Whisper/WhisperObject.py`:

- Add language detection
- Implement streaming transcription
- Optimize model loading

## Code Style Guidelines

### Python Style

Follow PEP 8 with these conventions:

```python
# Class names: PascalCase
class TranslatorEngine:
    pass

# Function/method names: camelCase (current convention)
def processAudioCycle():
    pass

# Constants: UPPER_CASE
SUPPORTED_ENGINES = {}

# Private methods: _prefixed
def _writeToFile():
    pass
```

### Documentation

Use docstrings for all public classes and methods:

```python
def translate(self, text, client):
    """
    Translate text to target language.
    
    Args:
        text (str): Input text to translate
        client: Optional API client for cloud services
        
    Returns:
        str: Translated text
        
    Raises:
        ValueError: If text is empty
    """
    pass
```

### Comments

- Explain **why**, not **what**
- Use `##` for major section markers
- Use `#` for inline comments

```python
## Initialize translator using factory pattern
# Factory handles all engine-specific instantiation
translatorObject = TranslatorFactory.create_translator(engine, config)
```

## Testing

### Manual Testing

Test new features with:

```bash
# Test translator
python test-tools/test-helsinki.py

# Test microphone
python test-tools/mic-avaiable-list.py

# Full integration test
python main.py
```

### Testing Checklist

Before submitting:

- [ ] Code runs without errors
- [ ] New features are documented
- [ ] Configuration options are in ConfigUI
- [ ] .env-sample is updated
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Logging added for new features

## Architecture Patterns

### Factory Pattern
Use for object creation with multiple implementations:
```python
obj = Factory.create(type, config)
```

### Abstract Base Class
Use for common interfaces:
```python
class Base(ABC):
    @abstractmethod
    def method(self):
        pass
```

### Configuration Object
Centralize all settings:
```python
config = ConfigObject()
value = config.getSetting()
```

## Commit Messages

Follow conventional commits:

```
feat: Add new translator engine
fix: Correct microphone detection
docs: Update getting started guide
refactor: Improve factory pattern
perf: Optimize audio processing
test: Add translator tests
```

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Write code
   - Update documentation
   - Test thoroughly

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

4. **Push to Fork**
   ```bash
   git push origin feature/your-feature
   ```

5. **Create Pull Request**
   - Clear description
   - List changes
   - Reference issues

## Common Development Tasks

### Adding a Language

1. Check language code: [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
2. Update language mappings if needed
3. Test with your translator

### Debugging

Enable verbose logging:
```bash
VERBOSE=True
```

Check logs for:
- Configuration loading
- Model initialization
- Audio processing
- Translation calls

### Performance Profiling

```python
import time

start = time.perf_counter()
# Your code here
elapsed = time.perf_counter() - start
print(f"⏱️ Took {elapsed:.2f}s")
```

## Questions?

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
- Review existing code for patterns
- Open an issue for discussion

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Spermwhale! 🚀**
