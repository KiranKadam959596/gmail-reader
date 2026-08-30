"""
Voice Assistant Module - Convert text to speech and process voice commands.

This module provides text-to-speech, speech recognition, and audio processing
capabilities with support for multiple languages and speech engines.
"""

import logging
from typing import Optional, List
from enum import Enum

import pyttsx3
from google.cloud import translate_v2
import speech_recognition as sr

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechEngine(Enum):
    """Available text-to-speech engines."""
    GTTS = "gtts"
    PYTTSX3 = "pyttsx3"
    AZURE = "azure"


class VoiceAssistant:
    """
    Handle voice synthesis, recognition, and translation.
    
    Attributes:
        language: Default language code (e.g., 'en', 'es', 'fr')
        engine: Text-to-speech engine to use
        recognizer: Speech recognizer instance
    """
    
    def __init__(self, language: str = 'en', engine: SpeechEngine = SpeechEngine.PYTTSX3):
        """
        Initialize VoiceAssistant.
        
        Args:
            language: Default language code
            engine: TTS engine to use
        """
        self.language = language
        self.engine = engine
        self.recognizer = sr.Recognizer()
        self.translator = translate_v2.Client()
        
        # Initialize pyttsx3 engine if selected
        if engine == SpeechEngine.PYTTSX3:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
        else:
            self.tts_engine = None
        
        logger.info(f"VoiceAssistant initialized with language: {language}, engine: {engine.value}")
    
    def speak(self, text: str, language: Optional[str] = None, save_to_file: Optional[str] = None) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            language: Language code (uses default if not specified)
            save_to_file: Optional file path to save audio
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            target_lang = language or self.language
            
            if self.engine == SpeechEngine.PYTTSX3:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                logger.info(f"Spoke text in {target_lang}")
                return True
            else:
                logger.warning(f"Engine {self.engine.value} not yet implemented")
                return False
                
        except Exception as e:
            logger.error(f"Failed to speak: {str(e)}")
            return False
    
    def listen(self, timeout: int = 10) -> Optional[str]:
        """
        Listen to microphone input and convert to text.
        
        Args:
            timeout: Maximum seconds to listen
        
        Returns:
            Recognized text or None if failed
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during listening: {str(e)}")
            return None
    
    def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code
        
        Returns:
            Translated text or None if failed
        """
        try:
            result = self.translator.translate_text(
                values=[text],
                target_language=target_language
            )
            translated = result['translations'][0]['translatedText']
            logger.info(f"Translated to {target_language}")
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return None
    
    def speak_translated(self, text: str, target_language: str) -> bool:
        """
        Translate text and speak in target language.
        
        Args:
            text: Text to translate and speak
            target_language: Target language code
        
        Returns:
            bool: True if successful
        """
        try:
            translated = self.translate_text(text, target_language)
            if translated:
                return self.speak(translated, language=target_language)
            return False
            
        except Exception as e:
            logger.error(f"Failed to speak translated text: {str(e)}")
            return False
    
    def process_email_voice(self, email: dict) -> bool:
        """
        Process and read an email with voice feedback.
        
        Args:
            email: Email dictionary with sender, subject, body
        
        Returns:
            bool: True if successful
        """
        try:
            sender = email.get('sender', 'Unknown')
            subject = email.get('subject', 'No subject')
            
            # Construct readable email text
            email_text = f"Email from {sender}. Subject: {subject}"
            
            logger.info(f"Reading email: {email_text}")
            return self.speak(email_text)
            
        except Exception as e:
            logger.error(f"Failed to process email voice: {str(e)}")
            return False
    
    def set_language(self, language: str) -> None:
        """
        Change the default language.
        
        Args:
            language: Language code
        """
        self.language = language
        logger.info(f"Language changed to: {language}")


if __name__ == '__main__':
    # Example usage
    assistant = VoiceAssistant(language='en')
    
    # Speak text
    assistant.speak("Hello! This is the Gmail Reader voice assistant.")
    
    # Translate and speak
    assistant.speak_translated("This is English text", "es")