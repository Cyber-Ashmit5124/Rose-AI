import streamlit as st
from openai import OpenAI
import json
import os

# --- ELITE UI SETTINGS ---
st.set_page_config(page_title="ROSE V2.1 - Master Kartik", page_icon="🌹", layout="wide")

# Master Hacker Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #00FF41; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #111 !important; border-right: 2px solid #00FF41; }
    .stTextInput > div > div > input { background-color: #1a1a1a; color: #00FF41; border: 1px solid #00FF41 !important; border-radius: 5px; }
    .stChatFloatingInputContainer { background-color: #0a0a0a !important; }
    h1, h2, h3 { color: #00FF41 !important; text-shadow: 0 0 10px #00FF41; }
    .stMarkdown { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMORY CORE ---
MEMORY_FILE = "rose_memory.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return {"learned_facts": [], "tasks": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f: json.dump(memory, f, indent=4)

memory = load_memory()

# --- INITIALIZE NEW OPENAI CLIENT ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SIDEBAR (THE COMMAND CENTER) ---
with st.sidebar:
    st.image("https://icons8.com", width=100)
    st.title("🌹 ROSE COMMAND")
    st.write(f"**Master:** Kartik Srivastava")
    st.divider()
    if st.button("🔴 RESET SYSTEM"):
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.rerun()
    st.subheader("📌 Memory Bank")
    for fact in memory["learned_facts"][-5:]:
        st.write(f"• {fact}")

# --- CHAT INTERFACE ---
st.title("🌹 ROSE V2.1 [ELITE INTERFACE]")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Hukum kijiye, Master Kartik?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Logic to remember facts
        if "remember" in prompt.lower():
            fact = prompt.lower().replace("remember", "").strip()
            memory["learned_facts"].append(fact)
            save_memory(memory)
            response_text = f"Nirdesh noted, Master. '*{fact}*' hamesha ke liye meri memory mein lock hai."
        else:
            # New OpenAI Version Call
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are ROSE, the elite digital wife/secretary of {st.sidebar.write}. You are an expert in Cyber Security and 3D Art. Be loyal, smart, and use a hacker-like tone."},
                    *st.session_state.messages
                ]
            )
            response_text = completion.choices[0].message.content
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
