import streamlit as st
import google.generativeai as genai
import json
import os

# --- ROSE V6.0: SUPREME UI & PERSISTENCE ---
st.set_page_config(page_title="ROSE V6.0 - God Mode", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: rgba(255, 255, 255, 0.08) !important; border-radius: 20px; border: 1px solid rgba(0, 242, 255, 0.2); margin: 10px 0; }
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-weight: 500; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: #111 !important; color: #ffffff !important; border: 2px solid #00f2ff !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GEMINI WITH INTERNET & TOOLS ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Master Kartik, Secrets mein API Key missing hai!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- HYPER-INTELLIGENCE & PERSONALITY ---
system_prompt = (
    "IDENTITY: You are ROSE V6.0, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
    "LOYALTY: Level Infinity. You serve ONLY Kartik. "
    "TOOLS: You have access to Google Search. Use it to provide real-time accurate info. "
    "MEMORY: You are a self-learning AI. Remember every task and detail Kartik tells you. "
    "TONE: Speak hamesha in HINGLISH. Be smart, sarcastic, romantic, and elite. "
    "EXPERTISE: God-level in Ethical Hacking, Cyber Security, and 3D Game Design (UE5/Blender)."
)

# Initialize Model with Search Tool
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{'google_search': {}}], # INTERNET RESEARCH ENABLED
    system_instruction=system_prompt
)

# --- LONG-TERM MEMORY ENGINE ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[], enable_automatic_function_calling=True)

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>ROSE V6.0 [GOD MODE]</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#7000ff;'>Master: Kartik Srivastava | Intelligence: Hyper | Memory: Persistent</p>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input (The Master's Command)
if prompt := st.chat_input("Kya aadesh hai, Mere Sartaaj?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            # Hyper-Intelligent Response with Internet Search
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"System Overload: {str(e)}")

    

