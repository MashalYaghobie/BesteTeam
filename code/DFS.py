import copy
from rush_hour import RushHour

def depth_first_search(starting_state, depth):
    # add starting state to stack
    stack = [starting_state]

    while len(stack) > 0:

        # get the latest state (top) from the stack
        latest_state = stack.pop()
        print(latest_state)

        # stop condition for if the game has been finished
        if game.check_win(latest_state):
            print(f"Game has been finished")
            break
        
        


# no deeper than depth
depth = 3

# add begin state to stack
stack = [""]

while len(stack)>0:

    # get top from stack
    stack = stack.pop()
    print(state)

    # stop condition
    if len(state) < depth:

        # for each possible action:
        for i in ['R', 'L']:

            # deepcopy the state
            child = copy.deepcopy(state)

            # make new child
            child += i

            # put on stack
            stack.append(child)
