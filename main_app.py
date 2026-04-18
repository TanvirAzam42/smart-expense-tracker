import threading
import time
import os
import sys

# ---------------- BACKEND ----------------
def run_backend():
    from backend.app import app, init_db

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

# Start backend in background thread
threading.Thread(target=run_backend, daemon=True).start()

# Wait for backend startup
time.sleep(2)

# ---------------- START GUI ----------------
import frontend.gui