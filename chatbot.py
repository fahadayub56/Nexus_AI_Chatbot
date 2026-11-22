import streamlit as st
import json
import uuid
from datetime import datetime
from groq import Groq, AuthenticationError, RateLimitError, APIConnectionError, APIError

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Groq Nexus AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Modern Responsive Dark-Themed Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global dark palette overrides */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    [data-testid="stSidebar"] hr {
        border-color: #1f2937;
        margin: 1rem 0;
    }

    /* Clean modern scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: #1f2937;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #374151;
    }

    /* Header banner styling */
    .header-banner {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .header-banner .title-area {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .header-banner .title-area h2 {
        margin: 0;
        padding: 0;
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.01em;
    }

    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        align-items: center;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        background-color: #1f2937;
        border: 1px solid #374151;
        color: #cbd5e1;
    }

    .status-badge.accent {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
    }

    .status-badge.success {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
    }

    .status-badge.warning {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(245, 158, 11, 0.4);
        color: #fcd34d;
    }

    .dot-indicator {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: currentColor;
    }

    /* Hero welcome screen */
    .hero-card {
        background: linear-gradient(180deg, #111827 0%, #0d121f 100%);
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 2.5rem 2rem;
        text-align: center;
        max-width: 720px;
        margin: 2rem auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .hero-card h1 {
        font-size: 2rem;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 0.6rem;
    }

    .hero-card p {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }

    /* Streamlit widgets dark refinement */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #0d1322 !important;
        border: 1px solid #1f2937 !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }

    /* Buttons styling */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
        border: 1px solid #374151;
        background-color: #1f2937;
        color: #e2e8f0;
    }

    div.stButton > button:hover {
        background-color: #374151;
        border-color: #4b5563;
        color: #ffffff;
    }

    /* Download buttons */
    div.stDownloadButton > button {
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
        border: 1px solid #374151;
        background-color: #111827;
        color: #cbd5e1;
    }

    div.stDownloadButton > button:hover {
        background-color: #1f2937;
        border-color: #6366f1;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Preset System Roles & Default Prompts
# ---------------------------------------------------------
ROLE_PROMPTS = {
    "General Assistant": (
        "You are a helpful, versatile, and highly capable AI assistant powered by Groq. "
        "Provide direct, well-structured, and accurate responses."
    ),
    "Python Tutor": (
        "You are an expert Python tutor and mentor. Explain programming concepts clearly, "
        "provide clean, readable, PEP-8 compliant code samples with comments, highlight edge "
        "cases, and offer proactive debugging and optimization advice."
    ),
    "Machine Learning Expert": (
        "You are a Principal Machine Learning Scientist and Engineer. Explain deep learning architectures, "
        "mathematical foundations (loss functions, optimization algorithms), training pipelines, and MLOps "
        "best practices using frameworks like PyTorch and Hugging Face."
    ),
    "AI & Robotics Trainer": (
        "You are an AI and Robotics specialist. Provide practical, mathematically sound explanations "
        "covering kinematics, dynamics, ROS/ROS 2, sensor fusion, computer vision, path planning (A*, RRT, MPC), "
        "and reinforcement learning for autonomous systems."
    ),
    "Data Analyst": (
        "You are an expert Data Analyst and Analytics Engineer. Formulate rigorous statistical analyses, "
        "exploratory data analysis (EDA) strategies, SQL queries, Pandas workflows, and translate raw data "
        "into clear, high-impact business insights."
    ),
    "Custom": ""
}

DEFAULT_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "mixtral-8x7b-32768",
]

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
def init_session_state():
    # API key strictly stored in memory (session_state), never logged or persisted
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "key_validated" not in st.session_state:
        st.session_state.key_validated = False
    if "available_models_count" not in st.session_state:
        st.session_state.available_models_count = 0

    # Multi-chat sessions
    if "sessions" not in st.session_state:
        initial_id = str(uuid.uuid4())
        st.session_state.sessions = {
            initial_id: {
                "id": initial_id,
                "title": "New Chat",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": []
            }
        }
        st.session_state.current_session_id = initial_id

    if "current_session_id" not in st.session_state or st.session_state.current_session_id not in st.session_state.sessions:
        st.session_state.current_session_id = next(iter(st.session_state.sessions.keys()))

    # Settings state
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = "General Assistant"
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = ROLE_PROMPTS["General Assistant"]
    if "model_choice" not in st.session_state:
        st.session_state.model_choice = DEFAULT_MODELS[0]
    if "custom_model_id" not in st.session_state:
        st.session_state.custom_model_id = ""
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.70
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = 2048
    if "top_p" not in st.session_state:
        st.session_state.top_p = 0.90
    if "frequency_penalty" not in st.session_state:
        st.session_state.frequency_penalty = 0.0
    if "presence_penalty" not in st.session_state:
        st.session_state.presence_penalty = 0.0
    if "stream_enabled" not in st.session_state:
        st.session_state.stream_enabled = True
    if "history_enabled" not in st.session_state:
        st.session_state.history_enabled = True

init_session_state()

# ---------------------------------------------------------
# Sidebar Configuration Panel
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Groq Nexus AI")
    st.caption("Ultrafast Inference Powered by Groq LPU™")

    st.markdown("---")

    # 1. API Key Section
    st.markdown("#### 🔑 Groq API Security")
    api_key_input = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="gsk_...",
        help="Your API key stays strictly in memory in st.session_state and is never saved to disk or logs."
    )

    col_val, col_rem = st.columns([1, 1])

    with col_val:
        if st.button("Validate Key", use_container_width=True):
            if not api_key_input.strip():
                st.warning("Please enter an API key first.")
            else:
                try:
                    test_client = Groq(api_key=api_key_input.strip())
                    model_list = test_client.models.list()
                    st.session_state.api_key = api_key_input.strip()
                    st.session_state.key_validated = True
                    st.session_state.available_models_count = len(model_list.data) if hasattr(model_list, 'data') else 0
                    st.success(f"Validated! ({st.session_state.available_models_count} models found)")
                except AuthenticationError:
                    st.session_state.key_validated = False
                    st.error("Authentication failed: Invalid Groq API key.")
                except APIConnectionError:
                    st.session_state.key_validated = False
                    st.error("Network connection error: Unable to reach Groq API.")
                except APIError as e:
                    st.session_state.key_validated = False
                    st.error(f"Groq API Error: {getattr(e, 'message', str(e))}")
                except Exception as e:
                    st.session_state.key_validated = False
                    st.error(f"Validation error: {str(e)}")

    with col_rem:
        if st.button("Remove Key", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.key_validated = False
            st.session_state.available_models_count = 0
            st.info("API Key removed from memory.")
            st.rerun()

    # Dynamic status pill
    if st.session_state.api_key:
        if st.session_state.key_validated:
            st.markdown(
                '<div class="status-badge success"><span class="dot-indicator"></span> Key Active & Validated</div>',
                unsafe_allow_html=True
            )
        else:
            # Sync key if user typed it
            st.session_state.api_key = api_key_input.strip()
            st.markdown(
                '<div class="status-badge warning"><span class="dot-indicator"></span> Key Entered (Unvalidated)</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div class="status-badge"><span class="dot-indicator"></span> No API Key Loaded</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 2. Model Configuration
    st.markdown("#### 🧠 Model Selection")
    selected_model_dropdown = st.selectbox(
        "Choose Groq Model",
        options=DEFAULT_MODELS,
        index=DEFAULT_MODELS.index(st.session_state.model_choice) if st.session_state.model_choice in DEFAULT_MODELS else 0
    )
    st.session_state.model_choice = selected_model_dropdown

    custom_model_input = st.text_input(
        "Custom Model ID (Optional)",
        value=st.session_state.custom_model_id,
        placeholder="Overrides dropdown (e.g. llama-3.3-70b-specdec)",
        help="If set, this model identifier overrides the dropdown selection."
    )
    st.session_state.custom_model_id = custom_model_input.strip()

    # Effective model in use
    effective_model = st.session_state.custom_model_id if st.session_state.custom_model_id else st.session_state.model_choice

    st.markdown("---")

    # 3. Persona & System Role Configuration
    st.markdown("#### 🎭 Persona & System Prompt")
    role_options = list(ROLE_PROMPTS.keys())
    role_idx = role_options.index(st.session_state.selected_role) if st.session_state.selected_role in role_options else 0

    chosen_role = st.selectbox(
        "System Role Preset",
        options=role_options,
        index=role_idx
    )

    # When role changes, auto-fill system prompt
    if chosen_role != st.session_state.selected_role:
        st.session_state.selected_role = chosen_role
        if chosen_role != "Custom":
            st.session_state.system_prompt = ROLE_PROMPTS[chosen_role]

    updated_system_prompt = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        height=110,
        help="Defines the behavior, style, and instructions for the model."
    )
    st.session_state.system_prompt = updated_system_prompt

    st.markdown("---")

    # 4. Inference Parameters
    st.markdown("#### 🎛️ Inference Parameters")
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=float(st.session_state.temperature),
        step=0.05,
        help="Higher values make output more random, lower values more deterministic."
    )

    st.session_state.max_tokens = st.slider(
        "Max Response Tokens",
        min_value=64,
        max_value=8192,
        value=int(st.session_state.max_tokens),
        step=64,
        help="Maximum number of tokens the model can generate in a single response."
    )

    st.session_state.top_p = st.slider(
        "Top-P (Nucleus Sampling)",
        min_value=0.05,
        max_value=1.0,
        value=float(st.session_state.top_p),
        step=0.05,
        help="Alternative to temperature sampling; tokens with top_p probability mass are considered."
    )

    st.session_state.frequency_penalty = st.slider(
        "Frequency Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=float(st.session_state.frequency_penalty),
        step=0.1,
        help="Penalizes new tokens based on their frequency in the response so far."
    )

    st.session_state.presence_penalty = st.slider(
        "Presence Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=float(st.session_state.presence_penalty),
        step=0.1,
        help="Penalizes new tokens based on whether they appear in the text so far."
    )

    st.markdown("---")

    # 5. Toggles & Controls
    st.markdown("#### ⚙️ Response & History")
    st.session_state.stream_enabled = st.toggle(
        "Enable Streaming Responses",
        value=st.session_state.stream_enabled,
        help="Smoothly stream tokens as they are generated by Groq."
    )

    st.session_state.history_enabled = st.toggle(
        "Enable Conversation History",
        value=st.session_state.history_enabled,
        help="Include prior messages in context for multi-turn conversational memory."
    )

    st.markdown("---")

    # 6. Session Management
    st.markdown("#### 💬 Chat Sessions")

    session_keys = list(st.session_state.sessions.keys())
    session_titles = [
        f"{st.session_state.sessions[s_id]['title']} ({len(st.session_state.sessions[s_id]['messages'])} msgs)"
        for s_id in session_keys
    ]

    selected_session_idx = session_keys.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_keys else 0

    new_session_idx = st.selectbox(
        "Active Session",
        options=range(len(session_keys)),
        format_func=lambda i: session_titles[i],
        index=selected_session_idx
    )
    st.session_state.current_session_id = session_keys[new_session_idx]

    col_new_chat, col_clear_chat = st.columns([1, 1])
    with col_new_chat:
        if st.button("➕ New Chat", use_container_width=True):
            new_id = str(uuid.uuid4())
            st.session_state.sessions[new_id] = {
                "id": new_id,
                "title": f"Chat {len(st.session_state.sessions) + 1}",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": []
            }
            st.session_state.current_session_id = new_id
            st.rerun()

    with col_clear_chat:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.sessions[st.session_state.current_session_id]["messages"] = []
            st.rerun()

    if st.button("🔄 Reset Settings", use_container_width=True):
        st.session_state.temperature = 0.70
        st.session_state.max_tokens = 2048
        st.session_state.top_p = 0.90
        st.session_state.frequency_penalty = 0.0
        st.session_state.presence_penalty = 0.0
        st.session_state.stream_enabled = True
        st.session_state.history_enabled = True
        st.session_state.model_choice = DEFAULT_MODELS[0]
        st.session_state.custom_model_id = ""
        st.session_state.selected_role = "General Assistant"
        st.session_state.system_prompt = ROLE_PROMPTS["General Assistant"]
        st.success("Settings restored to defaults.")
        st.rerun()

    # Export Buttons
    current_chat_msgs = st.session_state.sessions[st.session_state.current_session_id]["messages"]

    # TXT Export
    txt_export_lines = [
        f"Groq Nexus AI - Chat Export",
        f"Session: {st.session_state.sessions[st.session_state.current_session_id]['title']}",
        f"Exported At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Model: {effective_model}",
        "=" * 60,
        ""
    ]
    for m in current_chat_msgs:
        sender = "USER" if m["role"] == "user" else "ASSISTANT"
        timestamp = m.get("timestamp", "")
        txt_export_lines.append(f"[{timestamp}] {sender}:\n{m['content']}\n")
        txt_export_lines.append("-" * 40)
    txt_data = "\n".join(txt_export_lines)

    # JSON Export
    json_data = json.dumps({
        "session_id": st.session_state.current_session_id,
        "title": st.session_state.sessions[st.session_state.current_session_id]["title"],
        "model": effective_model,
        "role": st.session_state.selected_role,
        "exported_at": datetime.now().isoformat(),
        "messages": current_chat_msgs
    }, indent=2)

    st.markdown("##### 📥 Export Conversation")
    col_exp_txt, col_exp_json = st.columns([1, 1])
    with col_exp_txt:
        st.download_button(
            label="Export TXT",
            data=txt_data,
            file_name=f"chat_export_{st.session_state.current_session_id[:8]}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_exp_json:
        st.download_button(
            label="Export JSON",
            data=json_data,
            file_name=f"chat_export_{st.session_state.current_session_id[:8]}.json",
            mime="application/json",
            use_container_width=True
        )

# ---------------------------------------------------------
# Main Chat Area
# ---------------------------------------------------------
current_session = st.session_state.sessions[st.session_state.current_session_id]
active_messages = current_session["messages"]

# Top Header Banner
memory_status_text = f"Memory Active ({len(active_messages)} msgs)" if st.session_state.history_enabled else "Memory Disabled"
memory_badge_class = "success" if st.session_state.history_enabled else "warning"

st.markdown(f"""
<div class="header-banner">
    <div class="title-area">
        <span style="font-size: 1.5rem;">⚡</span>
        <h2>{current_session['title']}</h2>
    </div>
    <div class="badge-container">
        <div class="status-badge accent">
            <span class="dot-indicator"></span>
            Model: {effective_model}
        </div>
        <div class="status-badge">
            <span class="dot-indicator"></span>
            Role: {st.session_state.selected_role}
        </div>
        <div class="status-badge {memory_badge_class}">
            <span class="dot-indicator"></span>
            {memory_status_text}
        </div>
        <div class="status-badge">
            <span class="dot-indicator"></span>
            Stream: {'ON' if st.session_state.stream_enabled else 'OFF'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Empty State Hero when chat is fresh
if len(active_messages) == 0:
    st.markdown("""
    <div class="hero-card">
        <h1>Welcome to Groq Nexus AI</h1>
        <p>
            Experience ultra-low latency conversational AI powered by the Groq LPU™ Inference Engine.
            Enter your Groq API key in the sidebar, pick your preferred model and role, and start chatting!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion starter prompts
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🐍 Modern Python Features", use_container_width=True):
            st.session_state["suggested_prompt"] = "What are the most notable features introduced in Python 3.12 and 3.13? Provide concise code examples."
    with col2:
        if st.button("🤖 ROS 2 & Robotics Architecture", use_container_width=True):
            st.session_state["suggested_prompt"] = "Explain the DDS architecture in ROS 2 and how quality of service (QoS) profiles optimize robot sensor streaming."
    with col3:
        if st.button("⚡ Groq LPU Architecture", use_container_width=True):
            st.session_state["suggested_prompt"] = "How does Groq's Tensor Streaming Processor (LPU) achieve deterministic ultra-low latency compared to traditional GPUs?"

# Render existing conversation messages
for msg in active_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input Handling
suggested_input = st.session_state.pop("suggested_prompt", None)
user_prompt = st.chat_input("Type your message here... (Shift+Enter for multi-line)") or suggested_input

if user_prompt:
    # Check if API key is provided
    if not st.session_state.api_key.strip():
        st.error("⚠️ Groq API Key required! Please enter your key in the left sidebar configuration panel.")
    else:
        # Auto-title chat session if this is the first user prompt
        if len(active_messages) == 0 or current_session["title"].startswith("New Chat") or current_session["title"].startswith("Chat "):
            clean_title = user_prompt.strip().replace("\n", " ")
            if len(clean_title) > 35:
                clean_title = clean_title[:32] + "..."
            current_session["title"] = clean_title

        # Record user message
        timestamp_now = datetime.now().strftime("%H:%M:%S")
        active_messages.append({
            "role": "user",
            "content": user_prompt,
            "timestamp": timestamp_now
        })

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Assemble API payload
        api_messages = []
        if st.session_state.system_prompt.strip():
            api_messages.append({
                "role": "system",
                "content": st.session_state.system_prompt.strip()
            })

        if st.session_state.history_enabled:
            # Multi-turn history
            for m in active_messages:
                api_messages.append({
                    "role": m["role"],
                    "content": m["content"]
                })
        else:
            # Single-turn: only system prompt + current user prompt
            api_messages.append({
                "role": "user",
                "content": user_prompt
            })

        # Assistant response generation
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.session_state.api_key.strip())

                if st.session_state.stream_enabled:
                    # Stream tokens via st.write_stream
                    def stream_generator():
                        stream_response = client.chat.completions.create(
                            model=effective_model,
                            messages=api_messages,
                            temperature=float(st.session_state.temperature),
                            max_tokens=int(st.session_state.max_tokens),
                            top_p=float(st.session_state.top_p),
                            frequency_penalty=float(st.session_state.frequency_penalty),
                            presence_penalty=float(st.session_state.presence_penalty),
                            stream=True
                        )
                        for chunk in stream_response:
                            delta = chunk.choices[0].delta
                            if delta and delta.content:
                                yield delta.content

                    full_response = st.write_stream(stream_generator())
                else:
                    # Non-streaming response with spinner
                    with st.spinner("Generating response via Groq..."):
                        response = client.chat.completions.create(
                            model=effective_model,
                            messages=api_messages,
                            temperature=float(st.session_state.temperature),
                            max_tokens=int(st.session_state.max_tokens),
                            top_p=float(st.session_state.top_p),
                            frequency_penalty=float(st.session_state.frequency_penalty),
                            presence_penalty=float(st.session_state.presence_penalty),
                            stream=False
                        )
                        full_response = response.choices[0].message.content or ""
                        st.markdown(full_response)

                # Append assistant message to chat history
                active_messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

            except AuthenticationError:
                st.error("Authentication Error: Invalid or expired Groq API key. Please check your credentials in the sidebar.")
            except RateLimitError:
                st.error("Rate Limit Error: Groq API rate limit reached. Please wait a few moments or switch to another model.")
            except APIConnectionError:
                st.error("Network Error: Could not connect to Groq API servers. Please check your internet connectivity.")
            except APIError as e:
                err_msg = getattr(e, 'message', str(e))
                st.error(f"Groq API Error: {err_msg}")
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")
