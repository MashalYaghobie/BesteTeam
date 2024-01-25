import copy
from rush_hour import State, RushHour

class DepthFirstSearch:
    """
    In this class we will define some methods to create and use
    the depth first search algorithm for our rush hour case.
    """

    def __init__(self, game, max_depth):
        """
        In this method we define some starting variables as game,
        max_depth and we create the starting state for the game.
        """
        self.game = game
        self.max_depth = max_depth
        self.starting_state = State(list(game.vehicles.values()), len(game.board))

    def depth_first_search():
        """
        In this function we will run the depth first search algorithm
        for our rush hour case.
        """

        # add starting state to stack
        stack = [self.starting_state]

        while len(stack) > 0:

            # get the latest state (top) from the stack
            latest_state = stack.pop()

            if self.max_depth == 0:
                continue

            # stop condition for if the game has been finished
            if self.game.check_win(latest_state):
                print(f"Game has been finished")
                return True
            
            # create the child states and append them to our stack
            for move in latest_state.get_possible_moves():
                child_state = latest_state + move
                stack.append(child_state)
            
            self.max_depth -= 1

            # call the function again for next depth/layer
            self.search()
            
        return False

if __name__ == "__main__":
    # create the game
    game = RushHour()

    # set the depth limit
    depth_limit = 3

    # create the instances for the game for depth first search
    dfs_game = DepthFirstSearch(game, depth_limit)

    # run the depth first search algorithm
    result = dfs_game.search()

    if not result:
        print("Goal state has not been reached in the depth limit")
