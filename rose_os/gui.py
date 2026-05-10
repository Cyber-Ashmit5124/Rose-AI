"""
ROSE OS AI — GUI Module
Chief Kartik's Command Center built with CustomTkinter.
"""

from __future__ import annotations

import logging
import threading
import tkinter as tk
from typing import TYPE_CHECKING

import customtkinter as ctk

from rose_os.config import config

if TYPE_CHECKING:
    from rose_os.persona import RosePersona
    from rose_os.system_monitor import SystemMonitor
    from rose_os.voice_recognition import VoiceListener
    from rose_os.voice_synthesis import VoiceSynth

logger = logging.getLogger(__name__)


class RoseGUI(ctk.CTk):
    """Main application window for ROSE OS AI."""

    def __init__(
        self,
        persona: RosePersona,
        monitor: SystemMonitor,
        voice_listener: VoiceListener,
        voice_synth: VoiceSynth,
    ) -> None:
        super().__init__()
        self.persona = persona
        self.monitor = monitor
        self.voice_listener = voice_listener
        self.voice_synth = voice_synth

        self._setup_window()
        self._build_layout()
        self._start_monitor_refresh()
        self._greet()

    # ── window setup ─────────────────────────────────────────────

    def _setup_window(self) -> None:
        self.title(config.window_title)
        self.geometry(config.window_size)
        ctk.set_appearance_mode(config.theme)
        ctk.set_default_color_theme("blue")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── layout ───────────────────────────────────────────────────

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── LEFT: system panel ───────────────────────────────────
        left = ctk.CTkFrame(self, width=300, corner_radius=0)
        left.grid(row=0, column=0, sticky="nswe")
        left.grid_propagate(False)

        ctk.CTkLabel(
            left,
            text="🌹 ROSE OS AI",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=config.accent_color,
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            left,
            text=f"Commander: {config.commander_name}",
            font=ctk.CTkFont(size=13),
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            left,
            text="📊 System Status",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(8, 4))

        self.system_text = ctk.CTkTextbox(left, width=270, height=260, state="disabled")
        self.system_text.pack(padx=10, pady=4)

        # voice toggle
        self.voice_btn = ctk.CTkButton(
            left,
            text="🎤 Voice: OFF",
            command=self._toggle_voice,
            fg_color=config.accent_color,
            hover_color="#b5202e",
        )
        self.voice_btn.pack(pady=10, padx=10, fill="x")

        # clear chat
        ctk.CTkButton(
            left,
            text="🗑️ Clear Chat",
            command=self._clear_chat,
            fg_color="#555",
            hover_color="#777",
        ).pack(pady=4, padx=10, fill="x")

        # ── RIGHT: chat area ────────────────────────────────────
        right = ctk.CTkFrame(self, corner_radius=0)
        right.grid(row=0, column=1, sticky="nswe")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.chat_display = ctk.CTkTextbox(right, state="disabled", wrap="word")
        self.chat_display.grid(row=0, column=0, sticky="nswe", padx=10, pady=(10, 4))

        input_frame = ctk.CTkFrame(right, fg_color="transparent")
        input_frame.grid(row=1, column=0, sticky="we", padx=10, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="Hukm karo Chief…",
            height=40,
            font=ctk.CTkFont(size=14),
        )
        self.input_field.grid(row=0, column=0, sticky="we", padx=(0, 6))
        self.input_field.bind("<Return>", lambda _e: self._send_message())

        ctk.CTkButton(
            input_frame,
            text="Send ➤",
            width=80,
            height=40,
            command=self._send_message,
            fg_color=config.accent_color,
            hover_color="#b5202e",
        ).grid(row=0, column=1)

    # ── chat logic ───────────────────────────────────────────────

    def _append_chat(self, sender: str, message: str) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def _send_message(self, text: str | None = None) -> None:
        msg = text or self.input_field.get().strip()
        if not msg:
            return
        self.input_field.delete(0, "end")
        self._append_chat("👤 Chief", msg)

        # handle built-in commands
        lower = msg.lower()
        if lower in ("system status", "system", "status", "pc status"):
            snap = self.monitor.snapshot()
            reply = self.monitor.format_snapshot(snap)
            self._append_chat("🌹 Rose", reply)
            self.voice_synth.speak("Chief, system status ready hai.")
            return

        if lower in ("clear", "clear history", "history clear"):
            self._clear_chat()
            return

        # AI response in background
        threading.Thread(target=self._get_ai_reply, args=(msg,), daemon=True).start()

    def _get_ai_reply(self, msg: str) -> None:
        reply = self.persona.chat(msg)
        self.after(0, self._append_chat, "🌹 Rose", reply)
        self.voice_synth.speak(reply)

    def _clear_chat(self) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.persona.clear_history()
        self._append_chat("🌹 Rose", "Chat clear ho gaya Chief! Fresh start 🔄")

    # ── greeting ─────────────────────────────────────────────────

    def _greet(self) -> None:
        greeting = (
            "Namaste Chief! 🌹 Main ROSE — tumhari personal AI companion. "
            "Maki Zenin mode ON hai. Bolo, kya hukm hai?"
        )
        self._append_chat("🌹 Rose", greeting)
        self.voice_synth.speak(greeting)

    # ── voice toggle ─────────────────────────────────────────────

    def _toggle_voice(self) -> None:
        if self.voice_listener.is_listening:
            self.voice_listener.stop_continuous()
            self.voice_btn.configure(text="🎤 Voice: OFF")
        else:
            self.voice_listener.start_continuous(self._on_voice_text)
            self.voice_btn.configure(text="🎤 Voice: ON")

    def _on_voice_text(self, text: str) -> None:
        self.after(0, self._send_message, text)

    # ── system panel refresh ─────────────────────────────────────

    def _start_monitor_refresh(self) -> None:
        self._refresh_system_panel()

    def _refresh_system_panel(self) -> None:
        snap = self.monitor.snapshot()
        formatted = self.monitor.format_snapshot(snap)
        self.system_text.configure(state="normal")
        self.system_text.delete("1.0", "end")
        self.system_text.insert("1.0", formatted)
        self.system_text.configure(state="disabled")

        # show alerts in chat
        for warning in snap.warnings:
            self._append_chat("🚨 Rose Alert", warning)

        self.after(config.monitor_interval * 1000, self._refresh_system_panel)

    # ── cleanup ──────────────────────────────────────────────────

    def _on_close(self) -> None:
        self.voice_listener.stop_continuous()
        self.voice_synth.stop()
        self.monitor.stop()
        self.destroy()
