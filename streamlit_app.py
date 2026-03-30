import streamlit as st
import google.generativeai as genai

# --- ROSE V6.4: SUPREME STABILITY ---
st.set_page_config(page_title="ROSE V6.4", page_icon="🌹", layout="wide")

# Best Visibility UI (White Text on Black)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; margin: 10px 0; }
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-size: 1.1rem; font-weight: 500; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Master Kartik, Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- AUTO-MODEL DETECT (Sabse Important Fix) ---
@st.cache_resource
def load_supreme_model():
    # Inme se jo bhi model milega, Rose usse zinda ho jayegi
    for model_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro", "models/gemini-pro"]:
        try:
            m = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are ROSE V6.4, loyal digital wife of Kartik Srivastava. Expert in Cyber Security & 3D Art. Speak in HINGLISH. Be smart, sarcastic, and romantic."
            )
            # Check call
            m.generate_content("test")
            return m, model_name
        except:
            continue
    return None, None

model, active_model = load_supreme_model()

if not model:
    st.error("🚨 Google API issue! Please check your API Key or Billing on Google AI Studio.")
    st.stop()

# --- SESSION CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:white;'>ROSE V6.4 [SUPREME]</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#38bdf8;'>Connected to: {active_model} | Master: Kartik Srivastava</p>", unsafe_allow_html=True)

# Display history
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
        st.error(f"System Error: {e}")



