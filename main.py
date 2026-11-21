"""
main.py  (Lab 3: Voice-Controlled Navigation)

How it works: microphone, then Whisper (in a separate process), then Ollama,
then YOUR parsing and validation code, then robot movement.

Sections surrounded by big ### banners that say DO NOT EDIT are provided and
already work. Leave them exactly as they are. The sections marked TODO are
yours to write.

Run with:  python main.py     (Ctrl+C to stop)
"""

import asyncio
import atexit
import os
import subprocess
import sys
import traceback

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import Create3, event

from llm_ollama import ask_llm
from voice_helpers import (
    buildPrompt,
    describeBump,
    parseActions,
    validateAction,
)

# ---------------------------------------------------------------------------
# Settings (YOU edit these)
# ---------------------------------------------------------------------------
ROBOT_NAME = "YUCHAN-BOT"   # change to the name of YOUR robot

# TODO: choose these yourself and justify them in your design report.
MAX_DISTANCE_CM = 150          # largest single FORWARD/BACKWARD move allowed
MAX_ANGLE_DEG = 180            # largest single LEFT/RIGHT turn allowed
MAX_ACTIONS_PER_COMMAND = 6  # most actions one spoken command may run


# ---------------------------------------------------------------------------
# Shared state (YOU may add more variables here)
# ---------------------------------------------------------------------------
emergency_stopped = False      # set to True by handleEmergency
last_bump = (False, False)     # (left bumper, right bumper) at the last bump
history = []                   # list of {"role": ..., "content": ...} dicts

################################################################################
################################################################################
###                                                                          ###
###   !!!  DO NOT EDIT ANYTHING BELOW THIS LINE  !!!                         ###
###                                                                          ###
###   Robot connection and speech/LLM helpers are provided.                  ###
###   Do NOT change, delete, rename, move, or reformat anything              ###
###   between this banner and the matching END banner.                       ###
###   Changing it can break the lab. Edit only the TODO sections.            ###
###                                                                          ###
################################################################################
################################################################################

robot = Create3(Bluetooth(ROBOT_NAME))

# Speech-to-text runs in its own process, because sounddevice conflicts with
# the robot's Bluetooth library on Windows.
_here = os.path.dirname(os.path.abspath(__file__))
stt_process = subprocess.Popen(
    [sys.executable, "-u", os.path.join(_here, "stt_whisper.py")],
    cwd=_here,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    encoding="utf-8",
    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
)
atexit.register(stt_process.terminate)


def _get_speech_blocking():
    """Ask the STT worker to listen once and return what it heard."""
    stt_process.stdin.write("\n")
    stt_process.stdin.flush()
    while True:
        line = stt_process.stdout.readline()
        if line == "":
            raise RuntimeError("The speech-to-text process stopped unexpectedly.")
        line = line.rstrip("\n")
        if line.startswith("HEARD:"):
            return line[len("HEARD:"):].strip()
        print(line)  # status messages from the worker


async def getSpokenCommand():
    """Listens once and returns the text (empty string if nothing was heard)."""
    return await asyncio.to_thread(_get_speech_blocking)


async def askModel(messages):
    """Sends the messages to Ollama and returns the reply text."""
    return await asyncio.to_thread(ask_llm, messages)

################################################################################
################################################################################
###                                                                          ###
###   !!!  END OF THE 'DO NOT EDIT' SECTION  !!!                             ###
###   You may edit again below this line.                                    ###
###                                                                          ###
################################################################################
################################################################################

# Implementation for fail safe in robot!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (below is the code)
""" 
this calls handle emergency when the one of the buttons has been presssed
"""
#part of handleEmergency
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    print("Button Has Been Pressed")
    await handleEmergency(robot)

"""
this calls the fucntion handle emergy if the left bumper has beeen pressed
"""
#part of handleEmergency
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_either_bumped(robot):
    global last_bump
    print("The LEFT buttom has been pressed")
    last_bump = (True, False)
    await handleEmergency(robot)

"""
this calls the fucntion handle emergency when the right bumper has been pressed
"""
#part of handleEmergency
@event(robot.when_bumped, [False, True]) #when right bumper has been pressed
async def when_either_bumped(robot):
    global last_bump
    print("The RIGHT bumper has been pressed")
    last_bump = (False, True)
    await handleEmergency(robot)
