"""
ROSE OS AI — Global Hotkey Module
Press a keyboard shortcut anywhere in Windows to summon Rose.
Default: Ctrl+Shift+R
"""

from __future__ import annotations

import logging
import platform
import threading
from typing import Callable

logger = logging.getLogger(__name__)

HOTKEY_AVAILABLE = False
try:
    if platform.system() == "Windows":
        import keyboard

        HOTKEY_AVAILABLE = True
except ImportError:
    logger.info(
        "keyboard module not installed — global hotkeys disabled. "
        "Install with: pip install keyboard"
    )


class GlobalHotkey:
    """Register global hotkeys that work even when Rose is minimised."""

    DEFAULT_SUMMON = "ctrl+shift+r"

    def __init__(self) -> None:
        self._registered: dict[str, Callable[[], None]] = {}
        self._running = False

    def register(
        self,
        combination: str,
        callback: Callable[[], None],
    ) -> bool:
        """Register a global hotkey *combination* (e.g. 'ctrl+shift+r')."""
        if not HOTKEY_AVAILABLE:
            logger.warning("Hotkeys not available on this platform.")
            return False

        try:
            import keyboard as kb

            kb.add_hotkey(combination, callback, suppress=False)
            self._registered[combination] = callback
            logger.info("Global hotkey registered: %s", combination)
            return True
        except Exception:
            logger.exception("Failed to register hotkey %s", combination)
            return False

    def unregister_all(self) -> None:
        """Remove all registered hotkeys."""
        if not HOTKEY_AVAILABLE:
            return
        try:
            import keyboard as kb

            for combo in self._registered:
                kb.remove_hotkey(combo)
            self._registered.clear()
            logger.info("All hotkeys unregistered.")
        except Exception:
            logger.exception("Error unregistering hotkeys")

    def start_listener(self) -> None:
        """Start the hotkey listener in a background thread (Windows only)."""
        if not HOTKEY_AVAILABLE or self._running:
            return
        self._running = True
        logger.info("Global hotkey listener active.")

    def stop(self) -> None:
        """Stop the hotkey listener."""
        self._running = False
        self.unregister_all()
