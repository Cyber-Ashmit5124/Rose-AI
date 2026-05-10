"""
ROSE OS AI — System Tray Module
Rose sits in the Windows taskbar 24/7. Close the window? She's still there.
Right-click tray icon for quick actions.
"""

from __future__ import annotations

import logging
import sys
import threading
from typing import TYPE_CHECKING, Callable

logger = logging.getLogger(__name__)

try:
    from pystray import Icon, Menu, MenuItem
    from PIL import Image, ImageDraw

    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    logger.warning(
        "pystray/Pillow not installed — system tray disabled. "
        "Install with: pip install pystray Pillow"
    )

if TYPE_CHECKING:
    pass


def _create_rose_icon(size: int = 64) -> "Image.Image":
    """Generate a simple rose-red circle icon programmatically."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Rose red circle with dark border
    draw.ellipse([2, 2, size - 2, size - 2], fill=(230, 57, 70, 255))
    # Inner highlight
    draw.ellipse(
        [size // 4, size // 4, size * 3 // 4, size * 3 // 4],
        fill=(255, 100, 110, 255),
    )
    # "R" text approximation — small dot in center
    center = size // 2
    r = size // 8
    draw.ellipse(
        [center - r, center - r, center + r, center + r],
        fill=(255, 255, 255, 255),
    )
    return img


class RoseTray:
    """System tray icon for ROSE OS AI."""

    def __init__(
        self,
        on_show: Callable[[], None] | None = None,
        on_quit: Callable[[], None] | None = None,
        on_status: Callable[[], str] | None = None,
    ) -> None:
        self._on_show = on_show
        self._on_quit = on_quit
        self._on_status = on_status
        self._icon: Icon | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> bool:
        """Create and show the tray icon in a background thread."""
        if not TRAY_AVAILABLE:
            logger.warning("System tray not available.")
            return False

        menu = Menu(
            MenuItem("🌹 Show Rose", self._show_window, default=True),
            MenuItem("📊 System Status", self._show_status),
            Menu.SEPARATOR,
            MenuItem("❌ Quit Rose", self._quit),
        )

        self._icon = Icon(
            name="ROSE OS AI",
            icon=_create_rose_icon(),
            title="ROSE OS AI — Chief Kartik's Companion",
            menu=menu,
        )

        self._thread = threading.Thread(target=self._icon.run, daemon=True)
        self._thread.start()
        logger.info("System tray icon started 🌹")
        return True

    def stop(self) -> None:
        """Remove the tray icon."""
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass

    def notify(self, title: str, message: str) -> None:
        """Show a Windows notification balloon from the tray."""
        if self._icon:
            try:
                self._icon.notify(message, title)
            except Exception:
                logger.debug("Tray notification failed")

    def _show_window(self, icon: "Icon | None" = None, item: "MenuItem | None" = None) -> None:
        if self._on_show:
            self._on_show()

    def _show_status(self, icon: "Icon | None" = None, item: "MenuItem | None" = None) -> None:
        if self._on_status:
            status = self._on_status()
            self.notify("📊 System Status", status)

    def _quit(self, icon: "Icon | None" = None, item: "MenuItem | None" = None) -> None:
        self.stop()
        if self._on_quit:
            self._on_quit()
        else:
            sys.exit(0)
