from typing import Dict, Any, Optional
from utils.bhindi_client import BhindiClient
from utils.helpers import detect_intent, extract_agent_needed, parse_time_expression
from core.memory import SessionMemory
from core.personality import JarvisPersonality
from config import Config

class JarvisBrain:
    """Main AI orchestrator - the brain of JARVIS"""
    
    def __init__(self):
        self.bhindi = BhindiClient()
        self.memory = SessionMemory(context_window=Config.CONTEXT_WINDOW)
        self.personality = JarvisPersonality()
        self.active_agents = set()
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process user message and generate response"""
        
        # Add to memory
        self.memory.add_message('user', message)
        
        # Detect intent
        intent_data = detect_intent(message)
        intent = intent_data['intent']
        
        # Determine needed agents
        needed_agents = extract_agent_needed(message)
        
        # Add agents if needed
        for agent in needed_agents:
            if agent not in self.active_agents:
                self.bhindi.add_agent(agent)
                self.active_agents.add(agent)
        
        # Route to appropriate handler
        if intent == 'schedule':
            response = self._handle_schedule(message)
        elif intent == 'search':
            response = self._handle_search(message)
        elif intent == 'time':
            response = self._handle_time(message)
        else:
            response = self._handle_general(message)
        
        # Add response to memory
        self.memory.add_message('assistant', response['message'])
        
        return response
    
    def _handle_schedule(self, message: str) -> Dict[str, Any]:
        """Handle scheduling requests"""
        try:
            # Parse time expression
            cron, is_recurring = parse_time_expression(message)
            
            # Extract what to remind about
            content = message
            for word in ['remind me to', 'remind me', 'schedule', 'set alarm']:
                content = content.replace(word, '').strip()
            
            # Create schedule
            result = self.bhindi.create_schedule(
                content=f"Reminder: {content}",
                cron=cron,
                schedule_type='reminder'
            )
            
            if result.get('success'):
                response = f"{self.personality.acknowledge()} I've scheduled that for you, sir."
            else:
                response = f"{self.personality.error()} {result.get('error', 'Unknown error')}"
            
            return {
                'success': result.get('success', False),
                'message': response,
                'data': result
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"{self.personality.error()} {str(e)}",
                'data': None
            }
    
    def _handle_search(self, message: str) -> Dict[str, Any]:
        """Handle search requests"""
        try:
            result = self.bhindi.search_web(message)
            
            if result.get('success'):
                response = self.personality.format_response(
                    result.get('message', 'Here is what I found.')
                )
            else:
                response = f"{self.personality.error()} {result.get('error', 'Search failed')}"
            
            return {
                'success': result.get('success', False),
                'message': response,
                'data': result
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"{self.personality.error()} {str(e)}",
                'data': None
            }
    
    def _handle_time(self, message: str) -> Dict[str, Any]:
        """Handle time/date requests"""
        from datetime import datetime
        now = datetime.now()
        
        if 'date' in message.lower():
            response = f"Today is {now.strftime('%A, %B %d, %Y')}, sir."
        else:
            response = f"The time is {now.strftime('%I:%M %p')}, sir."
        
        return {
            'success': True,
            'message': response,
            'data': {'timestamp': now.isoformat()}
        }
    
    def _handle_general(self, message: str) -> Dict[str, Any]:
        """Handle general conversation"""
        try:
            # Get conversation context
            context = self.memory.get_context()
            
            # Send to Bhindi
            result = self.bhindi.chat(message, context)
            
            if result.get('success'):
                response = self.personality.format_response(
                    result.get('message', 'I understand, sir.')
                )
            else:
                response = f"{self.personality.error()} {result.get('error', 'I could not process that')}"
            
            return {
                'success': result.get('success', False),
                'message': response,
                'data': result
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"{self.personality.error()} {str(e)}",
                'data': None
            }
    
    def get_proactive_suggestions(self) -> Optional[str]:
        """Generate proactive suggestions based on context"""
        from datetime import datetime
        now = datetime.now()
        hour = now.hour
        
        # Morning suggestions
        if 6 <= hour < 9:
            return self.personality.proactive_suggestion(
                "the morning hour"
            ) + "check your schedule for today?"
        
        # Afternoon suggestions
        elif 12 <= hour < 14:
            return self.personality.proactive_suggestion(
                "the lunch hour"
            ) + "take a break, sir?"
        
        # Evening suggestions
        elif 18 <= hour < 20:
            return self.personality.proactive_suggestion(
                "the evening"
            ) + "review today's accomplishments?"
        
        return None