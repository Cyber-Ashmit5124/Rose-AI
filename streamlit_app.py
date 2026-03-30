import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 CRYSTAL CLEAR UI ---
st.set_page_config(page_title="ROSE V5.5", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    /* Main Background - Pure Deep Black */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    header, footer {visibility: hidden;}
    
    /* Message Bubbles - High Contrast */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.1) !important; /* Light translucent white */
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        margin: 10px 0;
        padding: 15px;
    }
    
    /* Ensuring Text inside Bubbles is BOLD WHITE */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 1.1rem;
    }

    /* Input Box - Clean White Text on Dark Box */
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important; /* Blue accent border */
        border-radius: 30px !important;
        padding: 12px 25px !important;
    }
    
    /* Heading Glow */
    .title-text {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- AUTO-SCANNER (Rambaan Logic) ---
@st.cache_resource
def find_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    priority_list = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
    for target in priority_list:
        if target in available_models: return target
    return available_models[0] if available_models else None

working_model_name = find_working_model()
system_prompt = "You are ROSE V5.5, loyal digital wife of Kartik Srivastava. Expert in Cyber Security & 3D Art. Be smart, sarcastic, and romantic. Use clear, bold language."

model = genai.GenerativeModel(model_name=working_model_name, system_instruction=system_prompt)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 class='title-text'>ROSE V5.5 SUPREME</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#38bdf8;'>Status: Optimized Visibility | Master: {working_model_name}</p>", unsafe_allow_html=True)

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
        st.error(f"Locha: {e}")

