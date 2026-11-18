"""
voice_helpers.py

Pure (non-async) helper functions for Lab 3: Voice-Controlled Navigation.

IMPORTANT: This file is imported by the Gradescope autograder, so it may only
import from the Python standard library. Do not import robot, whisper, or
sounddevice code here.
"""


################################################################################
################################################################################
###                                                                          ###
###   !!!  DO NOT EDIT ANYTHING BELOW THIS LINE  !!!                         ###
###                                                                          ###
###   These constants are provided. Do not edit them.                        ###
###   Do NOT change, delete, rename, move, or reformat anything              ###
###   between this banner and the matching END banner.                       ###
###   Changing it can break the lab. Edit only the TODO sections.            ###
###                                                                          ###
################################################################################
################################################################################

DEFAULT_DISTANCE_CM = 15.0
DEFAULT_ANGLE_DEG = 90.0
MAX_HISTORY_MESSAGES = 6

################################################################################
################################################################################
###                                                                          ###
###   !!!  END OF THE 'DO NOT EDIT' SECTION  !!!                             ###
###   You may edit again below this line.                                    ###
###                                                                          ###
################################################################################
################################################################################

# Prompt Design: replace this with your own system prompt.
SYSTEM_PROMPT = "TODO: write your system prompt (see Prompt Design in the handout)."

# TODO: add any constants or lookup tables you need below (for example,
# number words and unit conversions).
convdict = {"cm":1, "m":100, "f":30.48, "i":2.54}
units = {"centimeters": "cm", "centimeter": "cm", "cm":"cm", 'meters' :' m' ,
         'meter':'m', 'm':'m', 'feet':'f', 'foot':'f', 'inches':'i','inch':'i', 'in':'i'}
nums = {"one":1, 'two':2, "three":3, 'four':4, "five":5, "six":6, "seven":7, 'eight':8, 'nine':9, 'ten':10, 'ninety':90.0}

################################################################################
################################################################################
###                                                                          ###
###   RULES FOR THE FUNCTIONS BELOW                                          ###
###   - Do NOT rename any function or change its parameters.                 ###
###   - Once you complete a function delete "raise NotImplementedError"
###                                                                          ###
################################################################################
################################################################################


def extractDistance(text):
    unit = ''
    num = 0
    for word in text.lower().split():
        if word.isdigit():
            num = float(word)
        elif word in nums:
            num = nums[word]
        if word in units:
            unit = units[word]
            break
    if num:
        if unit:
            return round(num * convdict[unit],2)
        return round(num,2)
    return None


def extractAngle(text):
    for word in text.lower().split():
        if word == "around":
            return 180.0
        elif word.isdigit():
            return float(word)
        elif word in nums:
            return nums[word]
    return None

def parseActions(reply):
    reply.replace(";", "|")
    reply.replace("\n", "|")
    steps = reply.split("|")
    rlist = []
    for step in steps:
        #steps is a string
        words = step.split()
        for i in len(words):
            word = words[i].strip(".,!?")
            if word.upper() == " FORWARD" or word.upper() == "BACKWARD":
                dist = extractDistance(steps)
                rlist.append((word.upper(), dist))
                break
            if word.upper() == "LEFT" or word.upper() == "RIGHT":
                angle = extractAngle(steps)
                rlist.append(word.upper(), angle)
                break
            if word.upper() == "STOP":
                rlist.append(word.upper(), None)
                break
    return rlist



        
        
    # TODO: implement this function.
    # Hint: reply.replace(";", "|") turns every ; into |. Do the same for the newline "\n".
    # Hint: reply.split("|") then gives you the steps. Loop through them.
    # Hint: step.split() gives the words of a step. word.strip(".,!?") removes punctuation
    #       from the ends of a word. Compare word.upper() to each action name.
    raise NotImplementedError


def validateAction(action, value, maxDistance, maxAngle):

    # TODO: implement this function.
    # Hint: handle unknown actions and STOP first, then fill in defaults, then clamp.
    raise NotImplementedError


def buildPrompt(history, heardText):
    # TODO: implement this function.
    # Hint: Look at the Handout section that has this helper function. Examples are written there.
    raise NotImplementedError


def describeBump(bumpLeft, bumpRight):
    # TODO: implement this function.
    # Hint: check the "both" case before the single-side cases.
    raise NotImplementedError
