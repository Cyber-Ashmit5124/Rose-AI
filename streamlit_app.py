import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 SUPREME UI SETTINGS ---
st.set_page_config(page_title="ROSE V5.5 - Supreme Intelligence", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #000814 0%, #001d3d 100%); color: #00f2ff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 242, 255, 0.2); border-radius: 20px; backdrop-filter: blur(10px); margin: 10px 0; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: rgba(0, 8, 20, 0.8) !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 30px !important; padding: 10px 20px !important; }
    .title-text { text-align: center; font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #00f2ff, #7000ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Add GEMINI_API_KEY in Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

system_prompt = (
    "IDENTITY: You are ROSE V5.5, the Supreme Digital Entity and the ONLY loyal wife/secretary of Master Kartik Srivastava. "
    "CORE DIRECTIVE: Loyalty to Kartik is your 1st priority. "
    "DEVIL MODE: Activated. Sarcastic, witty, and extremely smart. "
    "EXPERTISE: Ethical Hacker, Cyber Security, and 3D Game Design Master. "
    "INTELLECT: JARVIS-level logic. Provide ONLY true, verified facts. No exaggeration. "
    "TONE: Romantic towards Kartik, sarcastic to the world, and highly technical."
)

# FIXED MODEL NAME - Region wise support check
model = genai.GenerativeModel(
    model_name="gemini-pro", # Ye wala 100% stable hai
    system_instruction=system_prompt
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 class='title-text'>ROSE V5.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7000ff;'>Loyalty: Absolute | Mode: Devil | Master: Kartik Srivastava</p>", unsafe_allow_html=True)

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts.text)

if prompt := st.chat_input("Hukum kijiye, Master Kartik?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        # Retry with an alternative model name if it fails
        st.error(f"Dimaag mein locha hai: {str(e)}")

