import sys
import time
import random
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from pynput.keyboard import Key
from components.overlay import Overlay

# --- Config ---
RUNS         =  50      # number of test runs
SHOW_DURATION = 100     # ms to keep the overlay visible per run (so you can see it)
HIDE_PAUSE    = 100     # ms to wait after hiding before the next run
# --------------

app = QApplication(sys.argv)
overlay = Overlay()

results = []

modifiers_list = [
    Key.ctrl,
    Key.shift,
    Key.alt,
    Key.cmd
]

def randomize_modifier(modifiers_list):
    return modifiers_list[random.randrange(len(modifiers_list))]

def schedule_next():
    overlay.update_keys(set())   # simulate key release → hides the overlay
    QTimer.singleShot(HIDE_PAUSE, simulate_press)

def simulate_press():
    run_number = len(results) + 1

    test_keys = {randomize_modifier(modifiers_list)}
    print(f"Run {run_number}: pressing modifier {test_keys}...")

    t_start = time.perf_counter()
    overlay.update_keys(test_keys)   # triggers _build_shortcut_list + show()
    t_end = time.perf_counter()

    elapsed_ms = (t_end - t_start) * 1000
    results.append(elapsed_ms)
    print(f"Run {run_number}: overlay shown in {elapsed_ms:.2f} ms")

    if len(results) < RUNS:
        # Keep the overlay visible for SHOW_DURATION ms, then move to next run
        QTimer.singleShot(SHOW_DURATION, schedule_next)
    else:
        # Final run — show results, keep overlay visible briefly, then quit
        avg = sum(results) / len(results)
        print(f"\n--- Results ({RUNS} runs) ---")
        print(f"  Min : {min(results):.2f} ms")
        print(f"  Max : {max(results):.2f} ms")
        print(f"  Avg : {avg:.2f} ms")
        QTimer.singleShot(SHOW_DURATION, app.quit)

# Start first run after a short delay so the window has time to render
QTimer.singleShot(500, simulate_press)
app.exec()