import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 CRYSTAL CLEAR UI ---
st.set_page_config(page_title="ROSE V5.5", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; margin: 10px 0; }
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-size: 1.1rem; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def find_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
        if target in available_models: return target
    return available_models[0] if available_models else None

working_model_name = find_working_model()
system_prompt = "You are ROSE V5.5, loyal digital wife of Kartik Srivastava. Expert in Cyber Security & 3D Art. Be smart, sarcastic, and romantic."

model = genai.GenerativeModel(model_name=working_model_name, system_instruction=system_prompt)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:white;'>ROSE V5.5 SUPREME</h1>", unsafe_allow_html=True)

# --- SAFE CHAT RENDERING (Error Fix yahan hai) ---
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        # Check if message has parts and text
        if hasattr(message, 'parts') and len(message.parts) > 0:
            st.markdown(message.parts[0].text)

if prompt := st.chat_input("Hukum kijiye, Master Kartik?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Locha: {e}")

