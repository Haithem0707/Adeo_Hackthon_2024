from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config import Config
from apps.services.firebase_service import FirebaseService


class SimpleChatbotService:
    def __init__(self, firebase_service, openai_api_key: str):
        self.firebase_service = firebase_service
        self.chat_model = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4",
            openai_api_key=openai_api_key
        )
        
        self.prompt = """You are an AI assistant for the Abu Dhabi Executive Council. Your role is to help government officials with research, analysis, and decision-making.

Previous conversation:
{chat_history}

Question: {question}

Provide a professional response that:
1. Addresses the question directly
2. References Abu Dhabi's Vision 2030 when relevant
3. Includes practical recommendations
4. Maintains appropriate confidentiality

Response:"""

    def chat(self, session_id: str, message: str, department: str = "general"):
        try:
            # Get chat history
            history = self.firebase_service.get_chat_history(session_id)
            
            # Format chat history
            formatted_history = "\n".join([
                f"User: {msg['content']}" if msg['role'] == 'user' else f"Assistant: {msg['content']}"
                for msg in history[-5:]  # Get last 5 messages for context
            ])
            
            # Generate response
            prompt_content = self.prompt.format(
                chat_history=formatted_history,
                question=message
            )
            
            response = self.chat_model.invoke([{"role": "user", "content": prompt_content}])
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Save user message
            self.firebase_service.save_chat_message(
                session_id=session_id,
                message={
                    "role": "user",
                    "content": message,
                    "department": department,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Save assistant response
            self.firebase_service.save_chat_message(
                session_id=session_id,
                message={
                    "role": "assistant",
                    "content": response_content,
                    "department": department,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return {
                "status": "success",
                "response": response_content
            }
            
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def get_summary(self, session_id: str):
        try:
            history = self.firebase_service.get_chat_history(session_id)
            
            if not history:
                return {
                    "status": "success",
                    "summary": "No conversation history found."
                }
            
            formatted_history = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in history
            ])
            
            summary_prompt = f"""Summarize this government conversation:

{formatted_history}

Provide:
1. Main topics discussed
2. Key recommendations made
3. Action items"""
            
            response = self.chat_model.invoke([{"role": "user", "content": summary_prompt}])
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "status": "success",
                "summary": response_content
            }
            
        except Exception as e:
            print(f"Summary error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }



