"""
ROSE OS AI — Text-to-Speech Module (Edge TTS)
Rose speaks with a natural Indian female voice — Maki Zenin style.
Uses Microsoft Edge TTS (hi-IN-SwaraNeural) for high-quality, realistic speech.
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import threading
import uuid
from queue import Queue

import edge_tts

from rose_os.config import config

logger = logging.getLogger(__name__)

# Audio playback — try multiple backends
_PLAYBACK_BACKEND: str | None = None

try:
    import pygame

    pygame.mixer.init()
    _PLAYBACK_BACKEND = "pygame"
except Exception:
    pass

if _PLAYBACK_BACKEND is None:
    try:
        import playsound as _ps  # noqa: F401

        _PLAYBACK_BACKEND = "playsound"
    except ImportError:
        pass

if _PLAYBACK_BACKEND is None:
    import platform

    if platform.system() == "Windows":
        _PLAYBACK_BACKEND = "winsound"
    else:
        _PLAYBACK_BACKEND = "system"

logger.info("TTS playback backend: %s", _PLAYBACK_BACKEND)


def _play_audio(filepath: str) -> None:
    """Play an audio file using the best available backend."""
    try:
        if _PLAYBACK_BACKEND == "pygame":
            import pygame

            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        elif _PLAYBACK_BACKEND == "playsound":
            from playsound import playsound

            playsound(filepath)
        elif _PLAYBACK_BACKEND == "winsound":
            os.system(f'powershell -c "(New-Object Media.SoundPlayer \'{filepath}\').PlaySync()"')
        else:
            os.system(f"aplay {filepath} 2>/dev/null || afplay {filepath} 2>/dev/null")
    except Exception:
        logger.exception("Audio playback failed")
    finally:
        try:
            os.remove(filepath)
        except OSError:
            pass


class VoiceSynth:
    """Natural Indian female TTS using Microsoft Edge TTS (Swara Neural)."""

    # Microsoft Edge TTS voices for Hindi
    VOICE_FEMALE_HINDI = "hi-IN-SwaraNeural"
    VOICE_MALE_HINDI = "hi-IN-MadhurNeural"

    def __init__(self) -> None:
        self._queue: Queue[str] = Queue()
        self._thread: threading.Thread | None = None
        self._running = False
        self._voice = self.VOICE_FEMALE_HINDI
        self._rate = config.voice_rate_edge
        self._volume = config.voice_volume_edge
        self._loop: asyncio.AbstractEventLoop | None = None

    # ── initialisation ───────────────────────────────────────────

    def initialise(self) -> bool:
        """Start the TTS worker thread."""
        try:
            self._running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            logger.info(
                "Voice synthesis initialised — %s (Natural Indian Female) 🔊",
                self._voice,
            )
            return True
        except Exception:
            logger.exception("TTS initialisation failed")
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

    def set_voice(self, voice_name: str) -> None:
        """Switch the TTS voice at runtime."""
        self._voice = voice_name
        logger.info("Voice changed to: %s", voice_name)

    # ── internal ─────────────────────────────────────────────────

    def _worker(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        while self._running:
            text = self._queue.get()
            if not text or not self._running:
                break
            try:
                self._loop.run_until_complete(self._synthesise_and_play(text))
            except Exception:
                logger.exception("TTS synthesis/playback error")
        self._loop.close()

    async def _synthesise_and_play(self, text: str) -> None:
        """Generate speech audio with Edge TTS and play it."""
        tmp_path = os.path.join(
            tempfile.gettempdir(), f"rose_tts_{uuid.uuid4().hex}.mp3"
        )
        communicate = edge_tts.Communicate(
            text,
            voice=self._voice,
            rate=self._rate,
            volume=self._volume,
        )
        await communicate.save(tmp_path)
        _play_audio(tmp_path)

    @property
    def is_ready(self) -> bool:
        return self._running
