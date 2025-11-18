# File: app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from rasa.core.agent import Agent
from models import db, User, Message, Analytics
import os
import json
from datetime import datetime
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import asyncio

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Cấu hình database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo database
db.init_app(app)

# Tạo bảng database khi khởi động
with app.app_context():
    db.create_all()

# Global agent
agent = None

def load_agent():
    """Load Rasa model"""
    global agent
    try:
        model_path = "models/latest"
        if not os.path.exists(model_path):
            logger.error(f"Model không tìm thấy: {model_path}")
            return False
        
        agent = Agent.load(model_path)
        logger.info("✅ Rasa model loaded thành công")
        return True
    except Exception as e:
        logger.error(f"Lỗi load model: {str(e)}")
        return False

# ==================== ROUTES - TRANG WEB ====================

@app.route('/', methods=['GET'])
def index():
    """Trang chủ - hiển thị Web UI"""
    return send_from_directory('.', 'index.html')

@app.route('/health', methods=['GET'])
def health():
    """Kiểm tra hệ thống có bình thường không"""
    return jsonify({
        'status': 'healthy',
        'bot_name': 'Unigrow Chatbot',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==================== XÁC THỰC NGƯỜI DÙNG ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Đăng ký tài khoản mới"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        
        if not all([username, password, email]):
            return jsonify({'error': 'Thiếu thông tin đăng ký'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Tên người dùng đã tồn tại'}), 400
        
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, email=email)
        
        db.session.add(user)
        db.session.commit()
        
        analytics = Analytics(user_id=user.id)
        db.session.add(analytics)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công!',
            'user_id': user.id
        }), 201
        
    except Exception as e:
        logger.error(f"Lỗi đăng ký: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Đăng nhập"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Tên đăng nhập hoặc mật khẩu sai'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Đăng nhập thành công!',
            'user_id': user.id,
            'username': user.username
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi đăng nhập: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== CHAT & LỊCH SỬ ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat - lưu lịch sử vào database"""
    try:
        data = request.json
        user_id = data.get('user_id')
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Tin nhắn không được trống'}), 400
        
        if not user_id:
            return jsonify({'error': 'Cần đăng nhập trước'}), 401
        
        if not agent:
            return jsonify({'error': 'Bot không hoạt động'}), 503
        
        # Xử lý tin nhắn
        bot_response = "Xin lỗi, tôi không hiểu."
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            responses = loop.run_until_complete(
                agent.handle_text(user_message)
            )
            
            loop.close()
            
            if responses:
                for resp in responses:
                    if isinstance(resp, dict) and 'text' in resp:
                        bot_response = resp['text']
                        break
        except Exception as e:
            logger.error(f"Lỗi Rasa: {str(e)}")
        
        # LƯU VÀO DATABASE
        try:
            user = User.query.get(user_id)
            if user:
                message = Message(
                    user_id=user_id,
                    user_message=user_message,
                    bot_response=bot_response
                )
                db.session.add(message)
                
                analytics = Analytics.query.filter_by(user_id=user_id).first()
                if analytics:
                    analytics.total_messages += 1
                    analytics.last_active = datetime.utcnow()
                
                db.session.commit()
        except Exception as e:
            logger.error(f"Lỗi lưu DB: {str(e)}")
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'bot_response': bot_response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi chat: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    """Xem lịch sử chat"""
    try:
        messages = Message.query.filter_by(user_id=user_id).order_by(
            Message.timestamp.desc()
        ).limit(50).all()
        
        history = []
        for msg in reversed(messages):
            history.append({
                'user_message': msg.user_message,
                'bot_response': msg.bot_response,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return jsonify({
            'success': True,
            'total': len(history),
            'history': history
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi lấy lịch sử: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/<int:user_id>', methods=['GET'])
def get_analytics(user_id):
    """Xem thống kê"""
    try:
        analytics = Analytics.query.filter_by(user_id=user_id).first()
        
        if not analytics:
            return jsonify({'error': 'Không tìm thấy thống kê'}), 404
        
        return jsonify({
            'success': True,
            'total_messages': analytics.total_messages,
            'average_response_time': analytics.average_response_time,
            'last_active': analytics.last_active.isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi thống kê: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Không tìm thấy'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Lỗi server'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 Unigrow AI Chatbot - API Server")
    print("=" * 50)
    
    print("Loading Rasa model...")
    if load_agent():
        print("✅ Model loaded!")
        print("\n" + "=" * 50)
        print("🚀 Starting Flask server...")
        print("📍 Web UI: http://localhost:5000")
        print("📡 API: http://localhost:5000/api")
        print("=" * 50 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("❌ Failed to load model")
        print("Hãy train model trước:")
        print("  rasa train --data data/ --domain domain.yml --config config.yml")
