import customtkinter as ctk
import config_manager
import threading
import keyboard
import main
import sys
import os
import webbrowser
import ctypes
from PIL import Image, ImageDraw
import pystray

class App(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        
        # Fix taskbar icon by setting App User Model ID
        myappid = 'mycompany.myproduct.subproduct.version' # Arbitrary string
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Could not set AUMID: {e}")

        self.title("Gemini Desktop Translator")
        self.geometry("400x550") # Increased height for link
        
        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # API Key
        self.api_key_label = ctk.CTkLabel(self.main_frame, text="Gemini API Key:")
        self.api_key_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.api_key_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.api_key_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
        
        # API Key Link
        self.link_label = ctk.CTkLabel(self.main_frame, text="Get API Key here", text_color="#3399FF", cursor="hand2")
        self.link_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open("https://aistudio.google.com/app/apikey"))
        
        # Target Language
        self.lang_label = ctk.CTkLabel(self.main_frame, text="Target Language:")
        self.lang_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        
        # Top 10+ Languages
        self.languages = [
            "English",
            "Portuguese",
            "Spanish",
            "Chinese (Simplified)",
            "Hindi",
            "French",
            "Arabic",
            "Bengali",
            "Russian",
            "Japanese",
            "German",
            "Italian"
        ]
        
        self.lang_menu = ctk.CTkOptionMenu(self.main_frame, values=self.languages)
        self.lang_menu.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Hotkey
        self.hotkey_label = ctk.CTkLabel(self.main_frame, text="Hotkey:")
        self.hotkey_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.hotkey_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.hotkey_frame.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.hotkey_entry = ctk.CTkEntry(self.hotkey_frame, placeholder_text="Press 'Set' to record")
        self.hotkey_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.set_hotkey_btn = ctk.CTkButton(self.hotkey_frame, text="Set", width=60, command=self.start_recording_hotkey)
        self.set_hotkey_btn.pack(side="right")
        
        # Save Button
        self.save_btn = ctk.CTkButton(self.main_frame, text="Save Settings", command=self.save_settings)
        self.save_btn.grid(row=7, column=0, padx=10, pady=10)
        
        # Status
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: Stopped", text_color="red")
        self.status_label.grid(row=8, column=0, padx=10, pady=10)
        
        # Start/Stop Listener
        self.listener_btn = ctk.CTkButton(self.main_frame, text="Start Listener", command=self.toggle_listener)
        self.listener_btn.grid(row=9, column=0, padx=10, pady=10)
        
        self.load_settings()
        self.is_running = False
        self.is_recording = False
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tray_icon = None

    def load_settings(self):
        config = config_manager.load_config()
        self.api_key_entry.insert(0, config.get("api_key", ""))
        
        saved_lang = config.get("target_language", "English")
        if saved_lang in self.languages:
            self.lang_menu.set(saved_lang)
        else:
            self.lang_menu.set("English")
            
        self.hotkey_entry.insert(0, config.get("hotkey", "ctrl+shift+x"))

    def start_recording_hotkey(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.set_hotkey_btn.configure(text="...", state="disabled")
        self.hotkey_entry.delete(0, "end")
        self.hotkey_entry.insert(0, "Press keys...")
        self.focus()
        
        threading.Thread(target=self.record_hotkey_thread, daemon=True).start()

    def record_hotkey_thread(self):
        try:
            hotkey = keyboard.read_hotkey(suppress=False)
            self.after(0, lambda: self.finish_recording(hotkey))
        except Exception as e:
            print(f"Error recording: {e}")
            self.after(0, lambda: self.finish_recording(None))

    def finish_recording(self, hotkey):
        self.is_recording = False
        self.set_hotkey_btn.configure(text="Set", state="normal")
        
        if hotkey:
            self.hotkey_entry.delete(0, "end")
            self.hotkey_entry.insert(0, hotkey)
        else:
            self.hotkey_entry.delete(0, "end")
            self.hotkey_entry.insert(0, "Error")

    def save_settings(self):
        api_key = self.api_key_entry.get().strip()
        target_lang = self.lang_menu.get()
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
            
    def get_tray_image(self):
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.png")
        if os.path.exists(icon_path):
            return Image.open(icon_path)
        
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
        self.withdraw()
        image = self.get_tray_image()
        menu = (pystray.MenuItem('Show', self.show_window), pystray.MenuItem('Exit', self.quit_app))
        self.tray_icon = pystray.Icon("name", image, "Gemini Translator", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon, item):
        self.tray_icon.stop()
        self.after(0, self.deiconify)

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        self.after(0, self.force_exit)

    def force_exit(self):
        if self.is_running and self.start_callback:
            self.start_callback(False, None)
        self.destroy()
        os._exit(0)

    def on_closing(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Exit Options")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
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
