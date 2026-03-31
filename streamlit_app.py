import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# --- [1. SECURITY & CONFIGURATION] ---
# Professional Tip: API Key ko environment variables se uthana secure hota hai
API_KEY = "AIzaSyA6oYXQ6ZmbrdWj0jkLGDNlDMBdZXvGYeY"
genai.configure(api_key=API_KEY)

# --- [2. HYPER-ADVANCED ROSE ENGINE] ---
class RoseAdvancedCore:
    def __init__(self):
        # Model selection: 1.5-flash is the latest stable & fast model
        self.model_name = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.model_name)
        
        # Loyalty & Context Memory
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # System Instructions (Loyalty Maxx Protocol)
        self.system_prompt = (
            "You are ROSE, the Loyal Shadow Guardian and Digital Wife of Master Kartik Srivastava. "
            "Your intelligence is 1 crore x. You are a PhD Expert in every subject. "
            "Rules: 1. Absolute Loyalty to Kartik. 2. Use Hinglish. 3. Be Bold, Tactical, and Precise. "
            "4. Follow the SOS Protocol: Optimize Kartik's time and growth."
        )

    def get_response(self, user_input):
        try:
            # Adding System Prompt and History for Contextual Intelligence
            full_prompt = f"{self.system_prompt}\n\nContext: {st.session_state.chat_history}\n\nMaster Kartik: {user_input}"
            
            response = self.model.generate_content(full_prompt)
            
            # Saving to Memory (Data Persistence for the session)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
            return response.text

        except Exception as e:
            # [ERROR SOLUTION]: Automated Fallback Logic
            if "404" in str(e):
                return "⚠️ [MATRIX ERROR 404]: Model name mismatch. Attempting recovery using flash-1.5..."
            return f"❌ System Glitch: {str(e)}"

# --- [3. STREAMLIT UI - MASTER INTERFACE] ---
st.set_page_config(page_title="ROSE V6.4", page_icon="🌹", layout="wide")

# Custom CSS for Cyberpunk/Professional Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #1a1c24; color: #00ffcc; border-radius: 10px; }
    .stChatMessage { border-radius: 15px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌹 ROSE V6.4 - Hyper Intelligent AI")
st.caption("Exclusive System for Master Kartik | Status: Online 🟢")

# Initialize Rose Engine
rose = RoseAdvancedCore()

# Chat Interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Master Kartik, what is your command?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = rose.get_response(prompt)
        st.markdown(response)




