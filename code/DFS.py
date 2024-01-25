import copy

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
