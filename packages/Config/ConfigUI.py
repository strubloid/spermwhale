import os
import sys
from dotenv import set_key, load_dotenv
from packages.Log.LogObject import LogObject

class ConfigUI:
    """Interactive configuration UI for missing or incomplete settings."""
    
    REQUIRED_CONFIGS = {
        'OPENAI_API_KEY': {
            'description': 'OpenAI API Key (required for GPT translator and Whisper)',
            'required': True,
            'secret': True
        },
        'TRANSLATOR_ENGINE': {
            'description': 'Translation Engine',
            'required': True,
            'secret': False,
            'options': ['gpt', 'helsinki', 'facebook'],
            'default': 'helsinki'
        },
        'TRANSLATION_LANGUAGE': {
            'description': 'Target Translation Language (e.g., pt, es, fr)',
            'required': True,
            'secret': False,
            'default': 'pt'
        },
        'FROM_TRANSLATION_LANGUAGE': {
            'description': 'Source Language',
            'required': False,
            'secret': False,
            'default': 'en'
        },
        'MODEL_SIZE': {
            'description': 'Whisper Model Size',
            'required': False,
            'secret': False,
            'options': ['tiny', 'base', 'small', 'medium', 'large'],
            'default': 'small'
        },
        'MICROPHONE': {
            'description': 'Microphone Index (leave blank for auto-selection)',
            'required': False,
            'secret': False,
            'default': '1'
        },
        'VERBOSE': {
            'description': 'Verbose Logging',
            'required': False,
            'secret': False,
            'options': ['True', 'False'],
            'default': 'True'
        }
    }

    @staticmethod
    def check_and_prompt_missing_configs(env_path=".env"):
        """
        Check for missing required configurations and prompt user to fill them.
        Returns True if all required configs are present, False otherwise.
        """
        load_dotenv(env_path)
        
        # Create .env if it doesn't exist
        if not os.path.exists(env_path):
            LogObject.log("📝 Creating new .env file...")
            with open(env_path, 'w') as f:
                f.write("# Spermwhale Configuration\n")
                f.write("# Generated configuration file\n\n")
        
        missing_configs = []
        
        # Check which configs are missing
        for key, config_info in ConfigUI.REQUIRED_CONFIGS.items():
            value = os.getenv(key)
            if not value or value.strip() == "":
                if config_info['required']:
                    missing_configs.append(key)
        
        # If nothing is missing, return early
        if not missing_configs:
            return True
        
        # Interactive setup
        LogObject.log("\n" + "="*60)
        LogObject.log("⚙️  Configuration Setup")
        LogObject.log("="*60)
        LogObject.log("Some required configurations are missing. Let's set them up.\n")
        
        for key in missing_configs:
            config_info = ConfigUI.REQUIRED_CONFIGS[key]
            ConfigUI._prompt_and_save(key, config_info, env_path)
        
        # Also offer to configure optional settings
        LogObject.log("\n" + "-"*60)
        LogObject.log("📋 Optional Settings")
        LogObject.log("-"*60)
        
        configure_optional = input("Would you like to configure optional settings? (y/n): ").strip().lower()
        if configure_optional == 'y':
            for key, config_info in ConfigUI.REQUIRED_CONFIGS.items():
                if not config_info['required'] and key not in missing_configs:
                    current_value = os.getenv(key, config_info.get('default', ''))
                    LogObject.log(f"\n📌 {config_info['description']}")
                    LogObject.log(f"   Current: {current_value}")
                    change = input("   Change this setting? (y/n): ").strip().lower()
                    if change == 'y':
                        ConfigUI._prompt_and_save(key, config_info, env_path)
        
        LogObject.log("\n" + "="*60)
        LogObject.log("✅ Configuration complete!")
        LogObject.log("="*60 + "\n")
        
        # Reload environment variables
        load_dotenv(env_path, override=True)
        return True

    @staticmethod
    def _prompt_and_save(key, config_info, env_path):
        """Prompt user for a configuration value and save it."""
        description = config_info['description']
        has_options = 'options' in config_info
        default = config_info.get('default', '')
        
        LogObject.log(f"\n🔧 {description}")
        
        if has_options:
            LogObject.log("   Options:")
            for i, option in enumerate(config_info['options'], 1):
                prefix = "→" if option == default else " "
                LogObject.log(f"   {prefix} {i}. {option}")
            
            while True:
                choice = input(f"   Select option (1-{len(config_info['options'])}) [default: {default}]: ").strip()
                
                if choice == "":
                    value = default
                    break
                
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(config_info['options']):
                        value = config_info['options'][choice_idx]
                        break
                    else:
                        LogObject.log("   ⚠️  Invalid option. Try again.")
                except ValueError:
                    LogObject.log("   ⚠️  Please enter a number.")
        else:
            if config_info.get('secret', False):
                prompt = f"   Enter {description}: "
            else:
                prompt = f"   Enter value [default: {default}]: " if default else f"   Enter value: "
            
            value = input(prompt).strip()
            
            if value == "" and default:
                value = default
            
            # Validate required fields
            if config_info['required'] and not value:
                LogObject.log("   ⚠️  This field is required!")
                return ConfigUI._prompt_and_save(key, config_info, env_path)
        
        # Save to .env
        set_key(env_path, key, value)
        
        display_value = "***" if config_info.get('secret', False) else value
        LogObject.log(f"   ✓ Saved: {key} = {display_value}")

    @staticmethod
    def display_current_config():
        """Display current configuration (hiding sensitive values)."""
        LogObject.log("\n" + "="*60)
        LogObject.log("📋 Current Configuration")
        LogObject.log("="*60)
        
        for key, config_info in ConfigUI.REQUIRED_CONFIGS.items():
            value = os.getenv(key, config_info.get('default', 'NOT SET'))
            if config_info.get('secret', False) and value != 'NOT SET':
                display_value = "***"
            else:
                display_value = value
            
            status = "✓" if value != 'NOT SET' else "✗"
            LogObject.log(f"{status} {config_info['description']}: {display_value}")
        
        LogObject.log("="*60 + "\n")
