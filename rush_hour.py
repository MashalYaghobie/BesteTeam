class Vehicle:
    def __init__(self, name, color, length, orientation, start_row, start_col):
        self.name = name # we'll use name to represent vehicles
        self.color = color # together with color, example: red car, green truck, etc.
        self.length = length
        self.orientation = orientation # 'H' for horizontal and 'V' for vertical
        self.row = start_row
        self.col = start_col

class RushHour:
    def __init__(self):
        self.board = [['.' for _ in range(6)] for _ in range(6)]
        self.vehicles = {}

    def add_vehicle(self, vehicle):
        # use identifier in addition to color for representing vehicles
        vehicle_id = f"{vehicle.name}{vehicle.color}"
        # add vehicle to dict
        self.vehicles[vehicle_id] = vehicle
        # logic for horizontal vehicles
        # loop over lenght and add to columns
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper() + vehicle.name[0].upper()
        # same but add to rows for vertical vehicles
        else:
            for i in range(vehicle.length):
                self.board[vehicle.row + i][vehicle.col] = vehicle.color[0].upper() + vehicle.name[0].upper()

    def display_board(self):
        unicode_map = {
            'RC': '🚗',  # Red car
            'BC': '🚙',  # Blue car
            'YC': '🚕',  # Yellow car
            'OB': '🚌',  # Orange bus
            'YT': '🚜',  # Yellow tractor
            'OT': '🚚',  # Orange truck
            'BB': '🚎',  # Blue bus
            'YS': '🛵',  # Yellow scooter
            'WB': '🚐',  # White bus
            'GT': '🚛',  # Green truck
            'BM': '🏍️',  # Black motor
            'WT': '🚑',  # White truck
            'GC': '🛻',  # Green car
            'GT': '🚃',  # Green train

            # more to be added later
            '.': '⬜'   # Empty space
        }

        for row in self.board:
            print(' '.join(unicode_map.get(cell, cell) for cell in row))
        print()

    def is_move_valid(self, vehicle, new_row, new_col):
        """Check if the vehicle can move to the new position without collision
        """
        if vehicle.orientation == 'H':
            start, end = sorted([vehicle.col, new_col])
            for col in range(start, end + vehicle.length):
                if col != vehicle.col and self.board[vehicle.row][col] != '.':
                    return True
        else:
            start, end = sorted([vehicle.row, new_row])
            for row in range(start, end + vehicle.length):
                if row != vehicle.row and self.board[row][vehicle.col] != '.':
                    return True
        return False

    def move_vehicle(self, vehicle_id, distance):
        vehicle = self.vehicles[vehicle_id]
        new_row, new_col = vehicle.row, vehicle.col

        if vehicle.orientation == 'H':
            # calculate new column position
            new_col += distance

            # check if the move is valid
            if 0 <= new_col <= 5 - vehicle.length + 1 and self.is_move_valid(vehicle, new_row, new_col):

                # clear vehicle's current position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = '.'
                    # update vehicle position
                    vehicle.col = new_col
                    # place vehicle at new position
                    for i in range(vehicle.length):
                        self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper()
            else:
                print("Invalid move")

        else:
            # similar logic for vertical movement
            new_row += distance
            if 0 <= new_row <= 5 - vehicle.length + 1 and self.is_move_valid(vehicle, new_row, new_col):

                for i in range(vehicle.length):
                    self.board[vehicle.row + i][vehicle.col] = '.'

                    vehicle.row = new_row
                for i in range(vehicle.length):
                    self.board[vehicle.row + i][vehicle.col] = vehicle.color[0].upper()

            else:
                print("Invalid move.")


    def check_win(self):
        # check if red car 'R' is in the winning position
        for row in self.board:
            if row[-1] == 'R': # checking the rightmost column for the red car
                return True
        return False

    def play_game(self):
        while True:
            self.display_board()
            user_input = input("Enter your move (color+name distance): ")
            vehicle_id, distance = user_input.split()
            distance = int(distance)

            if vehicle_id in self.vehicles:
                self.move_vehicle(vehicle_id, distance)
                if self.check_win():
                    print("Congratulations! You've won!")
                    self.display_board()
                    break
            else:
                print("Invalid vehicle color. Please try again.")

    def get_state(self):
        """Method for getting a string representation of the current
        state of the board.
        Example: a board that looks like this:
        . . . . . .
        . . A A . .
        . . B . . .
        . B B . C .
        . . . . C .
        . . . . . .
        will have a state string that looks like this:
        "...... ..AA.. ..B... .BB.C. ......"
        This allows easy comparisons between board states.
        """
        return ''.join(''.join(row) for row in self.board)


if __name__ == "__main__":
    # initialize and set up the game
    game = RushHour()
    game.add_vehicle(Vehicle("tractor", "yellow", 2, 'H', 0, 1))
    game.add_vehicle(Vehicle("car", "yellow", 3, 'H', 0, 3))
    game.add_vehicle(Vehicle("bus", "orange", 2, 'H', 1, 1))
    game.add_vehicle(Vehicle("car", "green", 2, 'V', 1, 3))
    game.add_vehicle(Vehicle("truck", "white", 2, 'H', 1, 4))
    game.add_vehicle(Vehicle("car", "red", 2, 'H', 2, 0))
    game.add_vehicle(Vehicle("truck", "orange", 2, 'V', 2, 2))
    game.add_vehicle(Vehicle("bus", "blue", 2, 'H', 3, 3))
    game.add_vehicle(Vehicle("scooter", "yellow", 2, 'V', 2, 5))
    game.add_vehicle(Vehicle("bus", "white", 2, 'H', 3, 0))
    game.add_vehicle(Vehicle("truck", "green", 2, 'V', 4, 0))
    game.add_vehicle(Vehicle("motor", "black", 2, 'V', 4, 2))
    game.add_vehicle(Vehicle("train", "green", 2, 'H', 4, 4))
    # Add more vehicles as needed

    # Start the game
    game.play_game()
