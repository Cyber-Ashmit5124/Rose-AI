"""
ROSE OS AI — System Monitor Module
Real-time PC health tracking: CPU, RAM, Disk, GPU temperature.
Rose's Advanced Eye — watches everything for Chief.
"""

from __future__ import annotations

import logging
import platform
import socket
import threading
import time
from dataclasses import dataclass

import psutil

from rose_os.config import config

logger = logging.getLogger(__name__)


@dataclass
class SystemSnapshot:
    """A single point-in-time reading of system health."""

    cpu_percent: float
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    battery_percent: float | None
    battery_plugged: bool | None
    cpu_temp: float | None
    boot_time: str
    os_name: str
    hostname: str
    ip_address: str

    # ── warnings ─────────────────────────────────────────────────

    @property
    def warnings(self) -> list[str]:
        alerts: list[str] = []
        if self.cpu_percent >= config.cpu_warning_threshold:
            alerts.append(
                f"⚠️ CPU bahut zyada load pe hai: {self.cpu_percent:.0f}%"
            )
        if self.ram_percent >= config.ram_warning_threshold:
            alerts.append(
                f"⚠️ RAM critical hai Chief: {self.ram_percent:.0f}%"
            )
        if self.cpu_temp and self.cpu_temp >= config.temp_warning_threshold:
            alerts.append(
                f"🔥 Temperature bahut high hai: {self.cpu_temp:.0f}°C — "
                "cooling check karo!"
            )
        if self.battery_percent is not None and self.battery_percent < 20:
            plug = "plugged in" if self.battery_plugged else "NOT charging"
            alerts.append(
                f"🔋 Battery low: {self.battery_percent:.0f}% ({plug})"
            )
        return alerts


class SystemMonitor:
    """Continuously monitors system resources and fires callbacks on alerts."""

    def __init__(self) -> None:
        self._running = False
        self._thread: threading.Thread | None = None
        self._latest: SystemSnapshot | None = None
        self._on_alert: list[callable] = []

    # ── public API ───────────────────────────────────────────────

    def snapshot(self) -> SystemSnapshot:
        """Take an immediate system snapshot."""
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        battery = psutil.sensors_battery()

        cpu_temp: float | None = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for entries in temps.values():
                    if entries:
                        cpu_temp = entries[0].current
                        break
        except Exception:
            pass

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except Exception:
            hostname = "unknown"
            ip_address = "unknown"

        snap = SystemSnapshot(
            cpu_percent=psutil.cpu_percent(interval=0.5),
            ram_percent=mem.percent,
            ram_used_gb=round(mem.used / (1024**3), 2),
            ram_total_gb=round(mem.total / (1024**3), 2),
            disk_percent=disk.percent,
            disk_used_gb=round(disk.used / (1024**3), 2),
            disk_total_gb=round(disk.total / (1024**3), 2),
            battery_percent=battery.percent if battery else None,
            battery_plugged=battery.power_plugged if battery else None,
            cpu_temp=cpu_temp,
            boot_time=time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time())
            ),
            os_name=f"{platform.system()} {platform.release()}",
            hostname=hostname,
            ip_address=ip_address,
        )
        self._latest = snap
        return snap

    def on_alert(self, callback: callable) -> None:
        """Register a callback that receives a list[str] of warnings."""
        self._on_alert.append(callback)

    def start(self) -> None:
        """Begin background monitoring."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("System monitor started 📊")

    def stop(self) -> None:
        self._running = False

    @property
    def latest(self) -> SystemSnapshot | None:
        return self._latest

    # ── internal ─────────────────────────────────────────────────

    def _loop(self) -> None:
        while self._running:
            snap = self.snapshot()
            warnings = snap.warnings
            if warnings:
                for cb in self._on_alert:
                    try:
                        cb(warnings)
                    except Exception:
                        logger.exception("Alert callback error")
            time.sleep(config.monitor_interval)

    def format_snapshot(self, snap: SystemSnapshot | None = None) -> str:
        """Return a human-readable summary of the system state."""
        s = snap or self._latest
        if s is None:
            return "System data not available yet."

        lines = [
            f"💻 OS: {s.os_name}",
            f"🖥️  Host: {s.hostname} ({s.ip_address})",
            f"⏱️  Boot: {s.boot_time}",
            "",
            f"🧠 CPU: {s.cpu_percent:.1f}%",
            f"📦 RAM: {s.ram_used_gb:.1f} / {s.ram_total_gb:.1f} GB "
            f"({s.ram_percent:.1f}%)",
            f"💾 Disk: {s.disk_used_gb:.1f} / {s.disk_total_gb:.1f} GB "
            f"({s.disk_percent:.1f}%)",
        ]

        if s.cpu_temp is not None:
            lines.append(f"🌡️  Temp: {s.cpu_temp:.0f}°C")

        if s.battery_percent is not None:
            plug = "⚡ Charging" if s.battery_plugged else "🔋 Battery"
            lines.append(f"{plug}: {s.battery_percent:.0f}%")

        if s.warnings:
            lines.append("")
            lines.extend(s.warnings)

        return "\n".join(lines)
