from duesentrieb.intents import Intent
from duesentrieb.constants import TABLE_CMDS
from duesentrieb.database import Element


def main_menu():
    while True:

        cmd = input("Enter next command.")
        topic = Intent(cmd)
        print(topic.intent)
        if topic.intent in TABLE_CMDS:
            recipe(topic)


def recipe(topic):  # type: (Intent) -> None
    print("start topic", topic.intent)
    cur_element_id = 0
    while True:
        element = Element(topic.intent, cur_element_id)
        print(element.description)

        cmd = input("Enter next command")
        intent = Intent(cmd)

        if intent.isCommand("repeat"):
            continue
        if intent.isCommand("prev"):
            cur_element_id = element.back
            continue
        if intent.isCommand("main"):
            return

        if element.type == "statement" and intent.isCommand("next"):
            assert len(element.fronts) == 1
            cur_element_id = element.fronts[0]
            continue
        elif element.type == "question":
            if intent in element.intents:
                # this is a branching intent, jump to it's id
                n = element.intents.index(intent)
                cur_element_id = element.fronts[n]


if __name__ == "__main__":
    main_menu()