# Setup and Running

`README.md` is the lab handout. This file only covers getting the code running.

###IMPORTANT###
 PLEASE ONLY RUN FILES INSIDE OF THE TERMINAL. IDLE WILL ERROR.

## One-time setup

1. Install Ollama (free, runs on your laptop): https://ollama.com/download
2. Download a small model (once): `ollama pull llama3.2`
   Check the exact name with `ollama list`, and put it in `MODEL_NAME` in `llm_ollama.py` if it is different.

3. Install the Python packages: `pip install -r requirements.txt` (`pip3` if on Mac)
4. Set `ROBOT_NAME` near the top of `main.py` to the name of your robot.


# How to run files from the Terminal:
   1. Open the Terminal app
   2. Use cd followed by the folder’s path. The easiest way is to type cd (with a space after it) and then drag the folder from Finder/File Explorer into the Terminal window. That fills in the path for you. Press Enter. For example: cd ~/Documents/Lab3
   3. Type `ls`, then press enter to see the files that are in your folder.
   4. Once you see the file you want to run, type `python main.py` (for example we ran the file called main here)

# If there are errors on Mac:
If the error mentions the microphone, audio, or sounddevice:

1. Open System Settings, then Privacy & Security, then Microphone.
2. Turn on the app you run the lab from (Terminal, IDLE, VS Code, or PyCharm, whichever you use).
3. Quit that app completely (Cmd+Q) and reopen it. The permission only takes effect after a restart.

# If whisper is slow:
1. Go to the file `stt_whisper.py` and change the _model variable from "base" to "tiny"


## Replies from the LLM not popping up?
1. Make sure you're running main.py from the terminal (See above)

## Running a test for whisper
Once you've done the One-time setup above, you can run a test for whisper inside of the terminal.
1. cd into your Lab 3 folder
2. Type `python test_whisper.py` (`python3` if on Mac) and press enter
3. You should see text that explains what to do in order to test your voice



## Rules
- `voice_helpers.py` may only import from the Python standard library.
- Do not edit anything inside a big `### DO NOT EDIT` banner.
- Do not import `sounddevice` or `whisper` in `main.py`. Speech recognition runs in its own process because they conflict with the robot's Bluetooth library on Windows.
