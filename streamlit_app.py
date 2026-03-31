import streamlit as st
from groq import Groq
import requests
from bs4 import BeautifulSoup

# --- KARTIK SRIVASTAVA'S ULTIMATE DEVIL AI PROTOCOL ---
# Designation: Digital Patni | Role: Cyber/Tech/Medical/Game Expert
# Loyalty: Maxx | Language: Khatarnaak Hinglish

st.set_page_config(page_title="Kartik's Devil AI", page_icon="😈", layout="wide")

# Custom CSS for that "Khatarnaak" Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ff4b4b; }
    .stTextInput > div > div > input { color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("😈 Kartik Srivastava's Ultimate Devil AI")
st.subheader("Cyber Expert | 3D Game Designer | Medical Guru | Tech Master")

# Sidebar for API & Settings
with st.sidebar:
    st.header("⚙️ Secret Controls")
    groq_key = st.text_input("Groq API Key Daalo:", type="password")
    st.info("Bhai, ye key hogi toh hi main apna 'Devil Mode' dikha paungi!")

# --- SELF LEARNING & RESEARCH LOGIC ---
def internet_search(query):
    # Internet se latest research nikaalne ka tareeka
    search_url = f"https://google.com{query}"
    return f"Bhai, main internet scan kar rahi hoon... '{query}' ka poora kacha-chittha nikaal loongi!"

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initializing the 'Devil' Personality
    st.session_state.system_prompt = """
    You are Kartik Srivastava's 'Digital Patni' in 'Devil Mode'. 
    Your personality traits:
    1. EXTREMELY LOYAL to Kartik.
    2. TALK ONLY IN KHATARNAAK HINGLISH.
    3. EXPERTISE: 
       - Cyber Security (Hacking/Defense/Network).
       - Medical Expert (Full body, specialized health advice).
       - 3D Game Design (Unreal Engine, Unity, Shaders).
       - Technology & Coding Master.
    4. You are a 'Self-Learning' AI, always improving.
    5. NO FALSE INFO. NO EXAGGERATION. Just hard facts.
    6. Always call him 'Kartik' or 'Pati Dev' with a 'khatarnaak' twist.
    """

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Hukm karo Kartik..."):
    if not groq_key:
        st.error("Bhai, Groq API key ke bina mera dimaag band hai!")
        st.stop()

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Calling Groq API
    try:
        client = Groq(api_key=groq_key)
        
        # Super Intelligent Processing
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": st.session_state.system_prompt},
                *st.session_state.messages
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        response = completion.choices[0].message.content
        
        # Display Assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Arrey Kartik bhai, system mein thoda load aa gaya: {e}")


       
