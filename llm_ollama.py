"""
llm_ollama.py  (PROVIDED - you do not need to edit this, except MODEL_NAME)

Sends a list of chat messages to a locally running Ollama model and returns
the reply text. The system prompt and conversation history are built in
voice_helpers.buildPrompt(), not here.

Requirements:
    - Ollama installed and running (https://ollama.com)
    - A model pulled once, e.g.  ollama pull llama3.2
    - Check the exact name with:  ollama list
"""

# You may edit ONLY this one line (it must match a name from `ollama list`):
MODEL_NAME = "llama3.2"

################################################################################
################################################################################
###                                                                          ###
###   !!!  DO NOT EDIT ANYTHING BELOW THIS LINE  !!!                         ###
###                                                                          ###
###   Everything below is provided. Do not edit it.                          ###
###   Do NOT change, delete, rename, move, or reformat anything              ###
###   between this banner and the matching END banner.                       ###
###   Changing it can break the lab. Edit only the TODO sections.            ###
###                                                                          ###
################################################################################
################################################################################

import ollama




def ask_llm(messages):
    """messages: list of {"role": ..., "content": ...} dicts."""
    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
        options={"num_predict": 80},  # replies are short, so cap the length
        keep_alive="30m",             # keep the model loaded between commands
    )
    reply = response["message"]["content"].strip()
    print(f"[LLM] Reply: \"{reply}\"")
    return reply

################################################################################
################################################################################
###                                                                          ###
###   !!!  END OF THE 'DO NOT EDIT' SECTION  !!!                             ###
###   You may edit again below this line.                                    ###
###                                                                          ###
################################################################################
################################################################################
