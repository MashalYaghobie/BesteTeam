import turtle
from code.game.rush_hour import RushHour
from code.game.rush_hour import Vehicle
from code.algorithms.random_algorithm import RushHourSolver
from code.algorithms.bfs import RushHourBFS
from code.algorithms.dfs import RushHourDFS
from code.algorithms.astar import RushHourAStar

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
        # hide the turtle
        turtle.hideturtle()
        # fastest speed for cursor
        turtle.speed('fastest')

        for row in range(len(self.game.board)):
            for col in range(len(self.game.board)):
                self.draw_cell(row, col)

    def draw_cell(self, row, col, redraw=False):
        """Draw the cells. If redraw is True, only the borders are redrawn.
        """
        if row is None:
            raise ValueError("Row value is None")
        # calculate the actual x and y coordinates
        x = (col - len(self.game.board) / 2) * self.cell_size
        y = (len(self.game.board) / 2 - row - 1) * self.cell_size

        # lift up turtle pen
        turtle.penup()
        # move the pen to cell location
        turtle.goto(x, y)
        # put down pen to start drawing
        turtle.pendown()

        if redraw:
            # redraw cell borders in black
            turtle.pencolor('black')

        turtle.pendown()
        # draw four walls of the cell
        for _ in range(4):
            turtle.forward(self.cell_size)
            # rotate 90 degrees after each wall
            turtle.left(90)

        if redraw:
            turtle.pencolor('black')

    def draw_vehicle(self, vehicle):
        """Draw the vehicles. Uses a color map to represent the vehicles.
        Colors the vehicles accordingly."""
        # hide the turtle
        turtle.hideturtle()
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
            'J': 'brown', 'K': 'lime', 'L': 'olive',
            'M': 'purple', 'N': 'chocolate', 'O': 'gold',
            'P': 'maroon', 'Q': 'turquoise', 'R': 'darkgreen',
            'S': 'navy', 'T': 'skyblue', 'U': 'lightgreen',
            'V': 'aquamarine', 'W': 'DarkRed', 'Y': 'DeepPink4',
            'AA': 'DarkOrange4', 'AB': 'DarkGoldenrod', 'AC': 'DarkMagenta',
            'AD': 'DarkGrey', 'AE': 'CornflowerBlue', 'AF': 'burlywood',
            'AG': 'brown4', 'AH': 'BlueViolet', 'AI': 'azure4', 'AJ': 'khaki',
            'AK': 'LimeGreen', 'AL': 'chocolate4', 'AM': 'DarkSlateBlue',
            'AN': 'cyan4', 'AO': 'chartreuse', 'AP': 'DarkBlue', 'AQ': 'DarkSeaGreen',
            'AR': 'DarkKhaki'
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

    def get_vehicle_coordinates(self, vehicle, row=None, col=None):
        """Get the position of a vehicle in a given state.
        If row and col are not provided, the current position
        of the vehicle is used.
        """
        # use current pos if none provided
        if row is None:
            row = vehicle.row
        if col is None:
            col = vehicle.col

        board_middle = len(self.game.board) / 2
        if vehicle.orientation == 'H':
            x = (col - board_middle) * self.cell_size
            y = (board_middle - row - 1) * self.cell_size
        else:  # 'V'
            # For vertical vehicles, we adjust by adding the length since we're drawing upwards
            x = (col - board_middle) * self.cell_size
            y = (board_middle - row - vehicle.length) * self.cell_size
        return x, y

    def clear_vehicle(self, vehicle, old_row, old_col):
        """
        Clears old position of the vehicle from the board.
        """
        # get coordinates for old position
        x, y = self.get_vehicle_coordinates(vehicle, old_row, old_col)
        # lift up pen
        turtle.penup()

        if vehicle.orientation == 'H':
            # calc range of columns the vehicle covered
            cols = range(old_col, old_col + vehicle.length)
            # rows remain same
            rows = [old_row]
        else:
            # calc range of rows covered by vehicle
            rows = range(old_row, old_row + vehicle.length)
            cols = [old_col]
        # go to old position
        turtle.goto(x, y)
        # fill the old position with white (background color)
        turtle.fillcolor('white')
        turtle.begin_fill()
        # draw over the vehicle
        if vehicle.orientation == 'H':
            for _ in range(2):
                turtle.forward(self.cell_size * vehicle.length)
                # turn 90 degrees
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

        # Redraw the cell borders for the cleared cells
        for row in rows:
            for col in cols:
                self.draw_cell(row, col, redraw=True)

    def update_board(self, vehicle_name):
        """
        Updates board by clearing old position and drawing new position.
        """
        # retrieve vehicle object
        vehicle = self.game.vehicles.get(vehicle_name)

        if vehicle:

            # clear old pos
            self.clear_vehicle(vehicle, vehicle.old_row, vehicle.old_col)
            # redraw at new pos
            self.draw_vehicle(vehicle)

    def solve_with_algorithm(self, solver):
        solver.solve_randomly()


