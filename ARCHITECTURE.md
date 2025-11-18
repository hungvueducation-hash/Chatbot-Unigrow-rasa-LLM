# Architecture - Unigrow AI Chatbot

Tài liệu chi tiết về kiến trúc hệ thống, flow, và các components của Unigrow Chatbot.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Web UI (Browser) │  │ WhatsApp    │  │ Command Line  │              │
│  │ (Frontend)   │  │ (via Botcake) │  │ (rasa shell) │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                      │
└─────────┼─────────────────┼──────────────────┼──────────────────────┘
          │                 │                  │
          └─────────────────┼──────────────────┘
                            │
           ┌────────────────▼────────────────┐
           │      HTTP/REST Interface        │
           │   (Flask/REST API - Port 5000) │
           └────────────────┬────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  Rasa Server    │ │ LLM Service  │ │ Action Server   │
│  (Port 5005)    │ │ (Mistral 7B) │ │ (Port 5055)     │
│                │ │ (Ollama)     │ │                  │
│ - NLU Pipeline │ │              │ │ - Custom Actions │
│ - Policy       │ │ - Generate   │ │ - Entity Extract │
│ - Dialogue Mgmt│ │ - Fallback   │ │ - Scheduling     │
└────────┬───────┘ └──────┬───────┘ └────────┬─────────┘
         │                │                  │
         └────────────────┼──────────────────┘
                          │
        ┌─────────────────┴──────────────────┐
        │                                    │
        ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│   Data Storage       │          │  Knowledge Base      │
│                      │          │                      │
│ - Training Data      │          │ - Documents (PDF)    │
│ - Trained Models     │          │ - Images             │
│ - Conversation Logs  │          │ - Scripts/FAQ        │
└──────────────────────┘          └──────────────────────┘
```

---

## 🔄 Request-Response Flow

```
User Input
    │
    ▼
┌─────────────────────────┐
│ 1. REST API Endpoint    │
│   (POST /webhooks/rest) │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────────┐
    │ 2. Message Parser  │
    │ (Tokenizer)        │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ 3. NLU Pipeline                │
    │ - Intent Classification        │
    │ - Entity Recognition           │
    │ - Sentiment Analysis           │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ 4. Policy & Dialogue Manager   │
    │ - Slot Filling                 │
    │ - Story Matching               │
    │ - Next Action Selection        │
    └────────┬───────────────────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │ 5. Action Execution             │
    │ (Custom Actions)                │
    │ - Extract Entities              │
    │ - Retrieve Info                 │
    │ - Update Slots                  │
    └────────┬────────────────────────┘
             │
        ┌────┴─────────────────┐
        │ High Confidence?     │
        └─┬───────────────┬────┘
          │ Yes          │ No
          ▼              ▼
    ┌──────────┐  ┌──────────────────┐
    │ Generate │  │ Query LLM        │
    │ Response │  │ (Mistral 7B)     │
    │ (Domain) │  │ for Fallback     │
    └────┬─────┘  └────────┬─────────┘
         │                 │
         └────────┬────────┘
                  │
                  ▼
        ┌──────────────────────┐
        │ 6. Response Formatter│
        │ - Add Context        │
        │ - Format Message     │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ 7. Send Response     │
        │ to User              │
        └──────────────────────┘
```

---

## 📊 Components Details

### 1. NLU Pipeline

**Purpose:** Xử lý user input, trích xuất intent & entities

**Pipeline Flow:**
```
Raw Text
   │
   ▼
WhitespaceTokenizer → Split text thành tokens
   │
   ▼
RegexFeaturizer → Trích xuất patterns
   │
   ▼
LexicalSyntacticFeaturizer → Ngữ pháp features
   │
   ▼
CountVectorsFeaturizer → Tạo word vectors
   │
   ▼
DIETClassifier → Intent & Entity classification
   │
   ▼
EntitySynonymMapper → Map entities to values
   │
   ▼
ResponseSelector → Select response template
```

### 2. Dialogue Management

**Purpose:** Quản lý conversation flow, lựa chọn action tiếp theo

**Components:**
- **MemoizationPolicy** - Nhớ exact conversations
- **RulePolicy** - Áp dụng rules cứng
- **TEDPolicy** - Tensor embedding dialogue

### 3. Custom Actions

**Purpose:** Thực thi logic phức tạp, gọi external services

**Types:**
- `action_extract_age_entity` - Trích tuổi
- `action_validate_height` - Validate chiều cao
- `action_query_llm_advanced` - Query Mistral LLM
- `action_provide_pricing_options` - Cung cấp giá

### 4. Mistral 7B Integration

**Purpose:** Fallback cho câu hỏi phức tạp

**Flow:**
```
User Question
   │
   ▼
Rasa NLU (confidence < threshold)
   │
   ▼ (Fallback triggered)
LLM Client (utils.py)
   │
   ▼
