from hmac import new
from queue import Queue
import copy
from random import random
from Python.draft_object_module import Pile, Card, Player

players: list[Player]

#Creates a list of Card objects
#Exists for testing purposes
def create_test_pile(prefix, card_count=14):
    pile = Pile([])
    for i in range(card_count):
        card = Card(prefix + str(i))
        pile.cards.append(card)
    return pile

card_list: list[Card]
card_list = []
for i in range(97, 123):
    string = "card_" + chr(i)
    card_list.append(Card(string))
card_list.append(Card("card_g"))
pile = Pile(card_list)
print(str(pile))
print(pile.remove_card_by_name('card_g'))
print(pile.remove_card_by_name('card_g'))
print(pile.remove_card_by_name('card_g'))