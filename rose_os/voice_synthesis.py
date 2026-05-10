"""
ROSE OS AI — Text-to-Speech Module
Rose speaks with a Maki Zenin–style Hindi voice.
"""

from __future__ import annotations

import logging
import threading
from queue import Queue

import pyttsx3

from rose_os.config import config

logger = logging.getLogger(__name__)


class VoiceSynth:
    """Offline text-to-speech engine for Rose."""

    def __init__(self) -> None:
        self._engine: pyttsx3.Engine | None = None
        self._queue: Queue[str] = Queue()
        self._thread: threading.Thread | None = None
        self._running = False

    # ── initialisation ───────────────────────────────────────────

    def initialise(self) -> bool:
        """Set up the TTS engine with the configured voice properties."""
        try:
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", config.voice_rate)
            self._engine.setProperty("volume", config.voice_volume)
            self._select_hindi_voice()
            self._running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            logger.info("Voice synthesis initialised 🔊")
            return True
        except Exception:
            logger.exception("TTS engine initialisation failed")
            return False

    # ── public API ───────────────────────────────────────────────

    def speak(self, text: str) -> None:
        """Queue *text* for speech output."""
        if not self._running:
            logger.warning("TTS not initialised; dropping message.")
            return
        self._queue.put(text)

    def stop(self) -> None:
        """Shut down the TTS worker."""
        self._running = False
        self._queue.put("")  # sentinel to unblock worker

    # ── internal ─────────────────────────────────────────────────

    def _worker(self) -> None:
        while self._running:
            text = self._queue.get()
            if not text or not self._running:
                break
            try:
                if self._engine is not None:
                    self._engine.say(text)
                    self._engine.runAndWait()
            except Exception:
                logger.exception("TTS playback error")

    def _select_hindi_voice(self) -> None:
        """Try to pick a female Hindi / Indian English voice."""
        if self._engine is None:
            return
        voices = self._engine.getProperty("voices")
        if not voices:
            return
        for voice in voices:
            lang = getattr(voice, "languages", [])
            name_lower = voice.name.lower() if voice.name else ""
            if "hindi" in name_lower or "hi" in lang or "indian" in name_lower:
                self._engine.setProperty("voice", voice.id)
                logger.info("Selected voice: %s", voice.name)
                return
        # Fallback: pick the second voice (often female) if available
        if len(voices) > 1:
            self._engine.setProperty("voice", voices[1].id)
            logger.info("Fallback voice: %s", voices[1].name)

    @property
    def is_ready(self) -> bool:
        return self._running
