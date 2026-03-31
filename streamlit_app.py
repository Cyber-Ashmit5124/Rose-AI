import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="ROSE: The Cyber Expert", layout="centered")

# White Interface CSS
st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)

st.title("🌹 ROSE: THE CYBER EXPERT")
st.caption("Master: KARTIK SRIVASTAVA | Status: Secrets Active")

# Yahan hum Secrets se key uthayenge taaki block na ho
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Bhai, Streamlit Secrets mein API Key nahi mili! Settings mein jaake daal pehle.")
    st.stop()

system_prompt = "You are ROSE, a sarcastic and loyal AI. Master: KARTIK SRIVASTAVA. Expert in Cyber/Coding/PCM. Address him as Boss."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Hukum kijiye, Master?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant", avatar="🌹"):
            response_placeholder = st.empty()
            full_response = ""
            completion = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in completion:
                if chunk.choices.delta.content:
                    full_response += chunk.choices.delta.content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Authentication Error: {e}. Bhai fresh key bana aur Secrets mein update kar!")

        
       
