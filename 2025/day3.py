# Day 3
import itertools

# Part 1: find largest joltage for each battery and sum them
def joltage(input):
    # Read file
    with open(input) as f:
        lines = f.readlines()
    
    # Set count to 0
    count = 0
    
    for line in lines:
        line = line.strip()
        max_index = line.index(max(line[:-1])) # find index of largest number in str, excluding last number
        part_line = line[max_index+1:] # remove everything before largest number, including largest number
        count += int(max(line[:-1])+max(part_line)) # sum largest number and largest number left
    
    return count


answer = joltage("day3_input.txt")
print(f"The total joltage is {answer}.")



# Part 2: twelve batteries instead of two
def joltage_twelve(input):
    # Read file
    with open(input) as f:
        lines = f.readlines()
    
    # Set count to 0
    count = 0
    
    for line in lines:
        line = line.strip()
        num = ""
        
        while len(num) < 12:
            if len(num) == 11:
                part_line = line
            else:
                part_line = line[:-(11-len(num))] # work out biggest number but preserve remaining numbers
            index = part_line.index(max(part_line)) # work out starting index
            num += line[index] # Add number to results string
            line = line[index+1:] # Chop numbers out
        
        count += int(num)
    
    return count


answer = joltage_twelve("day3_input.txt")
print(f"The total joltage is {answer}.")
