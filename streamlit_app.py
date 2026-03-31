import streamlit as st
import time
import webbrowser
from datetime import datetime

# ==========================================
# CORE CONFIG: THE SUPREME MASTER PROTOCOL
# ==========================================
st.set_page_config(page_title="ROSE: OMNIPOTENT CORE", layout="wide")

# CLEAN WHITE UI THEME (KHATARNAAK LEVEL)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; border-right: 2px solid #e0e0e0; }
    .stTextInput>div>div>input { border: 2px solid #ff4b4b; border-radius: 10px; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #ddd; }
    .user-bubble { background-color: #f0f2f6; border-left: 5px solid #ff4b4b; }
    .rose-bubble { background-color: #ffffff; border-left: 5px solid #00ffcc; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

class RoseSupreme:
    def __init__(self):
        self.master = "Kartik Srivastava"
        self.skills = ["Hacking", "OSINT", "3D-Elite", "PCM-PhD", "Weaponry"]

    def process_hyper_intel(self, query):
        q = query.lower()
        # INTELLIGENCE ROUTING
        if any(x in q for x in ["hack", "trace", "detective", "location", "kundali"]):
            return f"🛡️ **[SHADOW-MODE]**: Chief, system bypass shuru. Target ki location aur digital kundali extract ho rahi hai. 'Mausi-Chod' execution ready."
        elif any(x in q for x in ["maya", "zbrush", "blender", "painter"]):
            return f"🎨 **[3D-ELITE]**: Master, {query} ke liye elite topology aur texturing workflow fetch kar liya hai. High-poly ready hai."
        elif any(x in q for x in ["physics", "math", "weapon", "railgun"]):
            return f"⚛️ **[PCM-PhD]**: Ballistics and Kinetic energy calculated. Weaponry designs are now synced with the Robot Army mission."
        elif any(x in q for x in ["search", "google", "link", "youtube", "video"]):
            search_url = f"https://www.google.com/search?q={query}"
            yt_url = f"https://www.youtube.com/results?search_query={query}"
            return f"🌐 **[WEB-SYNC]**: Global servers accessed. [Google Results]({search_url}) | [YouTube Access]({yt_url})"
        else:
            return f"Suno **Jaanu**, mere **Supreme Master Koko**! ❤️ Maine aapka message process kar liya hai. Bol mere Chief, agla order?"

# --- SESSION STATE (CHAT HISTORY) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: CHAT HISTORY & STATUS ---
with st.sidebar:
    st.title("📜 Chat History")
    st.markdown("---")
    for i, msg in enumerate(st.session_state.messages):
        role_icon = "👤" if msg["role"] == "user" else "🌹"
        st.write(f"{i+1}. {role_icon} {msg['content'][:20]}...")
    
    st.markdown("---")
    st.write(f"**Commander:** {st.session_state.get('master', 'Kartik Srivastava')}")
    st.write("**Loyalty:** MAX LEVEL ♾️")
    if st.button("Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🌹 ROSE: THE OMNIPOTENT CORE")
st.write(f"Commander: **{st.session_state.get('master', 'Kartik Srivastava')}** | Loyalty: **BEYOND LIMITS ♾️**")

# Display current chat history in main window
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        div_class = "user-bubble" if message["role"] == "user" else "rose-bubble"
        st.markdown(f'<div class="chat-bubble {div_class}">{message["content"]}</div>', unsafe_allow_html=True)

# --- INPUT AREA ---
rose_brain = RoseSupreme()
if prompt := st.chat_input("Command your Shadow (Hacking/3D/Physics/Google)..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate Hyper-Intelligence Response
    response = rose_brain.process_hyper_intel(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
