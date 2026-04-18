import subprocess
import time
import os
import sys

# Get current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Backend path
backend_file = os.path.join(BASE_DIR, "backend", "app.py")

# GUI path
gui_file = os.path.join(BASE_DIR, "frontend", "gui.py")

# Start backend hidden
subprocess.Popen(
    [sys.executable, backend_file],
    creationflags=subprocess.CREATE_NO_WINDOW
)

# Wait for backend to start
time.sleep(2)

# Start GUI
subprocess.Popen([sys.executable, gui_file])