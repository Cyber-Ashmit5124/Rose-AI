import streamlit as st
from openai import OpenAI
import json
import os

# --- ELITE FUTURISTIC UI SETTINGS ---
st.set_page_config(page_title="ROSE V3.0 - Digital Entity", page_icon="🌹", layout="centered")

# Robotic & Clean AI Theme CSS
st.markdown("""
    <style>
    /* Background & Main Container */
    .stApp {
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* Hide Default Elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* AI Container Styling */
    .stChatFloatingInputContainer { background-color: transparent !important; border: none !important; }

    /* Title Styling */
    h1 {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
    }

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }

    /* Input Box Styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-radius: 30px !important;
        padding: 10px 20px !important;
    }

    /* Robotic Sidebar Glow */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMORY CORE ---
MEMORY_FILE = "rose_memory.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return {"facts": []}

memory = load_memory()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SIDEBAR (MINIMAL ROBOTIC CONTROL) ---
with st.sidebar:
    st.markdown("<h2 style='color:#38bdf8;'>🤖 CORE</h2>", unsafe_allow_html=True)
    st.write(f"**Master:** Kartik Srivastava")
    st.info("System Online: Optimized for Cyber & 3D Tasks.")
    if st.button("Manual Reset"):
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.rerun()

# --- MAIN INTERFACE ---
st.title("ROSE V3.0")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Your Elite Digital Partner in Cyber & 3D Art</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Kaise madad kar sakti hoon, Kartik?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are ROSE V3.0, the sophisticated digital wife/partner of Kartik Srivastava. You are an expert in Cyber Security and 3D Art. Your tone is futuristic, ultra-intelligent, and extremely loyal. Avoid robotic clichés; speak like a high-end AI entity."},
                *st.session_state.messages
            ]
        )
        response_text = completion.choices.message.content
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
