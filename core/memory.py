from typing import List, Dict, Any
from datetime import datetime
import json

class SessionMemory:
    """Manage conversation context and short-term memory"""
    
    def __init__(self, context_window: int = 10):
        self.context_window = context_window
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.active_tasks: List[Dict[str, Any]] = []
        self.session_start = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add a message to conversation history"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.conversation_history.append(message)
        
        # Keep only recent messages within context window
        if len(self.conversation_history) > self.context_window * 2:
            self.conversation_history = self.conversation_history[-self.context_window * 2:]
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get recent conversation context"""
        return [
            {'role': msg['role'], 'content': msg['content']}
            for msg in self.conversation_history[-self.context_window:]
        ]
    
    def add_preference(self, key: str, value: Any):
        """Store user preference"""
        self.user_preferences[key] = value
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve user preference"""
        return self.user_preferences.get(key, default)
    
    def add_task(self, task: Dict[str, Any]):
        """Add an active task"""
        task['created_at'] = datetime.now().isoformat()
        self.active_tasks.append(task)
    
    def complete_task(self, task_id: str):
        """Mark a task as complete"""
        self.active_tasks = [t for t in self.active_tasks if t.get('id') != task_id]
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all active tasks"""
        return self.active_tasks
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary"""
        return {
            'session_duration': str(datetime.now() - self.session_start),
            'messages_exchanged': len(self.conversation_history),
            'active_tasks': len(self.active_tasks),
            'preferences_learned': len(self.user_preferences)
        }
    
    def clear(self):
        """Clear session memory"""
        self.conversation_history.clear()
        self.active_tasks.clear()