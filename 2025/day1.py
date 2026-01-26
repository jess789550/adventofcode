# Day 1

## Part 1 ##

# Function that finds out number of times it lands on zero
def lands_on_zero(input, start):
    zero = 0
    
    with open(input) as f:
        lines = f.readlines()
    
    moves = [line.replace('\n', '') for line in lines]
    
    # Set the dial after the first move
    firstmove = moves[0]
    
    if firstmove.startswith('R'):
        dial = start + int(firstmove[1:])
    else:
        dial = start - int(firstmove[1:])
    
    dial = dial % 100
    
    if dial == 0:
        zero += 1
     
    # Loop through moves
    for move in moves[1:]:
        if move.startswith('R'):
            dial = dial + int(move[1:])
        else:
            dial = dial - int(move[1:])
        
        dial = dial % 100
    
        if dial == 0:
            zero += 1
    
    return zero


answer = lands_on_zero("day1_input.txt", 50)

print(f"The password is {answer}")

## Part 2 ##

# Function to determine the number of times the dial passes zero
def passes_zero(input, start):
    zero = 0
    
    with open(input) as f:
        lines = f.readlines()
    
    moves = [line.replace('\n', '') for line in lines]
    
    # Set the dial after the first move
    firstmove = moves[0]
    
    # Calculate number of full rotations
    full = int(firstmove[1:]) // 100
    zero += full
    
    # Calculate next number and if dial passes zero
    if firstmove.startswith('R'):
        dial = start + int(firstmove[1:])
        dial = dial % 100
        if dial < start:
            zero += 1
    else:
        dial = start - int(firstmove[1:])
        dial = dial % 100
        if dial > start or dial == 0:
            if start != 0:
                zero += 1
    
    # Loop through moves
    for move in moves[1:]:
    
        # Calculate number of full rotations
        full = int(move[1:]) // 100
        zero += full
        
        # Calculate next number and if dial passes zero
        if move.startswith('R'):
            previous = dial
            dial = dial + int(move[1:])
            dial = dial % 100
            if dial < previous:
                zero += 1
        else:
            previous = dial
            dial = dial - int(move[1:])
            dial = dial % 100
            if dial > previous or dial == 0:
                if previous != 0:
                    zero += 1
    return zero


answer = passes_zero("day1_input.txt", 50)

print(f"The password is {answer}")

# Answers on Reddit
# https://www.reddit.com/r/adventofcode/comments/1pb3y8p/2025_day_1_solutions/

