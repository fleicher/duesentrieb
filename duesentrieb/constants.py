from enum import Enum
from collections import namedtuple


CONTROL_CMDS = {
    "next": "cmd_next",
    "prev": "cmd_prev",
    "repeat": "cmd_repeat",
    "alternative": "cmd_alternative",
    "wrong": "cmd_wrong",
    "right": "cmd_right",
    "main": "cmd_main",

    "yes": "cmd_yes",
    "no": "cmd_no",
}

DB_NAME = "duesentrieb.db"