import random

RESPONSES = {
    "ack": [
        "Right away.",
        "Understood.",
        "On it.",
        "As you wish.",
        "Processing."
    ],
    "error": [
        "I didn't quite catch that.",
        "Please repeat the command.",
        "That command is unclear."
    ],
    "default": [
        "Processing..."
    ]
}

def reply(key):
    # If the key exists, pick a random response
    if key in RESPONSES:
        return random.choice(RESPONSES[key])
    else:
        # Fallback so the app doesn't crash
        return random.choice(RESPONSES["default"])