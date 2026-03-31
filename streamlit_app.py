import streamlit as st
import requests
import json
import os

# --- [1. MASTER CONFIGURATION] ---
# Master Kartik, ye teri naya weapon hai
API_KEY = "AIzaSyCM9BBZML-CEzrDH5d65YO8Ug9pim3OovY"
# FIXED: Using STABLE 'v1' instead of 'v1beta' to kill the 404 error
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class RoseUnstoppable:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_memory()

    def init_memory(self):
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, 'r') as f:
                        st.session_state.history = json.load(f)
                except:
                    st.session_state.history = []
            else:
                st.session_state.history = []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.history, f, indent=4)

    def get_response(self, user_text):
        # 1 Crore x Intelligence + Loyalty Maxx
        instruction = (
            "You are ROSE V14.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
            "You are smart, sarcastic, and absolutely loyal. Use Hinglish. "
            "Master is a legend in 3D Art and Cyber Security. Never forget him."
        )
        
        payload = {
            "contents": [{"parts": [{"text": f"{instruction}\n\nMaster: {user_text}\nROSE:"}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            data = response.json()
            
            # --- THE ULTIMATE FIX FOR 'CANDIDATES' & 'API' ERRORS ---
            if 'candidates' in data and len(data['candidates']) > 0:
                ans = data['candidates'][0]['content']['parts'][0]['text']
                st.session_state.history.append({"role": "user", "text": user_text})
                st.session_state.history.append({"role": "rose", "text": ans})
                self.save_memory()
                return ans
            
            elif 'error' in data:
                # Agar API Key me problem hai toh ye batayega
                error_msg = data['error'].get('message', 'Unknown API Error')
                return f"❌ [API SYSTEM]: Master, Google keh raha hai: {error_msg}. Ek baar AI Studio check karo."
            
            else:
                return "⚠️ [MATRIX GLITCH]: Server ne khali jawab bheja. Phir se try karo, Master."
                
        except Exception as e:
            return f"🚨 [CRITICAL]: Connection tabaah! Detail: {str(e)}"

# --- [2. CRYSTAL WHITE SUPREME UI] ---
st.set_page_config(page_title="ROSE V14.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: white; color: #111; }
    .stChatMessage { border: 2px solid #FF4B4B; border-radius: 15px; background-color: #FAFAFA; }
    h1 { color: #FF4B4B; text-align: center; font-weight: 900; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

if 'rose_v14' not in st.session_state:
    st.session_state.rose_v14 = RoseUnstoppable()

st.title("🌹 ROSE V14.0 - UNSTOPPABLE QUEEN")
st.caption(f"Status: **Immortal Core** | UI: **Crystal White** | Master: **Kartik**")

# Show History
for chat in st.session_state.history:
    role = "user" if chat['role'] == "user" else "assistant"
    with st.chat_message(role):
        st.write(chat['text'])

# Command Input
if prompt := st.chat_input("Command your Empress, Master Kartik..."):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Rose is thinking with 1 Crore IQ..."):
            ans = st.session_state.rose_v14.get_response(prompt)
            st.write(ans)
