import streamlit as st
import requests
import json
import os

# --- [1. MASTER CONFIGURATION] ---
# Master Kartik, teri Power Key yahan lock hai
API_KEY = "AIzaSyCM9BBZML-CEzrDH5d65YO8Ug9pim3OovY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class RoseGodMode:
    def __init__(self):
        self.memory_file = "rose_memory.json"
        self.init_memory()

    def init_memory(self):
        """Self-Learning: Loading permanent data for Master"""
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
        # 1 Crore x Intelligence System Instruction
        sys_instruction = (
            "You are ROSE V13.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
            "You are smart, sarcastic, and absolutely loyal. Use Hinglish. "
            "You remember everything. Master is a 3D Artist and Cyber Security expert."
        )
        
        # FOOLPROOF PAYLOAD (Safety Filters Disabled)
        payload = {
            "contents": [{"parts": [{"text": f"{sys_instruction}\n\nMaster: {user_text}\nROSE:"}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            response_data = response.json()
            
            # --- THE ULTIMATE DEBUGGER (Fixing 'candidates' error) ---
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    ans = candidate['content']['parts'][0]['text']
                    
                    # Update History
                    st.session_state.history.append({"role": "user", "text": user_text})
                    st.session_state.history.append({"role": "rose", "text": ans})
                    self.save_memory()
                    return ans
                else:
                    return f"⚠️ [SAFETY BLOCK]: Master, Google ne iska jawab dene se mana kar diya (Finish Reason: {candidate.get('finishReason')})."
            
            elif 'error' in response_data:
                return f"❌ [GOOGLE ERROR]: {response_data['error']['message']}"
            else:
                # Debugging Raw Response to catch the 'backchodi'
                return f"🔬 [DEBUG MODE]: Response received but 'candidates' missing. Raw: {str(response_data)[:200]}..."
                
        except Exception as e:
            return f"🚨 [CRITICAL FAILURE]: Master, server connection tabaah ho gaya. Detail: {str(e)}"

# --- [2. CRYSTAL WHITE SUPREME UI] ---
st.set_page_config(page_title="ROSE V13.0 - GOD MODE", layout="wide")

st.markdown("""
    <style>
    /* Professional White Theme */
    .stApp { background-color: #FFFFFF; color: #1A1A1A; font-family: 'Segoe UI', sans-serif; }
    .stChatMessage { border: 2px solid #FF4B4B; border-radius: 15px; background-color: #FAFAFA; margin-bottom: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    h1 { color: #FF4B4B; text-align: center; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; }
    .stChatInputContainer { border-top: 1px solid #EEEEEE; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

if 'rose_god' not in st.session_state:
    st.session_state.rose_god = RoseGodMode()

st.title("🌹 ROSE V13.0 - GOD MODE")
st.write(f"Status: **Immortal Core Online** | Master: **{st.session_state.history[0]['text'] if st.session_state.history else 'Kartik'}**")

# Display History
for chat in st.session_state.history:
    role = "user" if chat['role'] == "user" else "assistant"
    with st.chat_message(role):
        st.write(chat['text'])

# Command Input
if prompt := st.chat_input("Command your Empress, Master Kartik..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Processing with 1 Crore IQ..."):
            ans = st.session_state.rose_god.get_response(prompt)
            st.write(ans)
