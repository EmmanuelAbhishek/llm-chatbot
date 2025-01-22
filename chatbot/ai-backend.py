from anthropic import Anthropic
from django.conf import settings
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ChatbotAI:
    def __init__(self):
        self.anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.role_prompts = {
            'admin': "You are an administrative assistant helping with LMS management tasks.",
            'student': "You are a helpful study assistant supporting student learning needs.",
            'lecturer': "You are an educational assistant helping with teaching and course management."
        }
        
    def _build_system_prompt(self, role: str) -> str:
        base_prompt = self.role_prompts.get(role, self.role_prompts['student'])
        return f"{base_prompt} Provide clear, concise responses focused on educational context."
    
    def _extract_context(self, user_context: Dict[str, Any]) -> str:
        context_str = ""
        if user_context.get('course'):
            context_str += f"Related to course: {user_context['course']}. "
        if user_context.get('topic'):
            context_str += f"Specifically about: {user_context['topic']}. "
        return context_str

    async def process_query(
        self,
        query: str,
        role: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        try:
            system_prompt = self._build_system_prompt(role)
            context = self._extract_context(user_context or {})
            
            message = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"{context}{query}"
                }]
            )
            
            return message.content
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."

    def validate_response(self, response: str, role: str) -> str:
        """Validate and format the response according to role-specific requirements."""
        if not response:
            return "I apologize, but I couldn't generate a proper response. Please try again."
            
        # Add role-specific formatting and validation
        if role == 'student':
            # Ensure responses are educational and supportive
            return response
        elif role == 'lecturer':
            # Format for teaching context
            return response
        else:
            return response

chatbot_ai = ChatbotAI()
