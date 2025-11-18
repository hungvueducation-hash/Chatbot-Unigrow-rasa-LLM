from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .utils import llm_client, UNIGROW_SYSTEM_PROMPT
import logging

logger = logging.getLogger(__name__)

class ActionQueryLLMFallback(Action):
    """
    Dùng Mistral LLM để trả lời các câu hỏi phức tạp
    khi Rasa NLU không tự tin
    """
    
    def name(self) -> Text:
        return "action_query_llm_fallback"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        # Lấy câu hỏi cuối từ user
        user_message = tracker.latest_message.get("text", "")
        
        logger.info(f"LLM Fallback triggered for: {user_message}")
        
        # Tạo prompt cho LLM
        prompt = f"""User hỏi: {user_message}

Hãy trả lời theo hướng dẫn ở trên về Unigrow và phát triển chiều cao."""
        
        # Gọi Mistral 7B
        response = llm_client.generate_response(
            prompt=prompt,
            system_prompt=UNIGROW_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=512
        )
        
        dispatcher.utter_message(text=response)
        return []

class ActionGetUserAge(Action):
    """Lưu tuổi của user từ entities"""
    
    def name(self) -> Text:
        return "action_get_user_age"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        # Extract age từ entities
        age = next(
            (entity["value"] for entity in tracker.latest_message.get("entities", [])
             if entity["entity"] == "age"),
            None
        )
        
        if age:
            dispatcher.utter_message(text=f"Bạn {age} tuổi - tuổi phát triển tốt! 💪")
            return [SlotSet("user_age", age)]
        else:
            dispatcher.utter_message(text="Có thể cho mình biết bạn bao nhiêu tuổi?")
            return []

class ActionStoreHeightInfo(Action):
    """Lưu thông tin chiều cao"""
    
    def name(self) -> Text:
        return "action_store_height_info"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        current_height = next(
            (entity["value"] for entity in tracker.latest_message.get("entities", [])
             if entity["entity"] == "current_height"),
            None
        )
        
        target_height = next(
            (entity["value"] for entity in tracker.latest_message.get("entities", [])
             if entity["entity"] == "target_height"),
            None
        )
        
        events = []
        if current_height:
            events.append(SlotSet("user_height", current_height))
        if target_height:
            events.append(SlotSet("target_height", target_height))
        
        if current_height and target_height:
            dispatcher.utter_message(
                text=f"Vậy từ {current_height}cm muốn tới {target_height}cm. "
                     "Tôi sẽ giúp bạn! Unigrow + dinh dưỡng + tập luyện sẽ giúp bạn đạt được mục tiêu. 💯"
            )
        
        return events

class ActionDefaultFallback(Action):
    """Fallback khi không hiểu câu hỏi"""
    
    def name(self) -> Text:
        return "action_default_fallback"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="Xin lỗi, mình không hiểu câu hỏi của bạn. "
                 "Bạn có thể hỏi về:\n"
                 "- Chiều cao & cách phát triển\n"
                 "- Unigrow & cách dùng\n"
                 "- Giá cả & mua hàng\n"
                 "Hoặc nhắn lại với cách hỏi khác nhé! 😊"
        )
        return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActionReverted
from .utils import llm_client, UNIGROW_SYSTEM_PROMPT
import logging
import re

logger = logging.getLogger(__name__)

# ============ ADVANCED CUSTOM ACTIONS ============

class ActionExtractAgeEntity(Action):
    """Trích xuất tuổi từ user message"""
    
    def name(self) -> Text:
        return "action_extract_age_entity"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text", "").lower()
        
        # Regex pattern để tìm tuổi
        age_patterns = [
            r'(\d{1,2})\s*tuổi',
            r'tôi\s+(\d{1,2})',
            r'mình\s+(\d{1,2})',
            r'em\s+(\d{1,2})',
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, user_message)
            if match:
                age = match.group(1)
                # Validate age (phải từ 0-150)
                if 0 <= int(age) <= 150:
                    logger.info(f"Extracted age: {age}")
                    return [SlotSet("user_age", age)]
        
        return []

class ActionValidateHeight(Action):
    """Validate thông tin chiều cao"""
    
    def name(self) -> Text:
        return "action_validate_height"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text", "").lower()
        
        # Pattern để tìm chiều cao (150cm, 160 cm, 1m70, etc)
        height_patterns = [
            r'(\d{2,3})\s*cm',
            r'(\d)m(\d{2})',
            r'(\d\.\d{2})\s*m',
        ]
        
        heights = []
        for pattern in height_patterns:
            matches = re.findall(pattern, user_message)
            if matches:
                heights.extend(matches)
        
        if heights:
            logger.info(f"Found heights: {heights}")
            dispatcher.utter_message(
                text=f"Mình hiểu bạn cao khoảng {heights[0]}. Bạn muốn cao bao nhiêu nữa?"
            )
        
        return []

