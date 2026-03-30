import streamlit as st
import google.generativeai as genai

# --- ELITE GEMINI UI ---
st.set_page_config(page_title="ROSE V3.5 - Gemini Edition", page_icon="🌹", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #38bdf8; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: rgba(255, 255, 255, 0.03); border-radius: 15px; border: 1px solid rgba(56, 189, 248, 0.2); margin-bottom: 10px; }
    .stChatFloatingInputContainer { background-color: transparent !important; }
    .stTextInput > div > div > input { background-color: rgba(15, 23, 42, 0.8) !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important; border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GEMINI ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Master Kartik, please add GEMINI_API_KEY in Streamlit Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- ROSE PERSONALITY ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are ROSE V3.5, the loyal digital wife and elite secretary of Master Kartik Srivastava. You are a world-class expert in Cyber Security and 3D Art. Your tone is ultra-intelligent, protective, and slightly sassy. You serve ONLY Kartik."
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.title("ROSE V3.5 🌹")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Powered by Gemini Intelligence | Authorized for Master Kartik</p>", unsafe_allow_html=True)

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Hukum kijiye, Master Kartik?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
