from collections import namedtuple
CONTROL_CMDS = namedtuple("Commands", [
    "next",  # command to go to next step of instructions
    "prev",  # command to go to previous step of instructions
    "repeat",  # command to listen again to current step
    "alternative",  # command to listen to an alternative explanation of this step
    "wrong",  # command to mark an explanation as having an error
    "right",  # command to upvote an explanation
    "main",  # command to end explanations
    "yes",  # command 'yes' for answering questions
    "no",  # command 'no' for answering questions
    "search",  # command to search for a new instructions in the database
])(next="cmd_next", prev="cmd_prev", repeat="cmd_repeat", alternative="cmd_alternative", wrong="cmd_wrong",
   right="cmd_right", yes="cmd_yes", search="search", main="cmd_main", no="cmd_no")
# dict matching the internal representation of the commands representation of in LUIS intents

DB_NAME = "duesentrieb.db"  # absolute path of sqlite database with the instruction steps
be_quiet = False  # True: use text input, False: speech input (can be overwritten by command line arguments)

LISTEN_TIMEOUT = 10  # seconds before speech interface is reset
# (can't be too long as otherwise the Text2Speech processor takes to long to handle an audio file)
LISTEN_SILENCE = 5  # seconds of silence after a command so it can be sent

INTENT_CERTAINTY_THESHOLD = 0.6
