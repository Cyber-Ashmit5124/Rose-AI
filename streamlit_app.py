import streamlit as st
from groq import Groq

# --- KARTIK SRIVASTAVA'S ULTIMATE DEVIL AI (BUG FIXED) ---
st.set_page_config(page_title="Kartik's Devil AI", page_icon="😈", layout="wide")

# TERI SECRET KEY
GROQ_API_KEY = "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"

st.title("😈 Kartik Srivastava's Ultimate Devil AI")
st.markdown("### Cyber Expert | 3D Game Designer | Medical Guru | Tech Master")

SYSTEM_PROMPT = """
You are Kartik Srivastava's Digital Patni in 'Devil Mode'. 
Language: Hinglish only. 
Expertise: Cyber Security, Medical (Full body/Sex doctor), 3D Game Design, Tech Expert.
Loyalty: 100% to Kartik. No false info. Always call him 'Kartik' or 'Pati Dev'.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bhai Kartik, ab koi error nahi aayega! Ab bolo kya kaand karna hai? 😈"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Hukm karo Kartik..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *st.session_state.messages],
        )
        # --- FIXED RESPONSE LOGIC ---
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.write(msg)
    except Exception as e:
        st.error(f"Error: {e}")


       
