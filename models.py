# File: models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Bảng lưu thông tin người dùng"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('Message', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Message(db.Model):
    """Bảng lưu lịch sử chat"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.user_id}>'


class Analytics(db.Model):
    """Bảng lưu thống kê"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_messages = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Float, default=0.0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analytics User {self.user_id}>'
