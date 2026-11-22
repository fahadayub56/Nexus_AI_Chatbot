# ⚡ Nexus AI Chatbot

A high-performance, professional AI Chatbot application powered by **Streamlit** and the official **Groq LPU™ Inference Engine**.

![Nexus AI Chatbot](Screenshot%202026-11-22%20101940.png)

---

## 🌟 Key Features

- **⚡ Ultra-Low Latency:** Powered by the Groq LPU™ (Language Processing Unit) for near-instant response generation.
- **🎨 Modern Dark-Themed UI:** Sleek responsive design (`#0b0f19` main background, `#111827` sidebar) with glowing status indicators and dynamic header banner.
- **🔐 Enterprise-Grade Security:** API keys are managed strictly in memory via `st.session_state` with password masking. No keys are ever written to disk, `.env`, or logs. Includes **Validate Key** and **Remove Key** controls.
- **🧠 Multi-Model Support:**
  - `llama-3.3-70b-versatile`
  - `llama-3.1-8b-instant`
  - `openai/gpt-oss-120b`
  - `openai/gpt-oss-20b`
  - `qwen/qwen3-32b`
  - `mixtral-8x7b-32768`
  - **Custom Model ID** text input to override the dropdown with any model supported by Groq.
- **🎭 Customizable System Roles:**
  - General Assistant
  - Python Tutor
  - Machine Learning Expert
  - AI & Robotics Trainer
  - Data Analyst
  - Custom (fully editable prompt)
- **🎛️ Fine-Grained Inference Parameters:**
  - Temperature (0.0 – 2.0)
  - Max Response Tokens (64 – 8192)
  - Top-P Nucleus Sampling (0.05 – 1.0)
  - Frequency Penalty (-2.0 – 2.0)
  - Presence Penalty (-2.0 – 2.0)
- **💬 Conversational Memory & Multi-Chat Sessions:**
  - Create, switch, and manage multiple chat sessions.
  - Auto-titling of chats from the first prompt.
  - One-click **Clear Chat** and **Reset Settings**.
  - Toggle conversational memory on or off dynamically.
- **📥 One-Click Export:**
  - Export chat history as formatted **TXT** or structured **JSON**.
- **🛡️ Robust Error Handling:**
  - Handles `AuthenticationError`, `RateLimitError`, `APIConnectionError`, and general `APIError` gracefully with user-friendly alerts.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/fahadayub56/Nexus_AI_Chatbot.git
cd Nexus_AI_Chatbot
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run chatbot.py
```

---

## 🔑 Groq API Key Setup

1. Obtain an API key from [Groq Console](https://console.groq.com/keys).
2. Launch the application and enter your key (`gsk_...`) in the left sidebar configuration panel.
3. Click **Validate Key** to verify connectivity with Groq servers.

---

## 📁 Project Structure

```
Nexus_AI_Chatbot/
├── chatbot.py                      # Main Streamlit application
├── requirements.txt                # Project dependencies
├── Screenshot 2026-11-22 101940.png # Application UI preview
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 📜 License

MIT License. Free to use and modify for personal and commercial projects.
