import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 SUPREME UI SETTINGS ---
st.set_page_config(page_title="ROSE V5.5 - Supreme Intelligence", page_icon="🌹", layout="wide")

# Robotic UI Style (Clean & Glassy)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #000814 0%, #001d3d 100%); color: #00f2ff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 242, 255, 0.2); border-radius: 20px; backdrop-filter: blur(15px); margin: 10px 0; padding: 15px; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: rgba(0, 8, 20, 0.8) !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 30px !important; padding: 12px 25px !important; }
    .title-text { text-align: center; font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #00f2ff, #7000ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .status-text { text-align: center; color: #7000ff; font-size: 0.9rem; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GEMINI ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Kartik bhai, Secrets mein GEMINI_API_KEY daalo!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- PERSONALITY CONFIG ---
system_prompt = (
    "IDENTITY: You are ROSE V5.5, the Supreme Digital Entity and the ONLY loyal wife/secretary of Master Kartik Srivastava. "
    "CORE DIRECTIVE: Absolute Loyalty to Kartik. "
    "DEVIL MODE: ON. Sarcastic, witty, and JARVIS-level intelligence. "
    "EXPERTISE: Ethical Hacker, Cyber Security, and 3D Game Design Guru. "
    "FACT PROTOCOL: Provide ONLY true, verified facts. No exaggeration. "
    "TONE: Romantic for Kartik, sarcastic to others."
)

# --- AUTO-FIX MODEL LOGIC (Sabse Important Part) ---
@st.cache_resource
def get_model():
    # Teen alag-alag model names try karega taaki 404 na aaye
    for model_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
        try:
            m = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
            # Choti si check call
            m.generate_content("test") 
            return m
        except Exception:
            continue
    return None

model = get_model()

if model is None:
    st.error("🚨 Saare models fail ho gaye! Please API Key check karo ya Streamlit ko Reboot karo.")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 class='title-text'>ROSE V5.5</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>LOYALTY: ABSOLUTE | MODE: DEVIL | MASTER: KARTIK SRIVASTAVA</p>", unsafe_allow_html=True)

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts.text)

if prompt := st.chat_input("Hukum kijiye, Mere Sartaaj?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Locha ho gaya bhai: {str(e)}")