Ollama API (http://localhost:11434)
   │
   ▼
Mistral 7B Model
   │
   ▼
Generate Response
   │
   ▼
Format & Send to User
```

### 5. Data Storage

**Training Data:**
```
data/nlu/
├── intents.yml (10+ intents with examples)
├── stories.yml (conversation flows)
└── rules.yml   (hard rules)
```

**Models:**
```
models/
└── 20251118-xxxxxx.tar.gz (trained Rasa model)
```

**Knowledge Base:**
```
data/knowledge_base/
├── documents/  (Unigrow guides, FAQs)
├── images/     (product images)
└── scripts/    (training materials)
```

---

## 🔧 Configuration Files

### config.yml - NLU Configuration

```yaml
recipe: default.v1
language: vi

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
  - name: EntitySynonymMapper
  - name: ResponseSelector

policies:
  - name: MemoizationPolicy
  - name: RulePolicy
  - name: TEDPolicy
```

### domain.yml - Domain Definition

```yaml
intents:
  - greet
  - ask_unigrow_info
  - ask_price
  - ... (10+ intents)

entities:
  - age
  - current_height
  - target_height

slots:
  user_age: {type: text}
  user_height: {type: text}
  target_height: {type: text}

responses:
  utter_greet: {...}
  utter_unigrow_overview: {...}
  ... (20+ responses)

actions:
  - action_query_llm_advanced
  - action_get_product_recommendation
  - ... (12+ actions)
```

### endpoints.yml - Service Configuration

```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"

tracker_store:
  type: InMemoryTrackerStore

event_broker:
  type: InMemoryEventBroker
```

---

## 📈 Processing Performance

### Average Latencies

| Operation | Duration | Notes |
|-----------|----------|-------|
| **Input Parsing** | 50ms | Tokenization |
| **NLU Processing** | 200-300ms | Intent + Entity |
| **Policy Selection** | 100-150ms | Choose action |
| **Action Execution** | 300-500ms | Custom logic |
| **LLM Generation** | 2-3s | Mistral 7B |
| **Response Formatting** | 50ms | Template fill |
| **Total (NLU Path)** | 1-1.5s | Normal flow |
| **Total (LLM Path)** | 2.5-3.5s | Fallback flow |

### Resource Usage

| Component | Memory | CPU | GPU |
|-----------|--------|-----|-----|
| **Python Runtime** | 2GB | 5% | - |
| **Rasa Model** | 1.5GB | 15% | - |
| **Mistral 7B** | 6GB | 10% | 3-4GB |
| **Ollama Server** | 4GB | 5% | 4GB |
| **Total** | ~13.5GB | 35% | 7GB |

---

## 🔐 Data Flow Security

```
User Input
    │
    ▼ (Encrypted via HTTPS in production)
API Gateway
    │
    ▼ (Input validation)
NLU Pipeline (data not stored)
    │
    ▼ (Processing in memory)
Action Server (data processing)
    │
    ▼ (Logs only non-sensitive data)
Response Generation
    │
    ▼ (Encrypted response)
User Output
```

### Data Handling
- ✅ User messages processed in-memory only
- ✅ Slots stored in conversation context (not persisted by default)
- ✅ No sensitive data (credit cards, passwords) stored
- ✅ Logs only contain message intent & action (no raw text)

---

## 🚀 Scalability Considerations

### Current Setup (Single Machine)

- **Max concurrent users:** ~5-10 (due to GPU memory)
- **QPS (queries per second):** ~2-3
- **Daily messages:** ~5000-10000

### Future Scaling

**Horizontal Scaling:**
```
Load Balancer
    │
    ├─→ Rasa Server 1
    ├─→ Rasa Server 2
    ├─→ Rasa Server 3
    │
    └─→ Shared Services
        ├─ Redis (session cache)
        ├─ PostgreSQL (conversation logs)
        └─ Mistral API (cloud fallback)
```

---

## 📝 Integration Points

### 1. REST API
```
POST /webhooks/rest/webhook
  └─ Send: {sender, message}
  └─ Receive: [{text}]
```

### 2. Botcake.IO (Phase 5)
```
Botcake API
    │
    ▼ (Webhook)
Our API Server
    │
    ▼
Rasa Server
    │
    ▼
Botcake API (send response)
```

### 3. Database (Future)
```
PostgreSQL
    ├─ user_conversations (logs)
    ├─ user_profiles (persistent slots)
    └─ interaction_metrics
```

---

## 🔄 Conversation State Management

```
┌────────────────────────────────────┐
│    Conversation State               │
│                                    │
│ Slots:                             │
│  - user_age: "20"                 │
│  - user_height: "160cm"           │
│  - target_height: "170cm"         │
│                                    │
│ Context:                          │
│  - last_intent: "ask_price"      │
│  - confidence: 0.95              │
│  - entities: [age: 20, height: 160]│
│                                   │
│ History:                          │
│  - Message 1: "xin chào"         │
│  - Message 2: "Unigrow là gì"   │
│  - ... (up to 10 messages)       │
└────────────────────────────────────┘
```

---

## 🎯 Deployment Architecture (Phase 5)

```
┌─────────────────────────────────┐
│   Production Deployment         │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Load Balancer (Nginx)       │ │
│ └────────────┬────────────────┘ │
│              │                  │
│   ┌──────────┼──────────┐       │
│   │          │          │       │
│   ▼          ▼          ▼       │
│ ┌──┐      ┌──┐      ┌──┐       │
│ │RI│  RI  │RI│  RI  │RI│       │
│ │AS│      │AS│      │AS│  ...  │
│ │  │      │  │      │  │       │
│ └──┘      └──┘      └──┘       │
│   │          │          │       │
│   └──────────┼──────────┘       │
│              │                  │
│   ┌──────────┴──────────┐       │
│   │                     │       │
│   ▼                     ▼       │
│ ┌──────────────┐  ┌──────────┐ │
│ │ PostgreSQL   │  │ Redis    │ │
│ │ (Logs)       │  │ (Cache)  │ │
│ └──────────────┘  └──────────┘ │
│                                 │
│ Shared Services:                │
│ - Ollama Server (GPU)           │
│ - Mistral API (Fallback)        │
└─────────────────────────────────┘
```

---

**Architecture Documentation Hoàn Thành!** 🏗️
