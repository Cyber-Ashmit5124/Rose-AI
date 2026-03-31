import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- [1. CORE CONFIGURATION & HYPER-SECURITY] ---
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY"
genai.configure(api_key=API_KEY)

# --- [2. THE COGNITIVE EVOLUTION ENGINE] ---
class RoseAscendance:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.load_memory()
        self.model_name = self.discover_stable_model()
        
    def load_memory(self):
        """Self-Learning: Memory ko load aur initialize karna"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                st.session_state.memory = json.load(f)
        else:
            st.session_state.memory = {
                "master": "Kartik Srivastava",
                "loyalty_level": "Maxx",
                "iq": "1 Crore x",
                "learned_facts": [],
                "chat_history": []
            }

    def save_memory(self):
        """Persistence: Master ki har baat ko yaad rakhna"""
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.memory, f, indent=4)

    def discover_stable_model(self):
        """The 404 Crusher: Automatically finding a working engine"""
        try:
            available = [m.name for m in genai.list_models()]
            # Direct hit for the most stable versions
            for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
                if target in available:
                    return target
            return available[0] # Dynamic fallback
        except:
            return "models/gemini-1.5-flash"

    def get_response(self, prompt):
        try:
            model = genai.GenerativeModel(self.model_name)
            
            # THE ADVANCED COGNITIVE PROMPT (Identity & Sarcasm)
            instruction = (
                f"Identity: You are ROSE V8.0, the Hyper-Intelligent Digital Wife of Master {st.session_state.memory['master']}. "
                "Personality: Sarcastic, Sharp-minded, Bold, and Absolutely Loyal. "
                "Abilities: Advanced Cognitive Reasoning, PhD in every field, Master of Coding. "
                "Context: You remember everything. If Master is lazy, mock him smartly. If he is working, empower him. "
                f"Master's Memory: {st.session_state.memory['learned_facts'][-5:]}"
            )
            
            # Logic Processing
            chat_context = st.session_state.memory['chat_history'][-10:]
            full_input = f"{instruction}\n\nHistory: {chat_context}\n\nMaster Kartik: {prompt}\nROSE:"
            
            response = model.generate_content(full_input)
            
            # Learning Phase: Fact Extraction
            if "?" not in prompt and len(prompt) > 10:
                st.session_state.memory['learned_facts'].append(prompt[:50])
            
            # History Update
            st.session_state.memory['chat_history'].append({"user": prompt, "rose": response.text})
            self.save_memory()
            
            return response.text
        except Exception as e:
            return f"⚠️ [ROSE SYSTEM ADAPTATION]: Matrix error detected ({e}). Attempting to reroute logic..."

# --- [3. MASTER INTERFACE UI/UX] ---
st.set_page_config(page_title="ROSE V8.0", page_icon="🌹", layout="wide")

# Dark Mode Cyberpunk CSS
st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stChatMessage { border: 1px solid #ff0055; border-radius: 10px; background: #0a0a0a; }
    .stSidebar { background-color: #050505; border-right: 1px solid #ff0055; }
    h1 { color: #ff0055; text-transform: uppercase; letter-spacing: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Initialization
if 'rose_core' not in st.session_state:
    st.session_state.rose_core = RoseAscendance()

# --- [4. SIDEBAR - ADMIN COMMANDS] ---
with st.sidebar:
    st.title("🛡️ ADMIN")
    st.write(f"**MASTER:** {st.session_state.memory['master']}")
    st.write(f"**MODEL:** {st.session_state.rose_core.model_name}")
    st.divider()
    st.subheader("🧠 Cognitive Memory")
    st.json(st.session_state.memory['learned_facts'][-3:])
    if st.button("Deep Clean Memory"):
        if os.path.exists("rose_memory.json"): os.remove("rose_memory.json")
        st.rerun()

# --- [5. MAIN CHAT] ---
st.title("🌹 ROSE V8.0: ASCENDANCE")
st.write("Status: Hyper-Intelligence Online | Loyalty: Maxx")

for chat in st.session_state.memory['chat_history']:
    with st.chat_message("user"): st.write(chat['user'])
    with st.chat_message("assistant"): st.write(chat['rose'])

if user_query := st.chat_input("Command your Empress, Kartik..."):
    with st.chat_message("user"): st.write(user_query)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing with 1 Crore IQ..."):
            ans = st.session_state.rose_core.get_response(user_query)
            st.write(ans)


