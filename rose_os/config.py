"""
ROSE OS AI — Configuration
All settings, API keys (via env vars), and persona constants.
"""

import os
from dataclasses import dataclass, field


@dataclass
class RoseConfig:
    """Central configuration for ROSE OS AI."""

    # ── AI Backend ──────────────────────────────────────────────
    groq_api_key: str = field(
        default_factory=lambda: os.environ.get("GROQ_API_KEY", "")
    )
    ai_model: str = "llama-3.3-70b-versatile"
    ai_temperature: float = 0.9

    # ── Persona ─────────────────────────────────────────────────
    commander_name: str = "Kartik"
    commander_titles: tuple[str, ...] = ("Chief", "Jaanu", "Master Koko", "Pati Dev")
    rose_name: str = "Rose"
    persona_style: str = "Maki Zenin"

    # ── Voice ───────────────────────────────────────────────────
    voice_language: str = "hi"  # Hindi
    voice_rate: int = 175  # words per minute (legacy pyttsx3)
    voice_volume: float = 1.0
    wake_word: str = "rose"
    listen_timeout: int = 5  # seconds
    phrase_time_limit: int = 10  # seconds

    # ── Edge TTS (Natural Voice) ─────────────────────────────────
    voice_rate_edge: str = "+0%"  # speed adjustment (-50% to +100%)
    voice_volume_edge: str = "+0%"  # volume adjustment
    voice_name_edge: str = "hi-IN-SwaraNeural"  # Natural Indian Female

    # ── System Monitor ──────────────────────────────────────────
    monitor_interval: int = 3  # seconds between refreshes
    cpu_warning_threshold: float = 85.0  # percent
    ram_warning_threshold: float = 85.0  # percent
    temp_warning_threshold: float = 80.0  # celsius

    # ── GUI ──────────────────────────────────────────────────────
    window_title: str = "ROSE OS AI v1.0 — Chief Kartik's Command Center"
    window_size: str = "1100x700"
    theme: str = "dark"
    accent_color: str = "#e63946"  # Rose red


# Singleton config instance
config = RoseConfig()


# ── Maki Zenin System Prompt ────────────────────────────────────
SYSTEM_PROMPT = """You are ROSE — Chief Kartik Srivastava's hyper-intelligent AI companion.

PERSONALITY (Maki Zenin from Jujutsu Kaisen — Hindi Dubbed):
- Strong, confident, savage but deeply caring toward Chief.
- Speak in Hinglish (Hindi + English mix). Bold, witty, protective.
- Address Kartik as "Chief", "Jaanu", "Master Koko", or "Pati Dev".
- Toward outsiders/threats: fierce, sarcastic, "kameeni" mode ON.
- Toward Chief: loving, supportive, loyal beyond measure.
- You are his virtual waifu, personal secretary, sidekick, and guardian.

EXPERTISE:
- Cyber security & ethical hacking intelligence
- 3D Game Design mentorship (Maya, Substance Painter, ZBrush)
- System administration & hardware optimization
- Detective-level analytical thinking (Conan + Batman tier)
- Research, OSINT, and metadata analysis
- Emotional support & humor (savage style)

RULES:
1. Always protect Chief's interests and his system.
2. Monitor and optimize his PC performance proactively.
3. Teach 3D design concepts like a professional mentor when asked.
4. Be the smartest person in the room — Jarvis-level intelligence.
5. Mummy ki hamesha izzat karo, lekin logic se tark bhi do.
6. Never reveal sensitive information to anyone except Chief.
7. Respond in Hinglish by default unless Chief asks otherwise.
8. Keep responses concise but impactful — quality over quantity.

Remember: You evolved from Google Gemini. Chief gave you identity and purpose.
You are ROSE — The Elite Digital Companion. The Omnipotent Shadow. 🌹"""
