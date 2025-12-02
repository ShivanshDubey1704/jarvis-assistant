import requests
import json
from typing import Dict, Any, Optional, List
from config import Config

class BhindiClient:
    """Wrapper for Bhindi API interactions"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.BHINDI_API_KEY
        self.base_url = Config.BHINDI_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def chat(self, message: str, context: List[Dict] = None) -> Dict[str, Any]:
        """Send a chat message to Bhindi"""
        try:
            payload = {
                'message': message,
                'context': context or []
            }
            
            response = requests.post(
                f'{self.base_url}/chat',
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to communicate with Bhindi API'
            }
    
    def add_agent(self, agent_id: str) -> Dict[str, Any]:
        """Add an agent to the current session"""
        try:
            response = requests.post(
                f'{self.base_url}/agents/add',
                headers=self.headers,
                json={'agentId': agent_id},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_schedule(self, content: str, cron: str, schedule_type: str = 'reminder') -> Dict[str, Any]:
        """Create a schedule using Bhindi Scheduler"""
        try:
            payload = {
                'content': content,
                'cronExpression': cron,
                'type': schedule_type,
                'recurring': False
            }
            
            response = requests.post(
                f'{self.base_url}/scheduler/create',
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_web(self, query: str) -> Dict[str, Any]:
        """Search the web using Bhindi agents"""
        try:
            # First add perplexity agent
            self.add_agent('perplexity')
            
            # Then perform search
            return self.chat(f"Search for: {query}")
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_task(self, task: str, agent_id: str = None) -> Dict[str, Any]:
        """Execute a task using appropriate Bhindi agent"""
        try:
            if agent_id:
                self.add_agent(agent_id)
            
            return self.chat(task)
        except Exception as e:
            return {'success': False, 'error': str(e)}