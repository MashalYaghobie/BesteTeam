import pandas as pd


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
        
        # We set some starting values for the placement of each vehicle
        self.row = start_row
        self.col = start_col



class RushHour:
    """
    In this class we will define methods to create the rush hour game.
    We will add vehicles, create the board, move the vehicles and
    check if the game is done.
    """
    def __init__(self, file):
        """
        In this method we read the csv file,initialize the board 
        for the rush hour game, add vehicle-instances to a dictionary. 
        """
        # Read the csv file and get size of board
        self.rush_hour_file = pd.read_csv(file)
        size_board = max(self.rush_hour_file['col'])

        # Create the board with dots for the desired boardsize
        self.board = [['.' for _ in range(size_board)] for _ in range(size_board)]
        
        # Create a new dictionary for the vehicle-instances
        self.vehicles = {}

        # Call function
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
        inputed position without colliding with another vehicle.
        """
        # We check if the orientation of the vehicle is horizontal
        if vehicle.orientation == 'H':
            
            # Get the starting and ending column for the vehicle
            start, end = sorted([vehicle.col, new_col])
            
            # Loop through all the columns for the vehicle for its move
            for col in range(start, end + vehicle.length):
                if col < vehicle.col or col >= vehicle.col + vehicle.length:
                    # check if the place on the board is NOT a dot
                    if self.board[vehicle.row][col] != '.':
                        return False
        # for vertical oriented vehicles
        else:
            # get the starting and ending row for the vehicle
            start, end = sorted([vehicle.row, new_row])
            # loop through all the columns for the vehicle for its move
            for row in range(start, end + vehicle.length):
                if row < vehicle.row or row >= vehicle.row + vehicle.length:
                    # check if the place on the board is NOT a dot
                    if self.board[row][vehicle.col] != '.' and row != vehicle.row:
                        return False
        # return true if the move is valid
        return True



    def move_vehicle(self, vehicle_id, distance):
        """
        In this method we create the ability to move the vehicles across the board.
        """
        # create a vehicle variable from the dictionary using its id
        vehicle = self.vehicles[vehicle_id]
        new_row, new_col = vehicle.row, vehicle.col
        # check if the vehicle is horizontal oriented
        if vehicle.orientation == 'H':
            # calculate new column position
            new_col += distance
            # check if the move is valid
            if 0 <= new_col <= 5 - vehicle.length + 1 and self.is_move_valid(vehicle, new_row, new_col):
                # clear the current position of the vehicle
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = '.'
                # update vehicle position to the new position
                vehicle.col = new_col
                # place the vehicle at new position
                for i in range(vehicle.length):
                    self.board[vehicle.row][vehicle.col + i] = vehicle.name
            else:
                print("Invalid move")
        # if the vehicle is vertical oriented
        else:
            # calculate the new row position
            new_row += distance
            # check if the move is valid
            if 0 <= new_row <= 5 - vehicle.length + 1 and self.is_move_valid(vehicle, new_row, new_col):
                    # clear the current position of the vehicle
                    for i in range(vehicle.length):
                        self.board[vehicle.row + i][vehicle.col] = '.'
                    # update the vehicle position to the new position
                    vehicle.row = new_row
                    # place the vehicle at the new position
                    for i in range(vehicle.length):
                        self.board[vehicle.row + i][vehicle.col] = vehicle.name
            # otherwise give an error
            else:
                print("Invalid move.")


    def check_win(self):
        """
        In this method we check if the game has been finished
        The game is finished when the 'X' car reaches the right edge of the board.
        """
        # find row containing red car 'X'
        for row in self.board:
            if 'X' in row:
                # check if rightmost part of 'X' car is at the right edge of board
                red_car_index = row.index('X')
                if red_car_index + 1 == len(row) - 1:
                    # if the car is there we return True
                    return True
        return False

        
    def play_game(self):
        """
        In this method we create the ability to play the game by calling
        the defined methods.
        """
         # if the game has not been won yet we can still do additional moves
        while True:
            # display the board
            self.display_board()
            # ask for next move
            user_input = input("Enter your move (Name + distance, (format = A 1)): ")
            # create the vehicle id and distance from the users input
            vehicle_id, distance = user_input.split()
            distance = int(distance)
            # check if the vehicle is in our dictionary
            if vehicle_id in self.vehicles:
                # move the vehicle the asked distance
                self.move_vehicle(vehicle_id, distance)
                # check if we have finished/have won and break from the loop
                if self.check_win():
                    print("Congratulations! You've won!")
                    self.display_board()
                    break
            # if the vehicle is not in our dictionary we print an error
            else:
                print("Invalid vehicle name. Please try again")


    def get_state(self):
        """
        Method for getting a string representation of the current
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
    game = RushHour('gameboards/Rushhour6x6_1.csv')

    # Start the game
    game.play_game()
