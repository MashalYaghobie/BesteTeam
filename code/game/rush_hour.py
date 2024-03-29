import pandas as pd
import os
import copy
import re
import numpy as np


class Vehicle:
    """
    In this class we will set the base variables or values for the
    different vehicles for the rush hour game.
    """

    def __init__(self, name, length, orientation, start_row, start_col):
        """
        In this method we will create some base variables or values for the vehicles.
        """
        # Name is the name of the vehicle (A, B, C, etc)
        self.name = name

        # Length will be the length of the vehicle
        self.length = length

        # Orientation will be H for horizontal and V for vertical
        self.orientation = orientation

        # We set some starting values for the placement of each vehicle testst
        self.row = start_row
        self.col = start_col

        # store old position
        self.old_row = None
        self.old_col = None


    def get_move_description(self, distance):
        direction = 'right' if distance > 0 else 'left' if distance < 0 else 'none'
        return f"Move car {self.name} {abs(distance)} step(s) to the {direction}"



class RushHour:
    """
    In this class we will define methods to create the rush hour game.
    We will add vehicles, create the board, move the vehicles and
    check if the game is done.
    """

    def __init__(self, start_game=True, board_size=None, board=None):
        """
        In this method we read the csv file,initialize the board
        for the rush hour game, add vehicle-instances to a dictionary.
        """
        # Initilaize variables and call functions
        self.rush_hour_file = None
        if board_size is not None and board is not None:
            self.board_size = board_size
            self.board = board
            self.vehicles = {}
        else:
            self.start_game()
            self.initial_hashable_state = self.get_state_hashable()
    

    def get_state_grid(self):
        """
        Return an NxN 2D list corresponding to this state.  Each
        element has a number corresponding to the car that occupies
        that cell, or is a -1 if the cell is empty

        Returns
        -------
        list of list: The grid of numbers for the state
        """
        grid = [[-1] * self.board_size for _ in range(self.board_size)]

        for idx, vehicle in enumerate(self.vehicles.values()):
            # Determine the direction of increment based on orientation
            di, dj = (0, 1) if vehicle.orientation == 'H' else (1, 0)

            # Starting position of the vehicle
            i, j = vehicle.row, vehicle.col

            # Update grid cells occupied by this vehicle
            for _ in range(vehicle.length):
                grid[i][j] = idx
                i += di
                j += dj

        return grid


    def get_state_hashable(self):
        """
        Return a shorter string without line breaks that can be
        used to hash the state

        Returns
        -------
        string: A string representation of this state
        """
        if not hasattr(self, '_cached_state'):
            grid = self.get_state_grid()
            state_list = [str(cell) for row in grid for cell in row]
            self._cached_state = ''.join(state_list)
        return self._cached_state


    def clone(self):
        """
        Create a deep copy of the current RushHour game state.

        Returns:
        RushHour: A new RushHour object with the same state as the current one.
        """
        # Create a new RushHour instance without starting the game
        cloned_game = RushHour(start_game=False)

        # Set the board size and initialize the board based on this size
        cloned_game.board_size = self.board_size
        cloned_game.board = [['.' for _ in range(cloned_game.board_size)] for _ in range(cloned_game.board_size)]

        # Deep copy each vehicle
        cloned_game.vehicles = {}

        print("Cloning game state...")

        for name, vehicle in self.vehicles.items():
            cloned_vehicle = Vehicle(vehicle.name, vehicle.length, vehicle.orientation, vehicle.row, vehicle.col)
            cloned_game.vehicles[name] = cloned_vehicle

            # Assuming add_vehicle adjusts the board, we call it here
            cloned_game.add_vehicle(cloned_vehicle)

        return cloned_game


    def reset(self):
        """
        Reset the game board and its state to the initial configuration.
        """
        # Reset the board to its initial state
        self.board = [['.' for _ in range(len(self.board))] for _ in range(len(self.board))]

        # Reset the vehicles dictionary to its initial state
        self.vehicles = {}

        # Re-add all vehicles to the board
        self.read_all_vehicles()


    def read_all_vehicles(self):
        """
        In this method we read the input-file and create the variables
        for the vehicles such as name, orientation, length, starting column
        and starting row. Furthermore we add the vehicle instance to the dictionary.
        """
        # Loops through the csv file and assigns the values to variables
        for car in self.rush_hour_file.values:
            name = car[0]
            orientation = car[1]

            # We substract 1 because of indexing
            start_col = car[2] - 1
            start_row = car[3] - 1
            length = car[4]

            # Adds the vehicle to dictionary and places it on the board
            self.add_vehicle(Vehicle(name, length, orientation, start_row, start_col))


    def add_vehicle(self, vehicle):
        """
        In this method we add vehicles to the game and place them
        on the desired place on the board.
        """
        # We add the vehicle to the dictionary
        self.vehicles[vehicle.name] = vehicle

        # For horizontal oriented vehicles: loop over length and add to columns
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.board[vehicle.row][vehicle.col + i] = vehicle.name

        # For vertical oriented vehicles: loop over length and add to rows
        else:
            for i in range(vehicle.length):
                self.board[vehicle.row + i][vehicle.col] = vehicle.name


    def display_board(self):
        """
        In this method we print the board for visualization purposes.
        """
        # Loop through the rows in the board and add some space between the rows
        for row in self.board:
            print(' '.join(row))
        print()


    def is_move_valid(self, vehicle, new_row, new_col):
        """
        In this method we check if the vehicle is able to move to the
        inputed position without colliding with other vehicles.
        """
        # Initialize board size
        board_size = len(self.board)

        # Check if the move is valid for a horizontally oriented vehicle
        if vehicle.orientation == 'H':

            # Check if the new position is within our board size
            if new_col < 0 or new_col + vehicle.length > board_size:
                return False

            # Get the start and end columns of the vehicles movement line / path
            start_col = min(vehicle.col, new_col)
            end_col = max(vehicle.col + vehicle.length - 1, new_col + vehicle.length - 1)

            # Check for each cell in the path if there are other vehicles in the way
            for col in range(start_col, end_col + 1):

                # Skip the current position of the specific vehicle
                if col < vehicle.col or col >= vehicle.col + vehicle.length:

                    # If there is any cell in the vehicles path that is not empty the move is not valid
                    if self.board[vehicle.row][col] != '.' and col != vehicle.col:
                        return False

        # Check if the move is valid for a vertically oriented vehicle
        else:

            # Check if the new position is within our board size
            if new_row < 0 or new_row + vehicle.length > board_size:
                return False

            # Get the start and end rows of the vehicles movement line / path
            start_row = min(vehicle.row, new_row)
            end_row = max(vehicle.row + vehicle.length - 1, new_row + vehicle.length - 1)

            # Check for each cell in the path if there are any vehicles in the way
            for row in range(start_row, end_row + 1):

                # Skip the current position of the specific vehicle
                if row < vehicle.row or row >= vehicle.row + vehicle.length:

                    # If there is any cell in the vehicles path that is not empty the move is not valid
                    if self.board[row][vehicle.col] != '.' and row != vehicle.row:
                        return False

        # If there are no vehicles in the way, the move is valid
        return True


    def move_vehicle(self, vehicle_id, distance):
        """
        In this method we create the ability to move the vehicles across the board.
        """
        # Create a vehicle variable from the dictionary using its id
        vehicle = self.vehicles[vehicle_id]

        # Save the old position before making the move
        vehicle.old_row = vehicle.row
        vehicle.old_col = vehicle.col

        # Check if the vehicle is horizontal oriented
        if vehicle.orientation == 'H':

            # Calculate new column position
            new_col = vehicle.col + distance

            # Check if the move is valid
            if self.is_move_valid(vehicle, vehicle.row, new_col):
                # Clear the old position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.old_col + i] = '.'

                # Update vehicle position
                vehicle.col = new_col

                # Place the vehicle at new position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = vehicle.name

                # Return True to indicate succesful move
                return True

            else:
                # Invalid move
                return False

        # If the vehicle is vertical oriented
        else:

            # Calculate the new row position
            new_row = vehicle.row + distance

            # Check if the move is valid
            if self.is_move_valid(vehicle, new_row, vehicle.col):
                # Clear the old position
                for i in range(vehicle.length):
                    self.board[vehicle.old_row + i][vehicle.col] = '.'

                # Update the vehicle position to the new position
                vehicle.row = new_row

                # Place the vehicle at the new position
                for i in range(vehicle.length):
                    self.board[vehicle.row + i][vehicle.col] = vehicle.name
                return True

            # Otherwise give an error
            else:
                return False


    def check_win(self):
        """
        In this method we check if the game has been finished
        The game is finished when the 'X' car reaches the right edge of the board.
        """
        # Get the red car object
        red_car = self.vehicles.get('X')

        # Find row containing red car 'X'
        for row in self.board:
            if 'X' in row:

                # Check if rightmost part of 'X' car is at the right edge of board
                red_car_index = row.index('X')
                if red_car_index + red_car.length == len(row):

                    # If the car is there we return True
                    return True

        return False


    def start_game(self):
        """
        In this method we start the game by initializing the gameboards
        and asking user which board to play with.
        """
        # Initialize and set up the game
        current_directory = os.path.dirname(os.path.abspath(__file__))
        gameboards_dir = os.path.join(current_directory, '..', '..', 'gameboards')
        gameboards = [file for file in os.listdir(gameboards_dir)]

        # Display the gameboards files with numbers
        for number, file in enumerate(gameboards, 1):
            print(f"{number}: {file}")

        # Keep asking until user gives correct integer
        while True:

            # Ask user for an integer
            choice = int(input("Enter the number of the gameboard you want to play:"))

            # Check whether integer is correct and use integer to read the file
            if 1 <= choice <= 7:
                file_chosen = os.path.join(current_directory, '..', '..', 'gameboards', gameboards[choice-1])
                self.rush_hour_file = pd.read_csv(file_chosen)

                # Extract board size from file name
                match = re.search(r'(\d+)x\d+', file_chosen)
                if match:
                    self.board_size = int(match.group(1))
                else:
                    raise ValueError("Unable to determine board size from file name")

                # Initialize board based off file
                self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]

                # Initialize dictionaries and function
                self.vehicles = {}
                self.read_all_vehicles()
                self.initial_positions = {}
                break

            else:
                print("Invalid choice! Please choose a correct number!")


    def play_game(self):
        """
        In this method we create the ability to play the game by calling
        the defined methods.
        """
        # If the game has not been won yet we can still do additional moves
        while True:

            # Display the board
            self.display_board()

            # Ask for next move
            user_input = input("Enter your move (Name + distance, (format = A 1)): ")

            # Create the vehicle id and distance from the users input
            vehicle_id, distance = user_input.split()
            distance = int(distance)

            # Check if the vehicle is in our dictionary
            if vehicle_id in self.vehicles:

                # Move the vehicle the asked distance
                self.move_vehicle(vehicle_id, distance)

                # Check if we have finished/have won and break from the loop
                if self.check_win():
                    print("Congratulations! You've won!")
                    self.display_board()
                    break

            # If the vehicle is not in our dictionary we print an error
            else:
                print("Invalid vehicle name. Please try again")



if __name__ == "__main__":
    # Initialize the game
    game = RushHour()

    game.read_all_vehicles()

    game.play_game()
