import requests
import json
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class MistralLLMClient:
    """Client để gọi Mistral 7B thông qua Ollama"""
    
    def __init__(
        self,
        model_name: str = None,
        base_url: str = None
    ):
        self.model_name = model_name or os.getenv("MISTRAL_MODEL_NAME", "mistral")
        self.base_url = base_url or os.getenv("MISTRAL_BASE_URL", "http://localhost:11434")
        self.api_endpoint = f"{self.base_url}/api/generate"
    
    def generate_response(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Gọi Mistral 7B để generate response
        
        Args:
            prompt: Câu hỏi/prompt
            temperature: Độ ngẫu nhiên (0-1)
            max_tokens: Số token tối đa
            system_prompt: System prompt (hướng dẫn cho model)
        
        Returns:
            Response từ model
        """
        
        temperature = temperature or float(os.getenv("MISTRAL_TEMPERATURE", 0.7))
        max_tokens = max_tokens or int(os.getenv("MISTRAL_MAX_TOKENS", 512))
        
        # Thêm system prompt nếu có
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "temperature": temperature,
            "top_p": 0.9,
            "num_predict": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
        
        except requests.exceptions.ConnectionError:
            return "⚠️ Lỗi kết nối đến LLM. Vui lòng kiểm tra Ollama đang chạy."
        except Exception as e:
            return f"⚠️ Lỗi: {str(e)}"

# Khởi tạo client
llm_client = MistralLLMClient()

# System prompt cho Unigrow Bot
UNIGROW_SYSTEM_PROMPT = """
Bạn là bot hỗ trợ của Unigrow - một sản phẩm hỗ trợ phát triển chiều cao tự nhiên.

Yêu cầu:
1. Trả lời thân thiện, hỗ trợ về chiều cao và sản phẩm Unigrow
2. Luôn nhấn mạnh Unigrow là hỗ trợ, không phải thuốc
3. Khuyến khích lối sống lành mạnh: ngủ đủ, tập luyện, dinh dưỡng tốt
4. Trả lời tiếng Việt
5. Giữ conversation ngắn gọn, rõ ràng
6. Nếu không biết, nói thẳng không biết
7. Hỗ trợ bán hàng Unigrow một cách tự nhiên
"""
