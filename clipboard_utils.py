import pyperclip
import keyboard
import time
import platform

# Determine the copy/paste keys based on OS
IS_MAC = platform.system() == 'Darwin'
CTRL_KEY = 'command' if IS_MAC else 'ctrl'

def release_modifiers():
    """
    Explicitly releases modifier keys to prevent interference.
    """
    modifiers = ['ctrl', 'shift', 'alt', 'right ctrl', 'right shift', 'right alt', 'win']
    for key in modifiers:
        try:
            if keyboard.is_pressed(key):
                keyboard.release(key)
        except:
            pass

def copy_selection():
    """
    Simulates Ctrl+C to copy selected text.
    """
    release_modifiers()
    
    original_clipboard = pyperclip.paste()
    pyperclip.copy("") 
    
    # Use send with a slight delay to ensure clean press/release
    keyboard.send(f'{CTRL_KEY}+c')
    
    time.sleep(0.3) # Wait for OS to process copy
    
    copied_text = pyperclip.paste()
    
    if not copied_text:
        pyperclip.copy(original_clipboard)
        return None
        
    return copied_text

def paste_text(text):
    """
    Puts text into clipboard and simulates Ctrl+V to paste it.
    """
    pyperclip.copy(text)
    time.sleep(0.3) # Wait for clipboard update
    
    release_modifiers()
    
    # Explicitly press and release to avoid stuck keys
    keyboard.press(CTRL_KEY)
    keyboard.press('v')
    time.sleep(0.05)
    keyboard.release('v')
    keyboard.release(CTRL_KEY)
    
    # Final safety release of everything
    time.sleep(0.1)
    release_modifiers()

def restore_clipboard(text):
    pyperclip.copy(text)
