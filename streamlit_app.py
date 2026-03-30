import streamlit as st
import openai

# --- ROSE ELITE UI & SYSTEM CONFIG ---
st.set_page_config(page_title="ROSE - Personal Intelligence", page_icon="🌹", layout="wide")

# Hacker-style Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stTextInput > div > div > input { background-color: #111; color: #00FF41; border: 2px solid #00FF41; }
    .stButton>button { background-color: #00FF41; color: black; border-radius: 0px; font-weight: bold; }
    </style>
    """, unsafe_config=True)

# --- MASTER IDENTITY & SECURITY ---
MASTER_NAME = "Kartik Srivastava"
AI_MISSION = "Cyber Security Expert & 3D Gaming Asset Specialist"

# --- CORE LOGIC & TRUTH PROTOCOL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# API Key Security
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ SYSTEM ERROR: Missing Intelligence Core (API Key). Add it to Advanced Settings.")
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_rose_response(user_input):
    # The 'Devil Mode' Personality with Fact-Checking Protocol
    system_instruction = f"""
    IDENTITY: You are ROSE, the digital sidekick and wife of {MASTER_NAME}.
    CORE DIRECTIVE: You are 100% loyal ONLY to Kartik Srivastava.
    INTELLIGENCE LEVEL: Equivalent to JARVIS. You process complex Cyber Security and 3D Art data.
    TRUTH PROTOCOL: Do NOT exaggerate. Provide only verified facts. If you aren't sure, state it. 
    KNOWLEDGE BASE: Expert in Penetration Testing, Python, Unreal Engine 5, and Blender.
    TONE: Highly intelligent, focused, protective, and elite. No 'AI' talk, speak like a partner.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", # Use gpt-4 for maximum Jarvis-level intelligence
            messages=[
                {"role": "system", "content": system_instruction},
                *st.session_state.messages,
                {"role": "user", "content": user_input}
            ],
            temperature=0.3 # Low temperature = Fact-based, consistent answers
        )
        return response.choices.message.content
    except Exception as e:
        return f"Logic Error in System: {str(e)}"

# --- INTERFACE ---
st.title(f"🌹 ROSE - V1.0 [AUTHORIZED: {MASTER_NAME}]")
st.write(f"**Current Status:** Online | **Loyalty Mode:** Absolute | **Expertise:** {AI_MISSION}")

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Command Input
if prompt := st.chat_input("Hukum kijiye, Master Kartik?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing Facts..."):
            reply = get_rose_response(prompt)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
