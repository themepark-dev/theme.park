"""Emit synthetic log levels for local Dozzle screenshots without external services."""
import json
import os
import time
from datetime import datetime, timezone

name = os.environ.get("SAMPLE_NAME", "sample")
for level in ["debug", "info", "warn", "error"]:
    print(json.dumps({"time": datetime.now(timezone.utc).isoformat(), "level": level,
                      "message": f"Synthetic {name} {level} message for theme inspection",
                      "context": {"attempt": 2, "ready": True, "result": None}}))
print("Synthetic multiline message\n    first continuation\n    second continuation")
print("ANSI palette: " + " ".join(f"\033[{color}mColor {color}\033[0m" for color in range(30, 38)))
if os.environ.get("SAMPLE_EXIT") == "true":
    raise SystemExit(1)
sequence = 0
while True:
    sequence += 1
    level = ["info", "warn", "error", "debug"][sequence % 4]
    print(json.dumps({"time": datetime.now(timezone.utc).isoformat(), "level": level,
                      "message": f"Synthetic {name} heartbeat", "sequence": sequence}))
    time.sleep(5)
