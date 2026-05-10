"""
ROSE OS AI — Windows Auto-Start Module
Register/unregister Rose to start automatically when Windows boots.
"""

from __future__ import annotations

import logging
import os
import sys
import platform

logger = logging.getLogger(__name__)

APP_NAME = "ROSE_OS_AI"


def _get_exe_path() -> str:
    """Return the path to the running executable or script."""
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle
        return sys.executable
    return os.path.abspath(sys.argv[0])


def enable_autostart() -> bool:
    """Add Rose to Windows startup via Registry."""
    if platform.system() != "Windows":
        logger.info("Auto-start only supported on Windows.")
        return False

    try:
        import winreg

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        exe_path = _get_exe_path()

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')

        logger.info("Auto-start enabled: %s", exe_path)
        return True
    except ImportError:
        logger.warning("winreg not available — not on Windows.")
        return False
    except Exception:
        logger.exception("Failed to enable auto-start")
        return False


def disable_autostart() -> bool:
    """Remove Rose from Windows startup."""
    if platform.system() != "Windows":
        return False

    try:
        import winreg

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, APP_NAME)

        logger.info("Auto-start disabled.")
        return True
    except ImportError:
        return False
    except FileNotFoundError:
        logger.info("Auto-start was not enabled.")
        return True
    except Exception:
        logger.exception("Failed to disable auto-start")
        return False


def is_autostart_enabled() -> bool:
    """Check if Rose is registered to auto-start."""
    if platform.system() != "Windows":
        return False

    try:
        import winreg

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_QUERY_VALUE
        ) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except (ImportError, FileNotFoundError, OSError):
        return False
