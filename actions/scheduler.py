import time
import threading
from datetime import datetime, timedelta
from typing import List, Callable, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class MessageScheduler:
    """Scheduler để gửi tin nhắn tự động theo lịch"""
    
    def __init__(self):
        self.scheduled_messages: List[Dict[str, Any]] = []
        self.running = False
        self.thread = None
    
    def schedule_message(
        self,
        recipient_id: str,
        message: str,
        delay_seconds: int = 0,
        callback: Callable = None
    ):
        """
        Lên lịch gửi tin nhắn
        
        Args:
            recipient_id: ID người nhận
            message: Nội dung tin
            delay_seconds: Độ trễ (giây)
            callback: Hàm gọi sau khi gửi
        """
        scheduled_time = time.time() + delay_seconds
        self.scheduled_messages.append({
            "recipient_id": recipient_id,
            "message": message,
            "scheduled_time": scheduled_time,
            "callback": callback
        })
        logger.info(f"Scheduled message for {recipient_id} at {scheduled_time}")
    
    def schedule_sequence(
        self,
        recipient_id: str,
        messages: List[str],
        delay_between_messages: int = 5
    ):
        """
        Lên lịch gửi chuỗi tin nhắn
        
        Args:
            recipient_id: ID người nhận
            messages: Danh sách tin nhắn
            delay_between_messages: Độ trễ giữa các tin (giây)
        """
        current_delay = 0
        for i, message in enumerate(messages):
            self.schedule_message(
                recipient_id=recipient_id,
                message=message,
                delay_seconds=current_delay
            )
            current_delay += delay_between_messages
            logger.info(f"Scheduled message {i+1}/{len(messages)}")
    
    def schedule_daily_reminder(
        self,
        recipient_id: str,
        message: str,
        time_of_day: str = "09:00"  # Format: HH:MM
    ):
        """
        Lên lịch nhắc nhở hàng ngày
        
        Args:
            recipient_id: ID người nhận
            message: Nội dung tin
            time_of_day: Giờ gửi (HH:MM)
        """
        # Tính toán thời gian gửi tiếp theo
        now = datetime.now()
        target_time = datetime.strptime(time_of_day, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        
        if target_time <= now:
            # Nếu giờ đã qua, lên lịch cho ngày mai
            target_time += timedelta(days=1)
        
        delay = (target_time - now).total_seconds()
        self.schedule_message(
            recipient_id=recipient_id,
            message=message,
            delay_seconds=int(delay)
        )
    
    def process_scheduled_messages(self, send_function: Callable):
        """Xử lý tin nhắn theo lịch"""
        self.running = True
        logger.info("Scheduler started")
        
        while self.running:
            current_time = time.time()
            messages_to_send = []
            
            # Tìm tin nhắn cần gửi
            for i, scheduled in enumerate(self.scheduled_messages):
                if scheduled["scheduled_time"] <= current_time:
                    messages_to_send.append((i, scheduled))
            
            # Gửi tin nhắn (theo thứ tự ngược để tránh index shifts)
            for idx, scheduled in sorted(messages_to_send, key=lambda x: x[0], reverse=True):
                try:
                    send_function(scheduled["recipient_id"], scheduled["message"])
                    logger.info(f"Sent message to {scheduled['recipient_id']}")
                    
                    if scheduled["callback"]:
                        scheduled["callback"]()
                    
                    self.scheduled_messages.pop(idx)
                except Exception as e:
                    logger.error(f"Failed to send message: {e}")
            
            time.sleep(1)  # Check mỗi giây
    
    def start(self, send_function: Callable):
        """Bắt đầu scheduler trong background thread"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.thread = threading.Thread(
            target=self.process_scheduled_messages,
            args=(send_function,),
            daemon=True
        )
        self.thread.start()
        logger.info("Scheduler thread started")
    
    def stop(self):
        """Dừng scheduler"""
        self.running = False
        logger.info("Scheduler stopped")

# Global scheduler instance
scheduler = MessageScheduler()

# Ví dụ: Lead nurturing sequence
UNIGROW_NURTURE_SEQUENCE = [
    "Cảm ơn bạn đã quan tâm Unigrow! 😊",
    "Unigrow là sản phẩm hỗ trợ phát triển chiều cao với công thức riêng.",
    "Thành phần chứa Canxi, Vitamin D3, Zinc, Arginine & L-Lysine để hỗ trợ phát triển.",
    "Bạn có muốn biết thêm về cách dùng và hiệu quả không?",
    "Đặc biệt, hôm nay chúng tôi có khuyến mãi gói 3 hộp: chỉ 799k (tiết kiệm 100k)! 🔥"
]

def schedule_nurture_sequence(user_id: str):
    """Lên lịch lead nurturing sequence"""
    scheduler.schedule_sequence(
        recipient_id=user_id,
        messages=UNIGROW_NURTURE_SEQUENCE,
        delay_between_messages=10  # Cách nhau 10 giây
    )
    logger.info(f"Nurture sequence scheduled for {user_id}")
