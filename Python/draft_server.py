from hmac import new
from queue import Queue
import copy
from random import random

#Card object that is picked around in draft
#Glorified string
class Card:
    def __init__(self, name):
        self.name = name

#Pile of cards passed around in draft
#Holds list of cards
class Pile:
    cards: list[Card]

    #initializes the Pile with the cards list being empty by default
    #Card list can be passed in as a parameter
    def __init__(self, cards=[]):
        self.cards = cards

    #Prints every card in the pile
    def print(self):
        for card in self.cards:
            print(card.name, end=", ")
        print()

#Player that holds piles of cards.
#Players can pass piles to other players
class Player:
    incoming_piles: Queue[Pile]
    player_cards: list[Card]

    def __init__(self):
        self.incoming_piles = Queue[Pile]()


    def send_to(self, player):
        player.incoming_piles.put(self.incoming_piles.get())

    def print(self):
        q = self.incoming_piles
        new_q = Queue[Pile]()
        while not q.empty():
            temp = q.get()
            new_q.put(temp)
            temp.print()
        self.incoming_piles = new_q

#Creates a list of Card objects
#Exists for testing purposes
def create_test_pile(prefix, card_count=14):
    pile = Pile([])
    for i in range(card_count):
        card = Card(prefix + str(i))
        pile.cards.append(card)
    return pile

hand_a = create_test_pile("a")
hand_b = create_test_pile("b")
player1 = Player()
player2 = Player()
player1.incoming_piles.put(hand_a)
player2.incoming_piles.put(hand_b)
player1.print()
player2.print()
print()
player1.send_to(player2)
print("\nplayer1", end=":\t")
player1.print()
print("\nplayer2", end=":\t")
player2.print()

