from os import name
from queue import Queue

from sympy import false, true
from sympy.codegen.ast import none

class Card(str):
    name: str
    def __init__(self, name: str):
        """
        Creates a card with a card name.
        This is a glorified string. It exists to be passed around
        :param name: the name of the card.
        """
        self.name = name

    def read_card(self) -> str:
        """
        Reads the name of the card and returns it.
        :return: string of self.name
        """
        return self.name

class Pile:
    cards: list[Card]

    def __init__(self, cards: list[Card]):
        """
        Creates a Pile of cards, which represents a list of cards.
        :param cards: list of cards the pile represents
        """
        self.cards = cards

    def __str__(self):
        out = ""
        for card in self.cards:
            out += str(card) + ", "
        return out[:len(out) - 2]

    def remove_card_by_name(self, card_name: str):
        index = 0
        found = false
        for i, card in enumerate(self.cards):
            if str(card) == str(card_name):
                found = true
                index = i
        return str(index) + ": " + self.cards.pop(index) if found else none

    def remove_card_by_index(self, index: int):
        return self.cards.pop(index) if index < len(self.cards) else none


class Player:
    incoming_piles: Queue[Pile]
    hand: Pile
    player_name: str
    player_id: int
    next_player: Player

    def __init__(self, player_name: str, player_id: int, incoming_piles: Queue[Pile] = Queue[Pile](), hand: Pile = none):
        """
        Creates a player object that has a name, if, hand of cards, and a queue of incoming card piles.
        :param player_name: Name of the player the object represents.
        :param player_id: ID of the player (important to allow for reconnection).
        :param incoming_piles: a queue of piles coming towards this player.
        :param hand: A pile of cards in your hand. These are the only cards the client should have access to.
        """
        self.hand = hand
        self.incoming_piles = incoming_piles
        self.player_name = player_name
        self.player_id = player_id
        if self.hand == none and not self.incoming_piles.empty():
            self.hand = self.incoming_piles.get()

    def __str__(self):
        return "name: " + self.player_name + "\nid: " + str(self.player_id) + "\nhand: " + str(self.hand) + "incoming piles: " + str(self.incoming_piles.qsize())

    def add_pile(self, pile: Pile) -> Pile:
        """
        Adds a pile of cards to the queue. Then pops the front of the queue to the hand if the hand is empty.
        :param pile: Pile to add to the queue.
        :return: the inputted pile (for method chaining)
        """
        self.incoming_piles.put(pile)
        if self.hand is None:
            self.hand = self.incoming_piles.get()
        return pile

    def send_pile(self, player) -> None:
        """
        Sends the current hand to the next player.
        Adds this player's hand pile to the other player's incoming_pile queue.
        Replaces with the hand pile with the next pile in queue if there is one.
        Replaces the current hand with none if the queue is empty
        :param player: A player object to send this player's current hand to
        :return: nothing
        """
        player.add_pile(self.hand)
        if not self.incoming_piles.empty():
            self.hand = self.incoming_piles.get()
        else:
            self.hand = none

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