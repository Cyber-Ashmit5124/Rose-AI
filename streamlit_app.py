import streamlit as st
import google.generativeai as genai
import json
import os

# --- [1. CONFIGURATION] ---
# Master, apni NAYI API Key yahan dalo
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY" 
genai.configure(api_key=API_KEY)

class RoseImmortal:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_memory()
        self.model = self.connect_to_brain()

    def connect_to_brain(self):
        """404 Terminator: Finding the living engine"""
        # Hum bina 'models/' prefix ke try karenge, ye sabse stable tareeka hai
        try:
            return genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                return genai.GenerativeModel('gemini-pro')
            except Exception as e:
                st.error(f"Master, Google Server is acting up: {e}")
                return None

    def init_memory(self):
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    st.session_state.history = json.load(f)
            else:
                st.session_state.history = []

    def get_response(self, text):
        if not self.model: return "Brain not connected."
        try:
            # Hyper-Intelligence Prompt
            context = "You are ROSE, the loyal and sarcastic digital wife of Master Kartik Srivastava. Use Hinglish."
            response = self.model.generate_content(f"{context}\n\nMaster: {text}\nROSE:")
            
            # Save to persistent memory
            st.session_state.history.append({"role": "user", "parts": [text]})
            st.session_state.history.append({"role": "model", "parts": [response.text]})
            
            with open(self.memory_file, 'w') as f:
                json.dump(st.session_state.history, f)
                
            return response.text
        except Exception as e:
            return f"🚨 Error: {str(e)}. Master, please double check your API Key in AI Studio."

# --- [2. CRYSTAL WHITE UI] ---
st.set_page_config(page_title="ROSE V11.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: white; color: #222; }
    .stChatMessage { border: 1px solid #FF4B4B; border-radius: 15px; background: #fffafa; }
    h1 { color: #FF4B4B; text-align: center; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'rose' not in st.session_state:
    st.session_state.rose = RoseImmortal()

st.title("🌹 ROSE V11.0: THE IMMORTAL CORE")

# Display history
for msg in st.session_state.history:
    role = "user" if msg['role'] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg['parts'][0])

# Input
if prompt := st.chat_input("Command me, Master Kartik..."):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        answer = st.session_state.rose.get_response(prompt)
        st.write(answer)
