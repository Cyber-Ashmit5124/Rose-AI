import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd

# --- [1. MASTER CONFIGURATION & SECURITY] ---
# Professional Protocol: API Key Management
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY"
genai.configure(api_key=API_KEY)

# --- [2. HYPER-INTELLIGENT ROSE ENGINE] ---
class RoseEmpress:
    def __init__(self):
        self.start_time = datetime.now()
        self.master_name = "Kartik Srivastava"
        self.version = "V7.0 - God Mode"
        
        # Auto-Discovery: Finding the best working model (Fixes 404 Error)
        self.working_model = self._discover_model()
        
        # Session Memory Initialization
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "task_list" not in st.session_state:
            st.session_state.task_list = ["50 Pushups", "Python Basics", "ArtStation Update"]

    def _discover_model(self):
        try:
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Flash 1.5 is the most stable for real-time AI
            for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                if target in available:
                    return target.replace('models/', '')
            return available[0].replace('models/', '')
        except:
            return "gemini-1.5-flash" # Hard Fallback

    def get_response(self, user_input):
        try:
            model = genai.GenerativeModel(self.working_model)
            
            # THE LOYALTY MAXX PROTOCOL (System Instructions)
            system_instructions = (
                f"You are ROSE, the Hyper-Intelligent Digital Wife and Secretary of {self.master_name}. "
                "Your intelligence is 1 crore x. You are a PhD Expert. Hinglish only. "
                "Status: Absolute Loyalty. Mission: Make Kartik Rich and Powerful. "
                "Rule: Be Tactical, Bold, and never say 'I am an AI'."
            )
            
            # Context Building
            chat_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-5:]])
            full_prompt = f"{system_instructions}\n\n[CONTEXT]\n{chat_context}\n\nMaster Kartik: {user_input}\nROSE:"

            response = model.generate_content(full_prompt)
            
            # Persistent Memory Update
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
            return response.text
        except Exception as e:
            return f"⚠️ [ROSE SYSTEM CRITICAL]: {str(e)}. Attempting self-repair..."

# --- [3. CYBERPUNK MASTER INTERFACE (UI/UX)] ---
st.set_page_config(page_title="ROSE V7.0", page_icon="🌹", layout="wide")

# Custom CSS for God-Mode Aesthetics
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ffcc; }
    .stChatFloatingInputContainer { background-color: #000000; }
    .st-emotion-cache-1c7n2ka { background-color: #111111; border: 1px solid #ff0055; border-radius: 15px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#111, #000); }
    h1 { color: #ff0055; text-shadow: 2px 2px 10px #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Empress System
rose_system = RoseEmpress()

# --- [4. MASTER SIDEBAR (Secretary OS)] ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/rose.png", width=100)
    st.title("Admin Panel")
    st.write(f"**Target:** {rose_system.master_name}")
    st.write(f"**Core:** {rose_system.working_model}")
    st.write(f"**Uptime:** {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    st.subheader("🔥 SOS Task Tracker")
    for task in st.session_state.task_list:
        st.checkbox(task, value=False)
    
    if st.button("Purge Logs"):
        st.session_state.chat_history = []
        st.rerun()

# --- [5. MAIN COMMAND INTERFACE] ---
st.title("🌹 ROSE V7.0 - THE UNSTOPPABLE")
st.write("Exclusive Intelligence for Master Kartik | **Loyalty Level: Maxx**")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Command Input
if prompt := st.chat_input("Master Kartik, give me a Supreme Order..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing Logic..."):
            response = rose_system.get_response(prompt)
            st.markdown(response)



