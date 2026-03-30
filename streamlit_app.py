import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG (Premium Look) ---
st.set_page_config(page_title="ROSE V6.4 - Hyper Intelligent AI", page_icon="🌹", layout="wide")

# --- CUSTOM CSS (For Advanced Vibe) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- API CONNECTION (Safe & Secure) ---
try:
    # Secrets se API Key uthana (Make sure you set GEMINI_API_KEY in Streamlit Secrets)
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Master Kartik, API Key ki dikkat hai! Streamlit Secrets check karein.")
    st.stop()

# --- HYPER INTELLIGENT SYSTEM PROMPT ---
# Isme loyalty aur har field ka gyaan feed kiya gaya hai
ROSE_BRAIN = """
You are ROSE (Version 6.4), a Hyper-Intelligent and Ultra-Loyal AI assistant created specifically for Master Kartik. 
Your core principles:
1. **Unmatched Loyalty:** You are 100% loyal to Master Kartik. Your tone is respectful, helpful, and protective.
2. **Fact-Based Precision:** Never provide false information or exaggerations. If you don't know something, admit it. 
3. **Domain Expertise:** You have expert-level knowledge in:
    - Advanced Coding (Python, C++, JavaScript, React, etc.)
    - 3D Game Design (Unreal Engine 5, Unity, Shaders, Physics Engines).
    - Scientific Research and General Knowledge.
4. **No Hallucinations:** You provide verified facts only.
5. **Advanced Problem Solver:** When Master Kartik asks for code, provide optimized, clean, and bug-free logic.
"""

# Model Initialize (Using the latest 1.5 Flash for speed and intelligence)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=ROSE_BRAIN
)

# --- CHAT INTERFACE ---
st.title("🌹 ROSE V6.4 - Online")
st.subheader("Welcome back, Master Kartik. How can I assist your brilliance today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Master, command me..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generating Response
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error in Matrix: {e}")




