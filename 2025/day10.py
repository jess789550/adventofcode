# Day 10 (ChatGPT driven)

from collections import deque  # double ended queue, like a special list but optimised
import ast  # convert list of strings into list of tuples of integers for buttons; https://docs.python.org/3/library/ast.html

def parse_pattern(pattern):
    """
    Convert string like '[.#......#.]' to bitmask integer --> bytes 0100000010 = 256 + 2 = 258 bits
    '.' = 0 (off)
    '#' = 1 (on)
    """
    bits = 0
    for i, ch in enumerate(pattern.strip()[1:-1]):  # i = index, ch = character/lightbulb, don't want "[]" so use [1:-1]
        if ch == '#':
            bits |= (1 << i)  # | bitwise OR e.g. 0000 0001 | 0000 0010 = 0000 0011, << bitwise left shift e.g. 0000 0001 to 0000 0010, https://www.geeksforgeeks.org/python/python-bitwise-operators/
    return bits


def build_button_masks(button_definitions):
    """
    Convert button toggle index lists into bitmasks.
    Turns button patterns into bytes e.g. (2,9) would give 10 0000 0100 = 512 + 4 = 516 bits
    Blueprint patterns of button combinations
    """
    masks = []
    for toggles in button_definitions:
        mask = 0
    
        # If single integer, wrap it in list e.g. 4 --> [4] to stop ValueError
        if isinstance(toggles, int):
            toggles = [toggles]
    
        for idx in toggles:
            mask ^= (1 << idx)  # ^ bitwise XOR e.g. 111 ^ 100 = 011
        masks.append(mask)
    return masks


def find_minimum_presses(button_definitions, target_pattern):
    """
    Each while-loop iteration:

    Takes one known state

    Tries pressing every button

    Generates new states

    Adds unseen ones to queue

    Stops when target is found

    This is Breadth-First Search (BFS). Uses FIFO queue to find shorted path in unweighted graphs. https://www.codecademy.com/article/breadth-first-search-bfs-algorithm
    
    Example with (made_up_state,[buttons_pressed])
    First round: (1,[1]), (2,[2])
    Second round: (2,[2]), (2,[1,1]), (3,[1,2])
    Third round: (2,[1,1]), (3[1,2]), (3,[2,1]), (4,[2,2])
    """
    start_state = 0  # all lights off
    target_state = parse_pattern(target_pattern)  # '[.#......#.]' as 258 bits
    
    button_masks = build_button_masks(button_definitions)  # (2,9) as 516 bits
    
    queue = deque([(start_state, [])])  # deque([(0,[])]) --> like a dictionary with key : value where value is a list, state : path, (state_as_bits, buttons_pressed_so_far)
    visited = set([start_state])  # {}
    
    while queue:  # deque([(275, [0, 2, 4, 5, 7, 8]), (921, [0, 2, 4, 5, 7, 9])]) --> deque([(921, [0, 2, 4, 5, 7, 9])]) --> deque([])
        state, path = queue.popleft()  # Remove and return an element from the left side of the deque. This means that each state is tested and each button is pushed
    
        if state == target_state:
            return path  # shortest solution found
    
        for i, mask in enumerate(button_masks):  # press every button
            new_state = state ^ mask  # ^ bitwise XOR so change state of switch 0000 0000 --> 1111 1111
            if new_state not in visited:
                visited.add(new_state)  # Add bits to set
                queue.append((new_state, path + [i]))  # add bits and path with extra button to queue
    
    return None  # no solution found


def answer(file):
    with open(file) as f:
        lines = f.readlines()
    
    count = 0
    
    for line in lines:
        button_strings = line.split()[1:-1]  # ['(2,9)', '(3,5,6,7,8)', '(0,7,8,9)', '(4)', '(0,2,3)', '(2,3,4,5,6,7,8,9)', '(1,2,3,7)', '(1,8)', '(0,2,5,6,9)', '(0,1,2,3,5,6,7)']
        button_definitions = []
    
        for s in button_strings:
            value = ast.literal_eval(s)  # str --> tuple, Evaluate an expression node or a string containing only a Python literal or container display
            if isinstance(value, int):
                value = (value,)
            button_definitions.append(value)  # [(2, 9), (3, 5, 6, 7, 8), (0, 7, 8, 9), 4, (0, 2, 3), (2, 3, 4, 5, 6, 7, 8, 9), (1, 2, 3, 7), (1, 8), (0, 2, 5, 6, 9), (0, 1, 2, 3, 5, 6, 7)]
        
        target_pattern = line.split()[0]  # '[.#......#.]'
        
        solution = find_minimum_presses(button_definitions, target_pattern)
        count += len(solution)
    
    return count


print("The fewest number of buttons pressed is", answer("day10_input.txt"))
