# Keyboard Shortcut Overlay - Capstone Project 2
A desktop overlay that shows lists of shortcuts based on modifier (Ctrl, Shift, etc.) key presses.

## Authors
- @SuahSwag24 (Suah Li Jea Richie)

# How to Run - Keyboard Shortcut Overlay

This guide explains how to run the project either from source code (VS Code) or from a downloaded release package (Releases).

## System Requirements
- **OS:** Windows [10 / 11] (this app relies on `pywin32`, so it is Windows-only)
- **Python:** [3.14.5] (only needed if running from source)
- **Architecture:** [x64 / x86]

## Option 1: Run from Source (VS Code)

### 1. Clone the repository
```bash
git clone https://github.com/SuahSwag24/KeyboardShortcutOverlay.git
cd [REPO_FOLDER_NAME]
```

### 2. Open in VS Code
```bash
code .
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

**Required packages** (also listed in `requirements.txt`):
| Package | Version | Purpose |
|---|---|---|
| PyQt6 | [6.11.0] | GUI overlay rendering |
| pynput | [1.8.2] | Global keyboard hook/listener |
| pywin32 | [312] | Windows API integration |
| psutil | [7.2.2] | Process/window monitoring |

### 4. Run the application
```bash
python main.py
```

[Replace `main.py` with the actual entry-point filename if different]
 
## Option 2: Run from Release Package
 
1. Go to the [Releases page](https://github.com/SuahSwag24/KeyboardShortcutOverlay/releases) of this repository.
2. Download the latest release ZIP: `[KeyboardShortcutOverlay_Release_vX.X.zip]`
3. Choose one of the two package contents:
   - **Pre-built executable:** Extract the ZIP and run `KeyboardShortcutOverlay.exe` directly — no Python installation required.
   - **Source code package:** Extract the ZIP, then follow steps 3-4 under "Option 1" above (install dependencies, run `python main.py`).


## Application Behavior on Startup
 
When executed (either via `python main.py` or the `.exe`), the app does not show a window immediately:
 
1. The app launches and briefly delays before becoming active.
2. Once initialized, it runs silently in the background, listening for modifier key presses (Ctrl, Shift, etc.).
3. No main window is shown — the app waits for user input in this state.
4. When a modifier key is pressed, the shortcut overlay appears as expected; the app continues running normally in the background afterward.
5. A new system tray icon appears and many of the configuration functionality is located in the system tray
> This is expected behavior — the absence of an initial window is not a bug or hang, it's the app entering its listening state.
 
## How to Terminate the Application
 
The app has no visible main window or taskbar entry to close, so it must be exited via the **system tray**:
 
1. Locate the app's icon in the Windows system tray (bottom-right corner, near the clock). It uses the default Windows monitor icon unless a custom icon has been set.
   - If not visible, click the **^** (show hidden icons) arrow in the tray to expand it.
2. **Right-click** the tray icon.
3. Select **Exit** (or the equivalent close/quit option) from the context menu.
> Closing via Task Manager also works as a fallback, but exiting through the tray icon is the intended method.

## Notes / Known Limitations

- Runs with standard (non-admin) user privileges
- Windows Defender Smart App Control may flag the .exe as unrecognized as the app is unsigned. The only work-around is to disable Smart App Control in Windows Defender application **[Risky]**