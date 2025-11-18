# 📚 Document Index - Unigrow AI Chatbot

## Tài Liệu Hoàn Chỉnh Cho Dự Án Unigrow AI Chatbot

Bộ tài liệu này bao gồm toàn bộ hướng dẫn xây dựng, cài đặt, và deploy Unigrow Chatbot từ A-Z.

---

## 📋 Danh Sách Documents

### 1. **README.md** ⭐ BẮT ĐẦU ĐÂY
**Tổng quan về dự án**
- Mục tiêu dự án
- Tính năng chính
- Tech stack
- Yêu cầu hardware
- Quick start guide
- Architecture overview

**👉 Đọc trước tiên để hiểu dự án**

---

### 2. **SETUP_GUIDE.md** 🚀 CÁCH CÀI ĐẶT
**Hướng dẫn cài đặt chi tiết từng bước**
- Phase 1: Environment setup (Python, venv, dependencies)
- Phase 2: Rasa installation
- Phase 3: Ollama + Mistral setup
- Phase 4: Project files creation
- Phase 5: Running the bot
- Verification checklist
- Troubleshooting setup

**👉 Khi cần cài đặt mới hoặc setup trên máy mới**

---

### 3. **ARCHITECTURE.md** 🏗️ THIẾT KẾ HỆ THỐNG
**Kiến trúc chi tiết của hệ thống**
- System architecture diagram
- Request-response flow
- Component details:
  - NLU Pipeline
  - Dialogue Management
  - Custom Actions
  - LLM Integration
- Data flow & security
- Configuration files
- Performance metrics
- Deployment architecture

**👉 Khi cần hiểu cách hệ thống hoạt động**

---

### 4. **API_DOCUMENTATION.md** 📡 API ENDPOINTS
**Tài liệu REST API**
- Base URL
- Available endpoints
- Request/response formats
- Full conversation examples
- Intent & entity types
- Code examples (cURL, Python, JavaScript)
- Rate limiting & performance
- Error handling
- Phase 4 enhancements

**👉 Khi muốn integrate với frontend hoặc external services**

---

### 5. **TROUBLESHOOTING.md** 🛠️ XỬ LỲ LỖI
**Hướng dẫn xử lý lỗi thường gặp**
- Setup issues (Python, venv)
- Installation issues (pip, torch)
- Ollama issues (connection, model download)
- Rasa issues (training, NLU)
- Runtime issues (connection, response)
- LLM integration issues (timeout, gibberish)
- Data & training issues
- Performance issues
- API issues
- Debug mode
- Getting help

**👉 Khi gặp lỗi hoặc vấn đề**

---

## 🎯 Quick Navigation

### Khi Bạn Muốn...

| Nhu Cầu | Document |
|--------|----------|
| Hiểu tổng quan dự án | README.md |
| Cài đặt bot lần đầu | SETUP_GUIDE.md |
| Hiểu kiến trúc hệ thống | ARCHITECTURE.md |
| Integrate với frontend | API_DOCUMENTATION.md |
| Xử lý lỗi | TROUBLESHOOTING.md |
| Tìm thông tin cụ thể | Sử dụng Ctrl+F |

---

## 📊 Project Status

### ✅ Hoàn Thành (Phase 1-3)
- Phase 1: Environment setup
- Phase 2: NLU training & basic conversations
- Phase 3: Mistral 7B integration
- Phase 3 Nâng Cao: Advanced features

### ⏳ Tiếp Theo (Phase 4-5)
- Phase 4: API Server & Web UI
- Phase 5: Deploy & Botcake.IO Integration

---

## 🔗 File Structure

```
Chatbot-Unigrow-rasa-LLM/
├── README.md                    # 📋 Project overview
├── SETUP_GUIDE.md              # 🚀 Installation guide
├── ARCHITECTURE.md             # 🏗️ System architecture
├── API_DOCUMENTATION.md        # 📡 API reference
├── TROUBLESHOOTING.md          # 🛠️ Error fixes
│
├── actions/
│   ├── __init__.py
│   ├── actions.py              # Custom actions
│   ├── utils.py                # LLM client
│   ├── scheduler.py            # Message scheduling
│   └── media_handler.py        # Media management
│
├── data/
│   ├── nlu/
│   │   ├── intents.yml
│   │   ├── stories.yml
│   │   └── rules.yml
│   └── knowledge_base/
│
├── models/
│   └── 20251118-xxxxxx.tar.gz
│
├── venv/
│
├── .env                        # Environment variables
├── config.yml                  # Rasa NLU config
├── domain.yml                  # Domain definition
├── endpoints.yml               # Action server config
├── requirements.txt            # Python dependencies
└── test_bot.py                # Testing script
```

