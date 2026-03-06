import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
    }

    /* User message bubble */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* AI message bubble */
    .ai-message {
        background: #f0f2f6;
        color: #1a1a2e;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    .stSidebar .stMarkdown, .stSidebar label {
        color: white !important;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }

    .metric-value {
        font-size: 2em;
        font-weight: bold;
    }

    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }

    /* Hide default footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Welcome message */
    .welcome-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(245, 87, 108, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative, Lower values = more focused"
    )

    # Max turns slider
    max_turns = st.slider(
        "Context Length",
        min_value=5,
        max_value=50,
        value=10,
        help="Number of conversation turns before warning"
    )

    st.divider()

    # Stats display
    st.markdown("### 📊 Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="margin: 5px 0;">
            <div class="metric-value">{st.session_state.message_count}</div>
            <div class="metric-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        turns = st.session_state.message_count // 2
        st.markdown(f"""
        <div class="metric-card" style="margin: 5px 0;">
            <div class="metric-value">{turns}/{max_turns}</div>
            <div class="metric-label">Turns</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # System prompt customization
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI Assistant",
        height=100,
        help="Customize the AI's personality and behavior"
    )

    st.divider()

    # Actions
    st.markdown("### 🛠️ Actions")

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.session_state.session_start = datetime.now()
        st.rerun()

    # Session info
    st.divider()
    st.markdown(f"""
    <div style="color: #888; font-size: 0.8em; text-align: center;">
        Session started: {st.session_state.session_start.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# Main chat area
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🤖 AI ChatBot</h1>
    <p style="color: rgba(255,255,255,0.8);">Powered by LangChain & Ollama</p>
</div>
""", unsafe_allow_html=True)

# Initialize the LLM
@st.cache_resource
def get_llm(model_name, temp):
    return ChatOllama(model=model_name, temperature=temp)

llm = get_llm("qwen2.5-coder:3b", temperature)

# Create the chain
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# Chat history display
chat_container = st.container()

with chat_container:
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div class="welcome-box">
            <h2>👋 Welcome!</h2>
            <p>I'm your AI assistant. Ask me anything!</p>
            <p style="font-size: 0.9em; opacity: 0.9;">
                💡 Try asking about programming, science, creative writing, or just chat!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>{msg.content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>AI:</strong><br>{msg.content}
                </div>
                """, unsafe_allow_html=True)

# Context warning
current_turns = len(st.session_state.chat_history) // 2
if current_turns >= max_turns - 2 and current_turns < max_turns:
    st.warning(f"⚠️ Only {max_turns - current_turns} turn(s) left before context is full!")
elif current_turns >= max_turns:
    st.error("🚫 Context window is full! Please clear history to continue.")

# Input area
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

user_input = st.text_input(
    "Message",
    placeholder="Type your message here...",
    label_visibility="collapsed",
    key="input"
)

if user_input:
    if current_turns >= max_turns:
        st.error("Context window is full! Please clear the chat history to continue.")
    else:
        try:
            with st.spinner("AI is thinking..."):
                response = chain.invoke({
                    "question": user_input,
                    "chat_history": st.session_state.chat_history
                })

            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=response))
            st.session_state.message_count += 2

            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
