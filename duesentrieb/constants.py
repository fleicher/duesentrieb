from enum import Enum
from collections import namedtuple



CONTROL_CMDS = {
    "next": "cmd_next",
    "prev": "cmd_prev",
    "repeat": "cmd_repeat",
    "alternative": "cmd_alternative",
    "wrong": "cmd_wrong",
    "main": "cmd_main"
}

TABLE_CMDS = ["topic_bike", "topic_ikea"]

DB_NAME = "duesentrieb.db"