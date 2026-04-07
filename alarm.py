import threading
import time
import datetime
import re
from speak import speak

alarms = []

def set_alarm(query):
    now = datetime.datetime.now()
    seconds, minutes, hours = 0, 0, 0

    # Extract time units
    sec_match = re.search(r"(\d+)\s*second", query)
    min_match = re.search(r"(\d+)\s*minute", query)
    hour_match = re.search(r"(\d+)\s*hour", query)

    if sec_match: seconds = int(sec_match.group(1))
    if min_match: minutes = int(min_match.group(1))
    if hour_match: hours = int(hour_match.group(1))

    if seconds == 0 and minutes == 0 and hours == 0:
        return False, "I couldn't find a time duration."

    delta = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours)
    alarm_time = now + delta
    
    # Extract message
    msg = query.replace("remind me", "").replace("to", "", 1).replace("in", "")
    msg = re.sub(r"\d+\s*(second|minute|hour)s?", "", msg).strip()
    if not msg: msg = "Time is up!"

    alarms.append({"time": alarm_time, "msg": msg})
    return True, f"Alarm set for {alarm_time.strftime('%I:%M %p')}."

def _check_loop():
    while True:
        now = datetime.datetime.now()
        for alarm in alarms[:]:
            if now >= alarm["time"]:
                speak(f"Reminder: {alarm['msg']}")
                alarms.remove(alarm)
        time.sleep(1)

def start_alarm_thread():
    t = threading.Thread(target=_check_loop, daemon=True)
    t.start()
    