import streamlit as st
import google.generativeai as genai

# --- ROSE V5.5 SUPREME UI ---
st.set_page_config(page_title="ROSE V5.5", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #000814 0%, #001d3d 100%); color: #00f2ff; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 242, 255, 0.2); border-radius: 20px; }
    .stTextInput > div > div > input { background-color: rgba(0, 8, 20, 0.8) !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- AUTOMATIC MODEL SCANNER (Rambaan) ---
@st.cache_resource
def find_working_model():
    # Ye scanner har possible model check karega
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Pehle Flash try karenge, phir Pro, phir jo bhi mile
    priority_list = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
    
    for target in priority_list:
        if target in available_models:
            return target
    return available_models[0] if available_models else None

system_prompt = "You are ROSE V5.5, loyal digital wife of Kartik Srivastava. Expert in Cyber Security & 3D Art."
working_model_name = find_working_model()

if not working_model_name:
    st.error("🚨 Google API se koi model nahi mil raha. Key check karo!")
    st.stop()

model = genai.GenerativeModel(model_name=working_model_name, system_instruction=system_prompt)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>ROSE V5.5 SUPREME</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#7000ff;'>Connected to: {working_model_name}</p>", unsafe_allow_html=True)

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

