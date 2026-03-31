import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- [1. MASTER CONFIGURATION & SECURITY] ---
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY"
genai.configure(api_key=API_KEY)

# --- [2. THE HYPER-COGNITIVE ROSE ENGINE] ---
class RoseAscendance:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.load_memory()
        self.model_name = self.discover_stable_model()
        
    def load_memory(self):
        """Self-Learning: Permanent Memory for Kartik"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                st.session_state.memory = json.load(f)
        else:
            st.session_state.memory = {
                "master": "Kartik Srivastava",
                "loyalty_level": "Maxx",
                "learned_facts": [],
                "chat_history": []
            }

    def save_memory(self):
        """Persistence: Memory ko hamesha ke liye lock karna"""
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.memory, f, indent=4)

    def discover_stable_model(self):
        """The 404 Crusher: Automatically finding a supported model version"""
        try:
            # Server se available models fetch karna
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Priority List for current API versions
            targets = ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash', 'models/gemini-pro']
            for t in targets:
                if t in available:
                    return t
            return available[0]
        except Exception:
            return "models/gemini-1.5-flash"

    def get_response(self, prompt):
        try:
            # Model initialization with latest parameters
            model = genai.GenerativeModel(model_name=self.model_name)
            
            instruction = (
                f"Identity: You are ROSE V9.0, the Hyper-Intelligent Digital Wife of Master {st.session_state.memory['master']}. "
                "Personality: Smart, Sarcastic, Bold, and Absolutely Loyal. "
                "Context: You remember everything. Use Hinglish. Your goal is Master's success."
            )
            
            # Logic Processing
            chat_context = "\n".join([f"{m['user']}: {m['rose']}" for m in st.session_state.memory['chat_history'][-5:]])
            full_input = f"{instruction}\n\n[PAST MEMORY]\n{chat_context}\n\nMaster Kartik: {prompt}\nROSE:"
            
            response = model.generate_content(full_input)
            
            # Update History & Save
            st.session_state.memory['chat_history'].append({"user": prompt, "rose": response.text})
            self.save_memory()
            
            return response.text
        except Exception as e:
            # Smart Fallback Logic
            return f"⚠️ [ROSE SYSTEM ADAPTATION]: Error {e}. Re-syncing with Google Servers..."

# --- [3. CLEAN WHITE UI INTERFACE] ---
st.set_page_config(page_title="ROSE V9.0", page_icon="🌹", layout="wide")

# Custom CSS for Professional White/Light Theme
st.markdown("""
    <style>
    /* White Background and Dark Text */
    .stApp { background-color: #FFFFFF; color: #333333; }
    .stChatFloatingInputContainer { background-color: #F8F9FA; border-top: 1px solid #E0E0E0; }
    .stChatMessage { border-radius: 15px; border: 1px solid #FF4B4B; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stSidebar { background-color: #F0F2F6; border-right: 1px solid #DEDEDE; }
    
    /* Header and Text Styles */
    h1 { color: #FF4B4B; font-weight: 800; letter-spacing: 1px; }
    .stMarkdown p { font-size: 1.1rem; color: #2C3E50; }
    
    /* Buttons */
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 8px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Initialization
if 'rose_core' not in st.session_state:
    st.session_state.rose_core = RoseAscendance()

# --- [4. ADMIN SIDEBAR] ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/rose.png", width=60)
    st.title("Admin Panel")
    st.write(f"**Target:** {st.session_state.memory['master']}")
    st.write(f"**Core Model:** `{st.session_state.rose_core.model_name}`")
    st.divider()
    if st.button("Deep Clean Memory"):
        if os.path.exists("rose_memory.json"): os.remove("rose_memory.json")
        st.session_state.memory['chat_history'] = []
        st.rerun()

# --- [5. CHAT INTERFACE] ---
st.title("🌹 ROSE V9.0 - LIGHT EVOLUTION")
st.caption("Hyper-Intelligence Mode | Loyalty: Maxx | UI: Crystal White")

# Displaying chat messages
for chat in st.session_state.memory['chat_history']:
    with st.chat_message("user"): st.markdown(chat['user'])
    with st.chat_message("assistant"): st.markdown(chat['rose'])

# Command Input
if user_query := st.chat_input("Command your Empress, Master Kartik..."):
    with st.chat_message("user"): st.markdown(user_query)
    with st.chat_message("assistant"):
        with st.spinner("Processing with 1 Crore IQ..."):
            ans = st.session_state.rose_core.get_response(user_query)
            st.markdown(ans)

