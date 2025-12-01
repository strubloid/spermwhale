import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="webrtcvad")

from packages.Config.ConfigObject import ConfigObject
from packages.Config.ConfigUI import ConfigUI
from packages.Microphone.MicrophoneObject import MicrophoneObject
from packages.OpenAI.OpenAIObject import OpenAIObject
from packages.Whisper.WhisperObject import WhisperObject
from packages.Translator.TranslatorFactory import TranslatorFactory
from packages.Translator.Translator import Translator
from packages.Log.LogObject import LogObject
import os
import time
import torch

def main():

    try:
        
        ## Interactive configuration setup for missing values
        LogObject.log("🚀 Starting Spermwhale Transcription System\n")
        ConfigUI.check_and_prompt_missing_configs()

        ## Loading the environment variables
        config = ConfigObject()
        config.checkingEnvironmentVariables()

        ## Display current configuration
        ConfigUI.display_current_config()

        ## starting the client
        openAiObject = OpenAIObject(config)

        ## loading the client of OpenAI
        client = openAiObject.setup(openAiObject.getKey())
        
        ## Loading the whisper model and getting the model
        whisperObject = WhisperObject(config)
        model = whisperObject.getModel()
        print(f"🤖 Whisper Model: {config.getModelSize()}")

        ## Loading the microphone object
        mic = MicrophoneObject(config)
        print("🎤 Microphone")

        ## Initialize translator using factory pattern
        translator_engine = config.getTranslatorEngine()
        translatorObject = TranslatorFactory.create_translator(translator_engine, config)
        
        print(f"🌐 Translator: {translator_engine.upper()} → {translatorObject.getTargetLanguage()}")
        print(f"🗣️ CUDA Available: {torch.cuda.is_available()}")

        LogObject.log("\n🎙️ Ready to listen. Speak into the microphone...\n")

        # Main loop: listen -> transcribe -> translate
        while True:
            processAudioCycle(mic, model, client, config, translatorObject)

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'mic' in locals():
            mic.terminate()

## Function to process one cycle of audio recording, transcription, and translation.
## One full audio-processing cycle:
## 1. Record audio until silence.
## 2. Transcribe using Whisper.
## 3. Translate using OpenAI.
## 4. Save results to files.
def processAudioCycle(mic, model, client, config, translatorObject : Translator):
    try:
        audio_path = mic.listenUntilSilence()
        
        # Detailed timing breakdown
        total_start = time.perf_counter()
        
        # Transcription timing
        transcribe_start = time.perf_counter()
        segments, info = model.transcribe(audio_path)
        transcribe_time = time.perf_counter() - transcribe_start
        
        transcribedText = "".join([segment.text for segment in segments])
        
        # Translation timing
        translate_time = 0
        if transcribedText:
            translate_start = time.perf_counter()
            translatorObject.translate(transcribedText, client)
            translate_time = time.perf_counter() - translate_start
        
        total_time = time.perf_counter() - total_start
        print(f"⏱️ Total: {total_time:.2f}s (Transcribe: {transcribe_time:.2f}s | Translate: {translate_time:.2f}s)")

    except Exception as e:
        print(f"⚠️ Cycle failed: {e}")

    os.remove(audio_path)

if __name__ == "__main__":
    main()