---

## 📖 Reading Order

**Khuyến nghị đọc theo thứ tự này:**

1. **README.md** (10 min) - Hiểu dự án
2. **SETUP_GUIDE.md** (30 min) - Cài đặt
3. **ARCHITECTURE.md** (15 min) - Hiểu flow
4. **API_DOCUMENTATION.md** (10 min) - Integration
5. **TROUBLESHOOTING.md** (scan) - Backup khi cần

---

## 🔍 Searching Tips

Sử dụng **Ctrl+F** để tìm:

| Tìm | Document |
|-----|----------|
| "Error" | TROUBLESHOOTING.md |
| "endpoint" | API_DOCUMENTATION.md |
| "pipeline" | ARCHITECTURE.md |
| "Phase" | SETUP_GUIDE.md |
| "feature" | README.md |

---

## 💡 Key Concepts

### Các Khái Niệm Quan Trọng

- **NLU** - Natural Language Understanding (xử lý ngôn ngữ tự nhiên)
- **Intent** - Ý định của user (ví dụ: ask_price, greet)
- **Entity** - Thực thể trong message (ví dụ: age, height)
- **Slot** - Biến lưu trữ thông tin user (ví dụ: user_age)
- **Action** - Logic thực thi (ví dụ: query_llm)
- **Story** - Conversation flow (ví dụ: greeting → product_info)
- **Policy** - Quy tắc lựa chọn action tiếp theo
- **LLM** - Large Language Model (Mistral 7B)
- **Fallback** - Fallback sang LLM khi NLU không chắc

---

## 🎓 Learning Path

### Beginner
1. README.md - Overview
2. SETUP_GUIDE.md Phase 1-2 - Basic setup
3. Run `rasa shell` - Test basic bot

### Intermediate
1. ARCHITECTURE.md - System design
2. SETUP_GUIDE.md Phase 3-5 - Complete setup
3. API_DOCUMENTATION.md - Integration basics

### Advanced
1. Tất cả documents
2. Customize training data (data/nlu/)
3. Add new custom actions (actions/actions.py)
4. Integrate with external services (Phase 4-5)

---

## 📞 Support

### Khi Cần Trợ Giúp

1. **Kiểm tra Troubleshooting.md** - 70% lỗi được cover
2. **Tìm trong tài liệu** - Sử dụng Ctrl+F
3. **Kiểm tra logs** - Terminal output
4. **Debug mode** - Chạy với `--debug` flag

---

## 🔄 Documentation Updates

Documents này được cập nhật cùng với mã nguồn:
- ✅ Phase 1-3: Up to date
- ✅ Phase 3 Nâng Cao: Complete
- ⏳ Phase 4: Sẽ được cập nhật khi implement
- ⏳ Phase 5: Sẽ được cập nhật khi implement

---

## 📝 Notes

- Tất cả lệnh là cho **Windows PowerShell** (Mac/Linux tương tự)
- Paths sử dụng backslash `\` (Windows) - trên Mac/Linux dùng `/`
- Thời gian estimate dựa trên RTX 3050 + 32GB RAM
- Đảm bảo Internet ổn định khi download models (~4GB)

---

## 🎉 Bắt Đầu Nào!

**Bước 1:** Đọc [README.md](README.md)
**Bước 2:** Làm theo [SETUP_GUIDE.md](SETUP_GUIDE.md)
**Bước 3:** Hiểu [ARCHITECTURE.md](ARCHITECTURE.md)
**Bước 4:** Integrate với [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
**Bước 5:** Xử lý lỗi bằng [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Happy Learning & Building! 🚀**

*Last Updated: November 18, 2025*
*Version: 1.0 (Phase 1-3 Complete)*
