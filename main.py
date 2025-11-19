import gui
import clipboard_utils
import translator
import config_manager
import keyboard
import threading
import time

# Global state
is_listening = False
current_hotkey = None
status_callback = None
processing_lock = threading.Lock()

def process_translation():
    """
    Runs the translation logic. This should be called in a separate thread
    to avoid blocking the keyboard hook or causing state issues.
    """
    global processing_lock
    
    # Prevent multiple concurrent translations
    if not processing_lock.acquire(blocking=False):
        return

    try:
        if status_callback:
            status_callback("Translating...", "orange")
        
        # Small delay to ensure user has released keys physically
        time.sleep(0.2)
        
        # Get text
        original_text = clipboard_utils.copy_selection()
        
        if not original_text:
            print("No text selected or clipboard empty.")
            if status_callback:
                status_callback("Error: No text selected", "red")
            return
        
        print(f"Original text: {original_text[:50]}...")
        
        # Translate
        translated_text = translator.translate_text(original_text)
        
        print(f"Translated text: {translated_text[:50]}...")
        
        # Paste
        clipboard_utils.paste_text(translated_text)
        print("Translation pasted.")
        
        if status_callback:
            status_callback("Done!", "green")
            
    except Exception as e:
        print(f"Error: {e}")
        if status_callback:
            status_callback(f"Error: {e}", "red")
    finally:
        processing_lock.release()

def on_hotkey():
    if not is_listening:
        return
    
    # Run in a separate thread to not block the keyboard listener
    # and to allow better control over timing
    threading.Thread(target=process_translation).start()

def toggle_listener(enabled, callback=None):
    global is_listening, current_hotkey, status_callback
    is_listening = enabled
    status_callback = callback
    
    if current_hotkey:
        try:
            keyboard.remove_hotkey(current_hotkey)
        except Exception:
            pass
        current_hotkey = None

    if enabled:
        hotkey_str = config_manager.get_hotkey()
        try:
            # suppress=True blocks the key event from the OS.
            # This is good to prevent the key itself from being typed,
            # but we must ensure we don't block it forever if we crash.
            current_hotkey = keyboard.add_hotkey(hotkey_str, on_hotkey, suppress=True)
            print(f"Listener started. Press {hotkey_str} to translate.")
        except Exception as e:
            print(f"Error setting hotkey: {e}")
            is_listening = False
            if status_callback:
                status_callback(f"Error: {e}", "red")
    else:
        print("Listener stopped.")

def main_app():
    gui.run_gui(toggle_listener)

if __name__ == "__main__":
    main_app()
