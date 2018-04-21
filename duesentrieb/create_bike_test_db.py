from duesentrieb.database import setup_database
from duesentrieb.database import insert_element
from duesentrieb.database import remove_table

remove_table("content")
remove_table("structure")
setup_database()
insert_element("topic_bike", "You turn over the bike", id=0, fronts="1")
insert_element("topic_bike", "Flip the bike", id=0, )

insert_element("topic_bike", "Is it the back tire?", type="question", id=1, fronts="2,3", intents="cmd_yes,cmd_no")

insert_element("topic_bike", "Take off the back tire", id=2, fronts=4)
insert_element("topic_bike", "Take the back wheel away from the bike", id=3)

insert_element("topic_bike", "Remove the front tire", id=3, fronts=4)
insert_element("topic_bike", "take away the front tire", id=3)

insert_element("topic_bike", "now you are done", id=4)
