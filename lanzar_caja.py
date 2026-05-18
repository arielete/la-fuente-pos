import os
import subprocess
import time
import webview

PROJECT_DIR = r"C:\Users\Arielete\Desktop\caja_registradora"

os.chdir(PROJECT_DIR)

python_exe = os.path.join(PROJECT_DIR, "env", "Scripts", "python.exe")
manage_py = os.path.join(PROJECT_DIR, "manage.py")

server = subprocess.Popen(
    [python_exe, manage_py, "runserver", "127.0.0.1:8000"],
    cwd=PROJECT_DIR,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
)

time.sleep(3)

webview.create_window(
    "LA FUENTE POS",
    "http://127.0.0.1:8000/",
    width=1400,
    height=900,
    resizable=True
)

webview.start()

server.terminate()