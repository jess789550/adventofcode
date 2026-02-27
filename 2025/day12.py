# Day 12 (ChatGPT driven - backtracking algorithm)

from functools import lru_cache
import re
from concurrent.futures import ThreadPoolExecutor

# ==========================================================
# 1. SHAPES
# ==========================================================

def file_to_shapes(file):
    SHAPES_RAW = {}
    
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            if line.__contains__("x") or line == '':
                pass
            elif line.__contains__(":"):
                num = int(line.split(":")[0])
                SHAPES_RAW[num] = []
            else:
                SHAPES_RAW[num].append(line)
    
    return SHAPES_RAW

"""
SHAPES_RAW = {
    0: ["###",
        "##.",
        "##."],

    1: ["###",
        "##.",
        ".##"],

    2: [".##",
        "###",
        "##."],

    3: ["##.",
        "###",
        "##."],

    4: ["###",
        "#..",
        "###"],

    5: ["###",
        ".#.",
        "###"],
}
"""

# ==========================================================
# 2. ORIENTATION GENERATION
# ==========================================================

def shape_to_coords(shape):
    coords = []
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val == '#':
                coords.append((r, c))
    return coords

"""
shape = ["###"]
coords = [(0,0), (0,1), (0,2)]
"""

def normalize(coords):
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return sorted((r - min_r, c - min_c) for r, c in coords)

"""
shape = ["###"]
coords = [(0,0), (0,1), (0,2)]
coords = [(0,0), (0,1), (0,2)]
"""

def rotate(coords):
    return [(c, -r) for r, c in coords]

"""
shape = ["###"]
coords = [(0,0), (0,1), (0,2)]
coords = [(0,0), (1,0), (2,0)]
"""

def flip(coords):
    return [(r, -c) for r, c in coords]

"""
shape = ["###"]
coords = [(0,0), (0,1), (0,2)]
coords = [(0,0), (0,-1), (0,-2)]
"""

def generate_orientations(shape):
    base = shape_to_coords(shape)
    orientations = set()
    
    current = base
    for _ in range(4):
        # add current rotation
        orientations.add(tuple(normalize(current)))
    
        # add flipped version of this rotation
        flipped = flip(current)
        orientations.add(tuple(normalize(flipped)))
    
        # rotate for next iteration
        current = rotate(current)
    
    return [list(o) for o in orientations]

"""
shape = ["###"]
orientations = [[(0,0), (0,1), (0,2)], [(0,0), (0,-1), (0,-2)], [(0,0), (1,0), (2,0)]]
"""


# ==========================================================
# 3. GENERATE PLACEMENTS FOR ONE BOARD
# ==========================================================

def generate_placements(rows, cols):
    """
    Returns a dictionary:
        placements[shape_id] = list of bitmasks
    """
    placements = {sid: [] for sid in SHAPES_RAW}  # make sure this is top-level
    
    for sid, orientations in ALL_ORIENTATIONS.items():
        for orient in orientations:
            max_r = max(r for r, c in orient)
            max_c = max(c for r, c in orient)
            for base_r in range(rows - max_r + 1):   # +1 to include last row
                for base_c in range(cols - max_c + 1): # +1 to include last col
                    mask = 0
                    for r, c in orient:
                        rr = base_r + r
                        cc = base_c + c
                        bit = rr * cols + cc
                        mask |= 1 << bit
                    placements[sid].append(mask)
    
    return placements   

"""
rows, cols = 4, 4
placements = {0: [2,1,4], 1: [8,32,16], 2: [128,64,256]}
"""

# ==========================================================
# 4. EXISTENCE SOLVER (EARLY EXIT)
# ==========================================================

def exists_solution(rows, cols, requirements):
    total_area_needed = sum(
        requirements[sid] * SHAPE_SIZES[sid]
        for sid in SHAPES_RAW
    )
    if total_area_needed > rows * cols:
        return False  # fast reject
    
    placements = generate_placements(rows, cols)
    
    # capacity check per shape
    for sid, count in enumerate(requirements):
        if count > len(placements[sid]):
            return False
    
    # build piece list
    pieces = []
    for sid, count in enumerate(requirements):
        pieces.extend([sid] * count)
    
    # fail-fast ordering: shapes with fewer placements first
    pieces.sort(key=lambda sid: len(placements[sid]))
    
    FULL_MASK = 0
    target_piece_count = len(pieces)
    
    def backtrack(index, board_mask):
        if index == target_piece_count:
            return True  # found one valid packing
    
        sid = pieces[index]
    
        for placement in placements[sid]:
            if (board_mask & placement) == 0:
                if backtrack(index + 1, board_mask | placement):
                    return True  # EARLY EXIT
    
        return False
    
    return backtrack(0, FULL_MASK)

"""
rows, cols = 4, 4
requirements = [0,0,0,0,2,0]
backtrack = True
"""

# ==========================================================
# 5. PROCESS MANY CASES
# ==========================================================

def file_to_cases(file):
    """
    Reads a file containing grid specifications and requirements.
    Each line should be formatted like:
        4x4: 0 0 0 0 2 0
        12x5: 1 0 1 0 2 2
    Returns:
        List of tuples: (rows, cols, [req0..req5])
    """
    cases = []
    
    with open(file) as f:
        for line in f.readlines():
            if line.__contains__("x"):
                line_components = re.split(r'[x:\n ]+', line.strip())
                row = int(line_components[0])
                col = int(line_components[1])
                req = list(map(int, line_components[2:]))
                cases.append((row, col, req))
    
    return cases


def worker(case):
    """
    Wrapper function for multiprocessing.
    Returns True if grid is solvable, False otherwise.
    """
    rows, cols, req = case
    return exists_solution(rows, cols, req)


# Read file and get shapes
SHAPES_RAW = file_to_shapes("day12_input.txt")

# Create dictionary of orientations of shapes
ALL_ORIENTATIONS = {
    sid: generate_orientations(shape)
    for sid, shape in SHAPES_RAW.items()
}

"""
{0: [[(0,0), (0,1), (0,2)], [(0,0), (0,-1), (0,-2)], [(0,0), (1,0), (2,0)]], 1: [[(0,0), (0,1), (0,2)], [(0,0), (0,-1), (0,-2)], [(0,0), (1,0), (2,0)]], 2: [[(0,0), (0,1), (0,2)], [(0,0), (0,-1), (0,-2)], [(0,0), (1,0), (2,0)]]}
"""

# Get size of shape
SHAPE_SIZES = {
    sid: sum(row.count('#') for row in shape)
    for sid, shape in SHAPES_RAW.items()
}

"""
{0: 7, 1: 7, 2: 7}
"""

# Load your grid cases from a file
cases = file_to_cases("day12_input.txt")

"""
[(38, 48, ['18', '40', '41', '41', '30', '21'])]
"""

# Parallel processing for large number of grids
results = []
with ThreadPoolExecutor() as executor:
    results = list(executor.map(worker, cases))

solvable_count_parallel = sum(results)
print(f"Solvable grids (parallel): {solvable_count_parallel}")


"""
Answers: 
https://www.reddit.com/r/adventofcode/comments/1pkje0o/2025_day_12_solutions/

Other solutions were more basic and didn't look at flipping or rotating shapes. They didn't look at overlaps either.

Packages that were used: 
re, math prod, __future__ annotations, uuid (universally unique identifier), collections defaultdict and Iterator, itertools product, 
pathlib Path, ortools cp_model (Google integer programming problem tool), tqdm (progress bar), numpy, pulp (linear and mixed integer programming modeler),
shape3x3, typing
"""

