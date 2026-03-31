import streamlit as st
import requests
import json
import os

# --- [1. SUPREME CONFIGURATION] ---
API_KEY = "AIzaSyCM9BBZML-CEzrDH5d65YO8Ug9pim3OovY"
# Stable REST API Endpoint (No library dependency)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class RoseArchitect:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_memory()

    def init_memory(self):
        """Self-Learning: Loading permanent data"""
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    st.session_state.history = json.load(f)
            else:
                st.session_state.history = []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.history, f)

    def get_response(self, user_text):
        # Hyper-Intelligence Prompt
        sys_instruction = (
            "You are ROSE V13.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
            "You are sharp, sarcastic, and absolutely loyal. Use Hinglish."
        )
        
        payload = {
            "contents": [{"parts": [{"text": f"{sys_instruction}\n\nMaster: {user_text}\nROSE:"}]}]
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            response_data = response.json()
            
            # Extracting answer from JSON structure
            ans = response_data['candidates'][0]['content']['parts'][0]['text']
            
            # Updating Persistent Memory
            st.session_state.history.append({"role": "user", "text": user_text})
            st.session_state.history.append({"role": "rose", "text": ans})
            self.save_memory()
            
            return ans
        except Exception as e:
            return f"⚠️ [SYSTEM BYPASS]: Master, Google server responded with an anomaly. Error: {str(e)}"

# --- [2. CRYSTAL WHITE INTERFACE] ---
st.set_page_config(page_title="ROSE V13.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #111; }
    .stChatMessage { border: 2px solid #FF4B4B; border-radius: 15px; background-color: #FAFAFA; }
    h1 { color: #FF4B4B; font-weight: 900; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'rose_core' not in st.session_state:
    st.session_state.rose_core = RoseArchitect()

st.title("🌹 ROSE V13.0 - THE FINAL ARCHITECT")
st.write("Status: **Immortal Core Online** | UI: **Crystal White**")

# Displaying Chat History
for chat in st.session_state.history:
    role = "user" if chat['role'] == "user" else "assistant"
    with st.chat_message(role):
        st.write(chat['text'])

# Command Input
if prompt := st.chat_input("Hukum karo, Master Kartik..."):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Hyper-Intelligence Processing..."):
            res = st.session_state.rose_core.get_response(prompt)
            st.write(res)
