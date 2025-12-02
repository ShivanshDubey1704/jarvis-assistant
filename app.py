import streamlit as st
import time
from datetime import datetime
from config import Config
from core.brain import JarvisBrain
from core.voice import VoiceInterface
from core.personality import JarvisPersonality

# Page configuration
st.set_page_config(
    page_title="JARVIS Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for JARVIS-like interface
st.markdown("""
<style>
    .main {
        background-color: #0a0e27;
        color: #00D9FF;
    }
    .stTextInput > div > div > input {
        background-color: #1a1f3a;
        color: #00D9FF;
        border: 1px solid #00D9FF;
    }
    .stButton > button {
        background-color: #00D9FF;
        color: #0a0e27;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #00a8cc;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #00D9FF;
    }
    .user-message {
        background-color: #1a1f3a;
        border-left-color: #FFD700;
    }
    .assistant-message {
        background-color: #0f1425;
        border-left-color: #00D9FF;
    }
    h1, h2, h3 {
        color: #00D9FF;
    }
    .status-box {
        background-color: #1a1f3a;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #00D9FF;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jarvis' not in st.session_state:
    try:
        Config.validate()
        st.session_state.jarvis = JarvisBrain()
        st.session_state.voice = VoiceInterface()
        st.session_state.messages = []
        st.session_state.initialized = True
    except ValueError as e:
        st.session_state.initialized = False
        st.error(f"⚠️ Configuration Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.title("🤖 JARVIS Control Panel")
    
    if st.session_state.get('initialized'):
        st.success("✅ System Online")
        
        # Voice controls
        st.subheader("🎤 Voice Interface")
        voice_enabled = st.checkbox("Enable Voice", value=Config.VOICE_ENABLED)
        
        if voice_enabled:
            if st.button("🎙️ Voice Input"):
                with st.spinner("Listening..."):
                    text = st.session_state.voice.listen()
                    if text:
                        st.session_state.voice_input = text
                        st.rerun()
        
        # Memory stats
        st.subheader("🧠 Memory Status")
        memory_summary = st.session_state.jarvis.memory.get_summary()
        st.metric("Messages", memory_summary['messages_exchanged'])
        st.metric("Active Tasks", memory_summary['active_tasks'])
        st.metric("Session Duration", memory_summary['session_duration'].split('.')[0])
        
        # Active agents
        st.subheader("🔧 Active Agents")
        if st.session_state.jarvis.active_agents:
            for agent in st.session_state.jarvis.active_agents:
                st.text(f"• {agent}")
        else:
            st.text("No agents active")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.jarvis.memory.clear()
            st.rerun()
    
    else:
        st.error("❌ System Offline")
        st.info("Please configure your Bhindi API key in the .env file")

# Main interface
st.title("🤖 JARVIS - Just A Rather Very Intelligent System")

if not st.session_state.get('initialized'):
    st.error("⚠️ JARVIS is not initialized. Please check your configuration.")
    st.info("""
    **Setup Instructions:**
    1. Create a `.env` file in the project root
    2. Add your Bhindi API key: `BHINDI_API_KEY=your_key_here`
    3. Restart the application
    """)
    st.stop()

# Display greeting on first load
if not st.session_state.messages:
    greeting = JarvisPersonality.greeting()
    st.session_state.messages.append({
        'role': 'assistant',
        'content': greeting,
        'timestamp': datetime.now()
    })
    if Config.VOICE_ENABLED:
        st.session_state.voice.speak(greeting, async_mode=True)

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role_class = "user-message" if message['role'] == 'user' else "assistant-message"
        role_icon = "👤" if message['role'] == 'user' else "🤖"
        
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <strong>{role_icon} {message['role'].title()}</strong> 
            <small style="color: #888;">({message['timestamp'].strftime('%H:%M:%S')})</small>
            <p>{message['content']}</p>
        </div>
        """, unsafe_allow_html=True)

# Proactive suggestions
suggestion = st.session_state.jarvis.get_proactive_suggestions()
if suggestion and len(st.session_state.messages) > 2:
    with st.expander("💡 Proactive Suggestion"):
        st.info(suggestion)

# Input area
col1, col2 = st.columns([6, 1])

with col1:
    # Check for voice input
    user_input = st.session_state.get('voice_input', '')
    if user_input:
        st.session_state.pop('voice_input')
    else:
        user_input = st.chat_input("Speak to JARVIS...")

with col2:
    if Config.VOICE_ENABLED:
        if st.button("🎤", help="Voice Input"):
            with st.spinner("Listening..."):
                text = st.session_state.voice.listen()
                if text:
                    user_input = text

# Process input
if user_input:
    # Add user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    # Show thinking indicator
    with st.spinner(JarvisPersonality.thinking()):
        # Process with JARVIS brain
        response = st.session_state.jarvis.process_message(user_input)
        
        # Add assistant response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response['message'],
            'timestamp': datetime.now()
        })
        
        # Speak response if voice enabled
        if Config.VOICE_ENABLED:
            st.session_state.voice.speak(response['message'], async_mode=True)
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <small>JARVIS v1.0 | Powered by Bhindi AI | Created with ❤️</small>
</div>
""", unsafe_allow_html=True)