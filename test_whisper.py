"""
test_whisper.py

Tests the microphone and Whisper by themselves. No robot, no Ollama, and no
Bluetooth are needed.

Run it with:   python3 test_whisper.py      (on Windows: python test_whisper.py)

Press Enter, speak for about 4 seconds, and read what Whisper heard.
Type q and press Enter to quit.
"""

import time

# Importing this loads the Whisper model (this can take a few minutes the
# first time, because the model has to download).
from stt_whisper import listen_and_transcribe, RECORD_SECONDS

print("")
print("Whisper test. You will have " + str(RECORD_SECONDS) + " seconds to speak each time.")
print("Try things like: forward 40 centimeters, turn left 45 degrees, do that again.")

while True:
    choice = input("\nPress Enter to record (or type q to quit): ")
    if choice.strip().lower() == "q":
        break

    start = time.time()
    heard = listen_and_transcribe()
    elapsed = time.time() - start

    print("Whisper heard: " + repr(heard))
    print("Total time: " + str(round(elapsed, 1)) + " seconds")

print("Done.")
