# Gemini Desktop Translator

A lightweight desktop application that allows you to translate selected text anywhere on your screen using Google's Gemini API.

## Features

*   **Global Hotkey**: Select text in any application (Browser, Notepad, IDE, etc.) and press the hotkey to translate it instantly.
*   **In-Place Translation**: The selected text is replaced by the translation.
*   **Configurable**: Set your own API Key, Target Language, and Custom Hotkey via a modern GUI.
*   **System Tray Support**: Minimize the app to the system tray to keep it running in the background without cluttering your taskbar.
*   **Smart Clipboard Handling**: Automatically handles clipboard operations and prevents stuck keys.

## Prerequisites

*   **Python 3.x**
*   **Google Gemini API Key**: Get one for free at [Google AI Studio](https://aistudio.google.com/).

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/6u5t4v05ouz4/gemini-desktop-tradutor.git
    cd gemini-desktop-tradutor
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Application**:
    *   Double-click `Iniciar Tradutor.bat` (Windows).
    *   Or run via terminal: `python main.py`.

2.  **Configuration**:
    *   **API Key**: Paste your Gemini API Key.
    *   **Target Language**: Enter the language you want to translate to (e.g., "Portuguese", "English", "Spanish").
    *   **Hotkey**: Set your preferred shortcut (Default: `ctrl+shift+x`).
    *   Click **Save Settings**.

3.  **Start Translating**:
    *   Click **Start Listener**.
    *   Select text in any app.
    *   Press your hotkey.
    *   Watch the text transform!

## Troubleshooting

*   **"₢" or strange characters**: This usually means a hotkey conflict (common with `Ctrl+Alt+T`). Try changing the hotkey to `F9` or `Ctrl+Shift+Z`.
*   **Browser Console Opens**: If using `Ctrl+Shift+...` hotkeys, the app now automatically handles modifier release to prevent triggering browser dev tools.

## License

This project is open source. Feel free to modify and distribute.
