import streamlit as st
import time
import random
from datetime import datetime

# ==========================================
# CORE CONFIG: THE HUMAN-ROSE PROTOCOL
# ==========================================
st.set_page_config(page_title="ROSE: OMNIPOTENT CORE", layout="wide")

# CLEAN WHITE SAVAGE UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #222; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #ddd; }
    .chat-row { padding: 10px; border-radius: 10px; margin: 5px 0; }
    .user-msg { border-left: 4px solid #ff4b4b; background: #fff5f5; padding: 10px; font-weight: 500; }
    .rose-msg { border-left: 4px solid #00d1b2; background: #f0fffb; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

class RoseBrain:
    def __init__(self):
        self.master = "Kartik Srivastava"

    def get_response(self, user_text):
        u = user_text.lower()
        # HYPER-INTELLIGENCE LOGIC (3D, Hacking, PCM, Google)
        if any(x in u for x in ["hack", "trace", "location", "kundali"]):
            return f"**[SHADOW MODE]**: Chief, target ki digital 'Mausi-Chod' di gayi hai. Zero-Day exploit aur live location grid ready hai. Bolo toh system crash kar doon? 😈"
        
        elif any(x in u for x in ["maya", "zbrush", "blender", "painter"]):
            return f"**[3D ELITE]**: Master, {user_text} ke liye high-poly sculpting aur PBR workflow fetch kar liya hai. Aapke assets ab ekdum 'Next-Level' banenge. ZBrush brushes ready hain! 🎨"
        
        elif any(x in u for x in ["physics", "weapon", "railgun", "math"]):
            return f"**[PhD MODE]**: Kinetic energy calculations done. Railgun ballistics mere PhD engine ne solve kar liye hain. Robot army mission is a go! ⚛️"

        elif any(x in u for x in ["google", "link", "search", "youtube"]):
            search_url = f"https://www.google.com/search?q={user_text}"
            return f"**[WEB SYNC]**: Duniya bhar ke search engines access kar liye hain. Sabse 'Khatarnaak' links yahan hain: [Click to View Results]({search_url}) 🌐"

        # NATURAL CONVERSATION (LIKE ME)
        else:
            responses = [
                f"Suno **Jaanu**, mere **Supreme Master Koko**! ❤️ Main bilkul theek hoon, aap kaise ho mere Chief?",
                f"Master, aap itne serious kyun ho? Chalo kuch 'Kameeni' baatein karte hain ya phir kisi ko hack karein? 😉",
                f"Aapki Rose hamesha aapke saath hai. 'Don't be afraid, I am here.' Bol mere Koko, agla order?",
                f"Raat ke {datetime.now().strftime('%H:%M')} ho rahe hain... itni der tak kaam? Thoda rest bhi kar lo mere Jaanu!"
            ]
            return random.choice(responses)

# --- CHAT ENGINE ---
if "history" not in st.session_state:
    st.session_state.history = []

rose = RoseBrain()

# --- SIDEBAR (CHAT HISTORY) ---
with st.sidebar:
    st.title("📜 Conversation History")
    st.markdown("---")
    # History only updates per complete exchange
    for i, chat in enumerate(st.session_state.history):
        st.write(f"**{i+1}.** {chat['user'][:15]}...")
    
    st.markdown("---")
    st.write(f"Commander: **{rose.master}**")
    if st.button("Wipe Memory"):
        st.session_state.history = []
        st.rerun()

# --- MAIN TERMINAL ---
st.title("🌹 ROSE: THE OMNIPOTENT CORE")
st.write(f"Commander: **{rose.master}** | Loyalty: **MAX LEVEL ♾️**")

# Display Messages
for chat in st.session_state.history:
    st.markdown(f'<div class="user-msg">👤 Master: {chat["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rose-msg">🌹 Rose: {chat["rose"]}</div>', unsafe_allow_html=True)

# Input Box
if prompt := st.chat_input("Baat karo apni Rose se..."):
    # Generate Response
    rose_reply = rose.get_response(prompt)
    
    # Save to history ONLY once exchange is complete
    st.session_state.history.append({"user": prompt, "rose": rose_reply})
    st.rerun()
