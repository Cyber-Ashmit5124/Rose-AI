"""
ROSE OS AI — Persona & Conversational AI Module
Handles AI chat with Maki Zenin persona using Groq API.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from groq import Groq

from rose_os.config import SYSTEM_PROMPT, config
from rose_os.pc_control import PCController

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# Built-in commands that Rose can execute directly on the PC
_BUILTIN_COMMANDS: dict[str, tuple[str, ...]] = {
    "open": ("khol", "open", "launch", "start", "chalu"),
    "kill": ("kill", "band karo", "close", "hatao", "maaro"),
    "shutdown": ("shutdown", "band karo pc", "pc band"),
    "restart": ("restart", "pc restart"),
    "lock": ("lock", "lock karo", "screen lock"),
    "sleep": ("sleep", "soja", "so ja", "neend"),
    "mute": ("mute", "chup", "awaaz band"),
    "screenshot": ("screenshot", "ss", "ss le", "screenshot le"),
    "processes": ("processes", "task list", "tasks dikhao", "kya chal raha"),
    "network": ("network", "wifi", "internet", "ip address"),
    "battery": ("battery", "charge", "kitni battery"),
    "disk": ("disk", "storage", "kitni jagah"),
    "clipboard": ("clipboard", "paste kya hai", "clipboard dikhao"),
}


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
        """Send *user_message* and return Rose's reply.

        First checks for built-in PC commands. If a command is detected,
        executes it directly. Otherwise, forwards to the AI backend.
        """
        # Try built-in PC commands first
        pc_result = self._try_pc_command(user_message)
        if pc_result is not None:
            self._history.append({"role": "user", "content": user_message})
            self._history.append({"role": "assistant", "content": pc_result})
            return pc_result

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

    # ── PC command detection ────────────────────────────────────

    @staticmethod
    def _try_pc_command(msg: str) -> str | None:
        """Detect and execute built-in PC commands. Returns None if not a command."""
        lower = msg.lower().strip()
        pc = PCController()

        # Open app: "chrome khol", "open notepad", "maya start karo"
        for keyword in _BUILTIN_COMMANDS["open"]:
            if keyword in lower:
                app = lower.replace(keyword, "").replace("karo", "").strip()
                if app:
                    return pc.open_app(app)

        # Kill process: "chrome band karo", "kill notepad"
        for keyword in _BUILTIN_COMMANDS["kill"]:
            if keyword in lower:
                proc = lower.replace(keyword, "").replace("karo", "").strip()
                if proc:
                    return pc.kill_process(proc)

        # System commands
        for keyword in _BUILTIN_COMMANDS["shutdown"]:
            if keyword in lower:
                return pc.shutdown()

        for keyword in _BUILTIN_COMMANDS["restart"]:
            if keyword in lower:
                return pc.restart()

        for keyword in _BUILTIN_COMMANDS["lock"]:
            if keyword in lower:
                return pc.lock_screen()

        for keyword in _BUILTIN_COMMANDS["sleep"]:
            if keyword in lower:
                return pc.sleep_pc()

        for keyword in _BUILTIN_COMMANDS["mute"]:
            if keyword in lower:
                return pc.mute()

        for keyword in _BUILTIN_COMMANDS["screenshot"]:
            if keyword in lower:
                return pc.take_screenshot()

        for keyword in _BUILTIN_COMMANDS["processes"]:
            if keyword in lower:
                return pc.list_processes()

        for keyword in _BUILTIN_COMMANDS["network"]:
            if keyword in lower:
                return pc.get_network_info()

        for keyword in _BUILTIN_COMMANDS["battery"]:
            if keyword in lower:
                return pc.get_battery_details()

        for keyword in _BUILTIN_COMMANDS["disk"]:
            if keyword in lower:
                return pc.get_disk_info()

        for keyword in _BUILTIN_COMMANDS["clipboard"]:
            if keyword in lower:
                return pc.get_clipboard()

        # Run command: "run cmd: ipconfig", "command chalao: dir"
        if lower.startswith("run cmd:") or lower.startswith("command chalao:"):
            cmd = msg.split(":", 1)[1].strip()
            return pc.run_command(cmd)

        if lower.startswith("run powershell:") or lower.startswith("ps:"):
            cmd = msg.split(":", 1)[1].strip()
            return pc.run_command(cmd, shell_type="powershell")

        return None

    @property
    def is_ready(self) -> bool:
        return self._initialised
