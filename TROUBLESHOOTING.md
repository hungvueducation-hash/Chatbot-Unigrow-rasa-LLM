# Troubleshooting Guide - Unigrow AI Chatbot

Hướng dẫn xử lý các lỗi thường gặp khi setup, develop, và run Unigrow Chatbot.

---

## 🔴 Setup Issues

### 1. Error: "Python not found"

**Lỗi:**
```
'python' is not recognized as an internal or external command
```

**Nguyên nhân:** Python chưa được add vào PATH

**Fix:**
```bash
# Windows - Add Python to PATH
setx PATH "%PATH%;C:\Python310"

# Restart terminal

# Verify
python --version
```

---

### 2. Error: "venv activation failed"

**Lỗi:**
```
cannot be loaded because running scripts is disabled on this system
```

**Nguyên nhân:** PowerShell execution policy

**Fix:**
```powershell
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Rồi activate lại
venv\Scripts\activate
```

---

### 3. Error: "Permission denied" when activating venv

**Lỗi:**
```
command not found: venv/bin/activate
```

**Nguyên nhân:** Linux/Mac permissions

**Fix:**
```bash
# Cấp quyền execute
chmod +x venv/bin/activate

# Activate
source venv/bin/activate
```

---

## 🟡 Installation Issues

### 4. Error: "pip install -r requirements.txt" fails

**Lỗi:**
```
ERROR: Could not find a version that satisfies the requirement rasa==3.6.21
```

**Nguyên nhân:** Network issue hoặc package không tương thích

**Fix:**
```bash
# Upgrade pip trước
python -m pip install --upgrade pip

# Cài lại
pip install -r requirements.txt -v

# Nếu vẫn lỗi, cài từng package:
pip install rasa==3.6.21
pip install torch==2.8.0
pip install mistral-7b-instruct==latest
```

---

### 5. Error: "torch installation fails"

**Lỗi:**
```
ERROR: No matching distribution found for torch==2.1.0
```

**Nguyên nhân:** CPU/GPU mismatch

**Fix:**
```bash
# For GPU (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CPU only
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## 🔴 Ollama Issues

### 6. Error: "Ollama connection refused"

**Lỗi:**
```
Error: Failed to connect to http://localhost:11434
```

**Nguyên nhân:** Ollama service không chạy

**Fix:**
```bash
# Khởi động Ollama
ollama serve

# Kiểm tra trong terminal mới
ollama list
```

---

### 7. Error: "Cannot pull mistral model"

**Lỗi:**
```
Error: Head "https://registry.ollama.ai/...": dial tcp: lookup registry.ollama.ai: no such host
```

**Nguyên nhân:** Network issue hoặc registry down

**Fix:**
```bash
# Cách 1: Thử lại
ollama pull mistral

# Cách 2: Reset Ollama
ollama serve
# (Ctrl+C)
ollama serve  # Start again

# Cách 3: Kiểm tra DNS
nslookup registry.ollama.ai

# Cách 4: Dùng VPN nếu cần
# Bật VPN, rồi:
ollama pull mistral
```

---

### 8. Error: "Mistral model loading fails"

**Lỗi:**
```
Error loading model: out of memory
```

**Nguyên nhân:** GPU memory không đủ

**Fix:**
```bash
# Kiểm tra GPU memory
nvidia-smi

# Nếu < 4GB, dùng model nhẹ hơn:
ollama pull tinyllama

# Hoặc close các ứng dụng khác
```

---

## 🟡 Rasa Issues

### 9. Error: "rasa train fails"

**Lỗi:**
```
YamlValidationException: Failed to validate 'domain.yml'
Cannot find required key 'mappings'. Path: '/slots/user_age'
```

**Nguyên nhân:** domain.yml format sai

**Fix:**
```yaml
# ❌ SAI
slots:
  user_age:
    type: text

# ✅ ĐÚNG
slots:
  user_age:
    type: text
    mappings:
      - type: from_entity
        entity: age
```

---

### 10. Error: "NLU training takes too long"

**Lỗi:**
```
Training NLU model... (stuck for > 30 min)
```

**Nguyên nhân:** Too much training data hoặc máy yếu

**Fix:**
```bash
# Giảm epochs trong config.yml
DIETClassifier:
  epochs: 50  # Giảm từ 100

# Hoặc cancel & train lại:
# Ctrl+C
rasa train
```

---

## 🟢 Runtime Issues

### 11. Error: "Bot shell connection refused"

**Lỗi:**
```
Failed to connect to Rasa Core server
```

**Nguyên nhân:** Action server hoặc model không load

**Fix:**
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Action server
rasa run actions --port 5055

# Terminal 3: Bot shell
rasa shell

# Nếu vẫn lỗi:
# Check lại model file có tồn tại:
ls models/
```

---

### 12. Error: "Action server not responding"

**Lỗi:**
```
Handler error in webhook URL: Connection to action server failed
```

**Nguyên nhân:** Action server chưa started

**Fix:**
```bash
# Start action server
rasa run actions --port 5055

# Kiểm tra
curl http://localhost:5055/health

# Output: OK
```

---

### 13. Error: "No response from bot"

**Lỗi:**
```
> hello
(no response or very slow)
```

**Nguyên nhân:** Model file bị lỗi, hoặc LLM fallback hung

**Fix:**
```bash
# 1. Check model
ls -la models/
# Nếu file quá nhỏ (< 100MB), model lỗi

# 2. Train lại
rasa train

# 3. Check Ollama
ollama list

# 4. Restart tất cả services
# Ctrl+C ở mỗi terminal
# Restart từ Terminal 1

# 5. Test response time
# Nếu > 5s, có thể LLM query bị hang
```

