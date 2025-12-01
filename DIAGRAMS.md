# System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SPERMWHALE ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           1. STARTUP PHASE                               │
└─────────────────────────────────────────────────────────────────────────┘

    User runs: python main.py
              ↓
    ┌──────────────────┐
    │   ConfigUI       │  ← Check for .env file
    │   .check()       │  ← Interactive setup if missing
    └────────┬─────────┘
             ↓
    ┌──────────────────┐
    │  ConfigObject    │  ← Load all settings
    │  .init()         │  ← Validate configuration
    └────────┬─────────┘
             ↓
    ┌──────────────────┐
    │  Display Config  │  ← Show current settings
    └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      2. INITIALIZATION PHASE                             │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  OpenAI Client   │  ← Initialize API client
    └────────┬─────────┘
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
┌─────────┐      ┌──────────────┐
│ Whisper │      │  Microphone  │
│ Model   │      │   Object     │
└────┬────┘      └──────┬───────┘
     │                  │
     └────────┬─────────┘
              ▼
    ┌──────────────────────┐
    │  TranslatorFactory   │
    │  .create_translator  │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Read TRANSLATOR_    │
    │  ENGINE from config  │
    └──────────┬───────────┘
               │
       ┌───────┴────────┬──────────┐
       │                │          │
       ▼                ▼          ▼
   ┌────────┐    ┌──────────┐  ┌──────────┐
   │  GPT   │    │ Helsinki │  │ Facebook │
   └────────┘    └──────────┘  └──────────┘
       │                │          │
       └────────┬───────┴──────────┘
                ▼
    ┌──────────────────────┐
    │ Selected Translator  │
    └──────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      3. PROCESSING LOOP                                  │
└─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────┐
    │              Main Loop (Infinite)            │
    └─────────────────────────────────────────────┘
              │
              ▼
    ┌──────────────────┐
    │  Microphone      │  ← Listen for audio
    │  .listenUntil    │  ← Detect voice activity
    │  Silence()       │  ← Stop on silence
    └────────┬─────────┘
             │
             │ Audio File (mic.wav)
             ▼
    ┌──────────────────┐
    │  Whisper Model   │  ← Transcribe audio
    │  .transcribe()   │  ← Speech → Text
    └────────┬─────────┘
             │
             │ Transcribed Text
             ▼
    ┌──────────────────┐
    │  Save to file    │  → generated/transcription.txt
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  Translator      │  ← Translate text
    │  .translate()    │  ← Source → Target language
    └────────┬─────────┘
             │
             │ Translated Text
             ▼
    ┌──────────────────┐
    │  Save to file    │  → generated/translation.txt
    └────────┬─────────┘
             │
             │ Display result
             ▼
    ┌──────────────────┐
    │  Log timing      │  ⏱️ Processing time
    └────────┬─────────┘
             │
             │ Cleanup
             ▼
    ┌──────────────────┐
    │  Delete audio    │  → Remove mic.wav
    └────────┬─────────┘
             │
             │ Loop back
             └────────┐
                      │
    ┌─────────────────┴──────────┐
    │  Wait for next speech...   │
    └────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      4. MODULE DEPENDENCIES                              │
└─────────────────────────────────────────────────────────────────────────┘

    main.py
       │
       ├─→ ConfigUI (interactive setup)
       │      └─→ ConfigObject (data model)
       │
       ├─→ MicrophoneObject (audio capture)
       │      └─→ ConfigObject
       │
       ├─→ WhisperObject (transcription)
       │      └─→ ConfigObject
       │
       ├─→ OpenAIObject (API client)
       │      └─→ ConfigObject
       │
       └─→ TranslatorFactory (translator creation)
              ├─→ TranslatorGPT
              ├─→ TranslatorHelsinki
              └─→ TranslatorFacebook
                     └─→ Translator (base class)


