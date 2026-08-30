"""
Translator Module - Handle multi-language translation of email content.

Provides translation services using Google Cloud Translation API or
Hugging Face transformers for offline translation.
"""

import logging
from typing import Optional, Dict, List
from enum import Enum

from google.cloud import translate_v2
from textblob import TextBlob

logger = logging.getLogger(__name__)


class TranslationService(Enum):
    """Available translation services."""
    GOOGLE = "google"
    TEXTBLOB = "textblob"
    HUGGINGFACE = "huggingface"


class Translator:
    """
    Handle translation of email content to multiple languages.
    
    Attributes:
        service: Translation service to use
        client: Google Translate client (if using Google)
    """
    
    # Language code mappings
    LANGUAGE_CODES = {
        'english': 'en',
        'spanish': 'es',
        'french': 'fr',
        'german': 'de',
        'italian': 'it',
        'portuguese': 'pt',
        'russian': 'ru',
        'japanese': 'ja',
        'chinese': 'zh',
        'korean': 'ko',
        'hindi': 'hi',
        'arabic': 'ar',
    }
    
    def __init__(self, service: TranslationService = TranslationService.GOOGLE):
        """
        Initialize Translator.
        
        Args:
            service: Translation service to use
        """
        self.service = service
        
        if service == TranslationService.GOOGLE:
            try:
                self.client = translate_v2.Client()
                logger.info("Google Translation API initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Translate: {str(e)}")
                self.client = None
        else:
            self.client = None
        
        logger.info(f"Translator initialized with service: {service.value}")
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> Optional[str]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code or name
            source_language: Source language code (default: 'en')
        
        Returns:
            Translated text or None if failed
        """
        try:
            # Normalize language code
            target_lang = self._normalize_language_code(target_language)
            
            if self.service == TranslationService.GOOGLE:
                return self._translate_google(text, target_lang, source_language)
            elif self.service == TranslationService.TEXTBLOB:
                return self._translate_textblob(text, target_lang)
            else:
                logger.warning(f"Translation service {self.service.value} not implemented")
                return None
                
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return None
    
    def _translate_google(self, text: str, target_language: str, source_language: str) -> Optional[str]:
        """
        Translate using Google Cloud Translation API.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code
        
        Returns:
            Translated text or None
        """
        if not self.client:
            logger.error("Google Translate client not initialized")
            return None
        
        try:
            result = self.client.translate_text(
                values=[text],
                target_language=target_language,
                source_language=source_language
            )
            translated = result['translations'][0]['translatedText']
            logger.info(f"Translated from {source_language} to {target_language}")
            return translated
            
        except Exception as e:
            logger.error(f"Google translation error: {str(e)}")
            return None
    
    def _translate_textblob(self, text: str, target_language: str) -> Optional[str]:
        """
        Translate using TextBlob (simple, offline translation).
        
        Args:
            text: Text to translate
            target_language: Target language code
        
        Returns:
            Translated text or None
        """
        try:
            blob = TextBlob(text)
            translated = blob.translate(to=target_language)
            logger.info(f"Translated using TextBlob to {target_language}")
            return str(translated)
            
        except Exception as e:
            logger.error(f"TextBlob translation error: {str(e)}")
            return None
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Language code or None
        """
        try:
            if self.service == TranslationService.GOOGLE and self.client:
                result = self.client.detect_language(text)
                language = result['language']
                logger.info(f"Detected language: {language}")
                return language
            elif self.service == TranslationService.TEXTBLOB:
                blob = TextBlob(text)
                language = blob.detect_language()
                logger.info(f"Detected language: {language}")
                return language
            else:
                return None
                
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return None
    
    def batch_translate(self, texts: List[str], target_language: str) -> List[Optional[str]]:
        """
        Translate multiple texts to target language.
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
        
        Returns:
            List of translated texts
        """
        results = []
        for text in texts:
            translated = self.translate(text, target_language)
            results.append(translated)
        
        logger.info(f"Batch translated {len(texts)} texts")
        return results
    
    def _normalize_language_code(self, language: str) -> str:
        """
        Convert language name to code if needed.
        
        Args:
            language: Language name or code
        
        Returns:
            Language code
        """
        if len(language) == 2:
            return language.lower()  # Already a code
        
        return self.LANGUAGE_CODES.get(language.lower(), language.lower()[:2])


if __name__ == '__main__':
    # Example usage
    translator = Translator(TranslationService.TEXTBLOB)
    
    text = "Hello, how are you today?"
    
    # Detect language
    detected = translator.detect_language(text)
    print(f"Detected language: {detected}")
    
    # Translate to Spanish
    spanish = translator.translate(text, 'es')
    print(f"Spanish: {spanish}")
    
    # Translate to French
    french = translator.translate(text, 'fr')
    print(f"French: {french}")