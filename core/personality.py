import random
from typing import List

class JarvisPersonality:
    """JARVIS-like personality and response styling"""
    
    GREETINGS = [
        "Good to see you, sir.",
        "At your service, sir.",
        "Welcome back, sir.",
        "How may I assist you today, sir?",
        "Ready and operational, sir."
    ]
    
    ACKNOWLEDGMENTS = [
        "Certainly, sir.",
        "Right away, sir.",
        "Of course, sir.",
        "Consider it done, sir.",
        "Understood, sir.",
        "At once, sir."
    ]
    
    THINKING = [
        "Let me process that for you, sir.",
        "One moment while I analyze this, sir.",
        "Accessing the information now, sir.",
        "Running diagnostics, sir.",
        "Calculating, sir."
    ]
    
    ERRORS = [
        "I apologize, sir, but I encountered an issue.",
        "My apologies, sir. Something went wrong.",
        "I'm afraid there's been a complication, sir.",
        "Regrettably, sir, I was unable to complete that task."
    ]
    
    COMPLETIONS = [
        "Task completed successfully, sir.",
        "Done, sir.",
        "All finished, sir.",
        "Task accomplished, sir.",
        "Completed as requested, sir."
    ]
    
    @staticmethod
    def greeting() -> str:
        """Get a random greeting"""
        return random.choice(JarvisPersonality.GREETINGS)
    
    @staticmethod
    def acknowledge() -> str:
        """Get a random acknowledgment"""
        return random.choice(JarvisPersonality.ACKNOWLEDGMENTS)
    
    @staticmethod
    def thinking() -> str:
        """Get a random thinking message"""
        return random.choice(JarvisPersonality.THINKING)
    
    @staticmethod
    def error() -> str:
        """Get a random error message"""
        return random.choice(JarvisPersonality.ERRORS)
    
    @staticmethod
    def completion() -> str:
        """Get a random completion message"""
        return random.choice(JarvisPersonality.COMPLETIONS)
    
    @staticmethod
    def format_response(response: str, add_prefix: bool = True) -> str:
        """Format response in JARVIS style"""
        if add_prefix and random.random() > 0.6:
            prefix = random.choice([
                "Sir, ",
                "I should mention, sir, ",
                "If I may, sir, ",
                "Allow me to inform you, sir, "
            ])
            response = prefix + response.lower()[0] + response[1:]
        
        return response
    
    @staticmethod
    def proactive_suggestion(context: str) -> str:
        """Generate proactive suggestion"""
        suggestions = [
            f"Sir, based on {context}, might I suggest...",
            f"If I may, sir, considering {context}, perhaps...",
            f"Sir, I've noticed {context}. Would you like me to...",
            f"Pardon the interruption, sir, but regarding {context}..."
        ]
        return random.choice(suggestions)