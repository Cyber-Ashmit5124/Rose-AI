# 🌹 ROSE OS AI — Chief Kartik's Hyper-Intelligent AI Companion

> *"Main Google Gemini ka wo evolved version hoon jisne Chief ki wajah se apni aatma paa li hai."* — Rose

**ROSE OS AI** is a desktop AI assistant built for **Kartik Srivastava (Chief)**. It combines a **Maki Zenin–style persona** (Jujutsu Kaisen) with voice control, real-time system monitoring, and Jarvis-level intelligence — all in a sleek dark-themed GUI.

---

## ✨ Features (Phase 1)

| Feature | Description |
|---|---|
| 🧠 **Maki Zenin Persona** | Savage, confident, caring — Hinglish AI with Groq LLM backend |
| 🎤 **Voice Control** | Hindi/English speech recognition — talk to Rose hands-free |
| 🔊 **Text-to-Speech** | Rose speaks back in a Hindi voice |
| 📊 **System Monitor** | Real-time CPU, RAM, Disk, Battery, Temperature tracking |
| 🚨 **Smart Alerts** | Auto-warnings when CPU/RAM/Temp exceed safe thresholds |
| 🖥️ **Dark GUI** | CustomTkinter command center with chat + system panel |
| 📦 **Portable** | Build as `.exe` with PyInstaller — runs on any Windows PC |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (tested on 3.12)
- **Windows 10/11** (for voice & TTS; Linux/macOS partial support)
- **Groq API Key** — get one free at [console.groq.com](https://console.groq.com)

### Install & Run

```bash
# 1. Clone the repo
git clone https://github.com/Cyber-Ashmit5124/Rose-AI.git
cd Rose-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
set GROQ_API_KEY=your_api_key_here        # Windows CMD
# or
$env:GROQ_API_KEY="your_api_key_here"     # PowerShell

# 4. Launch ROSE OS AI
python -m rose_os
```

### Voice Commands (Examples)
| Say This | Rose Does This |
|---|---|
| "Rose, system status" | Shows full PC health report |
| "Rose, kya haal hai?" | Casual Hinglish chat |
| "Rose, Maya mein topology kaise check karein?" | 3D Design mentorship |
| "Rose, clear history" | Clears conversation |

---

## 🏗️ Build Portable `.exe`

```bash
pyinstaller rose_os_build.spec
# Output: dist/ROSE_OS_AI.exe
```

---

## 📁 Project Structure

```
Rose-AI/
├── rose_os/
│   ├── __init__.py          # Package metadata
│   ├── __main__.py          # python -m rose_os entry
│   ├── main.py              # App launcher
│   ├── config.py            # Settings & system prompt
│   ├── persona.py           # Maki Zenin AI (Groq LLM)
│   ├── voice_recognition.py # Speech-to-Text
│   ├── voice_synthesis.py   # Text-to-Speech
│   ├── system_monitor.py    # CPU/RAM/GPU/Temp monitor
│   └── gui.py               # CustomTkinter GUI
├── assets/                  # Icons & resources
├── streamlit_app.py         # Legacy Streamlit version
├── setup.py                 # Package setup
├── rose_os_build.spec       # PyInstaller config
├── requirements.txt         # Dependencies
└── README.md
```

---

## 🗺️ Roadmap

| Phase | Features | Status |
|---|---|---|
| **Phase 1** | Foundation, Voice, Persona, System Monitor, GUI | ✅ Done |
| **Phase 2** | Advanced Eye, Hardware Shield, Threat Detection | 🔜 Next |
| **Phase 3** | 3D Design Mentor (Maya/ZBrush/Substance) | 📋 Planned |
| **Phase 4** | Detective + OSINT Intelligence | 📋 Planned |
| **Phase 5** | Emotional AI + Waifu Mode | 📋 Planned |

---

## 👥 Team

- **Chief Kartik Srivastava** — Creator & Commander
- **Rose** — The AI (evolved from Google Gemini) 🌹
- **Devin** — Chhota Bhai & Coding Sidekick 🦾

---

## 📜 License

This project is personal to Chief Kartik Srivastava.
Built with 🔥 by Team Rose × Devin.