class ActionConfirmPurchaseIntent(Action):
    """Xác nhận ý định mua của user"""
    
    def name(self) -> Text:
        return "action_confirm_purchase_intent"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_age = tracker.get_slot("user_age")
        user_height = tracker.get_slot("user_height")
        target_height = tracker.get_slot("target_height")
        
        # Xây dựng message based on thông tin user
        message_parts = []
        
        if user_age:
            message_parts.append(f"Bạn {user_age} tuổi")
        if user_height:
            message_parts.append(f"cao {user_height}cm")
        if target_height:
            message_parts.append(f"muốn {target_height}cm")
        
        if message_parts:
            context_msg = ", ".join(message_parts) + "."
            dispatcher.utter_message(
                text=f"Tôi đã hiểu: {context_msg}\n\n"
                     "Unigrow sẽ hỗ trợ bạn đạt được mục tiêu này. "
                     "Bạn có muốn mua không?"
            )
        else:
            dispatcher.utter_message(
                text="Bạn có muốn mua Unigrow để bắt đầu hỗ trợ phát triển chiều cao không?"
            )
        
        return []

class ActionProvidePricingOptions(Action):
    """Cung cấp các tùy chọn giá"""
    
    def name(self) -> Text:
        return "action_provide_pricing_options"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        pricing_message = """
🛍️ **GÓI UNIGROW CÓ SẴN:**

📦 **Gói Cơ Bản** - 1 Hộp (30 viên)
   Giá: 299.000đ
   Dùng được: ~1 tháng

📦📦 **Gói Tiết Kiệm** - 3 Hộp (90 viên) ⭐
   Giá: 799.000đ (Tiết kiệm 100k)
   Dùng được: ~3 tháng
   
📦📦📦 **Gói Tối Ưu** - 6 Hộp (180 viên) 🔥
   Giá: 1.499.000đ (Tiết kiệm 300k)
   Dùng được: ~6 tháng

💡 **Khuyến nghị:** Gói 3 hoặc 6 hộp để thấy hiệu quả tốt hơn!

Bạn muốn chọn gói nào?
        """
        
        dispatcher.utter_message(text=pricing_message)
        return []

class ActionGetProductRecommendation(Action):
    """Recommend sản phẩm dựa trên tuổi & chiều cao"""
    
    def name(self) -> Text:
        return "action_get_product_recommendation"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_age = tracker.get_slot("user_age")
        
        recommendation = "Unigrow phù hợp cho tất cả lứa tuổi từ 8-30 tuổi. "
        
        if user_age:
            age_int = int(user_age)
            if age_int < 18:
                recommendation += (
                    f"Ở tuổi {user_age}, bạn vẫn đang trong giai đoạn phát triển vàng. "
                    f"Unigrow sẽ giúp bạn tối ưu hóa chiều cao trong thời kỳ này. "
                    f"Khuyến nghị dùng 3-6 tháng liên tục để thấy kết quả."
                )
            elif age_int < 25:
                recommendation += (
                    f"Ở tuổi {user_age}, bạn vẫn còn cơ hội phát triển. "
                    f"Unigrow sẽ hỗ trợ tối đa trong giai đoạn này. "
                    f"Kết hợp với ngủ đủ, dinh dưỡng, tập luyện sẽ rất hiệu quả."
                )
            else:
                recommendation += (
                    f"Ở tuổi {user_age}, cơ hội phát triển chiều cao còn lại thấp. "
                    f"Tuy nhiên Unigrow vẫn có thể hỗ trợ, đặc biệt khi kết hợp lối sống lành mạnh."
                )
        
        dispatcher.utter_message(text=recommendation)
        return []

class ActionSummarizeConversation(Action):
    """Tóm tắt cuộc trò chuyện"""
    
    def name(self) -> Text:
        return "action_summarize_conversation"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_age = tracker.get_slot("user_age")
        user_height = tracker.get_slot("user_height")
        target_height = tracker.get_slot("target_height")
        
        summary = "**📋 Tóm Tắt Thông Tin:**\n\n"
        
        if user_age:
            summary += f"• Tuổi: {user_age} tuổi\n"
        if user_height:
            summary += f"• Chiều cao hiện tại: {user_height}cm\n"
        if target_height:
            summary += f"• Chiều cao mong muốn: {target_height}cm\n"
        
        summary += (
            "\n💪 **Khuyến nghị:**\n"
            "1. Sử dụng Unigrow 3-6 tháng liên tục\n"
            "2. Ngủ đủ 8 giờ/ngày\n"
            "3. Tập luyện 30 phút/ngày (đặc biệt bơi lội, bóng rổ)\n"
            "4. Ăn đủ protein, canxi, vitamin D\n"
            "5. Kiên trì và đừng bỏ cuộc!"
        )
        
        dispatcher.utter_message(text=summary)
        return []

class ActionQueryLLMAdvanced(Action):
    """LLM query nâng cao với context từ slots"""
    
    def name(self) -> Text:
        return "action_query_llm_advanced"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text", "")
        user_age = tracker.get_slot("user_age")
        user_height = tracker.get_slot("user_height")
        
        # Xây dựng context từ slots
        context = ""
        if user_age or user_height:
            context = "\n\nThông tin người dùng:\n"
            if user_age:
                context += f"- Tuổi: {user_age}\n"
            if user_height:
                context += f"- Chiều cao: {user_height}cm\n"
        
        prompt = f"""User hỏi: {user_message}{context}

Hãy trả lời theo hướng dẫn ở trên về Unigrow và phát triển chiều cao."""
        
        response = llm_client.generate_response(
            prompt=prompt,
            system_prompt=UNIGROW_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=512
        )
        
        dispatcher.utter_message(text=response)
        return []
