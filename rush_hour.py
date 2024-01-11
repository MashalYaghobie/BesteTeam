import pandas as pd


class Vehicle:
    def __init__(self, name, length, orientation, start_row, start_col):
        self.name = name # We'll use name to represent vehicles (A, B, C, etc.)
        self.length = length
        self.orientation = orientation # 'H' for horizontal and 'V' for vertical
        self.row = start_row
        self.col = start_col

        
class RushHour:
    def __init__(self):
        # Initializes board and dictionary where vehicles will be stored
        self.board = [['.' for _ in range(6)] for _ in range(6)]
        self.vehicles = {}
        

    def read_all_vehicles(self, file):
        # Reads the csv file
        rush_hour_file = pd.read_csv(file)
        
        # Loops through the csv file and assings the values
        for car in rush_hour_file.values:
            name = car[0]
            orientation = car[1]
            
            # - 1 because of indexing 
            start_col = car[2] - 1
            start_row = car[3] - 1
            
            length = car[4]
            
            # Adds it to dict and places it on the board
            self.add_vehicle(Vehicle(name, length, orientation, start_row, start_col))
        
            
    def add_vehicle(self, vehicle):
        # Add vehicle to dict
        self.vehicles[vehicle.name] = vehicle
        
        # Logic for horizontal vehicles
        # Loop over length and add to columns
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.board[vehicle.row][vehicle.col + i] = vehicle.name
                
        # Same but add to rows for vertical vehicles
        else:
            for i in range(vehicle.length):
                self.board[vehicle.row + i][vehicle.col] = vehicle.name

                
    def display_board(self):
        # Displays the board
        for row in self.board:
            print(' '.join(row))
        print()

        
    def is_move_valid(self, vehicle, new_row, new_col):
        """Check if the vehicle can move to the new position without collision
        """
        if vehicle.orientation == 'H':
            start, end = sorted([vehicle.col, new_col])
            for col in range(start, end + vehicle.length):
                if col < vehicle.col or col >= vehicle.col + vehicle.length:
                    if self.board[vehicle.row][col] != '.':
                        return False
        else:
            start, end = sorted([vehicle.row, new_row])
            for row in range(start, end + vehicle.length):
                if row < vehicle.row or row >= vehicle.row + vehicle.length:
                    if self.board[row][vehicle.col] != '.' and row != vehicle.row:
                        return False
        return True

    
    def move_vehicle(self, vehicle_id, distance):
        vehicle = self.vehicles[vehicle_id]
        new_row, new_col = vehicle.row, vehicle.col

        if vehicle.orientation == 'H':
            # Calculate new column position
            new_col += distance

            # Check if the move is valid
            if 0 <= new_col <= 5 - vehicle.length + 1 and self.is_move_valid(vehicle, new_row, new_col):

                # Clear vehicle's current position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = '.'
                # Update vehicle position
                vehicle.col = new_col
                # Place vehicle at new position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = vehicle.name
            else:
                print("Invalid move")

        else:
            # Similar logic for vertical movement
            new_row += distance
            if 0 <= new_row <= 5 - vehicle.length and self.is_move_valid(vehicle, new_row, new_col):

                    for i in range(vehicle.length):
                        self.board[vehicle.row + i][vehicle.col] = '.'

                    vehicle.row = new_row
                    for i in range(vehicle.length):
                        self.board[vehicle.row + i][vehicle.col] = vehicle.name

            else:
                print("Invalid move.")


    def check_win(self):
        # Check if red car 'R' is in the winning position
        for row in self.board:
            if row[-1] == 'R': # Checking the rightmost column for the red car
                return True
        return False

    
    def play_game(self):
        while True:
            self.display_board()
            user_input = input("Enter your move (Name + distance, format = A 1): ")

            vehicle_id, distance = user_input.split()
            distance = int(distance)

            if vehicle_id in self.vehicles:
                self.move_vehicle(vehicle_id, distance)
                if self.check_win():
                    print("Congratulations! You've won!")
                    self.display_board()
                    break
            else:
                print("Invalid vehicle name. Please try again.")

                
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
    
    # Reads all the vehicles that are in the csv file
    game.read_all_vehicles('gameboards/Rushhour6x6_1.csv')

    # Start the game
    game.play_game()
