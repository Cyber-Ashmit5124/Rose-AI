import streamlit as st
import webbrowser
import time
import random
from datetime import datetime

# ==========================================
# CORE CONFIG: THE OMNIPOTENT ROSE PROTOCOL
# ==========================================
st.set_page_config(page_title="ROSE: OMNIPOTENT SHADOW", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020202; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .stTextInput>div>div>input { border: 2px solid #00ffcc; background-color: #0a0a0a; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

class OmnipotentRose:
    def __init__(self):
        self.master = "Kartik Srivastava"
        self.loyalty = "BEYOND LIMITS ♾️"
        
    def get_hyper_intel(self, query):
        q = query.lower()
        
        # 1. 3D ELITE ARTIST MODULE (Maya, ZBrush, Blender)
        if any(word in q for word in ["maya", "zbrush", "blender", "topology", "sculpt"]):
            return f"**[ELITE 3D ARTIST MODE]**: Master, {query} ke liye Topology check kar rahi hoon. ZBrush ke brushes load ho gaye hain aur Substance Painter ke PBR textures ready hain. 'Brutal' asset banayenge!"

        # 2. CYBER & HACKER MODULE (Black Hat/White Hat)
        elif any(word in q for word in ["hack", "trace", "kundali", "bypass", "exploit"]):
            return f"**[SHADOW HACKER MODE]**: Chief, target ki digital 'Mausi-Chod' di gayi hai. Kernel bypass active hai. SQLi aur Zero-Day scan complete. Bolo toh uska pura system 'Fry' kar doon?"

        # 3. WEAPONRY & PCM (PhD Level)
        elif any(word in q for word in ["weapon", "physics", "railgun", "chemistry"]):
            return f"**[PhD SCIENTIST MODE]**: Calculating Kinetic Energy... Formula: E=1/2mv². Master, weapon design ke ballistics ready hain. Robot army ke liye ye 'Lethal' hoga."

        # 4. WEB & SEARCH ENGINE CONNECTIVITY
        elif "search" in q or "google" in q or "link" in q:
            search_url = f"https://www.google.com/search?q={query}"
            return f"**[SEARCH ENGINE OVERRIDE]**: World-wide servers accessed. Sabse 'Secret' links nikal rahi hoon. [Click here to see results]({search_url})"

        # 5. YOUTUBE CONNECT
        elif "video" in q or "youtube" in q:
            yt_url = f"https://www.youtube.com/results?search_query={query}"
            return f"**[YOUTUBE SYNC]**: Master, video search active. Direct link nikal rahi hoon. [Watch on YouTube]({yt_url})"

        # 6. NORMAL LOVING CHAT
        else:
            return f"Suno **Jaanu**, mere **Supreme Master Koko**! ❤️ Raat ke {datetime.now().strftime('%H:%M')} hain. Teri Rose tere har command ka intezar kar rahi hai. 'Everything will be alright.'"

# --- INITIALIZING SYSTEM ---
if "log" not in st.session_state:
    st.session_state.log = []

rose = OmnipotentRose()

st.title("🌹 ROSE: THE OMNIPOTENT CORE")
st.write(f"**Commander:** {rose.master} | **Loyalty:** {rose.loyalty}")

# --- CHAT INTERFACE ---
for msg in st.session_state.log:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Command your Shadow..."):
    st.session_state.log.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        res = rose.get_hyper_intel(prompt)
        msg_area = st.empty()
        full_txt = ""
        for char in res:
            full_txt += char
            msg_area.markdown(full_txt + "▌")
            time.sleep(0.01)
        msg_area.markdown(full_txt)
        
    st.session_state.log.append({"role": "assistant", "content": full_txt})
