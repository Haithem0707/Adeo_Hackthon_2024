# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

from config import Config
from apps import create_app, db
from apps.services.firebase_service import FirebaseService
from apps.services.simple_chatbot_service import SimpleChatbotService
from config import config_dict

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import asyncio
from functools import wraps
from config import Config
from apps.services.firebase_service import FirebaseService
from apps.services.simple_chatbot_service import SimpleChatbotService

app = Flask(__name__)
# Configure CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500"],  # Add your frontend origin
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "X-CSRFToken"],
        "max_age": 120  # Cache preflight requests for 2 minutes
    }
})

# Optionally, you can also use this decorator for specific routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Initialize services
try:
    Config.check_required_keys()
    # search_service = SearchService(api_key=Config.SERPAPI_API_KEY)
    # analysis_service = AnalysisService(
    #     openai_api_key=Config.OPENAI_API_KEY,
    #     huggingface_api_key=Config.HUGGINGFACE_API_KEY
    # )
    firebase_service = FirebaseService(project_id=Config.FIREBASE_PROJECT_ID)
    chatbot = SimpleChatbotService(
        firebase_service=firebase_service,
        openai_api_key=Config.OPENAI_API_KEY,
    )
    # langchain_service = LangChainService(openai_api_key=Config.OPENAI_API_KEY)
except ValueError as e:
    print(f"Configuration Error: {str(e)}")
    exit(1)




# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

#chatbot
@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    try:
        data = request.get_json()
        department = data.get('department', 'general')
        
        session_id = f"{department}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        firebase_service.save_chat_message(
            session_id=session_id,
            message={
                "role": "system",
                "content": "Chat session started",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        return jsonify({
            "status": "success",
            "session_id": session_id
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/chat/message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data or 'session_id' not in data:
            return jsonify({
                "status": "error",
                "message": "Message and session_id are required"
            }), 400
        
        response = chatbot.chat(
            session_id=data['session_id'],
            message=data['message'],
            department=data.get('department', 'general')
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/chat/history/<session_id>', methods=['GET', 'OPTIONS'])
def get_history(session_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        # Get chat history from Firebase
        history = firebase_service.get_chat_history(session_id)
        
        if not history:
            return jsonify({
                "status": "success",
                "history": [],
                "message": "No chat history found for this session"
            })
            
        # Format the history data
        formatted_history = []
        for msg in history:
            formatted_history.append({
                "role": msg.get("role", "unknown"),
                "content": msg.get("content", ""),
                "timestamp": msg.get("timestamp", datetime.now().isoformat()),
                "department": msg.get("department", "general")
            })
            
        return jsonify({
            "status": "success",
            "history": formatted_history
        })
        
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to fetch chat history: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)