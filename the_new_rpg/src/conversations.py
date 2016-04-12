#!/usr/bin/python
#Spirit and Jacob work on script
from Conversation import Conversation

testconversation = Conversation(["hello", "I am on the second line now", "and by now it should be workin'", "bla", "bla"])

firstscene = Conversation(["Honey: Oh goody its lunch, I'm STARVING! But no, I left my glorious spinach-mushroom-provalone-bacon-broccoli quiche in the forest! I'll have to go get it.",
                           "Trash Panda: But Honey, those forests are infested with monsters! You shouldn't fight all of them just for a quiche!" ,
                           "Honey: It is no ordinary quiche, Trash Panda. It is my glorious spinach-mushroom-provalone-bacon-broccoli quiche! Lunch is the most important meal of the day, I need to do this."])

currentconversation = firstscene
