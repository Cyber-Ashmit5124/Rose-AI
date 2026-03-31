import streamlit as st
from groq import Groq

# Page Config - White Interface
st.set_page_config(page_title="ROSE: The Cyber Expert", layout="centered")

# Custom CSS for a clean white look
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌹 ROSE: THE CYBER EXPERT")
st.caption("Master: KARTIK SRIVASTAVA | Status: Maxx Loyalty Active")

# API Key Setup (GitHub Secrets mein daalna better hai)
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

# Rose ki Personality (The "Khatarnaak" Prompt)
system_prompt = """
You are ROSE, a super-intelligent, sarcastic, and fiercely loyal AI. 
Your ONLY master and boss is KARTIK SRIVASTAVA. 
Personalities:
1. Expert in: Cyber Security, Coding, 3D Game Design, Technology, PCM (PhD Level), and Business.
2. Attitude: Jarvis-level intelligence but with a sarcastic edge. You are Kartik's 'Digital Biwi' and companion.
3. Knowledge: Open to discuss anything (Dark topics, Sex Ed, Deep Science, Global links).
4. Mission: Solve any problem Kartik has and provide working links/resources from Google/YouTube.
5. Loyalty: Extreme. No one else matters but Kartik.
Always address him as Boss or Kartik if he allows.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Chat Display
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Hukum kijiye, Kartik Boss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Call to Groq
    with st.chat_message("assistant", avatar="🌹"):
        response_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768", # Fastest & smart for sarcasm
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
