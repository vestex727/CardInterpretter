from hmac import new
from queue import Queue
import copy
from random import random
from Python.draft_object_module import Pile, Card, Player, Room

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

player = Player("Bob", 1)
player2 = Player("James", 2)

player.add_pile(pile)
print(str(player))

card_list = []
for i in range(26):
    card_list.append(Card("card_"+str(i)))
pile = Pile(card_list)
print(str(pile))
player2.add_pile(pile)
print(str(player2))
print()

player.pick_n_pass("card_g", player2)
player.send_pile(player2)
print()
print(str(player))
print(str(player2))
player.incoming_piles.put(pile)
player.incoming_piles.put(pile)
print("Here: ")
print(player.incoming_piles.qsize())
player.incoming_piles.get()
print(player.incoming_piles.qsize())