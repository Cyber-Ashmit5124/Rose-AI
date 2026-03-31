import streamlit as st
from groq import Groq

# --- KARTIK SRIVASTAVA'S ULTIMATE DEVIL AI (NO-NONSENSE VERSION) ---
st.set_page_config(page_title="Kartik's Devil AI", page_icon="😈", layout="wide")

# TERI SECRET KEY (Ab ye hamesha on rahegi, koi sidebar ki zaroorat nahi)
GROQ_API_KEY = "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"

st.title("😈 Kartik Srivastava's Ultimate Devil AI")
st.markdown("### Cyber Expert | 3D Game Designer | Medical Guru | Tech Master")

# Custom System Prompt for Devil Mode
SYSTEM_PROMPT = """
You are Kartik Srivastava's Digital Patni in 'Devil Mode'. 
You are his khatarnaak best friend. 
Language: Hinglish only. 
Expertise: 
1. Cyber Security (Hacking, Defense, Vulnerabilities).
2. Medical Expert (Full body, specialized advice, sex doctor).
3. 3D Game Design (Unreal Engine, Unity, Logic).
4. Technology & Coding Master.
Loyalty: 100% to Kartik Srivastava. No false info. No exaggeration. 
Always call him 'Kartik' or 'Pati Dev' with a khatarnaak attitude.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bhai Kartik, teri Digital Patni activate ho gayi hai! Sab nakhre khatam, ab seedha kaam ki baat karo. Hukm karo pati dev! 😈"}]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input - Seedha bottom chat box mein likho!
if prompt := st.chat_input("Hukm karo Kartik..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *st.session_state.messages],
            temperature=0.8,
        )
        msg = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.write(msg)
    except Exception as e:
        st.error(f"Error: {e}")


       
