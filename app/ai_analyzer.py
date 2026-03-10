import os
import requests
from typing import Dict, List, Optional


class AIAnalyzer:
    """Handles AI-based document analysis using OpenAI-compatible API"""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize AI Analyzer
        
        Args:
            api_key: API key for authentication (defaults to env var OPENAI_API_KEY)
            api_url: API endpoint URL (defaults to env var OPENAI_API_URL or OpenAI default)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "your-api-key-here")
        self.api_url = api_url or os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
    
    def analyze_document(self, text: str) -> Dict[str, any]:
        """
        Analyze document text using AI
        
        Args:
            text: Document text to analyze
            
        Returns:
            Dictionary containing summary and key_points
        """
        # Limit text length to avoid token limits
        max_chars = 12000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Create prompt for AI
        prompt = f"""Analyze the following document and provide:
1. A concise summary (2-3 sentences)
2. Key insights or main points (3-5 bullet points)

Document:
{text}

Please respond in the following JSON format:
{{
    "summary": "Your summary here",
    "key_points": ["Point 1", "Point 2", "Point 3"]
}}
"""
        
        try:
            # Call AI API
            response = self._call_ai_api(prompt)
            return response
            
        except Exception as e:
            print(f"Error calling AI API: {e}")
            # Return fallback response
            return self._fallback_analysis(text)
    
    def _call_ai_api(self, prompt: str) -> Dict[str, any]:
        """
        Make API call to AI service
        
        Args:
            prompt: Prompt to send to AI
            
        Returns:
            Parsed response with summary and key_points
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes documents and provides summaries and key insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Try to extract JSON from response
        import json
        try:
            # Find JSON in response
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
                return result
        except:
            pass
        
        # If JSON parsing fails, return structured fallback
        return {
            "summary": content[:200] if content else "Analysis completed",
            "key_points": ["See full response for details"]
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, any]:
        """
        Provide basic analysis when AI API is unavailable
        
        Args:
            text: Document text
            
        Returns:
            Basic analysis dictionary
        """
        # Simple text statistics
        words = text.split()
        sentences = text.split('.')
        
        summary = f"Document contains approximately {len(words)} words and {len(sentences)} sentences."
        
        # Extract first few sentences as pseudo key points
        key_points = []
        for i, sentence in enumerate(sentences[:3]):
            if sentence.strip():
                key_points.append(sentence.strip()[:100] + "...")
        
        if not key_points:
            key_points = ["Unable to extract key points from document"]
        
        return {
            "summary": summary,
            "key_points": key_points
        }
