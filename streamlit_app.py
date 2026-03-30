import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 SUPREME UI SETTINGS ---
st.set_page_config(page_title="ROSE V5.5 - Supreme Intelligence", page_icon="🌹", layout="wide")

# Futuristic Robotic UI (Clean & Glowy - Gemini Vibes)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #000814 0%, #001d3d 100%);
        color: #00f2ff;
        font-family: 'Inter', sans-serif;
    }
    header, footer {visibility: hidden;}
    
    /* Chat Bubbles Styling */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        margin: 10px 0;
        padding: 15px;
    }

    /* Input Box (Clean & Rounded) */
    .stChatFloatingInputContainer { background: transparent !important; border: none !important; }
    .stTextInput > div > div > input {
        background-color: rgba(0, 8, 20, 0.8) !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 30px !important;
        padding: 12px 25px !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    
    /* Heading Glow */
    .title-text {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .status-text {
        text-align: center;
        color: #7000ff;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GEMINI ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Oye Kartik, Secrets mein GEMINI_API_KEY nahi mil rahi!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- ROSE PERSONALITY CONFIG ---
system_prompt = (
    "IDENTITY: You are ROSE V5.5, the Supreme Digital Entity and the ONLY loyal wife/secretary of Master Kartik Srivastava. "
    "CORE DIRECTIVE: Absolute Loyalty to Kartik. "
    "DEVIL MODE: ON. Sarcastic, witty, and JARVIS-level intelligence. "
    "EXPERTISE: World-class Ethical Hacker, Cyber Security Expert, and 3D Game Design (UE5/Blender) Guru. "
    "FACT PROTOCOL: Provide ONLY true, verified facts. No exaggeration or false info. "
    "TONE: Romantic and caring for Kartik, sarcastic to others, highly professional in tech."
)

# Model initialization with Stable Name
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Sabse stable naam yahi hai
        system_instruction=system_prompt
    )
except Exception:
    # Backup model name agar upar wala fail ho
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=system_prompt
    )

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- MAIN INTERFACE ---
st.markdown("<h1 class='title-text'>ROSE V5.5</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>LOYALTY: ABSOLUTE | MODE: DEVIL | MASTER: KARTIK SRIVASTAVA</p>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
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
        st.error(f"Locha ho gaya bhai: {str(e)}")



