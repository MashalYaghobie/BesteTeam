from collections import deque
from rush_hour import RushHour

class RushHourBFS(RushHour):
    """Extends the Rush Hour game class with BFS algorithm to solve this puzzle"""

    def solve_with_bfs(self):
        """Solves the Rush Hour puzzle using the BFS algorithm"""
        # deque allows fast appends and pops from both ends
        queue = deque([(self.get_state(), None, None)])
        # save visited states
        visited = set()
        # dictionary for tracking the path
        parents = {}
        # while there are states in the queue
        while queue:
            # remove leftmost item from the queue, which is the next state to explore
            current_state, parent_state, move_made = queue.popleft()
            # check if current state is winning
            if self.check_win():
                # call backtrack method and build path to the winning state
                return self.reconstruct_path(parents, current_state)
            # add current state to visited
            visited.add(current_state)
            # if current state has a parent, it's added to 'parents' with the move that led to it
            if parent_state:
                parents[current_state] = (parent_state, move_made)

            # get all possible moves from current state
                for vehicle_id, distance in self.get_all_possible_moves():
                    # apply move and check new state
                    if self.move_vehicle(vehicle_id, distance):
                        new_state = self.get_state()
                        # revert move after getting the state
                        self.move_vehicle(vehicle_id, -distance)

                        # if new state not visited, add it to the queue
                        if new_state not in visisted:
                            queue.append((new_state, current_state, (vehicle_id, distance)))

    def get_all_possible_moves(self):
        """Generate all possible valid moves from the current state"""
        moves = []
        for vehicle_id, vehicle in self.vehicles.items():
            # check possible moves in both directions
            for distance in [-1, 1]:
                if self.is_move_valid(vehicle, vehicle.row + (distance if vehicle.orientation == 'V' else 0),
                                      vehicle.col + (distance if vehicle.orientation == 'H' else 0)):
                    moves.append((vehicle_id, distance))
        return moves

    def reconstruct_path(self, parents, state):
        """Reconstructs the path from the initial state to the winning state."""
        path = []
        while state in parents:
            parent_state, move = parents[state]
            path.append(move)
            state = parent_state
        path.reverse()
        return path

if __name__ == "__main__":
    game = RushHourBFS()
    game.read_all_vehicles()

    solution = game.solve_with_bfs()
    print("Solution:", solution)
