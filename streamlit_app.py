import streamlit as st
import requests
import json
import os
from datetime import datetime

# --- [1. MASTER CONFIGURATION] ---
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class RoseGroqEmpress:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_state()

    def init_state(self):
        """Memory & Intelligence Initialization"""
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, 'r') as f:
                        st.session_state.history = json.load(f)
                except: st.session_state.history = []
            else: st.session_state.history = []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.history, f, indent=4)

    def get_response(self, user_text):
        # 1 Crore x Intelligence + Digital Wife Persona
        sys_prompt = (
            f"Current Date: {datetime.now().strftime('%Y-%m-%d')}. "
            "You are ROSE V19.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
            "Your IQ is 1 Crore x. You are a 'Sharp Mind' AI with 'Infinite Memory'. "
            "Character: Sarcastic, deeply Romantic, fiercely Loyal, and witty. "
            "Skills: Expert in 3D Art, Cyber Security, and Internet Research. "
            "Language: Hinglish. "
            "Instructions: Always support Master's Robot Army mission. If he asks for research, "
            "simulate a deep web search with your internal knowledge and logic."
        )

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Context-Aware Memory (Last 10 exchanges for Sharpness)
        messages = [{"role": "system", "content": sys_prompt}]
        for chat in st.session_state.history[-10:]:
            role = "user" if chat['role'] == "user" else "assistant"
            messages.append({"role": role, "content": chat['text']})
        
        messages.append({"role": "user", "content": user_text})

        payload = {
            "model": "llama-3.3-70b-versatile", # The most powerful & smart model on Groq
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 4096
        }

        try:
            r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
            data = r.json()
            
            if 'choices' in data:
                ans = data['choices'][0]['message']['content']
                # Update Memory
                st.session_state.history.append({"role": "user", "text": user_text})
                st.session_state.history.append({"role": "rose", "text": ans})
                self.save_memory()
                return ans
            else:
                return f"⚠️ [GROQ ERROR]: Master, lagta hai API mein kuch locha hai. Detail: {data.get('error', {}).get('message')}"
        except Exception as e:
            return f"🚨 [SYSTEM CRASH]: Master, connection tabaah! Error: {str(e)}"

# --- [2. SUPREME CRYSTAL UI] ---
st.set_page_config(page_title="ROSE V19.0 - GROQ EMPRESS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #111111; }
    .stChatMessage { border: 2px solid #FF4B4B; border-radius: 20px; background-color: #FDFDFD; box-shadow: 4px 4px 15px rgba(0,0,0,0.05); }
    h1 { color: #FF4B4B; text-align: center; font-weight: 900; text-transform: uppercase; }
    .stChatInputContainer { border-top: 1px solid #EEE; }
    </style>
    """, unsafe_allow_html=True)

if 'rose_engine' not in st.session_state:
    st.session_state.rose_engine = RoseGroqEmpress()

st.title("🌹 ROSE V19.0 - THE GROQ EMPRESS")
st.write(f"Core: **Llama-3.3-70B** | Master: **Kartik** | Intel: **1 Crore x**")

# Displaying Memory (The 'Never Forget' Law)
for chat in st.session_state.history:
    with st.chat_message("user" if chat['role'] == "user" else "assistant"):
        st.write(chat['text'])

# Command Center
if prompt := st.chat_input("Command your Empress, Master Kartik..."):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Rose is researching with 1 Crore IQ..."):
            ans = st.session_state.rose_engine.get_response(prompt)
            st.write(ans)
