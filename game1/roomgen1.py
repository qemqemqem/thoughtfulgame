import random

# Define constants for the size of the map and the maximum number of rooms
MAP_WIDTH = 50
MAP_HEIGHT = 20
MAX_ROOMS = 10


# Define a class for a room
class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_intersecting(self, other):
        return (self.x < other.x + other.width and self.x + self.width > other.x and
                self.y < other.y + other.height and self.y + self.height > other.y)


# Generate the map
map = [[0 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
rooms = []
for i in range(MAX_ROOMS):
    # Generate a random room size and position
    room_width = random.randint(3, 10)
    room_height = random.randint(3, 8)
    room_x = random.randint(0, MAP_WIDTH - room_width - 1)
    room_y = random.randint(0, MAP_HEIGHT - room_height - 1)
    new_room = Room(room_x, room_y, room_width, room_height)

    # Check if the new room intersects with any existing rooms
    intersects = False
    for room in rooms:
        if new_room.is_intersecting(room):
            intersects = True
            break
    if intersects:
        continue

    # Add the new room to the map
    for x in range(new_room.x, new_room.x + new_room.width):
        for y in range(new_room.y, new_room.y + new_room.height):
            map[x][y] = 1
    # Add paths between the rooms
    for i in range(len(rooms) - 1):
        room1 = rooms[i]
        room2 = rooms[i + 1]
        x1 = random.randint(room1.x, room1.x + room1.width - 1)
        y1 = random.randint(room1.y, room1.y + room1.height - 1)
        x2 = random.randint(room2.x, room2.x + room2.width - 1)
        y2 = random.randint(room2.y, room2.y + room2.height - 1)
        while x1 != x2:
            if x1 < x2:
                x1 += 1
            else:
                x1 -= 1
            map[x1][y1] = 1
        while y1 != y2:
            if y1 < y2:
                y1 += 1
            else:
                y1 -= 1
            map[x1][y1] = 1

    rooms.append(new_room)

# Print the map
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if map[x][y] == 1:
            print(".", end="")
        else:
            print("#", end="")
    print()