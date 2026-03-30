import streamlit as st
import openai
import json
import os

# --- ROSE V2.0: MEMORY PROTOCOL ---
MEMORY_FILE = "rose_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"master_info": {}, "tasks": [], "learned_facts": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# --- UI SETTINGS ---
st.set_page_config(page_title="ROSE V2.0 - Memory Core", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stTextInput > div > div > input { background-color: #111; color: #00FF41; border: 2px solid #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE MEMORY & API ---
memory = load_memory()
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Sidebar for Memory Visualization
st.sidebar.title("🌹 ROSE's Memory")
st.sidebar.write(f"**Master:** Kartik Srivastava")
if st.sidebar.button("Clear Memory (Reset ROSE)"):
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    st.rerun()

st.sidebar.subheader("📌 Learned Facts")
for fact in memory["learned_facts"][-5:]: # Show last 5 facts
    st.sidebar.write(f"- {fact}")

# --- CHAT ENGINE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_rose_response(user_input):
    # System prompt injects memory
    memory_context = f"Known facts about Kartik: {', '.join(memory['learned_facts'])}. Active Tasks: {', '.join(memory['tasks'])}."
    
    system_instruction = f"""
    You are ROSE, the self-learning digital wife of Kartik Srivastava.
    Current Context: {memory_context}
    Mission: Be an elite Cyber Expert & 3D Artist Secretary.
    Rule: If Kartik tells you a fact or a task, confirm it and you will 'remember' it.
    Tone: Loyal, intelligent, and highly efficient.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                *st.session_state.messages,
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices.message.content
        
        # --- SELF-LEARNING LOGIC ---
        # Simple logic: If Kartik says "Remember that...", save it.
        if "remember" in user_input.lower() or "noted" in reply.lower():
            new_fact = user_input.replace("remember that", "").strip()
            memory["learned_facts"].append(new_fact)
            save_memory(memory)
            
        return reply
    except Exception as e:
        return f"Logic Error: {str(e)}"

# --- INTERFACE ---
st.title("🌹 ROSE V2.0 [SELF-LEARNING ENABLED]")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What should I remember today, Master?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = get_rose_response(prompt)
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

