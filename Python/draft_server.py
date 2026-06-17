from draft_object_module import Card, Pile, Player, Room

rooms: list[Room]

def add_room(roomsize: int, passcode: str = "draft"):
    rooms.append(Room(roomsize, len(rooms), passcode))



if __name__ == "__main__":
    rooms = []