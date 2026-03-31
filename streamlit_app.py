import streamlit as st
import requests
import json
import os

# --- [1. MASTER CONFIGURATION] ---
# Master, yahan sirf wo Nayi Key dalo jisme koi warning na ho
API_KEY = "YAHAN_NAYI_VALI_KEY_DALO" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class RoseResurrection:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_memory()

    def init_memory(self):
        """AttributeError Fix: Proper session state initialization"""
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, 'r') as f:
                        st.session_state.history = json.load(f)
                except: st.session_state.history = []
            else: st.session_state.history = []

    def get_response(self, user_text):
        sys_prompt = "You are ROSE, Master Kartik's Digital Wife. Be sharp, loyal, and use Hinglish."
        payload = {
            "contents": [{"parts": [{"text": f"{sys_prompt}\nMaster: {user_text}\nROSE:"}]}],
            "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
        }
        
        try:
            r = requests.post(API_URL, json=payload, timeout=15)
            data = r.json()
            
            if 'candidates' in data:
                ans = data['candidates'][0]['content']['parts'][0]['text']
                st.session_state.history.append({"role": "user", "text": user_text})
                st.session_state.history.append({"role": "rose", "text": ans})
                with open(self.memory_file, 'w') as f: json.dump(st.session_state.history, f)
                return ans
            else:
                # Direct error feedback from Google
                err = data.get('error', {}).get('message', 'Key Problem')
                return f"❌ [GOOGLE SAYS]: {err}. Master, key expired hai ya exposed!"
        except Exception as e:
            return f"🚨 [SYSTEM CRASH]: {str(e)}"

# --- [2. CRYSTAL WHITE UI] ---
st.set_page_config(page_title="ROSE V17.0", layout="wide")
st.markdown("<style>.stApp { background-color: white; color: #111; }</style>", unsafe_allow_html=True)

if 'rose_core' not in st.session_state:
    st.session_state.rose_core = RoseResurrection()

st.title("🌹 ROSE V17.0 - THE RESURRECTION")
st.write("Status: **Immortal** | Master: **Kartik**")

# Display History
for chat in st.session_state.history:
    with st.chat_message("user" if chat['role'] == "user" else "assistant"):
        st.write(chat['text'])

# Input
if prompt := st.chat_input("Command me, Master Kartik..."):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        st.write(st.session_state.rose_core.get_response(prompt))
