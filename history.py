from datetime import datetime

FILE = "history.log"

def log(command):
    with open(FILE, "a") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {command}\n")
