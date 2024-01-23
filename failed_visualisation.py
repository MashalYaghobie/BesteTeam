import turtle
from rush_hour import RushHour
from rush_hour import Vehicle

# constants for the visuals
MAX_WINDOW_SIZE = 600  # max size for the window
BOARD_FILES = {
    6: ['gameboards/Rushhour6x6_1.csv', 'gameboards/Rushhour6x6_2.csv', 'gameboards/Rushhour6x6_3.csv'],
    9: ['gameboards/Rushhour9x9_4.csv', 'gameboards/Rushhour9x9_5.csv', 'gameboards/Rushhour9x9_6.csv'],
    12: ['gameboards/Rushhour12x12_7.csv']
}

class RushHourVisualizer:
    def __init__(self, game):
        self.game = game
        # window = board, cell = cube
        self.window, self.cell_size = self.setup_window(len(game.board))
        self.draw_board()
        self.draw_all_vehicles()

    def draw_all_vehicles(self):
        for vehicle in self.game.vehicles.values():
            self.draw_vehicle(vehicle)

    def setup_window(self, board_size):
        """Calculates the size of each cell based on the board
        size and sets up the Turtle window with an appropriate
        title and dimensions"""
        cell_size = MAX_WINDOW_SIZE // board_size
        # draw window with turtle function, add title
        window = turtle.Screen()
        window.title("Rush Hour game")
        # setup window of appropriate size
        window.setup(width=cell_size * board_size + 20, height=cell_size * board_size + 20)

        return window, cell_size

    def draw_board(self):
        """Draw the board"""
        # fastest speed for cursor
        turtle.speed('fastest')

        for row in range(len(self.game.board)):
            for col in range(len(self.game.board)):
                self.draw_cell(row, col)

    def draw_cell(self, row, col):
        """Draw the cells"""
        # calculate the actual x and y coordinates
        x = (col - len(self.game.board) / 2) * self.cell_size
        y = (len(self.game.board) / 2 - row - 1) * self.cell_size

        # lift up turtle pen
        turtle.penup()
        # move the pen to cell location
        turtle.goto(x, y)
        # put down pen to start drawing
        turtle.pendown()
        # draw four walls of the cell
        for _ in range(4):
            turtle.forward(self.cell_size)
            # rotate 90 degrees after each wall
            turtle.left(90)

    def draw_vehicle(self, vehicle):
        """Draw the vehicles. Uses a color map to represent the vehicles.
        Colors the vehicles accordingly."""
        # pick up pen
        turtle.penup()
        # get vehicle coordinates
        x, y = self.get_vehicle_coordinates(vehicle)
        # go to vehicle position
        turtle.goto(x, y)
        # reset heading to default (east)
        turtle.setheading(0)
        # pen down to start drawing
        turtle.pendown()
        # color map for coloring vehicles
        color_map = {
            'X': 'red',
            'A': 'blue', 'B': 'green', 'C': 'yellow',
            'D': 'violet', 'E': 'orange', 'F': 'pink',
            'G': 'grey', 'H': 'cyan', 'I': 'magenta',
            'J': 'brown', 'K': 'lime', 'L': 'olive'
        }
        vehicle_color = color_map.get(vehicle.name, 'blue') # default color is blue
        # start coloring
        turtle.fillcolor(vehicle_color)
        turtle.begin_fill()
        # draw horizontal vehicles
        if vehicle.orientation == 'H':
            for _ in range(2):
                turtle.forward(self.cell_size * vehicle.length)
                turtle.left(90)
                turtle.forward(self.cell_size)
                turtle.left(90)
        # vertical vehicles
        else:
            for _ in range(2):
                turtle.forward(self.cell_size)
                turtle.left(90)
                turtle.forward(self.cell_size * vehicle.length)
                turtle.left(90)
        turtle.end_fill()

    def update_board(self):
        """Clears the current board and redraws it with updated vehicle positions."""
        # turn off automatic screen updates
        turtle.tracer(0, 0)
        # Before moving vehicles, save their old positions
        old_positions = {v.name: self.get_vehicle_coordinates(v) for v in self.game.vehicles.values()}
        # debug
        print(f"Old vehicle position: {old_positions}")

        # clear old positions and redraw at new positions
        for vehicle in self.game.vehicles.values():
            # get new and previous coordinates
            old_x, old_y = old_positions[vehicle.name]
            new_x, new_y = self.get_vehicle_coordinates(vehicle)
            # debug
            print(f"New vehicle position: {new_x, new_y}.")

            # check if vehicle has moved, then clear and redraw
            if old_x != new_x or old_y != new_y:
                self.clear_vehicle(old_x, old_y, vehicle.length, vehicle.orientation)
                self.draw_vehicle(vehicle)
        # perform singe screen update
        turtle.update()
        # re-enable tracing for next updates
        turtle.tracer(1, 1)

    def clear_vehicle(self, x, y, length, orientation):
        """Clears old position of the vehicle."""
        # pick up pen
        turtle.penup()
        # go to vehicle location
        turtle.goto(x, y)
        # reset heading
        turtle.setheading(0)
        turtle.pendown()
        # use background color for clearing
        turtle.fillcolor('red') # debug color
        turtle.begin_fill()
        if orientation == 'H':
            for _ in range(2):
                turtle.forward(self.cell_size * length)
                turtle.right(90)
                turtle.forward(self.cell_size)
                turtle.right(90)
        else:
            for _ in range(2):
                turtle.forward(self.cell_size)
                turtle.right(90)
                turtle.forward(self.cell_size * length)
                turtle.right(90)
        turtle.end_fill()

    def get_vehicle_coordinates(self, vehicle):
        """Get the position of a vehicle in a given state."""
        board_middle = len(self.game.board) / 2
        if vehicle.orientation == 'H':
            x = (vehicle.col - board_middle) * self.cell_size
            y = (board_middle - vehicle.row - 1) * self.cell_size
        else:  # 'V'
            # For vertical vehicles, we adjust by adding the length since we're drawing upwards
            x = (vehicle.col - board_middle) * self.cell_size
            y = (board_middle - vehicle.row - vehicle.length) * self.cell_size
        return x, y

    def initial_draw(self):
        """Draws the initial state of the board."""
        # turn off animation for initial draw
        turtle.tracer(0, 0)
        self.draw_board()
        self.draw_all_vehicles()
        # update the drawing for initial state
        turtle.update()
        # re-enable tracing after initial draw
        turtle.tracer(1, 1)

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
    visualizer = RushHourVisualizer(game)
    # initial drawing of the board
    visualizer.initial_draw()

    # game loop
    while not game.check_win():
        move = input("Enter your move (Name + distance, format = A 1): ")
        vehicle_id, distance = move.split()
        distance = int(distance)

        if vehicle_id in game.vehicles:
            if game.move_vehicle(vehicle_id, distance):
                visualizer.update_board()
            else:
                print("Move not possible. Please try again.")
        else:
            print("Invalid vehicle name. Please try again")

    print("Congratulations! You've won!")
    visualizer.window.mainloop()

if __name__ == "__main__":
    main()
