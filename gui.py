import customtkinter as ctk
import config_manager
import threading
import keyboard
import main
import sys
import os
from PIL import Image, ImageDraw
import pystray

class App(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        
        self.title("Gemini Desktop Translator")
        self.geometry("400x450")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # API Key
        self.api_key_label = ctk.CTkLabel(self.main_frame, text="Gemini API Key:")
        self.api_key_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.api_key_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.api_key_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        # Target Language
        self.lang_label = ctk.CTkLabel(self.main_frame, text="Target Language:")
        self.lang_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.lang_entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g. Portuguese, English")
        self.lang_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Hotkey
        self.hotkey_label = ctk.CTkLabel(self.main_frame, text="Hotkey (e.g., ctrl+shift+x):")
        self.hotkey_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.hotkey_entry = ctk.CTkEntry(self.main_frame, placeholder_text="ctrl+shift+x")
        self.hotkey_entry.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        # Save Button
        self.save_btn = ctk.CTkButton(self.main_frame, text="Save Settings", command=self.save_settings)
        self.save_btn.grid(row=6, column=0, padx=10, pady=10)
        
        # Status
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: Stopped", text_color="red")
        self.status_label.grid(row=7, column=0, padx=10, pady=10)
        
        # Start/Stop Listener
        self.listener_btn = ctk.CTkButton(self.main_frame, text="Start Listener", command=self.toggle_listener)
        self.listener_btn.grid(row=8, column=0, padx=10, pady=10)
        
        self.load_settings()
        self.is_running = False
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tray_icon = None

    def load_settings(self):
        config = config_manager.load_config()
        self.api_key_entry.insert(0, config.get("api_key", ""))
        self.lang_entry.insert(0, config.get("target_language", ""))
        self.hotkey_entry.insert(0, config.get("hotkey", "ctrl+shift+x"))

    def save_settings(self):
        api_key = self.api_key_entry.get().strip()
        target_lang = self.lang_entry.get().strip()
        hotkey = self.hotkey_entry.get().strip()
        
        config = {
            "api_key": api_key,
            "target_language": target_lang,
            "hotkey": hotkey
        }
        config_manager.save_config(config)
        self.set_status("Settings Saved!", "green")
        self.after(2000, lambda: self.update_status_display())

    def set_status(self, text, color=None):
        self.status_label.configure(text=text)
        if color:
            self.status_label.configure(text_color=color)

    def update_status_display(self):
        hotkey = self.hotkey_entry.get().strip()
        if self.is_running:
            self.status_label.configure(text=f"Status: Listening ({hotkey})", text_color="green")
            self.listener_btn.configure(text="Stop Listener")
        else:
            self.status_label.configure(text="Status: Stopped", text_color="red")
            self.listener_btn.configure(text="Start Listener")

    def toggle_listener(self):
        self.is_running = not self.is_running
        self.update_status_display()
        if self.start_callback:
            self.start_callback(self.is_running, self.set_status)
            
    def create_image(self):
        # Generate a simple icon
        width = 64
        height = 64
        color1 = "blue"
        color2 = "white"
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        return image

    def minimize_to_tray(self):
        self.withdraw() # Hide window
        image = self.create_image()
        menu = (pystray.MenuItem('Show', self.show_window), pystray.MenuItem('Exit', self.quit_app))
        self.tray_icon = pystray.Icon("name", image, "Gemini Translator", menu)
        self.tray_icon.run()

    def show_window(self, icon, item):
        self.tray_icon.stop()
        self.after(0, self.deiconify) # Show window

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        self.after(0, self.force_exit)

    def force_exit(self):
        if self.is_running and self.start_callback:
            self.start_callback(False, None)
        self.destroy()
        os._exit(0)

    def on_closing(self):
        # Create a custom dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Exit Options")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self) # Make it modal-like
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="What would you like to do?")
        label.pack(pady=20)
        
        def on_tray():
            dialog.destroy()
            self.minimize_to_tray()
            
        def on_exit():
            dialog.destroy()
            self.force_exit()
            
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Minimize to Tray", command=on_tray).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Exit App", command=on_exit, fg_color="red", hover_color="darkred").pack(side="left", padx=10)

def run_gui(start_callback):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App(start_callback)
    app.mainloop()
