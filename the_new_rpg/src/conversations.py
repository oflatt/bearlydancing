#!/usr/bin/python
#Spirit and Jacob work on script
import graphics
from Conversation import Conversation
from Speak import Speak

longtestdialogue = ["bla", "bla", "a", "monster", "did", "do", "that", "really", "good", "dancin", "he was honey"]
shorttestdialoge = ["I talk just a little"]

testconversation = Conversation([Speak(graphics.honey_right0, longtestdialogue),
                                 Speak(graphics.honey_right2, shorttestdialoge),
                                 Speak(graphics.honey_right0, longtestdialogue),
                                 Speak(graphics.honey_right2, shorttestdialoge)])

ohhoney = ["Honey: Oh goody its lunch, I'm STARVING!",
           "But no, I left my glorious spinach-mushroom-provalone-",
          "bacon-broccoli quiche in the forest!",
           "I'll have to go get it."]
ohtp = ["bla"]

firstscene = Conversation([Speak(graphics.honey_right0, ohhoney),
                           Speak(graphics.tpanda, ohtp )])

oldfirst = Conversation([
      "",
      "Trash Panda: But Honey, those",
      "forests are infested with monsters!",
      " You shouldn't fight all of them",
      "just for a quiche!",
      "Honey: It is no ordinary quiche",
      ", Trash Panda. It is my glorious",
      "spinach-mushroom-provalone-bacon-",
      "broccoli quiche! Lunch is the most",
      " important meal of the day, I need",
      " to do this.",
      "TP: I thought breakfast was the-",
      "Honey: Shush, I'm leaving now.",
      " Time for adventure."])

secondscene = Conversation(["Monster: Who goes there!",
      "Honey: It's me, Honey! I'm just",
      " here to get my quiche.",
      "Monster: No one may pass!",
      "Honey: So what, do you want",
      " me to fight you?",
      "Monster: No! I want to DANCE fight!",
      " you",
      "Honey: Well that's a relief. I'm way",
      " better at dancing than fighting..."])

penultimatefight = Conversation(["Honey: Oh wow, they must be",
                                  "the last boss!",
                                  "Monster: ARGHGHGHGH!",
                                  "Honey: *gulp* Alright, let's go!"])

lastfight = Conversation(["Honey: What, I thought I was done!",
                          "Well, this should be easy.",
                          "Monster: Hehehehehe..."])

finalscene = Conversation(["Honey: *sniff sniff* Finally",
                           "... lunch time."])

currentconversation = testconversation
