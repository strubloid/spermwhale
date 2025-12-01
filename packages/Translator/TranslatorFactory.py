from packages.Translator.TranslatorGPT import TranslatorGPT
from packages.Translator.TranslatorHelsinki import TranslatorHelsinki
from packages.Translator.TranslatorFacebook import TranslatorFacebook
from packages.Log.LogObject import LogObject

class TranslatorFactory:
    """
    Factory class for creating translator instances based on configuration.
    Provides a clean, extensible way to instantiate different translation engines.
    """
    
    SUPPORTED_ENGINES = {
        'gpt': TranslatorGPT,
        'helsinki': TranslatorHelsinki,
        'facebook': TranslatorFacebook
    }
    
    @staticmethod
    def create_translator(engine_name: str, config):
        """
        Create a translator instance based on the specified engine name.
        
        Args:
            engine_name: String identifier for the translation engine ('gpt', 'helsinki', 'facebook')
            config: ConfigObject instance containing application configuration
            
        Returns:
            Translator instance
            
        Raises:
            ValueError: If the specified engine is not supported
        """
        engine_name = engine_name.lower().strip()
        
        if engine_name not in TranslatorFactory.SUPPORTED_ENGINES:
            supported = ", ".join(TranslatorFactory.SUPPORTED_ENGINES.keys())
            raise ValueError(
                f"❌ Unsupported translator engine: '{engine_name}'. "
                f"Supported engines: {supported}"
            )
        
        translator_class = TranslatorFactory.SUPPORTED_ENGINES[engine_name]
        LogObject.log(f"🔧 Initializing {engine_name.upper()} translator...")
        
        return translator_class(config)
    
    @staticmethod
    def get_supported_engines():
        """Return list of supported engine names."""
        return list(TranslatorFactory.SUPPORTED_ENGINES.keys())
    
    @staticmethod
    def get_engine_info():
        """Return detailed information about each supported engine."""
        return {
            'gpt': {
                'name': 'OpenAI GPT',
                'description': 'Cloud-based translation using OpenAI GPT models',
                'requires_api_key': True,
                'quality': 'Highest',
                'speed': 'Medium',
                'cost': 'Per API call'
            },
            'helsinki': {
                'name': 'Helsinki NLP',
                'description': 'Local translation using MarianMT models',
                'requires_api_key': False,
                'quality': 'High',
                'speed': 'Fast',
                'cost': 'Free (local)'
            },
            'facebook': {
                'name': 'Facebook NLLB',
                'description': 'Local translation using NLLB-200 model',
                'requires_api_key': False,
                'quality': 'High',
                'speed': 'Medium',
                'cost': 'Free (local)'
            }
        }
