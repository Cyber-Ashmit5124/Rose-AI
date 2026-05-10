"""
ROSE OS AI — Persona & Conversational AI Module
Handles AI chat with Maki Zenin persona using Groq API.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from groq import Groq

from rose_os.config import SYSTEM_PROMPT, config

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class RosePersona:
    """Maki Zenin–style AI persona powered by Groq LLM."""

    def __init__(self) -> None:
        self._history: list[dict[str, str]] = []
        self._client: Groq | None = None
        self._initialised = False

    # ── lifecycle ────────────────────────────────────────────────

    def initialise(self) -> bool:
        """Connect to the Groq backend. Returns True on success."""
        api_key = config.groq_api_key
        if not api_key:
            logger.error(
                "GROQ_API_KEY not set. "
                "Set it as an environment variable before launching ROSE."
            )
            return False
        try:
            self._client = Groq(api_key=api_key)
            self._initialised = True
            logger.info("Rose persona initialised — Maki mode ON 🔥")
            return True
        except Exception:
            logger.exception("Failed to initialise Groq client")
            return False

    # ── chat ─────────────────────────────────────────────────────

    def chat(self, user_message: str) -> str:
        """Send *user_message* and return Rose's reply."""
        if not self._initialised or self._client is None:
            return (
                "Chief, mera AI backend abhi connect nahi hua. "
                "GROQ_API_KEY set karo environment mein! 🔧"
            )

        self._history.append({"role": "user", "content": user_message})

        try:
            response = self._client.chat.completions.create(
                model=config.ai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *self._history,
                ],
                temperature=config.ai_temperature,
            )
            reply = response.choices[0].message.content or ""
            self._history.append({"role": "assistant", "content": reply})
            return reply
        except Exception:
            logger.exception("Groq API call failed")
            return (
                "Chief, abhi AI se baat karne mein dikkat aa rahi hai. "
                "Network ya API key check karo! ⚠️"
            )

    # ── utilities ────────────────────────────────────────────────

    def clear_history(self) -> None:
        """Wipe conversation history."""
        self._history.clear()
        logger.info("Conversation history cleared.")

    def get_history(self) -> list[dict[str, str]]:
        """Return a copy of the conversation history."""
        return list(self._history)

    @property
    def is_ready(self) -> bool:
        return self._initialised
