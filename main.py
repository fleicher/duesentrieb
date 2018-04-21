from typing import Union

from duesentrieb.speech import Intent
from duesentrieb.database import Element, has_topic
from duesentrieb.speech import say

USE_SPEECH = True


def main_menu():
    while True:

        topic_intent = Intent(use_speech=USE_SPEECH, anounce="")
        topic_name = checkmainmenu(topic_intent)
        if topic_name is not None:
            recipe(topic_name)


def recipe(topic_name):  # type: (str) -> Union[str, None]
    print("start topic", topic_name)
    cur_rank = 0
    cur_element_id = 0
    last_element_id = 0
    lastlast_element_id = 0
    while True:
        element = Element(topic_name, cur_element_id, rank=cur_rank)
        say(element.description)
        if 0 in element.fronts:
            return  # reached end of loop

        intent = Intent(use_speech=USE_SPEECH)
        if intent.intent is None:
            # no intent detected.
            continue
        if intent.isCommand("repeat"):
            continue
        if intent.isCommand("prev"):
            cur_element_id = lastlast_element_id
            continue
        if intent.isCommand("main"):
            return

        if intent.isCommand("right"):
            say("Good that you like this description")
            element.addRang(+1)
            continue

        if intent.isCommand("wrong") or intent.isCommand("alternative"):
            cur_rank += 1
            if intent.isCommand("wrong"):
                say("Ok, I will try again")
                element.addRang(-1)
            continue

        if element.type == "statement" and (intent.isCommand("next") or intent.isCommand("right") or intent.isCommand("yes")):
            assert len(element.fronts) == 1
            cur_element_id = element.fronts[0]
            lastlast_element_id = last_element_id
            last_element_id = cur_element_id
            continue
        elif element.type == "question":
            if intent.intent in element.intents:
                # this is a branching intent, jump to it's id
                n = element.intents.index(intent.intent)
                cur_element_id = element.fronts[n]
                lastlast_element_id = last_element_id
                last_element_id = cur_element_id

        res = checkmainmenu(intent)
        if res is not None:
            return res


def checkmainmenu(intent):  # type: (Intent) -> Union[str, None]
    if intent.isCommand("search"):
        for entity in intent.entities:
            if has_topic(entity["type"]):
                return entity["type"]


if __name__ == "__main__":
    main_menu()
