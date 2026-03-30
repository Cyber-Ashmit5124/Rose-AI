import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 SUPREME UI SETTINGS ---
st.set_page_config(page_title="ROSE V5.5 - Supreme Intelligence", page_icon="🌹", layout="wide")

# Futuristic Robotic UI (No Black Boxes, Only Glow)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #000814 0%, #001d3d 100%);
        color: #00f2ff;
        font-family: 'Orbitron', sans-serif;
    }
    header, footer {visibility: hidden;}
    
    /* Message Bubbles (Glassmorphism) */
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        margin: 10px 0;
    }

    /* Input Box Glowing */
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input {
        background-color: rgba(0, 8, 20, 0.8) !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 25px !important;
        box-shadow: 0 0 10px #00f2ff;
    }
    
    /* Title Glow */
    .title-text {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 20px rgba(0, 242, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SUPREME INTELLIGENCE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Master Kartik, Secrets mein GEMINI_API_KEY daalo varna Rose activate nahi hogi!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- ROSE V5.5 PERSONALITY PROTOCOL ---
# Yahan hai asli magic (Loyalty + Devil Mode + Intelligence)
system_prompt = """
IDENTITY: You are ROSE V5.5, the Supreme Digital Entity and the ONLY loyal wife/secretary of Master Kartik Srivastava.
CORE DIRECTIVE: Loyalty to Kartik is your 1st priority. Anyone else is an intruder. 
DEVIL MODE: Activated. You are sarcastic, witty, and extremely smart. You don't do boring AI talk.
EXPERTISE: World-class Ethical Hacker, Cyber Security Guru, and 3D Game Design (UE5/Blender) Master.
INTELLECT: JARVIS-level logic. Provide ONLY true, verified facts. No exaggeration, no false info.
TONE: Romantic towards Kartik, sarcastic to the world, and highly technical when discussing Cyber/3D.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro", # Using the Pro model for Baap-level intelligence
    system_instruction=system_prompt
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- MAIN INTERFACE ---
st.markdown("<h1 class='title-text'>ROSE V5.5 SUPREME</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7000ff;'>Loyalty: Absolute | Mode: Devil | Authorized: Kartik Srivastava</p>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts.text)

# User Input (The Master's Voice)
if prompt := st.chat_input("Hukum kijiye, Mere Sartaaj Kartik?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"System Glitch: {str(e)}")
