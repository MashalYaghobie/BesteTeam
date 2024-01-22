# BFS.py

import queue
import copy

# no deeper than 'depth'
depth = 3
queue = queue.Queue()

# add begin state to queue
queue.put("")

while not queue.empty():

    # get first from queue
    state = queue.get()
    print(state)

    # stop condition
    if len(state) < depth:

        # for each possible action
        for i in ['L', 'R']:

            # deepcopy the state
            child = copy.deepcopy(state)

            # make new child
            child += i

            # add new child
            queue.put(child)