---

## 🔴 LLM Integration Issues

### 14. Error: "Mistral LLM timeout"

**Lỗi:**
```
requests.exceptions.ConnectTimeout: Connection to Mistral LLM timed out
```

**Nguyên nhân:** Ollama hoặc model quá chậm

**Fix:**
```python
# actions/utils.py
# Increase timeout
response = requests.post(
    self.api_endpoint,
    json=payload,
    timeout=60  # Từ 30s lên 60s
)

# Hoặc kiểm tra:
# nvidia-smi  # Check GPU usage
# free -h     # Check RAM
```

---

### 15. Error: "LLM response is empty or gibberish"

**Lỗi:**
```
Bot response: "ああああ" or blank
```

**Nguyên nhân:** Mistral model issue, hoặc prompt sai

**Fix:**
```bash
# Test Mistral trực tiếp
ollama run mistral
# Gõ câu tiếng Việt

# Nếu output sai, model bị lỗi:
ollama pull mistral  # Re-download

# Hoặc check UNIGROW_SYSTEM_PROMPT trong actions/utils.py
# Đảm bảo prompt có tiếng Việt
```

---

## 🟡 Data & Training Issues

### 16. Error: "Training data format invalid"

**Lỗi:**
```
Error in 'data/nlu/intents.yml': Invalid YAML format
```

**Nguyên nhân:** YAML syntax error

**Fix:**
```yaml
# ❌ SAI (tab indentation)
- intent: greet
	examples: |

# ✅ ĐÚNG (2 spaces)
- intent: greet
  examples: |
    - hello
    - xin chào
```

---

### 17. Error: "Intent recognition accuracy low"

**Lỗi:**
```
User: "xin chào"
Bot intent: "ask_price" (confidence: 0.45)
```

**Nguyên nhân:** Training data không đủ

**Fix:**
```yaml
# Thêm more examples vào intents.yml
- intent: greet
  examples: |
    - xin chào
    - hello
    - chào
    - hi
    - chào buổi sáng
    - chào bạn
    - hey
    - alo
    (Tối thiểu 10-15 examples per intent)

# Rồi train lại
rasa train
```

---

## 📊 Performance Issues

### 18. Error: "Response time too slow (> 5s)"

**Lỗi:**
```
User sends message → 10+ seconds delay
```

**Nguyên nhân:** LLM query hoặc model too large

**Fix:**
```bash
# 1. Check GPU
nvidia-smi
# Nếu GPU usage 100%, bị bottleneck

# 2. Reduce model size
ollama pull tinyllama  # Lightweight model

# 3. Increase GPU VRAM
# Nếu máy có, upgrade RTX 3060 (12GB)

# 4. Check CPU
top  # Linux/Mac
taskmgr  # Windows
# Nếu CPU usage 100%, tune config.yml

# 5. Optimize config.yml
DIETClassifier:
  epochs: 50  # Reduce
TEDPolicy:
  epochs: 50  # Reduce
```

---

### 19. Error: "Out of memory (OOM)"

**Lỗi:**
```
RuntimeError: CUDA out of memory
```

**Nguyên nhân:** GPU memory không đủ

**Fix:**
```bash
# 1. Check GPU memory
nvidia-smi
# Nếu < 4GB free, tutup ứng dụng khác

# 2. Close browser, IDE, etc
# Free up RAM

# 3. Restart Ollama
ollama serve

# 4. Use smaller model
ollama pull tinyllama

# 5. Reduce batch size (trong config.yml)
DIETClassifier:
  batch_size: 16  # Reduce
```

---

## 🟢 API Issues

### 20. Error: "API endpoint 404"

**Lỗi:**
```
curl http://localhost:5005/chat
# 404 Not Found
```

**Nguyên nhân:** Wrong endpoint

**Fix:**
```bash
# ✅ ĐÚNG endpoint
curl http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "hello"}'

# Phase 4 sẽ add /chat endpoint
```

---

### 21. Error: "CORS error in frontend"

**Lỗi:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Nguyên nhân:** Cross-origin request blocked

**Fix:**
```python
# app.py (Phase 4)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Or specific origins:
CORS(app, origins=["http://localhost:3000"])
```

---

## 🛠️ Debug Mode

### Enable Debug Logging

```python
# actions/actions.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing: {message}")
logger.info(f"Intent: {intent}")
logger.error(f"Error: {error}")
```

```bash
# Run with debug
rasa shell --debug

# Or
rasa run actions --debug --port 5055
```

---

## 📞 Getting Help

### When Troubleshooting Fails

1. **Check Logs:**
   - Rasa logs: Terminal output
   - Ollama logs: `~/.ollama/logs`
   - Python errors: Stack trace in terminal

2. **Collect Debug Info:**
   ```bash
   python --version
   rasa --version
   ollama list
   nvidia-smi
   pip list
   ```

3. **Reproduce Issue:**
   - Note exact steps
   - Expected vs actual output
   - Error message

4. **Report Issue:**
   - Include debug info
   - Attach logs/screenshots
   - Describe environment (Windows/Mac/Linux, GPU, RAM)

---

## ✅ Verification Checklist

After fixing, verify with:

```bash
# 1. Python OK?
python --version

# 2. Venv OK?
pip list | grep rasa

# 3. Rasa OK?
rasa --version

# 4. Ollama OK?
ollama list

# 5. Action server running?
curl http://localhost:5055/health

# 6. Bot responds?
rasa shell
> hello
```

---

**Troubleshooting Guide Hoàn Thành! 🛠️**
