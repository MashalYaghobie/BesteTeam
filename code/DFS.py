import copy
from rush_hour import State

def depth_first_search(starting_state, max_depth):
    # add starting state to stack
    stack = [starting_state]

    while len(stack) > 0:

        # get the latest state (top) from the stack
        latest_state = stack.pop()
        # print(latest_state)

        if depth_limit == 0:
            continue

        # stop condition for if the game has been finished
        if game.check_win(latest_state):
            print(f"Game has been finished")
            return True
        
        # create the child states and append them to our stack
        for move in current_state.get_possible_moves():
            child_state = latest_state + move
            stack.append(child_state)

        # call the function again for next depth/layer
        depth_first_search(stack, depth_limit - 1)
        
    return False


if __name__ == "__main__":

    # create the starting state
    starting_state = State(vehicles, N)

    # set the depth limit
    depth_limit = 3

    result = depth_first_search(starting_state, depth_limit)

    if not result:
        print("Goal state has not been reached in the depth limit")
