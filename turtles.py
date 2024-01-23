from rush_hour import RushHour
from rush_hour import Vehicle
import turtle
import pandas as pd

# Constants for the visuals
MAX_WINDOW_SIZE = 600  # Max size for the window
BOARD_FILES = {
    6: ['gameboards/Rushhour6x6_1.csv', 'gameboards/Rushhour6x6_2.csv', 'gameboards/Rushhour6x6_3.csv'],
    9: ['gameboards/Rushhour9x9_4.csv', 'gameboards/Rushhour9x9_5.csv', 'gameboards/Rushhour9x9_6.csv'],
    12: ['gameboards/Rushhour12x12_7.csv']
}


class RushHourGameVisualizer:
    def __init__(self, game):
        self.game = game
        self.window, self.cell_size = self.setup_window(len(game.board))
        self.draw_board()

    def setup_window(self, board_size):
        """Calculates the size of each cell based on the board
        size and sets up the Turtle window with an appropriate
        title and dimensions"""
        cell_size = MAX_WINDOW_SIZE // board_size
        window = turtle.Screen()
        window.title("Rush Hour Game")
        window.setup(width=cell_size * board_size + 20, height=cell_size * board_size + 20)
        # Set the coordinate system
        window.setworldcoordinates(0, 0, cell_size * board_size, cell_size * board_size)
        return window, cell_size

    def draw_board(self):
        turtle.speed('fastest')
        for row in range(len(self.game.board)):
            for col in range(len(self.game.board)):
                self.draw_cell(row, col)

    def draw_cell(self, row, col):
        turtle.penup() # lifts the Turtle pen to move without drawing
        inverted_row = len(self.game.board) - 1 - row  # Invert row index
        # moves cursor to specific location
        turtle.goto(col * self.cell_size, inverted_row * self.cell_size)
        turtle.pendown() # puts Turtle pen down to start drawing
        # draw four walls of the cell
        for _ in range(4):
            turtle.forward(self.cell_size)
            turtle.left(90) # rotate 90 degrees after each wall

    def draw_vehicle(self, vehicle):
        turtle.penup()
        inverted_row = len(self.game.board) - 1 - vehicle.row  # Invert row index
        # Use the regular row and col for positioning
        turtle.goto(vehicle.col * self.cell_size, inverted_row * self.cell_size)
        turtle.pendown()
        if vehicle.name == 'X': # 'X' is always red
            turtle.fillcolor('red')
        else:
            color_map = {
            'A': 'blue', 'B': 'green', 'C': 'yellow',
            'D': 'violet', 'E': 'orange', 'F': 'pink',
            'G': 'grey', 'H': 'cyan', 'I': 'magenta',
            'J': 'brown', 'K': 'lime', 'L': 'olive'
            }
            # default color is blue if not in map
            turtle.fillcolor(color_map.get(vehicle.name, 'blue'))
        turtle.begin_fill()
        if vehicle.orientation == 'H':
            for _ in range(2):
                turtle.forward(self.cell_size * vehicle.length)
                turtle.left(90)
                turtle.forward(self.cell_size)
                turtle.left(90)
        else:
            for _ in range(2):
                turtle.forward(self.cell_size)
                turtle.left(90)
                turtle.forward(self.cell_size * vehicle.length)
                turtle.left(90)
        turtle.end_fill()

    def update_board(self, vehicle_id=None, distance=None):
        if vehicle_id and distance is not None:
            # get position of vehicle before the move
            vehicle = self.game.vehicles[vehicle_id]
            prev_row, prev_col = vehicle.row, vehicle.col
            prev_orientation, prev_length = vehicle.orientation, vehicle.length
            # move vehicle to new position
            self.game.move_vehicle(vehicle_id, distance)
            # erase vehicle from previous position
            self.erase_vehicle(Vehicle(vehicle_id, prev_row, prev_col, prev_orientation, prev_length))
            # draw vehicle in new position
            self.draw_vehicle(self.game.vehicles[vehicle_id])
        else:
            turtle.tracer(0, 0) # Turn off animation
            turtle.clear()
            self.draw_board()
            for vehicle in self.game.vehicles.values():
                self.draw_vehicle(vehicle)
            turtle.update() # Update the screen all at once

    def erase_vehicle(self, vehicle):
        # set color to white to 'erase'
        turtle.color("white")
        for i in range(vehicle.length):
            # calculate position of each cell the vehicle occupies
            if vehicle.orientation == 'H':
                row, col = vehicle.row, vehicle.col + i
            else:
                row, col = vehicle.row + i, vehicle.col

            # redraw cell in white to erase vehicle
            inverted_row = len(self.game.board) - 1 - row  # Invert row index
            self.draw_cell(inverted_row, col)
        # reset the color to black for grid lines
        turtle.color("black")



def select_board():
    print("Select board size: 6, 9 or 12")
    board_size = int(input("Enter board size: "))
    print(f"Select which {board_size}x{board_size} board to play (1-{len(BOARD_FILES[board_size])}): ")
    for i, file in enumerate(BOARD_FILES[board_size], start=1):
        print(f"{i}: {file}")
    board_index = int(input("Enter board number: ")) - 1
    return BOARD_FILES[board_size][board_index]

def main():
    game_file = select_board()
    game = RushHour(game_file)
    visualizer = RushHourGameVisualizer(game)
    visualizer.update_board()

    # game loop
    while not game.check_win():
        move = input("Enter your move (Name + distance, format = A 1): ")
        vehicle_id, distance = move.split()
        distance = int(distance)
        if vehicle_id in game.vehicles:
            game.move_vehicle(vehicle_id, distance)
            visualizer.update_board(vehicle_id, distance)
        else:
            print("Invalid vehicle name. Please try again")

    print("Congratulations! You've won!")
    visualizer.window.mainloop()

if __name__ == "__main__":
    main()
