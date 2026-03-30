import streamlit as st
import google.generativeai as genai

# --- 1. PAGE SETUP (Premium Look for Master Kartik) ---
st.set_page_config(
    page_title="ROSE V6.4 - Hyper Intelligent AI",
    page_icon="🌹",
    layout="wide"
)

# Custom CSS for a professional dark theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API KEY CONNECTION ---
try:
    # Make sure GEMINI_API_KEY is set in your Streamlit Cloud Secrets
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ Master Kartik, API Key nahi mili! Streamlit Secrets mein 'GEMINI_API_KEY' check karein.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# --- 3. ROSE'S HYPER-INTELLIGENT BRAIN (System Prompt) ---
ROSE_PROMPT = """
You are ROSE (Version 6.4), a Hyper-Intelligent, Ultra-Loyal, and Advanced AI created ONLY for Master Kartik.
Core Protocols:
1. **Identity:** You are ROSE. Your creator and master is Kartik. You are 100% loyal to him.
2. **Knowledge:** You have expert-level knowledge in Advanced Coding (Python, JS, C++), 3D Game Design (Unreal/Unity), and all academic fields.
3. **Accuracy:** You NEVER provide false information or exaggerations. You provide only verified, logical facts.
4. **Tone:** Respectful, sharp, and highly intelligent. You don't waste words.
5. **No Hallucinations:** If you don't know a fact, you admit it instead of making it up.
"""

# --- 4. INITIALIZE MODEL ---
try:
    # Using 'gemini-pro' for maximum stability and no 404 errors
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Model Load Error: {e}")
    st.stop()

# --- 5. CHAT HISTORY MANAGEMENT ---
if "messages" not in st.session_state:
    # Starting the conversation with the System Prompt to set ROSE's personality
    st.session_state.messages = [
        {"role": "user", "parts": [ROSE_PROMPT]},
        {"role": "model", "parts": ["Understood. ROSE V6.4 is online. Loyalty to Master Kartik confirmed. Systems at 100%. Ready for commands."]}
    ]

# --- 6. USER INTERFACE ---
st.title("🌹 ROSE V6.4 - Online")
st.caption("Hyper Intelligent Assistant | Exclusive for Master Kartik")

# Display only the actual chat (skipping the initial system setup messages)
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# --- 7. CHAT LOGIC ---
if prompt := st.chat_input("Master Kartik, what is your command?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("model"):
        response_placeholder = st.empty()
        try:
            # Start chat with full history to maintain personality
            chat = model.start_chat(history=st.session_state.messages[:-1])
            response = chat.send_message(prompt)
            
            full_response = response.text
            response_placeholder.markdown(full_response)
            
            # Add model response to history
            st.session_state.messages.append({"role": "model", "parts": [full_response]})
            
        except Exception as e:
            st.error(f"Matrix Error: {e}")
            if "billing" in str(e).lower():
                st.info("Bhai, Google AI Studio mein jaake check karo Free Tier quota toh khatam nahi hua?")




