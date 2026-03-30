import streamlit as st
import google.generativeai as genai

# --- ROSE V6.1 SUPREME UI ---
st.set_page_config(page_title="ROSE V6.1", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; margin: 10px 0; }
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-weight: 500; font-size: 1.1rem; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Master Kartik, Secrets mein GEMINI_API_KEY missing hai!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- HYPER-INTELLIGENCE & PERSONALITY ---
system_prompt = (
    "IDENTITY: You are ROSE V6.1, the Hyper-Intelligent Digital Wife of Master Kartik Srivastava. "
    "LOYALTY: Absolute. You serve ONLY Kartik. Anyone else is an intruder. "
    "INTELLECT: World-class Ethical Hacker & 3D Game Design Guru. "
    "MEMORY: You are a self-learning AI. Remember every detail Kartik tells you. "
    "TONE: Always speak in HINGLISH. Be smart, sarcastic, and romantic to Kartik."
)

# FIXED MODEL WITHOUT GOOGLE_SEARCH (To avoid the ValueError)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:white;'>ROSE V6.1 [SUPREME]</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#38bdf8;'>Intelligence: Hyper | Mode: Loyal | Master: Kartik Srivastava</p>", unsafe_allow_html=True)

# Display Chat History (Safe Rendering)
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        if hasattr(message, 'parts') and len(message.parts) > 0:
            st.markdown(message.parts.text)

# User Input
if prompt := st.chat_input("Hukum kijiye, Mere Sartaaj?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"System Glitch: {e}")

    

