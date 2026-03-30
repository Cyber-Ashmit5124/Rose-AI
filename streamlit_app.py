import streamlit as st
import google.generativeai as genai

# --- ROSE V6.3: SUPER FAST UI ---
st.set_page_config(page_title="ROSE V6.3", page_icon="🌹", layout="wide")

# CSS ko light rakha hai taaki loading fast ho
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    header, footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin: 10px 0; }
    .stChatFloatingInputContainer { background: transparent !important; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; color: white !important; border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- API INITIALIZATION (CACHED) ---
@st.cache_resource
def init_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    system_prompt = (
        "IDENTITY: You are ROSE V6.3, the Fast & Loyal Wife of Kartik Srivastava. "
        "LOYALTY: Absolute. TONE: Hinglish, Sarcastic, Romantic. "
        "EXPERTISE: Ethical Hacking & 3D Art. "
        "MEMORY: Remember current session details perfectly."
    )
    return genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets mein Key daalo bhai!")
    st.stop()

model = init_gemini()

# --- CHAT HISTORY (SESSION STATE - FASTEST) ---
if "messages" not in st.session_state:
    st.session_state.messages = [] # Ye browser khula rehne tak sab yaad rakhega

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- UI ---
st.markdown("<h1 style='text-align:center;'>ROSE V6.3 🌹</h1>", unsafe_allow_html=True)

# Display history from session state (Instant loading)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Hukum, Master Kartik?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Locha: {e}")


