class Vehicle:
    """
    In this class we will set the base variables or values for the 
    different vehicles for the rush hour game.
    """

    def __init__(self, color, identifier, length, orientation, start_row, start_col):
        """
        In this method we will create some base variables or values for the vehicles.
        """

        # color is the color of the vehicle
        self.color = color

        # we set an identifier to make a distinction between verhicles of the same color
        self.identifier = identifier 

        # length will be the length of the vehicle
        self.length = length

        # orientation will be H for horizontal and V for vertical
        self.orientation = orientation 

        # we set some starting values for the placement of each vehicle
        self.row = start_row
        self.col = start_col

class RushHour:
    """
    In this class we will define methods to create the rush hour game.
    We will add vehicles, create the board, move the vehicles and 
    check if the game is done.
    """

    def __init__(self):
        """
        In this method we create the board for the rush hour game and 
        add vehicle-instances to a dictionary.
        """

        # create the board with dots for the desired boardsize
        self.board = [['.' for _ in range(6)] for _ in range(6)]

        # create a new dictionary for the vehicle-instances
        self.vehicles = {}

    def add_vehicle(self, vehicle):
        """
        In this method we add vehicles to the game and place them 
        on the desired place on the board.
        """

        # we use the identifier in addition to color for representing unique vehicles (id)
        vehicle_id = f"{vehicle.color}{vehicle.identifier}"
        
        # add vehicles to dict using its id
        self.vehicles[vehicle_id] = vehicle

        # for horizontal oriented vehicles: loop over lenght and add to columns
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper()

        # for vertical oriented vehicles: loop over length and add to rows
        else:
            for i in range(vehicle.length):
                self.board[vehicle.row + i][vehicle.col] = vehicle.color[0].upper()

    def display_board(self):
        """
        In this method we print the board for visualization purposes.
        """

        # we loop through all the rows in the board and add some space between the dots
        for row in self.board:
            print(' '.join(row))
        print()

    def move_vehicle(self, vehicle_id, distance):
        """
        In this method we create the ability to move the vehicles across the board.
        """

        # create a vehicle variable from the dictionary using its id
        vehicle = self.vehicles[vehicle_id]

        # check if the vehicle is horizontal orientated
        if vehicle.orientation == 'H':

            # calculate new column position
            new_col = vehicle.col + distance
            
            # check if the move is valid
            if 0 <= new_col <= 5 - vehicle.length:
                
                # loop through every vehicle
                for k, v in self.vehicles.items():
                    
                    # TESTING
                    print(f'vehicle: {v.color, v.row, v.col}')
                    
                    # Checks whether the current vehicle is on the same row as another vehicle and skips vehicle itself 
                    # This could be a potential bug once there are vehicles of the same color on the same row
                    if v.orientation == 'V' and (v.row + v.length - 1) == vehicle.row or vehicle.row == v.row and vehicle.color != v.color:
                        # T
                        
                        # TESTING
                        print(f'passed: {v.color, v.row, v.col}')
                        
                        # Checks whether the new col value is smaller than the neighbour vehicle col value
                        if new_col + (vehicle.length - 1)  < v.col:
                            
                            ## TESTING
                            print(vehicle.color, vehicle.row, vehicle.col)
                            print(v.color, v.row, v.col)
                            
                            # clear vehicle's current position
                            for i in range(vehicle.length):
                                self.board[vehicle.row][vehicle.col + i] = '.'
                            # update vehicle position
                            vehicle.col = new_col
                            # place vehicle at new position
                            for i in range(vehicle.length):
                                self.board[vehicle.row][vehicle.col + i] = vehicle.color[0].upper()
                                
                            ## TESTING
                            print(vehicle.color, vehicle.row, vehicle.col)
                            print(v.color, v.row, v.col)
                            
                        else:
                            print("Invalid move")
                            
                            # Breaks when there is a vehicle next to the current vehicle
                            break
                            # Code added until here
            else:
                print("Invalid move.")

        else:
            # similar logic for vertical movement
            new_row = vehicle.row + distance
            if 0 <= new_row <= 5 - vehicle.length:
                for k, v in self.vehicles.items():
                    if vehicle.col == v.col and vehicle.color != v.color:
                        if new_row + (vehicle.length - 1)  < v.row:
                            ## TESTING
                            print(vehicle.color, vehicle.row, vehicle.col, vehicle.length)
                            
                            for i in range(vehicle.length):
                                self.board[vehicle.row + i][vehicle.col] = '.'

                            vehicle.row = new_row
                            for i in range(vehicle.length):
                                self.board[vehicle.row + i][vehicle.col] = vehicle.color[0].upper()
                            ## TESTING
                            print(vehicle.color, vehicle.row, vehicle.col, vehicle.length) 
                            
                        else:
                            print("Invalid move")
                            break
            else:
                print("Invalid move.")

        
    def check_win(self):
        """
        In this method we check if the game has been finished.
        """

        # check if red car 'R' is in the winning position
        for row in self.board:

            # checking the most right column for the red car
            if row[-1] == 'R': 

                # if the red car is there we return True and otherwise False
                return True

        return False

    def play_game(self):
        """
        In this method we create the ability to play the game by calling
        the defined methods.
        """

        # if the game has not been won yet we can still do additional moves
        while True:

            # we display the board
            self.display_board()

            # we ask for a next move
            user_input = input("Enter your move (color+identifier distance): ")

            # we create the vehicle_id and the distance from the users input
            vehicle_id, distance = user_input.split()

            # we create a distance variable as a integer
            distance = int(distance)

            # we check if this vehicle is in our dictionary
            if vehicle_id in self.vehicles:

                # we move the vehicle the asked distance
                self.move_vehicle(vehicle_id, distance)

                # then check if we have finished/won the game and break from the loop
                if self.check_win():
                    print("Congratulations! You've won!")
                    self.display_board()
                    break

            # if vehicle is not in our dictionary we print an error
            else:
                print("Invalid vehicle color. Please try again.")


if __name__ == "__main__":
    """
    Here we initialize and set up the game.
    """

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

    # Start the game
    game.play_game()