def select_board():
    print("Select board size: 6, 9 or 12")
    board_size = int(input("Enter board size: "))
    print(f"Select which {board_size}x{board_size} board to play (1-{len(BOARD_FILES[board_size])}): ")
    for i, file in enumerate(BOARD_FILES[board_size], start=1):
        print(f"{i}: {file}")
    board_index = int(input("Enter board number: ")) - 1
    return BOARD_FILES[board_size][board_index]

def extract_move(previous_state, current_state):
    """
    Compare two RushHour game states and identify the move made.
    Returns a tuple (vehicle_id, distance).
    """
    for vehicle_id, vehicle in current_state.vehicles.items():
        previous_vehicle = previous_state.vehicles[vehicle_id]
        if vehicle.row != previous_vehicle.row or vehicle.col != previous_vehicle.col:
            # Calculate distance moved
            distance = (vehicle.row - previous_vehicle.row) + (vehicle.col - previous_vehicle.col)
            return (vehicle_id, distance)
    return None


def main():
    game = RushHour()
    visualizer = RushHourVisualizer(game)
    # initial drawing of the board
    visualizer.initial_draw()

    # Display algorithm choices
    algorithms = {
        '1': ("Play Manually", None),
        '2': ("Random Algorithm", RushHourSolver),
        '3': ("Breadth-First Search (BFS)", RushHourBFS),
        '4': ("Depth-First Search (DFS)", RushHourDFS),
        '5': ("A* Algorithm", RushHourAStar),
    }

    print("Select an option for solving the Rush Hour puzzle:")
    for key, (name, _) in algorithms.items():
        print(f"{key}: {name}")

    # User selection
    choice = input("Enter the number of your choice: ")
    while choice not in algorithms:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter the number of your choice: ")

    # Execute selected option
    if choice == '1':
        # Play the game manually
        while not game.check_win():
            move = input("Enter your move (Vehicle ID + distance, format = A 1): ")
            vehicle_id, distance = move.split()
            distance = int(distance)

            if vehicle_id in game.vehicles:
                game.move_vehicle(vehicle_id, distance)
                visualizer.update_board(vehicle_id)
            else:
                print("Invalid vehicle name. Please try again")

        print("Congratulations! You've won!")
    else:
        _, AlgorithmClass = algorithms[choice]
        solver = AlgorithmClass(game)
        if choice == '3':
            solution_path = solver.bfs()
        elif choice == '4':
            states_path = solver.depth_first_search()
            # convert states to moves
            solution_path = []
            for i in range(1, len(states_path)):
                move = extract_move(states_path[i - 1], states_path[i])
                if move:
                    solution_path.append(move)
        elif choice == '5':
            states_path = solver.a_star()
            solution_path = []
            for i in range(1, len(states_path)):
                move = extract_move(states_path[i - 1], states_path[i])
                if move:
                    solution_path.append(move)
        else:
            solution_path = None
        # make the moves on the board
        if solution_path:
            for vehicle_id, distance in solution_path:
                game.move_vehicle(vehicle_id, distance)
                visualizer.update_board(vehicle_id)
                print(f"Moved {vehicle_id} by {distance} steps")
            if game.check_win():
                print("Congratulations! You've won!")
        else:
            print("No solution found.")



if __name__ == "__main__":
    main()
