# import whisper
from packages.Config.ConfigObject import ConfigObject
from packages.Log.LogObject import LogObject
from faster_whisper import WhisperModel
import torch

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


class WhisperObject:

    model = None
    modelSize = None

    ## Starting the WhisperObject class
    # => It initializes the class with a configuration object.
    # => It sets the model size and loads the Whisper model.
    # => The model size is obtained from the configuration object.
    # => The startingWhisperModel function is called to load the model.
    def __init__(self, config : ConfigObject):
        self.config = config
        self.modelSize = config.getModelSize()
        self.model = self.startingWhisperModel()

    ## This function loads the Whisper model and returns a model object.
    # => It uses faster-whisper for optimized performance
    # => Configured for maximum speed with CPU optimization
    def startingWhisperModel(self):

        LogObject.log("🔄 Loading Whisper model...")
        try:
            # Use faster-whisper with optimized settings for speed
            device = "cpu"  # Force CPU mode in WSL for stability
            compute_type = "int8"  # Use int8 for fastest inference
            
            model = WhisperModel(
                self.modelSize,
                device=device,
                compute_type=compute_type,
                cpu_threads=4,  # Optimize CPU threads
                num_workers=1
            )
            LogObject.log("✅ Whisper model loaded.")
            return model
        
        except Exception as e:
            raise RuntimeError(f"❌ Whisper model failed to load: {e}")

    ## Gets the Whisper model    
    def getModel(self):

        ## double checking if was loaded or not
        if not self.model:
            self.model = self.startingWhisperModel()

        return self.model       