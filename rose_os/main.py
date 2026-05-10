"""
ROSE OS AI — Main Entry Point
Launch the full desktop application.

Usage:
    python -m rose_os.main
    # or after PyInstaller build:
    rose_os.exe
"""

from __future__ import annotations

import logging
import sys

from rose_os.config import config
from rose_os.gui import RoseGUI
from rose_os.persona import RosePersona
from rose_os.system_monitor import SystemMonitor
from rose_os.voice_recognition import VoiceListener
from rose_os.voice_synthesis import VoiceSynth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-28s  %(levelname)-7s  %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║       ROSE OS AI v1.0 Starting       ║")
    logger.info("║   Commander: %s", f"{config.commander_name:<20} ║")
    logger.info("║   Persona : Maki Zenin 🔥            ║")
    logger.info("╚══════════════════════════════════════╝")

    # ── Initialise subsystems ────────────────────────────────────
    persona = RosePersona()
    if not persona.initialise():
        logger.warning(
            "AI persona failed to initialise — chat will run in offline mode."
        )

    monitor = SystemMonitor()
    monitor.start()

    voice_listener = VoiceListener()
    voice_synth = VoiceSynth()
    voice_synth.initialise()

    # ── Launch GUI ───────────────────────────────────────────────
    app = RoseGUI(
        persona=persona,
        monitor=monitor,
        voice_listener=voice_listener,
        voice_synth=voice_synth,
    )
    app.mainloop()

    # cleanup
    monitor.stop()
    voice_synth.stop()
    logger.info("ROSE OS AI shut down. Bye Chief! 🌹")


if __name__ == "__main__":
    main()