"""
this calls the function handle emergency when both of the bumpers have been pressed 
"""
#part of handleEmergency
@event(robot.when_bumped, [True, True]) #when both bumpers have been pressed
async def when_either_bumped(robot):
    global last_bump
    print("Both bumpers have been pressed")
    last_bump = (True, True)
    await handleEmergency(robot)


# ---------------------------------------------------------------------------
# TODO: Async Function 1 - handleEmergency
# ---------------------------------------------------------------------------
async def handleEmergency(robot):
    global emergency_stopped
    """
    Fail-safe that stops the robot immediately when something goes wrong.

    - Stop the wheels and set a solid red light.
    - Record that an emergency happened (the global emergency_stopped).
    - For bumper events, also save which bumpers were pressed in last_bump.
    """ 

    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_on_rgb(255, 0, 0)
    emergency_stopped = True
    #last_bump is being set in the functions just above when the bumbers are pressed
    #check the code above because that is also apart of step 2
# ---------------------------------------------------------------------------
# TODO: Async Function 2 - executeAction
# ---------------------------------------------------------------------------
async def executeAction(robot, action, value):
    global MAX_DISTANCE_CM #150 cm
    global MAX_ANGLE_DEG #180 degrees

    """
    Performs ONE already-validated action.

    FORWARD:  drive value centimeters forward
    BACKWARD: drive value centimeters in reverse
    LEFT:     turn left in place by value degrees
    RIGHT:    turn right in place by value degrees
    STOP:     stop the wheels

    If an emergency has been recorded, do nothing.
    """
    if emergency_stopped:
            return

    
    if action == "STOP": # this going to stop the robot
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_on_rgb(0, 255, 0)

    if action == "FORWARD":
        if value < MAX_DISTANCE_CM:
            await robot.move(value)
        else:
            await robot.move(MAX_DISTANCE_CM)
    elif action == "BACKWARD":
        if value < MAX_DISTANCE_CM:
            newValue = -1 * value
            await robot.move(newValue)
        else:
            newValue = -1 * MAX_DISTANCE_CM
            await robot.move(newValue)
    elif action == "LEFT":
        if value < MAX_ANGLE_DEG:
            await robot.turn_left(value)
        else:
            await robot.turn_left(MAX_ANGLE_DEG)
    elif action == "RIGHT": 
        if value < MAX_ANGLE_DEG:
            await robot.turn_right(value)
        else:
            await robot.turn_right(MAX_ANGLE_DEG)


# ---------------------------------------------------------------------------
# TODO: Main Routine - voiceControl
# ---------------------------------------------------------------------------
async def voiceControl(robot):
    """
    Parameters: robot (object)
    Returns: None

    Description: The high-level loop that combines everything. On each
    pass it should:

      1. Get the next spoken command from the speech-to-text worker.
      2. If there was a recent bump, add describeBump()'s note to the
         message and clear the emergency so the robot can move again.
      3. Build the messages with buildPrompt() and ask the language model.
      4. Convert the reply with parseActions(), then clean each action
         with validateAction().
      5. Run the valid actions in order with executeAction(). If an
         emergency occurs partway, drop the remaining actions.
      6. Add the person's message and the model's reply to the history.
      7. If the reply contained no usable actions, print a message and
         listen again. The robot must not move.

    Wrap the loop body in try and except so one bad reply or error does
    not end the session. Choose the maximum distance and angle yourself
    and limit how many actions one reply can run.

    Remember: to change a global variable inside a function you need the
    `global` keyword.
    """
    print("Voice control is active. Press Ctrl+C to stop.")
    # TODO: implement this function.
    while True:
        try:
            pass  ####Your Code here!###
        except Exception:
            traceback.print_exc()
            print("[MAIN] Something went wrong (see error above). Listening again...")



################################################################################
################################################################################
###                                                                          ###
###   !!!  DO NOT EDIT ANYTHING BELOW THIS LINE  !!!                         ###
###                                                                          ###
###   Starting the program is provided.                                      ###
###   Do NOT change, delete, rename, move, or reformat anything              ###
###   between this banner and the matching END banner.                       ###
###   Changing it can break the lab. Edit only the TODO sections.            ###
###                                                                          ###
################################################################################
################################################################################

# Starts voiceControl once the robot is connected.
@event(robot.when_play)
async def play(robot):
    await voiceControl(robot)


robot.play()

################################################################################
################################################################################
###                                                                          ###
###   !!!  END OF THE 'DO NOT EDIT' SECTION  !!!                             ###
###   You may edit again below this line.                                    ###
###                                                                          ###
################################################################################
################################################################################
