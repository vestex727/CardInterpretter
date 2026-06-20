from draft_object_module import Card, Pile, Player, Room

rooms: list[Room]
MAX_ID_NUM = 1000
taken_player_ids = [False] * MAX_ID_NUM
taken_room_ids = [False] * 100


if __name__ == "__main__":
    rooms = []


def get_hand(room_number: int, player_id: int):
    player = __get_player_in_room(room_number, player_id)
    return str(player.hand)


def pick_card(card_index: int, room_number: int, player_id: int):
    player = __get_player_in_room(room_number, player_id)
    player.pick_n_pass_by_index(card_index)


def pick_last_card(room_number: int, player_id: int):
    room = __get_room_by_number(room_number)
    room.number_of_players_ready += 1
    player = __get_player_in_room(room_number, player_id)
    player.last_pick()


def check_if_players_are_ready(room_number: int):
    room = __get_room_by_number(room_number)
    return room.number_of_players_ready == room.player_count


def create_room(player_name: str, room_size: int, passcode: str = "draft"):
    """
    Creates a room and a player to be added into the room.
    :param player_name: Name of the player who is creating the room.
    :param room_size: Size of the room (max number of players).
    :param passcode: Password required to join the room.
    :return: Player ID, followed by the room number, followed by seat number
    """
    creator = Player(player_name, __get_new_id())
    room_number = len(rooms)
    room = Room(room_size, room_number, passcode)
    rooms.append(room)
    room.let_player_join(creator)
    return [creator.player_id, room_number]


def join_room(player_name: str, room_number: int, passcode: str, seat_number: int = 0):
    """
    Attempts to let a user join a room. If the room exists, they have the right passcode, there is room in the lobby, and the seat number is available, a new player object is created and put into the room.
    If some condition is not met, returns an error message explaining the problem.
    :param player_name: Name of the user to be associated with the player object.
    :param room_number: Room number of the room the player is trying to join.
    :param passcode: Code to join the room.
    :param seat_number: Seat number to try to sit at. Default value of 0 will set the seat at the lowest seat number available. Any seat number outside the range of (0, max number) will also result in the first available seat being given.
    :return: Tuple of [response string, player_id, seat_number]
    """
    room = __get_room_by_number(room_number)
    if room is None:
        return ["No such room exists", -1, -1]
    if room.passcode != passcode:
        return ["Wrong Password or Room Number", -1, -1]

    id = __get_new_id()
    player = Player(player_name, id)

    if 0 < seat_number <= len(room.players):
        response = room.let_player_join(player=player, seat_number=seat_number)
    else:
        response = room.let_player_join(player=player)
    return [response, id, seat_number]


def leave_room(room_number: int, player_id: int):
    """
    Removes player from room. Despite name, can be used to kick players as well as to leave peacefully.
    :param room_number: room to remove player from.
    :param player_id: id of player to remove from room.
    :return: Nothing.
    """
    room = __get_room_by_number(room_number)
    room.remove_player_by_id(player_id)


def add_room(room_size: int, passcode: str = "draft"):
    rooms.append(Room(room_size, len(rooms), passcode))


def delete_room(room_number: int):
    """
    Deletes the room with a room id equal to room number.
    Garbage collection will handle the players.
    Frees room id to be reused.
    #TODO send notice to players room has been deleted.
    :param room_number: id of room to be deleted.
    :return: Nothing. Ashes to ashes, dust to dust.
    """
    for room in rooms:
        if int(room) == room_number:
            rooms.remove(room)
            taken_room_ids[room_number] = False
            break


def __get_player_in_room(room_number: int, player_id: int):
    room: Room
    if len(rooms) == 0:
        return None
    room_is_found = False
    for r in rooms:
        if int(r) == room_number:
            room = r
            room_is_found = True
            break
    if not room_is_found:
        return None
    return room.get_player_by_id(player_id)


def __get_new_id():
    """
    Finds the lowest available player id, sets it to unavailable, and returns it.
    :return: Lowest available id.
    """
    id_number = taken_player_ids.index(False)
    taken_player_ids[id_number] = True
    return id_number


def __get_room_by_number(room_number: int):
    """
    Finds a room based off of the room number.
    :param room_number: Room Number of room to find.
    :return: The room searched for if it exists. None otherwise.
    """
    for room in rooms:
        if int(room) == room_number:
            return room
    return None