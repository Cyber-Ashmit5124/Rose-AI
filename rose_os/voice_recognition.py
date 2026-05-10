"""
ROSE OS AI — Voice Recognition Module
Listens to Chief's voice commands using SpeechRecognition.
"""

from __future__ import annotations

import logging
import threading
from typing import Callable

import speech_recognition as sr

from rose_os.config import config

logger = logging.getLogger(__name__)


class VoiceListener:
    """Microphone listener that converts speech to text."""

    def __init__(self) -> None:
        self._recogniser = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._listening = False
        self._thread: threading.Thread | None = None

    # ── calibration ──────────────────────────────────────────────

    def calibrate(self, duration: float = 1.0) -> None:
        """Adjust for ambient noise."""
        try:
            with self._microphone as source:
                logger.info("Calibrating microphone for ambient noise…")
                self._recogniser.adjust_for_ambient_noise(source, duration=duration)
                logger.info("Microphone calibrated ✓")
        except Exception:
            logger.exception("Microphone calibration failed")

    # ── single listen ────────────────────────────────────────────

    def listen_once(self) -> str | None:
        """Block until one phrase is captured, then return the text (or None)."""
        try:
            with self._microphone as source:
                logger.debug("Listening…")
                audio = self._recogniser.listen(
                    source,
                    timeout=config.listen_timeout,
                    phrase_time_limit=config.phrase_time_limit,
                )
            text = self._recogniser.recognize_google(
                audio, language=config.voice_language
            )
            logger.info("Recognised: %s", text)
            return str(text)
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            logger.debug("Speech not understood")
            return None
        except sr.RequestError:
            logger.exception("Google Speech API error")
            return None
        except Exception:
            logger.exception("Unexpected voice recognition error")
            return None

    # ── continuous background listen ─────────────────────────────

    def start_continuous(self, on_text: Callable[[str], None]) -> None:
        """Start listening in a background thread; call *on_text* for each phrase."""
        if self._listening:
            return
        self._listening = True
        self._thread = threading.Thread(
            target=self._continuous_loop, args=(on_text,), daemon=True
        )
        self._thread.start()
        logger.info("Continuous voice listening started 🎤")

    def stop_continuous(self) -> None:
        """Signal the background listener to stop."""
        self._listening = False
        logger.info("Voice listening stopped.")

    def _continuous_loop(self, on_text: Callable[[str], None]) -> None:
        self.calibrate()
        while self._listening:
            text = self.listen_once()
            if text:
                on_text(text)

    @property
    def is_listening(self) -> bool:
        return self._listening
