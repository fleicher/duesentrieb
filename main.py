from duesentrieb.speech import Intent
from duesentrieb.database import Element, has_topic
from duesentrieb.speech import say

USE_SPEECH = True

def main_menu():

    while True:

        topic = Intent(use_speech=USE_SPEECH, anounce="")
        if has_topic(topic.intent):
            recipe(topic.intent)


def recipe(topic_name):  # type: (str) -> None
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


if __name__ == "__main__":
    main_menu()
