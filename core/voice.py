import pyttsx3
import speech_recognition as sr
import threading
from typing import Optional, Callable
from config import Config

class VoiceInterface:
    """Handle voice input and output"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', Config.VOICE_RATE)
        self.engine.setProperty('volume', Config.VOICE_VOLUME)
        
        # Set voice (try to find a good male voice)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.recognizer = sr.Recognizer()
        self.is_speaking = False
    
    def speak(self, text: str, async_mode: bool = False):
        """Convert text to speech"""
        if not Config.VOICE_ENABLED:
            return
        
        def _speak():
            self.is_speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            finally:
                self.is_speaking = False
        
        if async_mode:
            thread = threading.Thread(target=_speak)
            thread.start()
        else:
            _speak()
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                
                print("🔄 Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"📝 Heard: {text}")
                return text
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def stop(self):
        """Stop speaking"""
        if self.is_speaking:
            self.engine.stop()