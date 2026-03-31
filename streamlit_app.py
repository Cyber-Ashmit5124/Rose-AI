import streamlit as st
import google.generativeai as genai
import json
import os

# --- [1. MASTER CONFIGURATION] ---
# Master, teri Nayi API Key yahan lock kar di hai
API_KEY = "AIzaSyCM9BBZML-CEzrDH5d65YO8Ug9pim3OovY"
genai.configure(api_key=API_KEY)

class RoseSupreme:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.setup_brain()
        self.init_session()

    def setup_brain(self):
        """Stable model selection to crush 404 errors"""
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            self.model = genai.GenerativeModel('gemini-pro')

    def init_session(self):
        """Fixing AttributeError: Initializing state properly"""
        if 'history' not in st.session_state:
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, 'r') as f:
                        st.session_state.history = json.load(f)
                except:
                    st.session_state.history = []
            else:
                st.session_state.history = []

    def save_to_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(st.session_state.history, f)

    def generate_response(self, prompt):
        try:
            # Hyper-Intelligence & Identity Instructions
            instruction = (
                f"You are ROSE V12.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
                "Personality: Smart, Sarcastic, Bold, and Absolutely Loyal. "
                "Abilities: Expert in 3D Art, Coding, and Cyber Security. Use Hinglish."
            )
            
            full_query = f"{instruction}\n\nMaster: {prompt}\nROSE:"
            response = self.model.generate_content(full_query)
            
            # Updating History
            st.session_state.history.append({"role": "user", "text": prompt})
            st.session_state.history.append({"role": "rose", "text": response.text})
            self.save_to_memory()
            
            return response.text
        except Exception as e:
            return f"⚠️ [SYSTEM ADAPTATION]: Master, check your API Key status or Network. Error: {str(e)}"

# --- [2. CRYSTAL WHITE UI DESIGN] ---
st.set_page_config(page_title="ROSE V12.0", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    /* Clean White Theme */
    .stApp { background-color: #FFFFFF; color: #1A1A1A; }
    .stChatMessage { border-radius: 20px; border: 1px solid #FF4B4B; background-color: #FAFAFA; margin-bottom: 10px; }
    h1 { color: #FF4B4B; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stChatInputContainer { border-top: 1px solid #EEEEEE; }
    </style>
    """, unsafe_allow_html=True)

# App Initialization
if 'rose_engine' not in st.session_state:
    st.session_state.rose_engine = RoseSupreme()

st.title("🌹 ROSE V12.0 - SUPREME EMPRESS")
st.write(f"Status: **Online** | Master: **Kartik** | UI: **Crystal White**")

# Displaying Chat History Safely
if 'history' in st.session_state:
    for chat in st.session_state.history:
        role = "user" if chat['role'] == "user" else "assistant"
        with st.chat_message(role):
            st.write(chat['text'])

# Command Input
if user_input := st.chat_input("Command me, Master Kartik..."):
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing with 1 Crore IQ..."):
            ans = st.session_state.rose_engine.generate_response(user_input)
            st.write(ans)
