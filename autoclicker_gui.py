#!/usr/bin/env python3
"""
Vibe Clicker - a dark-themed auto clicker with a GUI.

Setup:  pip install pynput
Run:    python autoclicker_gui.py
Hotkey: F6 toggles clicking from anywhere.
"""

import threading
import time
import tkinter as tk

from pynput import keyboard, mouse

BG, CARD, FG, MUTED = "#12121a", "#1c1c28", "#eaeaf5", "#8a8aa5"
ACCENT, STOP = "#7c5cff", "#ff4d6d"


class VibeClicker:
    def __init__(self, root):
        self.root = root
        self.mouse = mouse.Controller()
        self.running = False
        self.count = 0
        self.cps = tk.DoubleVar(value=10)
        self.button = tk.StringVar(value="left")

        root.title("Vibe Clicker")
        root.configure(bg=BG)
        root.geometry("340x420")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        self.build_ui()

        threading.Thread(target=self.click_loop, daemon=True).start()
        self.hotkeys = keyboard.Listener(on_press=self.on_key)
        self.hotkeys.start()
        root.protocol("WM_DELETE_WINDOW", self.close)

    # ---------- UI ----------
    def build_ui(self):
        tk.Label(self.root, text="VIBE CLICKER", bg=BG, fg=FG,
                 font=("Helvetica", 18, "bold")).pack(pady=(24, 2))
        tk.Label(self.root, text="press F6 anywhere to toggle", bg=BG, fg=MUTED,
                 font=("Helvetica", 10)).pack()

        card = tk.Frame(self.root, bg=CARD)
        card.pack(fill="x", padx=24, pady=20, ipady=8)

        self.cps_label = tk.Label(card, bg=CARD, fg=FG, font=("Helvetica", 12))
        self.cps_label.pack(pady=(12, 0))
        tk.Scale(card, from_=1, to=50, orient="horizontal", variable=self.cps,
                 command=self.update_label, bg=CARD, fg=FG, troughcolor=BG,
                 highlightthickness=0, activebackground=ACCENT, showvalue=False,
                 length=240).pack(pady=4)
        self.update_label()

        row = tk.Frame(card, bg=CARD)
        row.pack(pady=(8, 4))
        for name in ("left", "middle", "right"):
            tk.Radiobutton(row, text=name.title(), value=name, variable=self.button,
                           bg=CARD, fg=FG, selectcolor=BG, activebackground=CARD,
                           activeforeground=ACCENT, highlightthickness=0,
                           font=("Helvetica", 10)).pack(side="left", padx=6)

        self.counter = tk.Label(self.root, text="0 clicks", bg=BG, fg=MUTED,
                                font=("Helvetica", 11))
        self.counter.pack()

        self.btn = tk.Button(self.root, text="START", command=self.toggle,
                             bg=ACCENT, fg="white", activebackground=ACCENT,
                             font=("Helvetica", 14, "bold"), relief="flat",
                             bd=0, padx=40, pady=10, cursor="hand2")
        self.btn.pack(pady=18)

    def update_label(self, *_):
        self.cps_label.config(text=f"{int(self.cps.get())} clicks / second")

    # ---------- logic ----------
    def toggle(self):
        self.running = not self.running
        self.btn.config(text="STOP" if self.running else "START",
                        bg=STOP if self.running else ACCENT,
                        activebackground=STOP if self.running else ACCENT)

    def on_key(self, key):
        if key == keyboard.Key.f6:
            self.root.after(0, self.toggle)  # hop back onto the UI thread

    def click_loop(self):
        while True:
            if self.running:
                btn = getattr(mouse.Button, self.button.get())
                self.mouse.click(btn)
                self.count += 1
                self.root.after(0, lambda c=self.count: self.counter.config(text=f"{c:,} clicks"))
                time.sleep(1.0 / max(self.cps.get(), 1))
            else:
                time.sleep(0.02)

    def close(self):
        self.running = False
        self.hotkeys.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    VibeClicker(root)
    root.mainloop()