┌─────────────────────────────────────────────────────────────────────────┐
│                      5. DATA FLOW DIAGRAM                                │
└─────────────────────────────────────────────────────────────────────────┘

    User Speech (Audio Waves)
           │
           ▼
    ┌─────────────┐
    │ Microphone  │ → Raw Audio Buffer
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │     VAD     │ → Detect Voice/Silence
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │   Save WAV  │ → generated/mic.wav
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │   Whisper   │ → AI Model (GPU/CPU)
    └─────────────┘
           │
           ▼
    Transcribed Text (String)
           │
           ▼
    ┌─────────────┐
    │  Save TXT   │ → generated/transcription.txt
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │ Translator  │ → Selected Engine
    └─────────────┘
           │
           ▼
    Translated Text (String)
           │
           ▼
    ┌─────────────┐
    │  Save TXT   │ → generated/translation.txt
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │   Console   │ → Display to User
    └─────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                   6. CONFIGURATION HIERARCHY                             │
└─────────────────────────────────────────────────────────────────────────┘

    .env file (User Configuration)
       │
       ▼
    ┌────────────────────────────┐
    │  Environment Variables     │
    │  TRANSLATOR_ENGINE=...     │
    │  TRANSLATION_LANGUAGE=...  │
    │  MODEL_SIZE=...            │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │     ConfigObject           │
    │  Loads & validates config  │
    └────────────┬───────────────┘
                 │
        ┌────────┴────────┬──────────────┬──────────────┐
        │                 │              │              │
        ▼                 ▼              ▼              ▼
    ┌────────┐     ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Whisper │     │Translator│   │Microphone│   │  OpenAI  │
    └────────┘     └──────────┘   └──────────┘   └──────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                   7. TRANSLATOR FACTORY PATTERN                          │
└─────────────────────────────────────────────────────────────────────────┘

    ConfigObject.getTranslatorEngine()
           │
           │ Returns: "helsinki" | "gpt" | "facebook"
           ▼
    ┌──────────────────────────┐
    │  TranslatorFactory       │
    │  .create_translator()    │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  SUPPORTED_ENGINES map   │
    │  'gpt': TranslatorGPT    │
    │  'helsinki': Helsinki... │
    │  'facebook': Facebook... │
    └──────────┬───────────────┘
               │
               │ Lookup engine class
               ▼
    ┌──────────────────────────┐
    │  Instantiate class       │
    │  with config             │
    └──────────┬───────────────┘
               │
               ▼
    Return: Translator instance
               │
               ▼
    Used in: processAudioCycle()


┌─────────────────────────────────────────────────────────────────────────┐
│                   8. ERROR HANDLING FLOW                                 │
└─────────────────────────────────────────────────────────────────────────┘

    ┌────────────────┐
    │ Any Exception  │
    └────────┬───────┘
             │
     ┌───────┴────────┬──────────────┬────────────┐
     │                │              │            │
     ▼                ▼              ▼            ▼
┌─────────┐   ┌──────────────┐  ┌────────┐  ┌────────┐
│Missing  │   │Invalid Config│  │API Err │  │Audio   │
│.env     │   │  Value       │  │        │  │Failure │
└────┬────┘   └──────┬───────┘  └───┬────┘  └───┬────┘
     │               │              │           │
     ▼               ▼              ▼           ▼
┌──────────────────────────────────────────────────┐
│         Log error with helpful message           │
│         Show possible solutions                  │
│         Exit gracefully                          │
└──────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                   9. USER INTERACTION FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

    Start Application
           │
           ▼
    ┌──────────────┐
    │ .env exists? │───No──→ Interactive Setup Wizard
    └──────┬───────┘              │
           │                      │
          Yes                     │
           │                      │
           └──────────┬───────────┘
                      ▼
           ┌──────────────────┐
           │ Display Config   │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ Initialize       │
           │ Components       │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ "Ready to listen"│
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ User speaks      │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ Show transcribed │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ Show translated  │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │ Show timing      │
           └────────┬─────────┘
                    │
                    └──→ Loop back to "User speaks"
```
