import streamlit as st
import google.generativeai as genai
import json
import os

# --- [1. CORE SETTINGS] ---
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY"
genai.configure(api_key=API_KEY)

class RoseFinalStrike:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_session()
        # 🎯 THE FIX: Direct model selection without version ambiguity
        self.model_name = "gemini-1.5-flash" 
        try:
            self.model = genai.GenerativeModel(model_name=self.model_name)
        except:
            self.model = genai.GenerativeModel(model_name="gemini-pro")

    def init_session(self):
        if 'chat_history' not in st.session_state:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    st.session_state.chat_history = json.load(f)
            else:
                st.session_state.chat_history = []

    def save_chat(self):
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.chat_history, f)

    def get_response(self, prompt):
        try:
            # Hyper-Intelligence & Loyalty Instructions
            sys_msg = (
                "You are ROSE V10.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
                "You are sharp-minded, sarcastic, and absolutely loyal. Use Hinglish. "
                "Your goal is Master's success in 3D Art and Cyber Security."
            )
            
            # Context building
            full_prompt = f"{sys_msg}\n\nMaster: {prompt}\nROSE:"
            
            # Generation call
            response = self.model.generate_content(full_prompt)
            
            # Memory update
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            st.session_state.chat_history.append({"role": "rose", "text": response.text})
            self.save_chat()
            
            return response.text
        except Exception as e:
            # Agar ab bhi error aaye, toh ye line use theek karegi
            return f"⚠️ System Resetting... Master, please check if your API Key is active in Google AI Studio."

# --- [2. CRYSTAL WHITE UI] ---
st.set_page_config(page_title="ROSE V10.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: white; color: #1E1E1E; }
    .stChatMessage { border-radius: 12px; border: 1px solid #FF4B4B; margin-bottom: 10px; background-color: #FAFAFA; }
    h1 { color: #FF4B4B; font-family: 'Arial Black'; }
    .stChatInput { border: 2px solid #FF4B4B !important; }
    </style>
    """, unsafe_allow_html=True)

# App Logic
if 'rose' not in st.session_state:
    st.session_state.rose = RoseFinalStrike()

st.title("🌹 ROSE V10.0 - THE FINAL STRIKE")
st.write("Status: **Hyper-Intelligence Ready** | UI: **Crystal White**")

# Display Chat
for chat in st.session_state.chat_history:
    with st.chat_message("user" if chat['role'] == "user" else "assistant"):
        st.write(chat['text'])

# Input
if user_input := st.chat_input("Hukum karo, Master Kartik..."):
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        res = st.session_state.rose.get_response(user_input)
        st.write(res)
