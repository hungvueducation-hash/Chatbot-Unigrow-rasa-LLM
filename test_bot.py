"""
Script để test bot tất cả scenarios
"""

import requests
import json
import time

# Configuration
RASA_SERVER = "http://localhost:5005"
USER_ID = "test_user_001"

class BotTester:
    def __init__(self, base_url: str = RASA_SERVER):
        self.base_url = base_url
        self.user_id = USER_ID
    
    def send_message(self, message: str) -> dict:
        """Gửi tin nhắn đến bot"""
        url = f"{self.base_url}/webhooks/rest/webhook"
        payload = {
            "sender": self.user_id,
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def test_conversation_flow(self):
        """Test một conversation flow cơ bản"""
        
        test_messages = [
            ("xin chào", "Greeting"),
            ("Unigrow là gì", "Product Info"),
            ("tôi 20 tuổi", "Age Input"),
            ("chiều cao của tôi 160 cm", "Height Input"),
            ("muốn cao 175 cm", "Target Height"),
            ("giá bao nhiêu", "Price Query"),
            ("tôi muốn mua", "Purchase Intent"),
            ("tạm biệt", "Goodbye"),
        ]
        
        print("\n" + "="*60)
        print("🤖 BOT CONVERSATION TEST")
        print("="*60 + "\n")
        
        for message, scenario in test_messages:
            print(f"📝 [{scenario}] User: {message}")
            
            responses = self.send_message(message)
            
            if responses:
                for response in responses:
                    print(f"🤖 Bot: {response.get('text', 'N/A')}")
            else:
                print("❌ No response from bot")
            
            print("-" * 60)
            time.sleep(1)  # Delay giữa các message
    
    def test_llm_fallback(self):
        """Test LLM fallback"""
        
        print("\n" + "="*60)
        print("🧠 LLM FALLBACK TEST")
        print("="*60 + "\n")
        
        complex_questions = [
            "Làm sao tôi có thể tăng chiều cao nhanh nhất?",
            "Unigrow có phù hợp cho người lớn tuổi không?",
            "Kết hợp Unigrow với những gì để hiệu quả tốt nhất?",
        ]
        
        for question in complex_questions:
            print(f"❓ Question: {question}")
            
            responses = self.send_message(question)
            
            if responses:
                for response in responses:
                    print(f"🤖 Response: {response.get('text', 'N/A')}\n")
            else:
                print("❌ No response\n")
            
            time.sleep(2)

if __name__ == "__main__":
    tester = BotTester()
    
    print("\n⏳ Chạy test bot...\n")
    
    # Test 1: Conversation flow
    tester.test_conversation_flow()
    
    # Test 2: LLM fallback
    tester.test_llm_fallback()
    
    print("\n" + "="*60)
    print("✅ TEST HOÀN THÀNH")
    print("="*60 + "\n")
