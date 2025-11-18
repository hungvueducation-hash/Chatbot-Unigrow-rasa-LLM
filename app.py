# File: app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from rasa.core.agent import Agent
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Global agent
agent = None

def load_agent():
    """Load Rasa model"""
    global agent
    try:
        model_path = "models/latest"
        if not os.path.exists(model_path):
            logger.error(f"Model not found at {model_path}")
            return False
        
        agent = Agent.load(model_path)
        logger.info("Rasa model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

# ==================== API ENDPOINTS ====================

@app.route('/', methods=['GET'])
def index():
    """Serve Web UI"""
    return send_from_directory('.', 'index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'bot_name': 'Unigrow Chatbot',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

# NEW CODE (FIXED):
@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint - Process user message"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not agent:
            return jsonify({'error': 'Bot not loaded'}), 503
        
        # Simple text message - send to Rasa
        # Rasa 3.6 returns response directly
        import asyncio
        
        # Run async handler
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            responses = loop.run_until_complete(
                agent.handle_text(user_message)
            )
        finally:
            loop.close()
        
        # Extract text response
        bot_response = "I'm sorry, I couldn't understand that. Could you rephrase?"
        
        if responses:
            # responses is a list of dicts
            for response in responses:
                if isinstance(response, dict) and 'text' in response:
                    bot_response = response['text']
                    break
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'bot_response': bot_response,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in /api/chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

        
    except Exception as e:
        logger.error(f"Error in /api/chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get list of available intents"""
    try:
        if not agent:
            return jsonify({'error': 'Bot not loaded'}), 503
        
        intents = list(agent.domain.intents)
        return jsonify({
            'intents': intents,
            'total': len(intents)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in /api/intents: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Bot status"""
    return jsonify({
        'bot_loaded': agent is not None,
        'model_path': 'models/latest',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Get bot metrics"""
    return jsonify({
        'conversations_processed': 'N/A (track in production)',
        'average_response_time': 'N/A',
        'uptime': 'N/A',
        'version': '1.0.0'
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 Unigrow AI Chatbot - API Server")
    print("=" * 50)
    
    # Load agent
    print("Loading Rasa model...")
    if load_agent():
        print("✅ Model loaded successfully!")
        print("\n" + "=" * 50)
        print("🚀 Starting Flask server...")
        print("📍 Web UI: http://localhost:5000")
        print("📡 API: http://localhost:5000/api")
        print("=" * 50 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("❌ Failed to load model")
        print("Make sure you've trained the model first:")
        print("  rasa train --data data/ --domain domain.yml --config config.yml")
