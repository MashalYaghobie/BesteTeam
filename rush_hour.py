class Vehicle:
    def __init__(self, color, identifier, length, orientation, start_row, start_col):
        self.color = color # we'll use color to represent vehicles
        self.identifier = identifier # attribute to uniquely represent vehicles
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
        vehicle_id = f"{vehicle.color}{vehicle.identifier}"
        # add vehicle to dict
        self.vehicles[vehicle_id] = vehicle
        # logic for horizontal vehicles
        # loop over lenght and add to columns
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper()
        # same but add to rows for vertical vehicles
        else:
            for i in range(vehicle.length):
                self.board[vehicle.row + i][vehicle.col] = vehicle.color[0].upper()

    def display_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def move_vehicle(self, vehicle_id, distance):
        vehicle = self.vehicles[vehicle_id]
        if vehicle.orientation == 'H':
            # calculate new column position
            new_col = vehicle.col + distance

            # check if the move is valid
            if 0 <= new_col <= 5 - vehicle.length:
                # clear vehicle's current position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = '.'
                # update vehicle position
                vehicle.col = new_col
                # place vehicle at new position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper()

            else:
                print("Invalid move.")
        else:
            # similar logic for vertical movement
            new_row = vehicle.row + distance
            if 0 <= new_row <= 5 - vehicle.length:
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
            user_input = input("Enter your move (color+identifier distance): ")
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


if __name__ == "__main__":
    # initialize and set up the game
    game = RushHour()
    game.add_vehicle(Vehicle("blue", "1", 2, 'H', 0, 1))
    game.add_vehicle(Vehicle("yellow", "1", 3, 'H', 0, 3))
    game.add_vehicle(Vehicle("orange", "1", 2, 'H', 1, 1))
    game.add_vehicle(Vehicle("blue", "2", 2, 'V', 1, 3))
    game.add_vehicle(Vehicle("green", "1", 2, 'H', 1, 4))
    game.add_vehicle(Vehicle("red", "1", 2, 'H', 2, 0))
    game.add_vehicle(Vehicle("lightblue", "1", 2, 'V', 2, 2))
    game.add_vehicle(Vehicle("blue", "3", 2, 'H', 3, 3))
    game.add_vehicle(Vehicle("lightblue", "2", 2, 'V', 2, 5))
    game.add_vehicle(Vehicle("green", "2", 2, 'H', 3, 0))
    game.add_vehicle(Vehicle("orange", "2", 2, 'V', 4, 0))
    game.add_vehicle(Vehicle("green", "3", 2, 'V', 4, 2))
    game.add_vehicle(Vehicle("green", "4", 2, 'H', 4, 4))
    # Add more vehicles as needed

    # Start the game
    game.play_game()
