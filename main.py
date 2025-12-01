import warnings
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Suppress all ALSA/audio warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Redirect ALSA errors to /dev/null
import sys
if sys.platform == 'linux':
    try:
        from ctypes import *
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        def py_error_handler(filename, line, function, err, fmt):
            pass
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        asound = cdll.LoadLibrary('libasound.so.2')
        asound.snd_lib_error_set_handler(c_error_handler)
    except:
        pass

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
        ConfigUI.check_and_prompt_missing_configs()

        ## Loading the environment variables
        config = ConfigObject()
        config.checkingEnvironmentVariables()

        ## starting the client
        openAiObject = OpenAIObject(config)

        ## loading the client of OpenAI
        client = openAiObject.setup(openAiObject.getKey())
        
        ## Loading the whisper model and getting the model
        whisperObject = WhisperObject(config)
        model = whisperObject.getModel()

        ## Loading the microphone object
        mic = MicrophoneObject(config)

        ## Initialize translator using factory pattern
        translator_engine = config.getTranslatorEngine()
        translatorObject = TranslatorFactory.create_translator(translator_engine, config)

        print(f"\n🎙️ Ready [{config.getModelSize()}|{translator_engine}] ...\n")

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
