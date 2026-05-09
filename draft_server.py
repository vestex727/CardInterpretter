

drafting_hand = []
picked_cards = []
player_count = 0
test_card_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]

def add_hand_to_queue(player, hand):
    drafting_hand[player].append(hand)

def get_next_hand(player):
    if drafting_hand[player]:
        return drafting_hand[player].pop(0)
    return "Not Ready"

def pick_card(player, name):
    drafting_hand[player][0].remove(name)
    drafting_hand[player+1].append(drafting_hand[player].pop(0))

def initialize_drafting_hands():
    global drafting_hand
    global picked_cards
    for i in range(player_count):
        drafting_hand.append([])
        picked_cards.append([])

def create_test_hands(player_number):
    player_count = player_number
    initialize_drafting_hands()
    for player in range(player_count):
        hand = []
        i = 0

def create_3d_arrays(player_number):
    a = [[[(str(i) + str(j) + str(k)) for k in range(14)] for j in range(1)] for i in range(player_number)]
    for i in a:
        print(i)
        for j in range(player_number):
            print(j)

    print(a)

def print_drafting_hands():
    print(drafting_hand)
    print(picked_cards)

create_3d_arrays(8)