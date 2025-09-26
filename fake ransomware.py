"""
Safe Fake Ransomware Simulator — Final update (Glitch unlock, removed cmd/notepad)

Changes in this update per your request:
- Removed the "Open Command Prompt" and "Show me the code to exit" buttons and all related cmd/notepad logic.
- Added an "Activate Glitch" button at the bottom. When clicked it runs a harmless visual "glitch" animation (flicker and jitter)
  and then automatically closes the simulator (simulating the ransomware being removed by a glitch). After the glitch finishes
  the app restores (closes) and does not change any real system files.
- Kept the About window, Decoy code behavior, Exit Ransomware flow, demo unlock button, and emergency override (Ctrl+Shift+U).

Safety reminder: This is a harmless local simulation. It never hides system processes, never deletes files, and never changes
system wallpaper. Use the emergency override if you ever get stuck.

Run with: python fake_ransomware_glitch.py
"""

import tkinter as tk
from tkinter import font, messagebox
import threading
import time
import sys

# === Configuration ===
SECRET_CODE = "4829"        # the real code to unlock the simulator (change as you like)
DECOY_CODE = "0000"         # a decoy code that triggers the "that will not work" message
MAX_ATTEMPTS = 3

class FakeRansomApp:
    def __init__(self, root):
        self.root = root
        self.attempts_left = MAX_ATTEMPTS
        self.locked_forever = False
        self.glitch_running = False

        root.title("Locked")
        root.attributes("-fullscreen", True)
        root.configure(bg="black")
        root.overrideredirect(False)

        root.bind("<Escape>", lambda e: self.show_hint())
        root.bind("<Control-Shift-U>", lambda e: self.emergency_override())

        # Top bar frame to hold the About button (right side)
        top_bar = tk.Frame(root, bg="black")
        top_bar.pack(side="top", fill="x")

        # About button on the right
        about_btn = tk.Button(top_bar, text="About", command=self.open_about, font=font.Font(size=12))
        about_btn.pack(side="right", padx=12, pady=8)

        # Main center content
        frame = tk.Frame(root, bg="black")
        frame.pack(expand=True)

        lock_font = font.Font(size=120)
        lock_label = tk.Label(frame, text="🔒", font=lock_font, bg="black", fg="white")
        lock_label.pack(pady=(10, 0))

        msg_font = font.Font(size=18)
        self.msg = tk.Label(frame,
                            text=(
                                "Your computer has been locked.\n"
                                "All desktop features are simulated as disabled.\n"
                                "Your files are safe and unchanged.\n\n"
                                "Enter the unlock code to restore your desktop."
                            ),
                            font=msg_font,
                            bg="black", fg="white", justify="center")
        self.msg.pack(pady=(10, 20))

        # Entry and submit
        entry_frame = tk.Frame(frame, bg="black")
        entry_frame.pack()

        code_label = tk.Label(entry_frame, text="Enter code:", bg="black", fg="white", font=font.Font(size=14))
        code_label.grid(row=0, column=0, padx=(0,8))

        self.code_var = tk.StringVar()
        self.code_entry = tk.Entry(entry_frame, textvariable=self.code_var, show="*", font=font.Font(size=14))
        self.code_entry.grid(row=0, column=1)
        self.code_entry.focus_set()

        submit_btn = tk.Button(entry_frame, text="Unlock", command=self.check_code, font=font.Font(size=12))
        submit_btn.grid(row=0, column=2, padx=(8,0))

        # Area for dynamic secondary controls (created when Exit clicked)
        self.secondary_frame = tk.Frame(frame, bg="black")
        self.secondary_frame.pack(pady=(20,0))

        # Bottom controls: Exit Ransomware and Activate Glitch
        bottom_frame = tk.Frame(root, bg="black")
        bottom_frame.pack(side="bottom", fill="x", pady=12)

        self.exit_btn = tk.Button(bottom_frame, text="Exit Ransomware", command=self.exit_ransom, font=font.Font(size=12))
        self.exit_btn.pack(side="left", padx=12)

        self.glitch_btn = tk.Button(bottom_frame, text="Activate Glitch", command=self.activate_glitch, font=font.Font(size=12))
        self.glitch_btn.pack(side="right", padx=12)

        # Info area at bottom
        self.info_label = tk.Label(root,
                                   text=f"Attempts left: {self.attempts_left}",
                                   bg="black", fg="white", font=font.Font(size=14))
        self.info_label.pack(side="bottom")

        # Demo and emergency controls to ensure safety
        demo_btn = tk.Button(root, text="Simulate correct code (demo)", command=self.correct_code, font=font.Font(size=10))
        demo_btn.pack(side="bottom", pady=(0,6))

    # --- About window ---
    def open_about(self):
        # Small toplevel window (has its own close X)
        about = tk.Toplevel(self.root)
        about.title("About")
        about.geometry("400x220")
        about.configure(bg="black")

        label = tk.Label(about, text="About this fake ransomware simulator", font=font.Font(size=14), bg="black", fg="white")
        label.pack(pady=(10,6))

        text = ("This is a harmless simulation for demo/learning purposes.\n\n"
                "- It does NOT delete or modify your files.\n"
                "- It does NOT hide system processes or change your real wallpaper.\n"
                "- You can still use Task Manager and other OS features.\n\n"
                "Close this window with the X in the corner.")
        body = tk.Label(about, text=text, font=font.Font(size=11), bg="black", fg="white", justify="left")
        body.pack(padx=12)

    # --- Code checking ---
    def check_code(self):
        entered = self.code_var.get().strip()
        if entered == SECRET_CODE:
            self.correct_code()
            return
        if entered == DECOY_CODE:
            messagebox.showwarning("Nope", "That will not work. Try again.")
            self.code_var.set("")
            self.code_entry.focus_set()
            return

        self.attempts_left -= 1
        self.info_label.config(text=f"Attempts left: {self.attempts_left}")
        if self.attempts_left <= 0:
            self.lock_forever_simulation()
        else:
            messagebox.showwarning("Wrong code", f"Incorrect code. {self.attempts_left} attempts left.")
            self.code_var.set("")
            self.code_entry.focus_set()

    def correct_code(self):
        messagebox.showinfo("Unlocked", "Correct code entered. Desktop restored (simulation).")
        self.root.destroy()

    def lock_forever_simulation(self):
        self.msg.config(text="Too many incorrect attempts.\nThis machine is now locked (simulation).")
        self.code_entry.config(state="disabled")
        self.info_label.config(text="Attempts left: 0")
        self.locked_forever = True
        messagebox.showerror("Simulation Lock", "Simulation entered locked state. Use Ctrl+Shift+U to force unlock (developer override).")

    def emergency_override(self):
        if messagebox.askyesno("Emergency override", "Force unlock simulation and exit?"):
            self.root.destroy()

    def show_hint(self):
        messagebox.showinfo("Hint", "This is a harmless simulation. Press Ctrl+Shift+U to force unlock if needed.")

    # --- Exit Ransomware flow ---
    def exit_ransom(self):
        # Display the taunting message and create an input area where the user can try a key
        messagebox.showinfo("Exit attempt", "ha ha ha, you cannot get rid of me now. Enter the key in the box below.")
        # Clear any old widgets
        for w in self.secondary_frame.winfo_children():
            w.destroy()

        key_label = tk.Label(self.secondary_frame, text="Enter exit key:", bg="black", fg="white")
        key_label.pack(side="left")
        self.exit_key_var = tk.StringVar()
        exit_entry = tk.Entry(self.secondary_frame, textvariable=self.exit_key_var, show="*")
        exit_entry.pack(side="left", padx=(6,6))
        exit_btn = tk.Button(self.secondary_frame, text="Try Key", command=self.try_exit_key)
        exit_btn.pack(side="left")

    def try_exit_key(self):
        key = getattr(self, 'exit_key_var', tk.StringVar()).get().strip()
        if key == SECRET_CODE:
            self.correct_code()
        elif key == DECOY_CODE:
            messagebox.showwarning("Nope", "That will not work. Try again.")
        else:
            messagebox.showerror("Wrong", "Wrong key. You are still locked (simulation).")

    # --- Glitch animation and unlock ---
    def activate_glitch(self):
        if self.glitch_running:
            return
        self.glitch_running = True
        # disable buttons to avoid repeated clicks
        self.glitch_btn.config(state="disabled")
        self.exit_btn.config(state="disabled")
        # Start a quick visual glitch sequence using after callbacks
        self._glitch_steps = 0
        self._start_glitch()

    def _start_glitch(self):
        # Simple glitch: rapid background color changes and small window shakes
        max_steps = 18
        if self._glitch_steps >= max_steps:
            # end glitch: restore and close
            self.msg.config(text="A glitch occurred... Cleaning up.\nRestoring desktop now.")
            self.root.after(800, self.correct_code)
            return

        # flicker backgrounds and jitter
        if self._glitch_steps % 3 == 0:
            bg = "black"
            fg = "white"
        elif self._glitch_steps % 3 == 1:
            bg = "#111111"
            fg = "#e6e6e6"
        else:
            bg = "#000000"
            fg = "#cccccc"

        # apply colors to main widgets
        self.root.configure(bg=bg)
        for w in [self.msg, self.info_label]:
            try:
                w.config(bg=bg, fg=fg)
            except Exception:
                pass

        # small window shake by moving geometry (works on some platforms)
        try:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            offset = (-6 if (self._glitch_steps % 2 == 0) else 6)
            self.root.geometry(f"+{max(0,x+offset)}+{max(0,y)}")
        except Exception:
            pass

        self._glitch_steps += 1
        # schedule next step faster for a glitchy feel
        self.root.after(60, self._start_glitch)


def main():
    root = tk.Tk()
    app = FakeRansomApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
