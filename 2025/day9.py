# Day 9
from itertools import combinations  # https://docs.python.org/3/library/itertools.html
from collections import defaultdict  # https://docs.python.org/3/library/collections.html#collections.defaultdict

# Function that find biggest area between coordinates
def area(file):
    # Read data
    with open(file) as f:
        lines = f.readlines()
    
    # Strip whitespace
    lines = [line.strip('\n') for line in lines]
    
    # Get number of coordinates
    n = len(lines)
    
    # Track combinations of coordinates
    combo = []
    
    for i, j in combinations(range(n), 2): 
        combo.append((lines[i], lines[j]))
        
    print(combo)

    # Calculate area of rectangle and store biggest
    previous_area = 0
    
    for c in combo:
        coordinate1 = c[0].split(",")
        print("coordinate1", coordinate1)
        x1 = int(coordinate1[0])
        y1 = int(coordinate1[1])
    
        coordinate2 = c[1].split(",")
        print("coordinate2", coordinate2)
        x2 = int(coordinate2[0])
        y2 = int(coordinate2[1])
    
        current_area = (abs((x1-x2))+1)*(abs((y1-y2))+1)
        print("current_area", current_area)
    
        if current_area > previous_area:
            previous_area = current_area
        
        print("previous_area", previous_area)
    
    return previous_area


answer = area("day9_input.txt")
print(f"The biggest rectangle area is {answer}")


# Helper function that determines if the rectangle has red/green tiles (ChatGPT)
def rectangle_is_valid(x1, y1, x2, y2, filled_tiles):
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            if (x, y) not in filled_tiles:
                return False
    return True


# Function that find biggest area between coordinates that have other coordinates on their row/col (ChatGPT) - takes too long
def area2(file):
    # Store coordinates
    coords = []
    
    # Read data
    with open(file) as f:
        for line in f:
            rm_whitespace = line.strip()
            split_coords = rm_whitespace.split(",")
            str_to_int = map(int, split_coords)
            map_to_tuple = tuple(str_to_int)
            coords.append(map_to_tuple)
    
        # coords = [tuple(map(int, line.strip().split(","))) for line in f]  # more efficient way written by ChatGPT
    
    red_tiles = set(coords)
    rows = defaultdict(list)  # dictionary with key and list value {k:[v]}
    cols = defaultdict(list)
    
    # Get list of x and y coordinates that are linked
    for x, y in red_tiles:
        rows[y].append(x)  # find all x-coordinates linked to y-coordinate (all red tiles)
        cols[x].append(y)  # find all y-coordinates linked to x-coordinate (all red tiles)
    
    green_tiles = set()  # green tiles exist between red tiles
    
    # Horizontal greens
    for y, xs in rows.items():
        xs.sort()  # sort x-coordinates linked to each y-coordinate
        for i in range(len(xs) - 1):
            for x in range(xs[i] + 1, xs[i + 1]):  # start next to red tile and finish at next red tile
                green_tiles.add((x, y))  # add points in between red tiles
    
    # Vertical greens
    for x, ys in cols.items():
        ys.sort()
        for i in range(len(ys) - 1):
            for y in range(ys[i] + 1, ys[i + 1]):
                green_tiles.add((x, y))
    
    # Combine into grid
    filled_tiles = red_tiles | green_tiles
    print("filled_tiles", filled_tiles)
    print("red_tiles", red_tiles)
    print("green_tiles", green_tiles)
    
    # Determine bounding box - all tiles in side red/green loops are green tiles
    min_x = min(x for x, y in filled_tiles)  # left
    max_x = max(x for x, y in filled_tiles)  # right
    min_y = min(y for x, y in filled_tiles)  # bottom
    max_y = max(y for x, y in filled_tiles)  # top
    
    changed = True  # continue loop if new green tiles added to filled tiles
    
    while changed:  # takes too long
        changed = False
        new_tiles = set()
    
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in filled_tiles:
    
                    # Check if surrounded (up, down, left, right)
                    if (
                        (x - 1, y) in filled_tiles and  # left
                        (x + 1, y) in filled_tiles and  # right
                        (x, y - 1) in filled_tiles and  # down
                        (x, y + 1) in filled_tiles  # up
                    ):
                        new_tiles.add((x, y))  # add green tile
    
        if new_tiles:  # will be empty if no new tiles found
            filled_tiles |= new_tiles  # add new tiles to filled tiles if not already there
            green_tiles |= new_tiles
            changed = True  # repeat loop to find more new tiles
    
    # Set maximum area
    max_area = 0
    
    # Calculate area of rectangle and store biggest
    for (x1, y1), (x2, y2) in combinations(coords, 2):  # more efficient way of looping through combinations
        print("coords",(x1, y1), (x2, y2))
        if rectangle_is_valid(x1, y1, x2, y2, filled_tiles):  # if True then area made up of green/red tiles
            print("VALID")
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            print("area", area)
            max_area = max(max_area, area)  # take biggest area (previous vs current)
            print("max_area", max_area)
        
    return max_area


answer = area2("day9_input.txt")
print(f"The biggest rectangle area is {answer}")


"""
Solutions on Reddit use Python package shapely which creates polygons from coordinates
https://shapely.readthedocs.io/en/stable/index.html
https://www.reddit.com/r/adventofcode/comments/1phywvn/2025_day_9_solutions/
https://github.com/stOneskull/AoC/blob/main/2025/09/movie2.py

Solution without shapely
https://github.com/mgtezak/Advent_of_Code/blob/master/2025/09/p2.py
"""
