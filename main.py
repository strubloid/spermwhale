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
        start_time = time.perf_counter()
        # result = model.transcribe(audio_path, fp16=torch.cuda.is_available())
        segments, info = model.transcribe(audio_path)
        transcribedText = "".join([segment.text for segment in segments])
        # print(f"🗣️ Transcribed: {transcribedText}")
        if transcribedText:
            translatorObject.translate(transcribedText, client)

        print(f"⏱️: {time.perf_counter() - start_time:.2f}s")

    except Exception as e:
        print(f"⚠️ Cycle failed: {e}")

    os.remove(audio_path)

if __name__ == "__main__":
    main()
