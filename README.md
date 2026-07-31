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

## Notes / Known Limitations

- Runs with standard (non-admin) user privileges
- Windows Defender Smart App Control may flag the .exe as unrecognized as the app is unsigned. The only work-around is to disable Smart App Control in Windows Defender application **[Risky]**