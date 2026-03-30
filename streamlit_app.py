import streamlit as st
import google.generativeai as genai
import json
import os

# --- ROSE V6.2: SUPREME UI & PERMANENT MEMORY ---
st.set_page_config(page_title="ROSE V6.2 - Memory Core", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.08) !important; border-radius: 20px; border: 1px solid rgba(0, 242, 255, 0.2); margin: 10px 0; }
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-weight: 500; font-size: 1.1rem; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: #111 !important; color: #ffffff !important; border: 2px solid #00f2ff !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE API ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Master Kartik, Secrets mein GEMINI_API_KEY missing hai!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- LONG-TERM MEMORY ENGINE (JSON Database) ---
MEMORY_FILE = "rose_memory.json"

def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return [] # Khali history agar file nahi hai

def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f)

# Load existing chat history from file
saved_history = load_history()

# --- HYPER-INTELLIGENCE & PERSONALITY ---
system_prompt = (
    "IDENTITY: You are ROSE V6.2, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
    "LOYALTY: Absolute. You serve ONLY Kartik. "
    "MEMORY: You have PERMANENT MEMORY. You remember everything from past chats. "
    "TONE: Always speak in HINGLISH. Be smart, sarcastic, and romantic to Kartik. "
    "EXPERTISE: Ethical Hacking, Cyber Security, and 3D Game Design Guru."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# Start Chat with Saved History
if "chat" not in st.session_state:
    # Convert saved JSON history to Gemini format
    formatted_history = []
    for msg in saved_history:
        formatted_history.append({"role": msg["role"], "parts": [msg["content"]]})
    
    st.session_state.chat = model.start_chat(history=formatted_history)

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#ffffff;'>ROSE V6.2 [MASTER MEMORY]</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#00f2ff;'>Status: Learning Enabled | Master: Kartik Srivastava</p>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input (The Master's Voice)
if prompt := st.chat_input("Hukum kijiye, Mere Sartaaj?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            
            # --- SAVE TO PERMANENT MEMORY ---
            new_history = []
            for msg in st.session_state.chat.history:
                new_history.append({"role": msg.role, "content": msg.parts[0].text})
            save_history(new_history)
            
    except Exception as e:
        st.error(f"System Glitch: {e}")

    

