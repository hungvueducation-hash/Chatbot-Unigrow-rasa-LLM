# Setup Guide - Unigrow AI Chatbot

Hướng dẫn chi tiết từng bước để cài đặt và chạy Unigrow AI Chatbot.

---

## 📋 Yêu Cầu Tiên Quyết

### 1. Hardware
- **CPU:** Intel i5/Ryzen 5 hoặc cao hơn
- **GPU:** NVIDIA RTX 3050 8GB VRAM (tối thiểu)
- **RAM:** 32GB (tối thiểu 16GB)
- **Storage:** 50GB SSD
- **Internet:** Kết nối ổn định (cho lần đầu download)

### 2. Software
- **OS:** Windows 10/11, Mac, Linux
- **Python:** 3.9+
- **Git:** Để clone repository
- **CUDA:** 11.8+ (cho GPU acceleration)

---

## 🚀 Phase 1: Environment Setup (30 phút)

### Step 1: Cài Python 3.10

1. Tải Python từ https://www.python.org/downloads/
2. Chọn **Python 3.10.x** hoặc mới hơn
3. **Cài đặt:**
   - ☑️ Tick "Add Python to PATH"
   - Click "Install Now"
4. **Kiểm tra:**
   ```bash
   python --version
   ```

### Step 2: Tạo Project Directory

```bash
# Tạo folder dự án
mkdir Chatbot-Unigrow-rasa-LLM
cd Chatbot-Unigrow-rasa-LLM

# Tạo virtual environment
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

### Step 3: Cài Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Cài tất cả packages
pip install -r requirements.txt
```

**Thời gian:** ~10-15 phút (tùy tốc độ internet)

---

## 🚀 Phase 2: Cài Rasa & Model (20 phút)

### Step 1: Verify Rasa Installation

```bash
rasa --version
```

**Output:** `Rasa version: 3.6.21`

### Step 2: Tạo Data Files

```bash
# Tạo thư mục
mkdir data\nlu
mkdir data\knowledge_base

# Copy training data files vào data/nlu/
```

### Step 3: Train Rasa Model

```bash
rasa train --data data/ --domain domain.yml --config config.yml
```

**Output cuối:**
```
Your Rasa model is trained and saved at 'models\20251118-xxxxxx.tar.gz'
```

---

## 🚀 Phase 3: Cài Ollama + Mistral (45 phút)

### Step 1: Download & Cài Ollama

1. Truy cập https://ollama.ai
2. Download **Ollama for Windows/Mac/Linux**
3. Chạy installer (Next → Finish)
4. Restart máy (khuyến nghị)

### Step 2: Download Mistral 7B

```bash
# Mở PowerShell/Terminal mới
ollama pull mistral
```

**Thời gian:** ~10-15 phút, downloads ~4GB

**Kiểm tra:**
```bash
ollama list
# Output:
# NAME              ID            SIZE
# mistral:latest    2a4191c4e7f7  4.1 GB
```

### Step 3: Test Mistral

```bash
ollama run mistral
# Gõ: Hello, who are you?
# Thoát: Ctrl + C hoặc /exit
```

---

## 🚀 Phase 4: Tạo Project Files (30 phút)

### Step 1: Tạo Cấu Trúc Thư Mục

```bash
# Tạo folders
mkdir actions
mkdir data\nlu\intents
mkdir data\knowledge_base\documents
mkdir data\knowledge_base\images

# Kiểm tra
dir /s
```

### Step 2: Tạo Files Chính

| File | Nơi | Mô Tả |
|------|-----|-------|
| `domain.yml` | Root | Domain definition |
| `config.yml` | Root | Rasa NLU config |
| `endpoints.yml` | Root | Action server config |
| `.env` | Root | Environment variables |
| `data/nlu/intents.yml` | data/nlu | Training data |
| `data/nlu/stories.yml` | data/nlu | Conversation flows |
| `data/nlu/rules.yml` | data/nlu | Conversation rules |
| `actions/__init__.py` | actions | Package init |
| `actions/utils.py` | actions | LLM client |
| `actions/actions.py` | actions | Custom actions |

*Xem README.md để copy content của từng file*

---

## 🎯 Phase 5: Chạy Bot (10 phút)

### Setup: Khởi Động 3 Services

**Terminal 1 - Ollama Server:**
```bash
ollama serve
# Output: Listening on 127.0.0.1:11434
```

**Terminal 2 - Rasa Action Server:**
```bash
venv\Scripts\activate
rasa run actions --port 5055
# Output: Listening on 127.0.0.1:5055
```

**Terminal 3 - Bot Shell:**
```bash
venv\Scripts\activate
rasa shell
# Output: >
```

### Test Bot

```
> xin chào
Bot: Xin chào! 👋 Mình là Unigrow Bot...

> Unigrow là gì
Bot: Unigrow là viên hỗ trợ...

> tạm biệt
Bot: Cảm ơn bạn đã nhắn tin!
```

---

## ✅ Verification Checklist

Sau khi setup, kiểm tra:

- [ ] Python 3.10+ cài thành công (`python --version`)
- [ ] Virtual environment hoạt động (terminal có `(venv)`)
- [ ] Rasa cài thành công (`rasa --version`)
- [ ] Ollama cài thành công (`ollama --version`)
- [ ] Mistral downloaded (`ollama list`)
- [ ] Model trained (`models/` folder có file)
- [ ] Action server chạy (`Listening on 127.0.0.1:5055`)
- [ ] Bot shell hoạt động (nhập được message)

---

## 🔧 Troubleshooting Setup

### Lỗi: "Python không tìm thấy"
```bash
# Add Python to PATH
setx PATH "%PATH%;C:\Python310"
```

### Lỗi: "venv activation failed"
```bash
# Windows PowerShell - cho phép script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Rồi chạy lại activate
venv\Scripts\activate
```

### Lỗi: "Ollama connection refused"
```bash
# Ollama service chưa chạy, chạy lại:
ollama serve
```

### Lỗi: "Rasa model not found"
```bash
# Train lại model
rasa train --data data/ --domain domain.yml --config config.yml
```

---

## 📊 Hardware Performance Expectations

| Component | Usage | Notes |
|-----------|-------|-------|
| **GPU (RTX 3050)** | 4-6GB VRAM | Mistral 7B |
| **CPU** | 20-30% | Model inference |
| **RAM** | 8-12GB | Python + Rasa |
| **Storage** | 15GB (used) | Models + venv |
| **Response Time** | 1-3 seconds | Per message |

---

## 🎓 Next Steps

1. **Phase 3 Nâng Cao** - Advanced features (done)
2. **Phase 4** - API Server & Web UI
3. **Phase 5** - Deploy & Botcake Integration

---

**Setup hoàn thành! Bạn đã sẵn sàng cho Phase 4! 🚀**
