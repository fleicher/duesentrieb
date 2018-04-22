"""
main entry point for starting listening server
"""

from typing import Union
import argparse
from duesentrieb.speech import Intent
from duesentrieb.database import InstructionsElement, has_topic
from duesentrieb.speech import say
import duesentrieb.constants
from duesentrieb.constants import CONTROL_CMDS as CMD


def main(be_quiet=None):
    if be_quiet is not None:
        duesentrieb.constants.be_quiet = be_quiet
    while True:
        topic_intent = Intent(announce="")
        topic_name = check_for_search(topic_intent)
        if topic_name is not None and topic_name != "no_entity":
            iterate_through_instructions(topic_name)


def iterate_through_instructions(topic_name):  # type: (str) -> Union[str, None]
    print("start topic", topic_name)
    current_alternative = 0  # pointer to the current alternative that is given to the user (if more than one exist)
    cur_element_id = 0  # pointer to current node in tree
    last_element_id = 0  # pointer to go backwards
    lastlast_element_id = 0  # pointer to go backwards
    speak = True  # True: this while loop will give auditive feedback to the user
    while True:
        element = InstructionsElement(topic_name, cur_element_id, cur_alternative=current_alternative)
        if speak:
            say(element.description)
        speak = True  # reset muting the voice (is only reactivated if the current intent is None

        if 0 in element.fronts:
            return  # reached end of loop

        intent = Intent()

        #############################
        #  iterate through commands #
        #  also see constants.py    #
        #############################
        if intent.is_command(CMD.repeat):
            # repeat this command
            continue
        if intent.is_command(CMD.prev):
            cur_element_id = lastlast_element_id
            continue
        if intent.is_command(CMD.main):
            return
        if intent.is_command(CMD.right):
            # upvoting a description step
            say("Thank you for your good feedback.")
            element.vote_on_element(+1)
            continue
        if intent.is_command(CMD.wrong) or intent.is_command(CMD.alternative):
            # repeat variation of the current command
            current_alternative += 1
            if intent.is_command("wrong"):
                # downvoting a description step
                say("Thank you for your honest feedback.")
                element.vote_on_element(-1)
            continue

        # there are two types of nodes in the description, "statements" and "questions".
        # The former don't branch (there is only one entry in "fronts", the latter do (and for now has two entries)
        if element.type == "statement" and (
                        intent.is_command(CMD.next) or intent.is_command(CMD.right) or intent.is_command(CMD.yes)):
            assert len(element.fronts) == 1
            # update the pointers for the next step
            cur_element_id = element.fronts[0]
            lastlast_element_id = last_element_id
            last_element_id = cur_element_id
            continue
        elif element.type == "question":
            assert len(element.fronts) >= 2
            if intent.intent in element.intents:
                # this is a branching intent, jump to it's id
                n = element.intents.index(intent.intent)
                cur_element_id = element.fronts[n]
                lastlast_element_id = last_element_id
                last_element_id = cur_element_id

        # query if
        res = check_for_search(intent)
        if res is not None:
            # the user has started a new search
            return res

        if intent.intent is None or res == "no_entity":
            # no intent detected, no need to repeat the current step
            speak = False
            continue


def check_for_search(intent):  # type: (Intent) -> Union[str, None]
    if intent.is_command("search"):
        for entity in intent.entities:
            if has_topic(entity["type"]):
                print("there is a new search")
                return entity["type"]
        return "no_entity"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--silent", action="store_true", default=False)
    args = parser.parse_args()
    main(args.silent)
