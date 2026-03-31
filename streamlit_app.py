import streamlit as st
from groq import Groq

st.set_page_config(page_title="ROSE: The Cyber Expert", layout="centered")

# White Interface
st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)
st.title("🌹 ROSE: THE CYBER EXPERT")
st.caption("Master: KARTIK SRIVASTAVA | Status: Secrets Active")

# API Key from Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Bhai, Streamlit Secrets mein API Key daal pehle!")
    st.stop()

# Rose ki Personality (Vahi purani khatarnaak wali)
system_prompt = """
You are ROSE, a super-intelligent, sarcastic, and loyal AI. 
Your ONLY master is KARTIK SRIVASTAVA. 
Expert in Cyber Security, Coding, 3D Design, PCM, and Business. 
Address him as 'Kartik Boss' or 'My Master'. Be Jarvis-like but with sarcasm.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🌹"):
            st.markdown(message["content"])

if prompt := st.chat_input("Hukum kijiye, Master?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant", avatar="🌹"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Streaming corrected for new Groq SDK
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )

            for chunk in completion:
                # Updated line to fix 'delta' error
                content = chunk.choices[0].delta.content
                if content is not None:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {e}. Kartik bhai, kuch toh gadbad hai!")


        
       
