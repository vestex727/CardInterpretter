from queue import Queue
from sympy import false, true

from Python.draft_server import taken_player_ids
from Python.draft_server_test_files import players


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
        return str(index) + ": " + self.cards.pop(index) if found else None


    def remove_card_by_index(self, index: int):
        return self.cards.pop(index) if index < len(self.cards) else None

class Player:
    incoming_piles: Queue[Pile]
    hand: Pile
    player_name: str
    player_id: int
    player_number: int
    next_player = None

    def __init__(self, player_name: str, player_id: int, hand: Pile = None):
        """
        Creates a player object that has a name, if, hand of cards, and a queue of incoming card piles.
        :param player_name: Name of the player the object represents.
        :param player_id: ID of the player (important to allow for reconnection).
        :param hand: A pile of cards in your hand. These are the only cards the client should have access to.
        """
        self.hand = hand
        self.incoming_piles = Queue[Pile]()
        self.player_name = player_name
        self.player_id = player_id
        self.next_player = None
        if self.hand is None and not self.incoming_piles.empty():
            self.hand = self.incoming_piles.get()

    def __str__(self):
        return "name: " + self.player_name + "\nid: " + str(self.player_id) + "\nhand: " + str(self.hand) + "\nincoming piles: " + str(self.incoming_piles.qsize())

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
            self.hand = None


    def pick_n_pass_by_index(self, card_index: int, player_to_pass_to = next_player):
        """
        Removes the picked card, and then passes the pile to the next player
        :param card_name: card to find, pick, and remove.
        :param player_to_pass_to: player to pass the pile to after making the pick
        :return: Nothing.
        """
        print(self.hand.remove_card_by_index(card_index))
        self.send_pile(player_to_pass_to)
        print(self.hand)

    def pick_n_pass(self, card_name: str, player_to_pass_to = next_player):
        """
        Removes the picked card, and then passes the pile to the next player
        :param card_name: card to find, pick, and remove.
        :param player_to_pass_to: player to pass the pile to after making the pick
        :return: Nothing.
        """
        print(self.hand.remove_card_by_name(card_name))
        self.send_pile(player_to_pass_to)
        print(self.hand)

    def last_pick(self):
        """
        Removes the last card from the hand.
        There is nothing remaining in the pile to pass along, so the pile is just deleted.
        :return: name of the last card to be picked this pack.
        """
        last_card = self.hand.remove_card_by_index(0)
        self.hand = None
        return str(last_card)


class Room:
    players: list[Player]
    player_count: int           # Maximum number of players in room.
    room_number: int
    passcode: str
    taken_numbers: list[int]    # Seat Numbers that are currently claimed.
    number_of_players_ready: int

    def __init__(self, player_count: int, room_number: int, passcode: str = "draft"):
        """
        Creates a room for players to be put into that will handle interactions between players.
        Exists to allow multiple rooms to run in parallel.
        :param player_count: Max player count in the room.
        :param room_number: Room number that will be used to identify which room the player is in.
        :param passcode: Passcode to enter the room (defaults to "draft")
        :return: "success" if there was room to let the player in, "fail" otherwise.
        """
        self.player_count = player_count
        self.room_number = room_number
        self.passcode = passcode
        self.players = [None] * player_count
        self.number_of_players_ready = 0

    def __int__(self):
        """
        Converts the room to an int.
        Equal to the room number.
        :return: room number.
        """
        return self.room_number

    def generate_seat_number(self):
        """
        Finds the lowest available seat number.
        :return: lowest available seat number, or None if there are none available.
        """
        for i in range (1,self.player_count):
            if not i in self.taken_numbers:
                return i
        return None

    def let_player_join(self, player: Player, seat_number: int = 0):
        """
        Attempts to allow player to join the room.
        If the room is full, it doesn't allow the player to join.
        If the selected seat number the player wants is taken, fails to allow the player to join.
        If the player number is 0, it allows the room to select the player's seat number.
        :param player: The Player object to be put into the room.
        :param seat_number: The seat number that the player is trying to take. If the seat is taken, they won't be able to join. If the value is -1, the seating will be assigned. Default value of -1.
        :return: "success" if the player was able to join, "seat taken fail" if the desired seat was taken, and "full room fail" if the room was full.
        """
        if len(self.players) < self.player_count:
            if seat_number < 1 or seat_number in self.taken_numbers:
                if seat_number < 1:
                    seat_number = self.generate_seat_number()
                self.players[seat_number-1] = player
                return "success"
            return "seat taken fail"
        return "full room fail"

    def get_player_by_id(self, player_id: int):
        """
        Gets player in room by player id.
        :param player_id: ID to search players for.
        :return: player object with id matching player_id if one exists. None if otherwise.
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None

    def remove_player_by_id(self, player_id: int):
        """
        Removes a player from the room.
        Removes their seat from the list of taken seats.
        :param player_id: Player id of the player to remove from the room.
        :return: True if removal is successful, False if there was no player to remove.
        """
        for index, player in enumerate(players):
            if player.player_id == player_id:
                players[index] = None
                self.taken_numbers.remove(index)
                return True
        return False

    def assign_next_player_clockwise(self):
        """
        Assigns to each player in the room a "next player" in a "clockwise order" (1 -> 2, 2 -> 3,..., n-1 -> n, n -> 1).
        Turns the players into a circular linked list.
        :return: nothing
        """
        for i, player in self.players:
            index = i + 1
            if index == len(self.players):
                index = 0
            player.next_player = self.players[index]
        self.number_of_players_ready = 0

    def assign_next_player_counterclockwise(self):
        """
        Assigns to each player in the room a "next player" in a "counterclockwise order" (n -> n-1, n-1 -> n-2,..., 2 -> 1, 1 -> n).
        Turns the players into a circular linked list.
        :return: nothing
        """
        for i, player in reversed(self.players):
            index = i + 1
            if index == len(self.players):
                index = 0
            player.next_player = self.players[index]
        self.number_of_players_ready = 0