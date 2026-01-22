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


answer = lands_on_zero("day1_input.txt", 50) # 1180

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
    
    if firstmove.startswith('R'):
        dial = start + int(firstmove[1:])
        if dial < start:
            zero += 1
    else:
        dial = start - int(firstmove[1:])
        if dial > start:
            zero += 1
    
    dial = dial % 100
    
    if dial == 0:
        zero += 1
    
    if abs(int(firstmove[1:])) > 99:
        zero += abs(int(firstmove[1:])) // 100
    
    # Loop through moves
    for move in moves[1:]:
        if move.startswith('R'):
            dial = dial + int(move[1:])
            if dial < start:
                zero += 1
        else:
            dial = dial - int(move[1:])
            if dial > start:
                zero += 1
        
        dial = dial % 100
    
        if dial == 0:
            zero += 1
     
        if abs(int(move[1:])) > 99:
            zero += abs(int(move[1:])) // 100
    
    return zero


passes_zero("day1_input.txt", 50) # Supposed to be 6892


# Answers on Reddit
# https://www.reddit.com/r/adventofcode/comments/1pb3y8p/2025_day_1_solutions/
# Simpler solution is to total the number of turns and divide by 100





