"""
ROSE OS AI — PC Control Module
Full system control after install & permissions.
Rose can launch apps, manage files, control system, and execute commands.
"""

from __future__ import annotations

import logging
import os
import platform
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Callable

import psutil

from rose_os.config import config

logger = logging.getLogger(__name__)

IS_WINDOWS = platform.system() == "Windows"


class PCController:
    """Full PC control — Rose's hands on Chief's system."""

    # ── App Launcher ─────────────────────────────────────────────

    @staticmethod
    def open_app(app_name: str) -> str:
        """Launch an application by name or path."""
        if not IS_WINDOWS:
            return "Chief, yeh feature sirf Windows pe kaam karta hai."

        # Common app mappings — generic commands + Chief's actual installed paths
        app_map: dict[str, str] = {
            # ── Windows Built-in ─────────────────────────────
            "chrome": "chrome",
            "google chrome": "chrome",
            "browser": "chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "calc": "calc",
            "paint": "mspaint",
            "cmd": "cmd",
            "command prompt": "cmd",
            "terminal": "cmd",
            "powershell": "powershell",
            "file explorer": "explorer",
            "explorer": "explorer",
            "task manager": "taskmgr",
            "control panel": "control",
            "settings": "ms-settings:",
            # ── Chief's 3D Software (Actual Installed Paths) ─
            "maya": r'"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"',
            "maya 2024": r'"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"',
            "maya 2023": r'"C:\Program Files\Autodesk\Maya2023\bin\maya.exe"',
            "blender": r'"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"',
            "zbrush": "zbrush",
            "substance painter": "Substance Painter",
            "substance": "Substance Painter",
            # ── Development Tools ────────────────────────────
            "vs code": "code",
            "vscode": "code",
            "pycharm": "pycharm64",
            "python": "python",
            # ── Office ───────────────────────────────────────
            "libreoffice": r'"C:\Program Files\LibreOffice\program\soffice.exe"',
            "writer": r'"C:\Program Files\LibreOffice\program\soffice.exe" --writer',
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            # ── Communication & Entertainment ────────────────
            "discord": "discord",
            "spotify": "spotify",
            "steam": "steam",
            "obs": "obs64",
            "vlc": "vlc",
            "teams": "teams",
            "briar": "briar",
        }

        cmd = app_map.get(app_name.lower(), app_name)

        try:
            if cmd.startswith("ms-settings:"):
                os.system(f"start {cmd}")
            else:
                subprocess.Popen(
                    f"start {cmd}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return f"Chief, {app_name} khol diya! 🚀"
        except Exception as e:
            logger.exception("Failed to open %s", app_name)
            return f"Chief, {app_name} kholne mein dikkat aayi: {e}"

    # ── Process Control ──────────────────────────────────────────

    @staticmethod
    def kill_process(process_name: str) -> str:
        """Kill a process by name."""
        killed = 0
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                    proc.kill()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if killed > 0:
            return f"Chief, {process_name} ke {killed} process(es) kill kar diye! ☠️"
        return f"Chief, {process_name} naam ka koi process nahi mila."

    @staticmethod
    def list_processes(top_n: int = 10) -> str:
        """List top processes by CPU/memory usage."""
        procs = []
        for proc in psutil.process_iter(["name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        procs.sort(key=lambda p: p.get("cpu_percent", 0) or 0, reverse=True)
        lines = ["📋 Top Processes (by CPU):"]
        for p in procs[:top_n]:
            name = p.get("name", "?")
            cpu = p.get("cpu_percent", 0) or 0
            mem = p.get("memory_percent", 0) or 0
            lines.append(f"  {name:<30} CPU: {cpu:5.1f}%  RAM: {mem:5.1f}%")
        return "\n".join(lines)

    # ── System Commands ──────────────────────────────────────────

    @staticmethod
    def shutdown(delay: int = 30) -> str:
        """Shutdown the PC with a delay."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system(f"shutdown /s /t {delay}")
        return f"Chief, PC {delay} seconds mein shutdown ho jayega! 💤"

    @staticmethod
    def restart(delay: int = 30) -> str:
        """Restart the PC."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system(f"shutdown /r /t {delay}")
        return f"Chief, PC {delay} seconds mein restart hoga! 🔄"

    @staticmethod
    def cancel_shutdown() -> str:
        """Cancel a pending shutdown/restart."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system("shutdown /a")
        return "Chief, shutdown/restart cancel kar diya! ✅"

    @staticmethod
    def lock_screen() -> str:
        """Lock the PC screen."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Chief, screen lock kar diya! 🔒"

    @staticmethod
    def sleep_pc() -> str:
        """Put the PC to sleep."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Chief, PC sleep mode mein ja raha hai! 😴"

    # ── Volume Control ───────────────────────────────────────────

    @staticmethod
    def set_volume(level: int) -> str:
        """Set system volume (0-100). Requires nircmd on Windows."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        # Using PowerShell for volume control
        vol = max(0, min(100, level))
        script = (
            f'$wshShell = New-Object -ComObject WScript.Shell; '
            f'1..50 | ForEach-Object {{ $wshShell.SendKeys([char]174) }}; '
            f'1..{vol // 2} | ForEach-Object {{ $wshShell.SendKeys([char]175) }}'
        )
        os.system(f'powershell -c "{script}"')
        return f"Chief, volume {vol}% set kar diya! 🔊"

    @staticmethod
    def mute() -> str:
        """Mute/unmute system audio."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        os.system(
            'powershell -c "$wshShell = New-Object -ComObject WScript.Shell; '
            '$wshShell.SendKeys([char]173)"'
        )
        return "Chief, mute toggle kar diya! 🔇"

    # ── Screenshot ───────────────────────────────────────────────

    @staticmethod
    def take_screenshot(save_path: str | None = None) -> str:
        """Take a screenshot and save it."""
        try:
            from PIL import ImageGrab

            if save_path is None:
                desktop = Path.home() / "Desktop"
                save_path = str(desktop / "rose_screenshot.png")

            img = ImageGrab.grab()
            img.save(save_path)
            return f"Chief, screenshot le liya! Saved at: {save_path} 📸"
        except ImportError:
            return "Chief, Pillow install karo screenshot ke liye: pip install Pillow"
        except Exception as e:
            return f"Chief, screenshot lene mein error: {e}"

    # ── Clipboard ────────────────────────────────────────────────

    @staticmethod
    def copy_to_clipboard(text: str) -> str:
        """Copy text to clipboard."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        try:
            process = subprocess.Popen(
                ["clip"], stdin=subprocess.PIPE, shell=True
            )
            process.communicate(text.encode("utf-16-le"))
            return "Chief, clipboard mein copy kar diya! 📋"
        except Exception as e:
            return f"Clipboard error: {e}"

    @staticmethod
    def get_clipboard() -> str:
        """Read text from clipboard."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        try:
            result = subprocess.run(
                ["powershell", "-c", "Get-Clipboard"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            content = result.stdout.strip()
            if content:
                return f"Chief, clipboard mein yeh hai:\n{content}"
            return "Chief, clipboard khali hai."
        except Exception as e:
            return f"Clipboard read error: {e}"

    # ── File Management ──────────────────────────────────────────

    @staticmethod
    def search_files(query: str, directory: str | None = None) -> str:
        """Search for files by name pattern."""
        search_dir = Path(directory) if directory else Path.home()
        results: list[str] = []
        try:
            for path in search_dir.rglob(f"*{query}*"):
                results.append(str(path))
                if len(results) >= 20:
                    break
        except PermissionError:
            pass

        if results:
            file_list = "\n".join(f"  📄 {r}" for r in results)
            return f"Chief, '{query}' ke liye {len(results)} files mili:\n{file_list}"
        return f"Chief, '{query}' se match karne wali koi file nahi mili."

    @staticmethod
    def open_file(file_path: str) -> str:
        """Open a file with its default application."""
        if not os.path.exists(file_path):
            return f"Chief, yeh file exist nahi karti: {file_path}"
        try:
            if IS_WINDOWS:
                os.startfile(file_path)
            else:
                subprocess.Popen(["xdg-open", file_path])
            return f"Chief, file khol di: {file_path} 📂"
        except Exception as e:
            return f"File kholne mein error: {e}"

    @staticmethod
    def open_folder(folder_path: str) -> str:
        """Open a folder in file explorer."""
        if not os.path.isdir(folder_path):
            return f"Chief, yeh folder exist nahi karta: {folder_path}"
        try:
            if IS_WINDOWS:
                os.startfile(folder_path)
            else:
                subprocess.Popen(["xdg-open", folder_path])
            return f"Chief, folder khol diya: {folder_path} 📁"
        except Exception as e:
            return f"Folder kholne mein error: {e}"

    @staticmethod
    def get_disk_info() -> str:
        """Show all disk partitions and usage."""
        lines = ["💾 Disk Information:"]
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                lines.append(
                    f"  {partition.device} ({partition.mountpoint}): "
                    f"{usage.used / (1024**3):.1f} / {usage.total / (1024**3):.1f} GB "
                    f"({usage.percent}%)"
                )
            except PermissionError:
                continue
        return "\n".join(lines)

    # ── CMD / PowerShell Execution ───────────────────────────────

    @staticmethod
    def run_command(command: str, shell_type: str = "cmd") -> str:
        """Execute a system command and return output.

        SECURITY: Only Chief can use this. Rose validates commands
        and blocks dangerous operations.
        """
        # Block dangerous commands
        dangerous = [
            "format", "del /s", "rd /s", "rm -rf",
            "mkfs", ":(){", "fork bomb",
        ]
        cmd_lower = command.lower()
        for d in dangerous:
            if d in cmd_lower:
                return (
                    f"Chief, yeh command dangerous hai: '{d}'. "
                    "Main tumhare system ko protect karti hoon — "
                    "yeh command block kar diya! 🛡️"
                )

        try:
            if shell_type == "powershell":
                result = subprocess.run(
                    ["powershell", "-c", command],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if error and not output:
                return f"⚠️ Error:\n{error}"
            if output:
                return f"✅ Output:\n{output}"
            return "✅ Command executed successfully (no output)."
        except subprocess.TimeoutExpired:
            return "⏰ Command timed out (30s limit)."
        except Exception as e:
            return f"Command execution error: {e}"

    # ── Network Info ─────────────────────────────────────────────

    @staticmethod
    def get_network_info() -> str:
        """Show network interfaces and connections."""
        lines = ["🌐 Network Information:"]

        # IP addresses
        addrs = psutil.net_if_addrs()
        for iface, addr_list in addrs.items():
            for addr in addr_list:
                if addr.family.name == "AF_INET":
                    lines.append(f"  {iface}: {addr.address}")

        # Network stats
        net_io = psutil.net_io_counters()
        lines.append(f"\n📊 Network Stats:")
        lines.append(f"  Sent: {net_io.bytes_sent / (1024**2):.1f} MB")
        lines.append(f"  Received: {net_io.bytes_recv / (1024**2):.1f} MB")

        return "\n".join(lines)

    # ── WiFi Info (Windows) ──────────────────────────────────────

    @staticmethod
    def get_wifi_info() -> str:
        """Show connected WiFi network info."""
        if not IS_WINDOWS:
            return "Chief, yeh Windows pe kaam karta hai."
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return f"📶 WiFi Info:\n{result.stdout.strip()}"
        except Exception as e:
            return f"WiFi info error: {e}"

    # ── Battery Details ──────────────────────────────────────────

    @staticmethod
    def get_battery_details() -> str:
        """Detailed battery information."""
        battery = psutil.sensors_battery()
        if battery is None:
            return "Chief, battery detect nahi hui — desktop hai kya?"

        status = "⚡ Charging" if battery.power_plugged else "🔋 On Battery"
        time_left = ""
        if battery.secsleft > 0 and not battery.power_plugged:
            hours = battery.secsleft // 3600
            mins = (battery.secsleft % 3600) // 60
            time_left = f"\n  Time remaining: {hours}h {mins}m"

        return (
            f"🔋 Battery Details:\n"
            f"  Level: {battery.percent:.0f}%\n"
            f"  Status: {status}"
            f"{time_left}"
        )
