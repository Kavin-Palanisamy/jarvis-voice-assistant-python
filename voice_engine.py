"""
voice_engine.py
Handles Speech-to-Text (STT) and Text-to-Speech (TTS).
Uses faster-whisper for STT and pyttsx3 for TTS fallback.
"""

import asyncio
import os
import pyttsx3
from logger import get_logger

logger = get_logger()

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set a professional voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "Hazel" in voice.name or "George" in voice.name or "Zira" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 170)
        self.whisper_model = None
        
        logger.info("Voice engine initialized.")
        
    def _init_whisper(self):
        """Lazy load whisper model so it doesn't block startup."""
        if not self.whisper_model:
            logger.info("Loading faster-whisper base model...")
            try:
                from faster_whisper import WhisperModel
                self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
                logger.info("faster-whisper loaded successfully.")
            except ImportError:
                logger.error("faster-whisper not installed. Speech recognition disabled.")
            except Exception as e:
                logger.error(f"Failed to load faster-whisper: {e}")

    async def speak(self, text: str):
        """Asynchronously plays TTS."""
        logger.info(f"JARVIS Speaking: {text}")
        
        # Run blocking pyttsx3 engine in a separate thread so it doesn't block asyncio
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._speak_sync, text)

    def _speak_sync(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    async def listen(self) -> str:
        """Records microphone snippet and transcribes it (Placeholder)."""
        self._init_whisper()
        
        logger.info("Listening (stub)...")
        await asyncio.sleep(1) # simulate gathering audio
        return "simulate user holding spacebar or saying wake word"

if __name__ == "__main__":
    async def test():
        ve = VoiceEngine()
        await ve.speak("System online, sir.")
    asyncio.run(test())
