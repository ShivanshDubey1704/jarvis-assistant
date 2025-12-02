import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def parse_time_expression(text: str) -> Tuple[str, bool]:
    """Parse natural language time expressions into cron format"""
    text = text.lower()
    now = datetime.now()
    
    # Daily patterns
    if 'every day' in text or 'daily' in text:
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            period = time_match.group(3)
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            return f"{minute} {hour} * * *", True
    
    # Hourly patterns
    if 'every hour' in text or 'hourly' in text:
        return "0 * * * *", True
    
    # Specific time today/tomorrow
    time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        period = time_match.group(3)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        target_time = now.replace(hour=hour, minute=minute, second=0)
        
        if 'tomorrow' in text:
            target_time += timedelta(days=1)
        elif target_time <= now:
            target_time += timedelta(days=1)
        
        return f"{target_time.minute} {target_time.hour} {target_time.day} {target_time.month} *", False
    
    # Default: 5 minutes from now
    future_time = now + timedelta(minutes=5)
    return f"{future_time.minute} {future_time.hour} {future_time.day} {future_time.month} *", False

def detect_intent(message: str) -> Dict[str, any]:
    """Detect user intent from message"""
    message_lower = message.lower()
    
    intents = {
        'schedule': ['remind', 'schedule', 'set alarm', 'wake me', 'meeting'],
        'search': ['search', 'find', 'look up', 'what is', 'who is', 'google'],
        'weather': ['weather', 'temperature', 'forecast'],
        'time': ['time', 'date', 'what day'],
        'task': ['do', 'execute', 'perform', 'run', 'create'],
        'question': ['?', 'how', 'why', 'when', 'where', 'what', 'who'],
    }
    
    for intent, keywords in intents.items():
        if any(keyword in message_lower for keyword in keywords):
            return {'intent': intent, 'confidence': 0.8}
    
    return {'intent': 'general', 'confidence': 0.5}

def format_response(response: str, style: str = 'jarvis') -> str:
    """Format response in JARVIS style"""
    if style == 'jarvis':
        prefixes = [
            "Certainly, sir. ",
            "Right away, sir. ",
            "Of course, sir. ",
            "At your service, sir. ",
            "Understood, sir. "
        ]
        
        # Add prefix occasionally for personality
        import random
        if random.random() > 0.7:
            response = random.choice(prefixes) + response
    
    return response

def extract_agent_needed(message: str) -> List[str]:
    """Determine which Bhindi agents are needed for a task"""
    message_lower = message.lower()
    agents = []
    
    agent_keywords = {
        'perplexity': ['search', 'find', 'look up', 'google'],
        'bhindi-scheduler-v2': ['remind', 'schedule', 'alarm', 'meeting'],
        'open-weather': ['weather', 'temperature', 'forecast'],
        'google-gmail': ['email', 'send mail', 'gmail'],
        'calculator': ['calculate', 'math', 'compute'],
        'time': ['time', 'date', 'timezone'],
    }
    
    for agent, keywords in agent_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            agents.append(agent)
    
    return agents